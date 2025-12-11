import os
import re
import math
import datetime
import subprocess
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
ASSETS = os.path.join(ROOT, "assets")
TEMPLATE = os.path.join(ROOT, "template_readme.md")
OUTPUT = os.path.join(ROOT, "README.md")

USER = os.environ.get("GITHUB_REPOSITORY", "").split("/")[0]
REPO = os.environ.get("GITHUB_REPOSITORY", "").split("/")[1]

if not os.path.exists(ASSETS):
    os.makedirs(ASSETS)

# ---------------------------------------------------------
# 공통 log 파서
# ---------------------------------------------------------
def parse_log(out):
    commits = []
    for line in out:
        if "|" not in line:
            continue
        ts, msg = line.split("|", 1)
        date = datetime.datetime.fromtimestamp(int(ts)).date()
        commits.append({"date": date, "msg": msg})
    return commits


# ---------------------------------------------------------
# Commit fetcher
# ---------------------------------------------------------
def get_commits_recent():
    out = subprocess.check_output(
        ["git", "log", "--since=60 days ago", "--pretty=%ct|%B"]
    ).decode().strip().split("\n")
    return parse_log(out)


def get_commits_all():
    out = subprocess.check_output(
        ["git", "log", "--pretty=%ct|%B"]
    ).decode().strip().split("\n")
    return parse_log(out)


# ---------------------------------------------------------
# 문제 수 추출 함수 (핵심)
# ---------------------------------------------------------
def extract_solved(msg):
    nums = re.findall(r"(\d+)문제", msg)
    return sum(int(n) for n in nums) if nums else 0


# ---------------------------------------------------------
# 최근 기준(today / weekly / heatmap)
# ---------------------------------------------------------
def parse_recent_info(commits):
    today = datetime.date.today()
    week_start = today - datetime.timedelta(days=today.weekday())

    today_solved = 0
    weekly_solved = 0
    WEEKLY_GOAL = 10
    heatmap = defaultdict(int)

    for c in commits:
        commit_date = c["date"]
        msg = c["msg"]
        solved = extract_solved(msg)

        # Heatmap
        heatmap[str(commit_date)] += solved

        # 오늘
        if commit_date == today:
            today_solved += solved

        # 이번 주
        if commit_date >= week_start:
            weekly_solved += solved

    return today_solved, weekly_solved, WEEKLY_GOAL, heatmap


# ---------------------------------------------------------
# 전체 commit 기반 누적
# ---------------------------------------------------------
def parse_total_info(commits):
    total = 0
    for c in commits:
        total += extract_solved(c["msg"])
    return total


# ---------------------------------------------------------
# 도넛 그래프용 색상 그라데이션
# ---------------------------------------------------------
def lerp(a, b, t):
    return int(a + (b - a) * t)


def donut_color(percent):
    start = (188, 220, 255)  # 연한 블루
    end = (0, 85, 255)       # 진한 블루

    r = lerp(start[0], end[0], percent)
    g = lerp(start[1], end[1], percent)
    b = lerp(start[2], end[2], percent)
    return f"rgb({r},{g},{b})"


# ---------------------------------------------------------
# Donut SVG 생성
# ---------------------------------------------------------
def generate_donut(path, value, goal, label):
    percent = 0 if goal == 0 else min(value / goal, 1)
    radius = 40
    C = 2 * math.pi * radius
    progress = percent * C

    stroke_color = donut_color(percent)

    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg width="160" height="160" xmlns="http://www.w3.org/2000/svg">
  <circle cx="80" cy="80" r="{radius}" stroke="#e5e7eb" stroke-width="12" fill="none"/>
  <circle cx="80" cy="80" r="{radius}" stroke="{stroke_color}" stroke-width="12"
    fill="none"
    stroke-dasharray="{progress} {C - progress}"
    transform="rotate(-90 80 80)"
    stroke-linecap="round"/>
  <text x="80" y="80" font-size="20" text-anchor="middle" dominant-baseline="middle">{value}</text>
  <text x="80" y="105" font-size="12" text-anchor="middle">{label}</text>
</svg>
"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)


# ---------------------------------------------------------
# Heatmap SVG (블루 계열 + 범례 추가)
# ---------------------------------------------------------
def generate_heatmap(path, heatmap):
    today = datetime.date.today()
    dates = [(today - datetime.timedelta(days=i)) for i in range(59, -1, -1)]

    # 블루 팔레트
    def color(v):
        if v == 0: return "#ebf2ff"
        if v < 2: return "#c6dbff"
        if v < 4: return "#7bb0ff"
        if v < 7: return "#4a90ff"
        return "#0066ff"

    cell, gap, rows, cols = 14, 4, 7, 10
    width = cols * (cell + gap)
    height = rows * (cell + gap)

    svg = [f'<svg width="{width}" height="{height + 40}" xmlns="http://www.w3.org/2000/svg">']

    # Grid
    for idx, day in enumerate(dates):
        r = idx % rows
        c = idx // rows
        v = heatmap.get(str(day), 0)
        tooltip = f"{day} — {v} solved"

        svg.append(
            f'<rect x="{c*(cell+gap)}" y="{r*(cell+gap)}" width="{cell}" height="{cell}" '
            f'rx="3" fill="{color(v)}"><title>{tooltip}</title></rect>'
        )

    # Legend
    svg.append('<g transform="translate(0, 110)">')

    legend = [
        ("0", "#ebf2ff"),
        ("1", "#c6dbff"),
        ("3", "#7bb0ff"),
        ("5", "#4a90ff"),
        ("10+", "#0066ff"),
    ]

    x_offset = 0
    for label, col in legend:
        svg.append(f'<rect x="{x_offset}" y="0" width="14" height="14" fill="{col}" />')
        svg.append(f'<text x="{x_offset + 20}" y="12" font-size="12">{label}</text>')
        x_offset += 55

    svg.append("</g></svg>")

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))


# ---------------------------------------------------------
# 실행
# ---------------------------------------------------------
recent = get_commits_recent()
all_commits = get_commits_all()

today_solved, weekly_solved, weekly_goal, heatmap_data = parse_recent_info(recent)
total_solved = parse_total_info(all_commits)

generate_donut(os.path.join(ASSETS, "today.svg"), today_solved, 1, "solved")
generate_donut(os.path.join(ASSETS, "weekly.svg"), weekly_solved, weekly_goal, "solved")
generate_donut(os.path.join(ASSETS, "total.svg"), total_solved, max(total_solved, 1), "solved")
generate_heatmap(os.path.join(ASSETS, "heatmap.svg"), heatmap_data)

with open(TEMPLATE, "r", encoding="utf-8") as f:
    txt = f.read()

now_kst = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
txt = txt.replace("{{TODAY_COUNT}}", str(today_solved))
txt = txt.replace("{{WEEKLY_COUNT}}", str(weekly_solved))
txt = txt.replace("{{WEEKLY_GOAL}}", str(weekly_goal))
txt = txt.replace("{{TOTAL_SOLVED}}", str(total_solved))
txt = txt.replace("{{UPDATED_AT}}", now_kst.strftime("%Y-%m-%d %H:%M"))
txt = txt.replace("{{USER}}", USER)
txt = txt.replace("{{REPO}}", REPO)

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write(txt)

print("README updated.")
