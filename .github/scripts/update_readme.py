import os
import re
import math
import datetime
import pytz
import subprocess
from collections import defaultdict

# ---------------------------------------------------------
# 경로 설정
# ---------------------------------------------------------
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
ASSETS = os.path.join(ROOT, "assets")
TEMPLATE = os.path.join(ROOT, "template_readme.md")
OUTPUT = os.path.join(ROOT, "README.md")

USER = os.environ.get("GITHUB_REPOSITORY", "").split("/")[0]
REPO = os.environ.get("GITHUB_REPOSITORY", "").split("/")[1]

if not os.path.exists(ASSETS):
    os.makedirs(ASSETS)

# ---------------------------------------------------------
# KST 날짜 계산 함수
# ---------------------------------------------------------
def today_kst():
    kst = pytz.timezone("Asia/Seoul")
    return datetime.datetime.now(kst).date()

def to_kst_date(ts):
    kst = pytz.timezone("Asia/Seoul")
    return datetime.datetime.fromtimestamp(ts, kst).date()

# ---------------------------------------------------------
# git log 파싱
# ---------------------------------------------------------
def parse_log(out):
    commits = []
    for line in out:
        if "|" not in line:
            continue
        ts, msg = line.split("|", 1)
        date_kst = to_kst_date(int(ts))
        commits.append({"date": date_kst, "msg": msg})
    return commits

# ---------------------------------------------------------
# Commit fetcher
# ---------------------------------------------------------
def get_commits_recent():
    out = subprocess.check_output(
        ["git", "log", "--since=60 days ago", "--pretty=%ct|%s"]
    ).decode().strip().split("\n")
    return parse_log(out)

def get_commits_all():
    out = subprocess.check_output(
        ["git", "log", "--pretty=%ct|%s"]
    ).decode().strip().split("\n")
    return parse_log(out)

# ---------------------------------------------------------
# 문제 수 추출
# ---------------------------------------------------------
def extract_solved(msg):
    nums = re.findall(r"(\d+)문제", msg)
    return sum(int(n) for n in nums) if nums else 0

# ---------------------------------------------------------
# 최근(today, weekly, heatmap)
# ---------------------------------------------------------
def parse_recent_info(commits):
    today = today_kst()
    week_start = today - datetime.timedelta(days=today.weekday())

    today_solved = 0
    weekly_solved = 0
    WEEKLY_GOAL = 10

    heatmap = defaultdict(int)

    for c in commits:
        commit_date = c["date"]
        solved = extract_solved(c["msg"])

        # Heatmap(60일)
        heatmap[str(commit_date)] += solved

        if commit_date == today:
            today_solved += solved

        if commit_date >= week_start:
            weekly_solved += solved

    return today_solved, weekly_solved, WEEKLY_GOAL, heatmap

# ---------------------------------------------------------
# 전체 누적 해결 문제수
# ---------------------------------------------------------
def parse_total_info(commits):
    total = 0
    for c in commits:
        total += extract_solved(c["msg"])
    return total

# ---------------------------------------------------------
# Donut 색상 보간
# ---------------------------------------------------------
def lerp(a, b, t):
    return int(a + (b - a) * t)

def donut_color(percent):
    start = (220, 236, 255)
    end = (74, 163, 255)

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
# Heatmap SVG
# ---------------------------------------------------------
def generate_heatmap(path, heatmap):
    today = today_kst()
    dates = [(today - datetime.timedelta(days=i)) for i in range(59, -1, -1)]

    def color(v):
        if v == 0:
            return "#ebf2ff"
        if 1 <= v <= 3:
            return "#7bb0ff"
        if 4 <= v <= 5:
            return "#4a90ff"
        return "#0066ff"


    cell, gap, rows, cols = 14, 4, 7, 10
    width = cols * (cell + gap)
    height = rows * (cell + gap)

    svg = [f'<svg width="{width}" height="{height + 60}" xmlns="http://www.w3.org/2000/svg">']

    # Heatmap
    for idx, day in enumerate(dates):
        r = idx % rows
        c = idx // rows
        v = heatmap.get(str(day), 0)
        tooltip = f"{day} — {v} solved"

        svg.append(
            f'<rect x="{c*(cell+gap)}" y="{r*(cell+gap)}" '
            f'width="{cell}" height="{cell}" rx="3" fill="{color(v)}">'
            f'<title>{tooltip}</title></rect>'
        )

    # Legend
    legend_items = [
        ("0문제", "#ebf2ff"),
        ("1–3", "#7bb0ff"),
        ("4–5", "#4a90ff"),
        ("6+", "#0066ff"),
    ]



    legend_y = height + 20
    x_offset = 0

    for label, col in legend_items:
        svg.append(f'<rect x="{x_offset}" y="{legend_y}" width="12" height="12" fill="{col}" />')
        svg.append(f'<text x="{x_offset + 18}" y="{legend_y + 10}" font-size="10">{label}</text>')
        x_offset += 55   # 기존 60 → 55로 압축

    svg.append("</svg>")

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))

# ---------------------------------------------------------
# 실행
# ---------------------------------------------------------
recent = get_commits_recent()
all_commits = get_commits_all()

today_solved, weekly_solved, WEEKLY_GOAL, heatmap_data = parse_recent_info(recent)
total_solved = parse_total_info(all_commits)

TODAY_GOAL = 3
WEEKLY_GOAL = 10

generate_donut(os.path.join(ASSETS, "today.svg"), today_solved, TODAY_GOAL, "solved")
generate_donut(os.path.join(ASSETS, "weekly.svg"), weekly_solved, WEEKLY_GOAL, "solved")
generate_donut(os.path.join(ASSETS, "total.svg"), total_solved, max(total_solved, 1), "solved")
generate_heatmap(os.path.join(ASSETS, "heatmap.svg"), heatmap_data)

with open(TEMPLATE, "r", encoding="utf-8") as f:
    txt = f.read()

now_kst = datetime.datetime.now(pytz.timezone("Asia/Seoul"))

txt = txt.replace("{{TODAY_COUNT}}", str(today_solved))
txt = txt.replace("{{TODAY_GOAL}}", str(TODAY_GOAL))
txt = txt.replace("{{WEEKLY_COUNT}}", str(weekly_solved))
txt = txt.replace("{{WEEKLY_GOAL}}", str(WEEKLY_GOAL))
txt = txt.replace("{{TOTAL_SOLVED}}", str(total_solved))
txt = txt.replace("{{UPDATED_AT}}", now_kst.strftime("%Y-%m-%d %H:%M"))
txt = txt.replace("{{USER}}", USER)
txt = txt.replace("{{REPO}}", REPO)

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write(txt)

print("README updated.")
