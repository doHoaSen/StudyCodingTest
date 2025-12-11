import os
import re
import math
import datetime
import subprocess
from collections import defaultdict

# ============================================================
# 0) 경로 설정 — Repo root 정확히 지정
# ============================================================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(SCRIPT_DIR))   # repo root
ASSETS = os.path.join(ROOT, "assets")

if not os.path.exists(ASSETS):
    os.makedirs(ASSETS)

TEMPLATE = os.path.join(ROOT, "template_readme.md")
OUTPUT = os.path.join(ROOT, "README.md")

USER, REPO = os.environ.get("GITHUB_REPOSITORY", "user/repo").split("/")

# ============================================================
# 1) Commit Log 가져오기
# ============================================================
def get_commits():
    cmd = ["git", "log", "--since=60 days ago", "--pretty=%ad|%s", "--date=short"]
    out = subprocess.check_output(cmd).decode().strip().split("\n")
    commits = []
    for line in out:
        if "|" not in line:
            continue
        date, msg = line.split("|", 1)
        commits.append({"date": date, "msg": msg})
    return commits

# ============================================================
# 2) Commit 파싱
# ============================================================
def parse_commit_info(commits):
    today = datetime.date.today()
    week_start = today - datetime.timedelta(days=today.weekday())

    today_solved = 0
    weekly_solved = 0
    total_solved = 0
    WEEKLY_GOAL = 10

    cat_count = {"이코테": 0, "프로그래머스": 0, "BOJ": 0}
    heatmap = defaultdict(int)

    for c in commits:
        msg = c["msg"].strip()

        m = re.match(r"(\d{6})\s+(.*)", msg)
        if not m:
            continue

        commit_date = datetime.datetime.strptime(m.group(1), "%y%m%d").date()

        # solved count
        mm = re.search(r"(\d+)문제", msg)
        solved = int(mm.group(1)) if mm else 0

        if commit_date == today:
            today_solved += solved
        if commit_date >= week_start:
            weekly_solved += solved
        total_solved += solved

        # 카테고리 판별
        body = m.group(2)
        if "이코테" in body:
            cat_count["이코테"] += solved
        elif "프로그래머스" in body:
            cat_count["프로그래머스"] += solved
        elif "BOJ" in body or "boj" in body.lower():
            cat_count["BOJ"] += solved

        heatmap[str(commit_date)] += solved

    return today_solved, weekly_solved, WEEKLY_GOAL, total_solved, cat_count, heatmap

# ============================================================
# 3) Donut SVG 생성
# ============================================================
def generate_donut(path, value, goal, label):
    percent = 0 if goal == 0 else min(value / goal, 1)
    r = 40
    C = 2 * math.pi * r
    progress = percent * C

    svg = f"""
<svg width="120" height="120">
  <circle cx="60" cy="60" r="{r}" stroke="#e6e6e6" stroke-width="10" fill="none"/>
  <circle cx="60" cy="60" r="{r}" stroke="#4aa3ff" stroke-width="10"
    fill="none"
    stroke-dasharray="{progress} {C-progress}"
    transform="rotate(-90 60 60)"
    stroke-linecap="round"/>
  <text x="60" y="60" font-size="18" text-anchor="middle" dominant-baseline="middle">{value}</text>
  <text x="60" y="85" font-size="11" text-anchor="middle" fill="#555">{label}</text>
</svg>
"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)

# ============================================================
# 4) Heatmap SVG
# ============================================================
def generate_heatmap(path, heatmap):
    today = datetime.date.today()
    dates = [(today - datetime.timedelta(days=i)) for i in range(59, -1, -1)]

    max_val = max(heatmap.values()) if heatmap else 1

    def color(v):
        if v == 0: return "#ebedf0"
        if v < 2: return "#c6e48b"
        if v < 5: return "#7bc96f"
        if v < 10: return "#239a3b"
        return "#196127"

    cell = 14
    gap = 3
    cols = 9
    rows = 7

    svg_w = cols * (cell + gap)
    svg_h = rows * (cell + gap)

    svg = [f'<svg width="{svg_w}" height="{svg_h}">']

    for idx, d in enumerate(dates):
        r = idx % rows
        c = idx // rows
        v = heatmap.get(str(d), 0)
        svg.append(
            f'<rect x="{c*(cell+gap)}" y="{r*(cell+gap)}" width="{cell}" height="{cell}" fill="{color(v)}" rx="3"/>'
        )

    svg.append("</svg>")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))

# ============================================================
# 실행
# ============================================================
commits = get_commits()
today_solved, weekly_solved, weekly_goal, total_solved, cat_count, heatmap_data = parse_commit_info(commits)

# Donuts
generate_donut(os.path.join(ASSETS, "today.svg"), today_solved, 1, "solved")
generate_donut(os.path.join(ASSETS, "weekly.svg"), weekly_solved, weekly_goal, "solved")
generate_donut(os.path.join(ASSETS, "total.svg"), total_solved, total_solved or 1, "solved")

generate_donut(os.path.join(ASSETS, "ikote.svg"), cat_count["이코테"], max(cat_count["이코테"], 1), f"{cat_count['이코테']}")
generate_donut(os.path.join(ASSETS, "programmers.svg"), cat_count["프로그래머스"], max(cat_count["프로그래머스"], 1), f"{cat_count['프로그래머스']}")
generate_donut(os.path.join(ASSETS, "boj.svg"), cat_count["BOJ"], max(cat_count["BOJ"], 1), f"{cat_count['BOJ']}")

generate_heatmap(os.path.join(ASSETS, "heatmap.svg"), heatmap_data)

# README update
with open(TEMPLATE, "r", encoding="utf-8") as f:
    txt = f.read()

txt = txt.replace("{{TODAY_COUNT}}", str(today_solved))
txt = txt.replace("{{WEEKLY_COUNT}}", str(weekly_solved))
txt = txt.replace("{{WEEKLY_GOAL}}", str(weekly_goal))
txt = txt.replace("{{TOTAL_SOLVED}}", str(total_solved))
txt = txt.replace("{{USER}}", USER)
txt = txt.replace("{{REPO}}", REPO)
txt = txt.replace("{{UPDATED_AT}}", str(datetime.datetime.now())[:16])

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write(txt)

print("README updated.")
