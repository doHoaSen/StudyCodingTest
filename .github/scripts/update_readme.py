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
# 문제 수 추출 함수
# ---------------------------------------------------------
def extract_solved(msg):
    nums = re.findall(r"(\d+)문제", msg)
    return sum(int(n) for n in nums) if nums else 0


# ---------------------------------------------------------
# 최근(today / weekly / heatmap)
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
        solved = extract_solved(c["msg"])

        # Heatmap
        heatmap[str(commit_date)] += solved

        if commit_date == today:
            today_solved += solved

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
# 도넛 그래프 색상 보간 (0% → 연파랑, 100% → #4aa3ff)
# ---------------------------------------------------------
def lerp(a, b, t):
    return int(a + (b - a) * t)


def donut_color(percent):
    start = (220, 236, 255)   # 0% → 매우 연한 파랑 (#dcecff)
    end = (74, 163, 255)      # 100% → 기존 색 #4aa3ff

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

    # 🎨 퍼센트 기반 색상
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
# Heatmap SVG (기존 블루 계열 유지 + 범례)
# ---------------------------------------------------------
def generate_heatmap(path, heatmap):
    today = datetime.date.today()
    dates = [(today - datetime.timedelta(days=i)) for i in range(59, -1, -1)]

    # 색상 규칙
    def color(v):
        if v == 0:
            return "#ebf2ff"    # 0
        if v <= 2:
            return "#7bb0ff"    # 1–2
        if v <= 5:
            return "#4a90ff"    # 3–5
        return "#0066ff"        # 6+

    cell, gap, rows, cols = 14, 4, 7, 10

    grid_width = cols * (cell + gap)
    grid_height = rows * (cell + gap)

    legend_height = 40
    padding = 20

    # 🔥 SVG 전체 높이/너비 넉넉하게
    total_width = 260
    total_height = grid_height + legend_height + padding

    svg = [
        f'<svg viewBox="0 0 {total_width} {total_height}" '
        f'width="{total_width}" height="{total_height}" xmlns="http://www.w3.org/2000/svg">'
    ]

    # -------------------------
    # 1) Heatmap 그리기
    # -------------------------
    for idx, day in enumerate(dates):
        r = idx % rows
        c = idx // rows

        v = heatmap.get(str(day), 0)
        tooltip = f"{day} — {v} solved"

        x = c * (cell + gap)
        y = r * (cell + gap)

        svg.append(
            f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="3" fill="{color(v)}">'
            f'<title>{tooltip}</title></rect>'
        )

    # -------------------------
    # 2) 범례 그리기
    # -------------------------
    legend_y = grid_height + 20
    legend_items = [
        ("0", "#ebf2ff"),
        ("1–2", "#7bb0ff"),
        ("3–5", "#4a90ff"),
        ("5+", "#0066ff"),
    ]

    x_offset = 10
    for label, col in legend_items:
        svg.append(
            f'<rect x="{x_offset}" y="{legend_y}" width="14" height="14" fill="{col}" />'
        )
        svg.append(
            f'<text x="{x_offset + 20}" y="{legend_y + 12}" font-size="13">{label}</text>'
        )
        x_offset += 70  # 넉넉하게 간격 확보

    svg.append("</svg>")

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))


# ---------------------------------------------------------
# 실행
# ---------------------------------------------------------
recent = get_commits_recent()
all_commits = get_commits_all()

today_solved, weekly_solved, weekly_goal_old, heatmap_data = parse_recent_info(recent)
total_solved = parse_total_info(all_commits)

# ---------- 수정된 목표값 설정 ----------
TODAY_GOAL = 3
WEEKLY_GOAL = 10
# total goal은 total_solved 자체가 goal

generate_donut(os.path.join(ASSETS, "today.svg"), today_solved, TODAY_GOAL, "solved")
generate_donut(os.path.join(ASSETS, "weekly.svg"), weekly_solved, WEEKLY_GOAL, "solved")
generate_donut(os.path.join(ASSETS, "total.svg"), total_solved, max(total_solved, 1), "solved")
generate_heatmap(os.path.join(ASSETS, "heatmap.svg"), heatmap_data)

with open(TEMPLATE, "r", encoding="utf-8") as f:
    txt = f.read()

now_kst = datetime.datetime.utcnow() + datetime.timedelta(hours=9)

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

