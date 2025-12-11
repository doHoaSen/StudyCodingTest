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
# 1) Commit Log 가져오기 (timestamp 기반)
# ---------------------------------------------------------
def get_commits():
    cmd = ["git", "log", "--since=60 days ago", "--pretty=%ct|%s"]
    out = subprocess.check_output(cmd).decode("utf-8").strip().split("\n")

    commits = []
    for line in out:
        if "|" not in line:
            continue
        ts, msg = line.split("|", 1)
        date = datetime.datetime.fromtimestamp(int(ts)).date()
        commits.append({"date": date, "msg": msg})
    return commits


# ---------------------------------------------------------
# 2) Commit 파싱
# ---------------------------------------------------------
def parse_commit_info(commits):
    today = datetime.date.today()
    week_start = today - datetime.timedelta(days=today.weekday())

    today_solved = 0
    weekly_solved = 0
    total_solved = 0
    WEEKLY_GOAL = 10

    heatmap = defaultdict(int)

    for c in commits:
        commit_date = c["date"]
        msg = c["msg"]

        m = re.search(r"(\d+)문제", msg)
        solved = int(m.group(1)) if m else 0

        if commit_date == today:
            today_solved += solved
        if commit_date >= week_start:
            weekly_solved += solved

        total_solved += solved
        heatmap[str(commit_date)] += solved

    return today_solved, weekly_solved, WEEKLY_GOAL, total_solved, heatmap


# ---------------------------------------------------------
# 3) Donut SVG 생성
# ---------------------------------------------------------
def generate_donut(path, value, goal, label):
    percent = 0 if goal == 0 else min(value / goal, 1)
    radius = 40
    C = 2 * math.pi * radius
    progress = percent * C

    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg width="160" height="160" xmlns="http://www.w3.org/2000/svg">
  <circle cx="80" cy="80" r="{radius}" stroke="#e5e7eb" stroke-width="12" fill="none"/>
  <circle cx="80" cy="80" r="{radius}" stroke="#4aa3ff" stroke-width="12"
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
# 4) Heatmap SVG 생성
# ---------------------------------------------------------
def generate_heatmap(path, heatmap):
    today = datetime.date.today()
    dates = [(today - datetime.timedelta(days=i)) for i in range(59, -1, -1)]

    def color(v):
        if v == 0: return "#ebedf0"
        if v < 2: return "#c6e48b"
        if v < 5: return "#7bc96f"
        if v < 10: return "#239a3b"
        return "#196127"

    cell = 14
    gap = 4
    cols = 10
    rows = 7

    svg_w = cols * (cell + gap)
    svg_h = rows * (cell + gap)

    svg = [f'<svg width="{svg_w}" height="{svg_h}" xmlns="http://www.w3.org/2000/svg">']

    for idx, day in enumerate(dates):
        r = idx % rows
        c = idx // rows

        v = heatmap.get(str(day), 0)
        fill = color(v)
        tooltip = f"{day} — {v} solved"

        svg.append(
            f'<rect x="{c * (cell + gap)}" y="{r * (cell + gap)}" '
            f'width="{cell}" height="{cell}" rx="3" fill="{fill}">'
            f'<title>{tooltip}</title></rect>'
        )

    svg.append("</svg>")

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))


# ---------------------------------------------------------
# 실행
# ---------------------------------------------------------
commits = get_commits()
today_solved, weekly_solved, weekly_goal, total_solved, heatmap_data = parse_commit_info(commits)

# Donut 생성
generate_donut(os.path.join(ASSETS, "today.svg"), today_solved, 1, "solved")
generate_donut(os.path.join(ASSETS, "weekly.svg"), weekly_solved, weekly_goal, "solved")
generate_donut(os.path.join(ASSETS, "total.svg"), total_solved, max(total_solved, 1), "solved")

# Heatmap 생성
generate_heatmap(os.path.join(ASSETS, "heatmap.svg"), heatmap_data)

# README 업데이트
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
