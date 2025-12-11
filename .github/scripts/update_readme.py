import os
import re
import math
import datetime
import subprocess
from collections import defaultdict

# -------------------------
# 경로 설정 (안정 버전)
# -------------------------
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
ASSETS = os.path.join(ROOT, "assets")
TEMPLATE = os.path.join(ROOT, "template_readme.md")
OUTPUT = os.path.join(ROOT, "README.md")

if not os.path.exists(ASSETS):
    os.makedirs(ASSETS)

# -------------------------
# Commit 로그 수집
# -------------------------
def get_commits():
    cmd = ["git", "log", "--since=60 days ago", "--pretty=%ad|%s", "--date=short"]
    lines = subprocess.check_output(cmd).decode().strip().split("\n")

    commits = []
    for line in lines:
        if "|" not in line:
            continue
        d, msg = line.split("|", 1)
        commits.append({"date": d, "msg": msg.strip()})
    return commits

# -------------------------
# Commit 파싱
# -------------------------
def parse_commit_info(commits):
    today = datetime.date.today()
    week_start = today - datetime.timedelta(days=today.weekday())

    today_solved = 0
    weekly_solved = 0
    total_solved = 0
    WEEKLY_GOAL = 10

    cat = {"이코테": 0, "프로그래머스": 0, "BOJ": 0}
    heatmap = defaultdict(int)

    for c in commits:
        msg = c["msg"]

        # 날짜 파싱 YYMMDD
        m = re.match(r"(\d{6})", msg)
        if not m:
            continue

        commit_date = datetime.datetime.strptime(m.group(1), "%y%m%d").date()

        solved_match = re.search(r"(\d+)문제", msg)
        solved = int(solved_match.group(1)) if solved_match else 0

        # 날짜별 누적
        if commit_date == today:
            today_solved += solved

        if commit_date >= week_start:
            weekly_solved += solved

        total_solved += solved
        heatmap[str(commit_date)] += solved

        # 카테고리
        if "이코테" in msg:
            cat["이코테"] += solved
        if "프로그래머스" in msg:
            cat["프로그래머스"] += solved
        if "BOJ" in msg or "boj" in msg.lower():
            cat["BOJ"] += solved

    return today_solved, weekly_solved, WEEKLY_GOAL, total_solved, cat, heatmap

# -------------------------
# Donut 그래프 생성
# -------------------------
def generate_donut(path, value, goal, label):
    percent = (value / goal) if goal else 0
    percent = min(percent, 1)

    radius = 40
    C = 2 * math.pi * radius
    progress = C * percent

    svg = f"""
<svg width="140" height="140">
  <circle cx="70" cy="70" r="{radius}" stroke="#e5e7eb" stroke-width="12" fill="none"/>
  <circle cx="70" cy="70" r="{radius}" stroke="#4aa3ff" stroke-width="12"
    fill="none" stroke-dasharray="{progress} {C-progress}"
    transform="rotate(-90 70 70)" stroke-linecap="round"/>
  <text x="70" y="70" font-size="20" text-anchor="middle" dominant-baseline="middle">{value}</text>
  <text x="70" y="95" font-size="12" text-anchor="middle">{label}</text>
</svg>
"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)

# -------------------------
# Heatmap 생성
# -------------------------
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

    cell = 18
    gap = 4
    rows = 7
    cols = math.ceil(len(dates) / rows)

    svg_w = cols * (cell + gap)
    svg_h = rows * (cell + gap)

    svg = f'<svg width="{svg_w}" height="{svg_h}">'

    for i, d in enumerate(dates):
        r = i % rows
        c = i // rows
        val = heatmap.get(str(d), 0)
        svg += f'<rect x="{c*(cell+gap)}" y="{r*(cell+gap)}" width="{cell}" height="{cell}" fill="{color(val)}" rx="3"/>'

    svg += "</svg>"

    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)

# -------------------------
# 실행
# -------------------------
commits = get_commits()
today_solved, weekly_solved, weekly_goal, total_solved, cat_count, heatmap_data = parse_commit_info(commits)

generate_donut(os.path.join(ASSETS, "today.svg"), today_solved, 1, "solved")
generate_donut(os.path.join(ASSETS, "weekly.svg"), weekly_solved, weekly_goal, "solved")
generate_donut(os.path.join(ASSETS, "total.svg"), total_solved, total_solved if total_solved else 1, "solved")

generate_donut(os.path.join(ASSETS, "ikote.svg"), cat_count["이코테"], cat_count["이코테"] or 1, "")
generate_donut(os.path.join(ASSETS, "programmers.svg"), cat_count["프로그래머스"], cat_count["프로그래머스"] or 1, "")
generate_donut(os.path.join(ASSETS, "boj.svg"), cat_count["BOJ"], cat_count["BOJ"] or 1, "")

generate_heatmap(os.path.join(ASSETS, "heatmap.svg"), heatmap_data)

# README 업데이트
with open(TEMPLATE, "r", encoding="utf-8") as f:
    t = f.read()

t = t.replace("{{TODAY_COUNT}}", str(today_solved))
t = t.replace("{{WEEKLY_COUNT}}", str(weekly_solved))
t = t.replace("{{WEEKLY_GOAL}}", str(weekly_goal))
t = t.replace("{{TOTAL_SOLVED}}", str(total_solved))
t = t.replace("{{UPDATED_AT}}", str(datetime.datetime.now())[:16])

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write(t)
