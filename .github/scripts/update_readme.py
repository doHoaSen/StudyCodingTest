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

if not os.path.exists(ASSETS):
    os.makedirs(ASSETS)

# ---------------------------------------------------------
# 1) Commit Log 가져오기 (정확한 날짜/시간)
# ---------------------------------------------------------
def get_commits():
    cmd = [
        "git", "log",
        "--since=60 days ago",
        "--pretty=%ad|%s",
        "--date=short"
    ]
    logs = subprocess.check_output(cmd).decode("utf-8").strip().split("\n")

    commits = []
    for line in logs:
        if "|" not in line:
            continue
        date, msg = line.split("|", 1)
        commits.append({"date": date.strip(), "msg": msg.strip()})
    return commits


# ---------------------------------------------------------
# 2) Commit 파싱 (문제수 / 날짜 / 카테고리)
# ---------------------------------------------------------
def parse_commit_info(commits):

    today = datetime.date.today()
    week_start = today - datetime.timedelta(days=today.weekday())

    today_solved = 0
    weekly_solved = 0
    total_solved = 0
    WEEKLY_GOAL = 10

    cat = {"이코테": 0, "프로그래머스": 0, "BOJ": 0}
    heat = defaultdict(int)

    for c in commits:
        date = c["date"]
        msg = c["msg"]

        # 날짜 파싱
        try:
            commit_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        except:
            continue

        # N문제 파싱
        mm = re.search(r"(\d+)문제", msg)
        solved = int(mm.group(1)) if mm else 0

        # 오늘
        if commit_date == today:
            today_solved += solved

        # 이번 주
        if commit_date >= week_start:
            weekly_solved += solved

        total_solved += solved

        # 카테고리
        if "이코테" in msg:
            cat["이코테"] += solved
        if "프로그래머스" in msg:
            cat["프로그래머스"] += solved
        if "BOJ" in msg or "boj" in msg.lower():
            cat["BOJ"] += solved

        # Heatmap 기록
        heat[str(commit_date)] += solved

    return today_solved, weekly_solved, WEEKLY_GOAL, total_solved, cat, heat


# ---------------------------------------------------------
# 3) Donut SVG 생성 (GitHub 렌더 확정)
# ---------------------------------------------------------
def generate_donut(path, value, goal, label):
    percent = 0 if goal == 0 else min(value / goal, 1)
    radius = 45
    C = 2 * math.pi * radius
    progress = percent * C

    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg width="200" height="200" viewBox="0 0 200 200">
  <circle cx="100" cy="100" r="{radius}" stroke="#e5e7eb" stroke-width="14" fill="none"/>
  <circle cx="100" cy="100" r="{radius}" stroke="#4aa3ff" stroke-width="14" fill="none"
    stroke-dasharray="{progress} {C - progress}"
    transform="rotate(-90 100 100)"
    stroke-linecap="round"/>
  <text x="100" y="100" font-size="26" text-anchor="middle" dominant-baseline="middle">{value}</text>
  <text x="100" y="135" font-size="14" text-anchor="middle" fill="#555">{label}</text>
</svg>
"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)


# ---------------------------------------------------------
# 4) Heatmap SVG 생성 (GitHub 렌더 최적화)
# ---------------------------------------------------------
def generate_heatmap(path, heat):

    today = datetime.date.today()
    dates = [(today - datetime.timedelta(days=i)) for i in range(59, -1, -1)]

    def color(v):
        if v == 0: return "#ebedf0"
        if v < 2: return "#c6e48b"
        if v < 5: return "#7bc96f"
        if v < 10: return "#239a3b"
        return "#196127"

    cell = 18
    gap = 4
    rows = 7
    cols = math.ceil(len(dates) / rows)

    svg_w = cols * (cell + gap) + 40
    svg_h = rows * (cell + gap) + 40

    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg width="{svg_w}" height="{svg_h}" viewBox="0 0 {svg_w} {svg_h}">
"""

    for idx, d in enumerate(dates):
        r = idx % rows
        c = idx // rows
        v = heat.get(str(d), 0)
        x = 20 + c * (cell + gap)
        y = 20 + r * (cell + gap)
        svg += f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" fill="{color(v)}" rx="3"/>\n'

    svg += "</svg>"

    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)


# ---------------------------------------------------------
# 5) 실행
# ---------------------------------------------------------
commits = get_commits()
today_solved, weekly_solved, weekly_goal, total_solved, cat, heat = parse_commit_info(commits)

# Donuts
generate_donut(os.path.join(ASSETS, "today.svg"), today_solved, 1, "solved")
generate_donut(os.path.join(ASSETS, "weekly.svg"), weekly_solved, weekly_goal, "solved")
generate_donut(os.path.join(ASSETS, "total.svg"), total_solved, max(total_solved, 1), "solved")

generate_donut(os.path.join(ASSETS, "ikote.svg"), cat["이코테"], max(cat["이코테"], 1), "")
generate_donut(os.path.join(ASSETS, "programmers.svg"), cat["프로그래머스"], max(cat["프로그래머스"], 1), "")
generate_donut(os.path.join(ASSETS, "boj.svg"), cat["BOJ"], max(cat["BOJ"], 1), "")

# Heatmap
generate_heatmap(os.path.join(ASSETS, "heatmap.svg"), heat)

# README update
with open(TEMPLATE, "r", encoding="utf-8") as f:
    txt = f.read()

txt = txt.replace("{{TODAY_COUNT}}", str(today_solved))
txt = txt.replace("{{WEEKLY_COUNT}}", str(weekly_solved))
txt = txt.replace("{{WEEKLY_GOAL}}", str(weekly_goal))
txt = txt.replace("{{TOTAL_SOLVED}}", str(total_solved))
txt = txt.replace("{{UPDATED_AT}}", str(datetime.datetime.now())[:16])

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write(txt)

print("README updated.")
