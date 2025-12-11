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
# 1) Commit Log 가져오기
# ---------------------------------------------------------
def get_commits():
    cmd = ["git", "log", "--since=60 days ago", "--pretty=%ad|%s", "--date=short"]
    out = subprocess.check_output(cmd).decode("utf-8").strip().split("\n")
    commits = []
    for line in out:
        if "|" not in line:
            continue
        date, msg = line.split("|", 1)
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
    WEEKLY_GOAL = 10  # 고정 목표

    cat_count = {"이코테": 0, "프로그래머스": 0, "BOJ": 0}
    heatmap = defaultdict(int)

    for c in commits:
        msg = c["msg"].strip()

        # YYMMDD date part 파싱
        m = re.match(r"(\d{6})\s+(.*)", msg)
        if not m:
            continue

        date_str = m.group(1)
        category_info = m.group(2)

        commit_date = datetime.datetime.strptime(date_str, "%y%m%d").date()

        # N문제 파싱
        mm = re.search(r"(\d+)문제", msg)
        solved = int(mm.group(1)) if mm else 0

        # 오늘/주간 계산
        if commit_date == today:
            today_solved += solved

        if commit_date >= week_start:
            weekly_solved += solved

        total_solved += solved

        # 카테고리 분류
        if "이코테" in msg:
            cat_count["이코테"] += solved
        elif "프로그래머스" in msg:
            cat_count["프로그래머스"] += solved
        elif "BOJ" in msg or "boj" in msg.lower():
            cat_count["BOJ"] += solved

        # Heatmap 기록
        heatmap[str(commit_date)] += solved

    return today_solved, weekly_solved, WEEKLY_GOAL, total_solved, cat_count, heatmap


# ---------------------------------------------------------
# 3) Donut SVG 생성
# ---------------------------------------------------------
def generate_donut(path, value, goal, label):
    percent = 0 if goal == 0 else min(value / goal, 1)
    radius = 40
    C = 2 * math.pi * radius
    progress = percent * C

    svg = f"""
<svg width="120" height="120">
  <circle cx="60" cy="60" r="{radius}" stroke="#ddd" stroke-width="10" fill="none"/>
  <circle cx="60" cy="60" r="{radius}" stroke="#4aa3ff" stroke-width="10"
    fill="none"
    stroke-dasharray="{progress} {C - progress}"
    transform="rotate(-90 60 60)"
    stroke-linecap="round"/>
  <text x="60" y="60" font-size="18" text-anchor="middle" dominant-baseline="middle">{value}</text>
  <text x="60" y="85" font-size="11" text-anchor="middle" fill="#555">{label}</text>
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
    max_val = max(heatmap.values()) if heatmap else 1

    # 깃허브 스타일 색상 단계
    def color(v):
        if v == 0: return "#ebedf0"
        if v < 2: return "#c6e48b"
        if v < 5: return "#7bc96f"
        if v < 10: return "#239a3b"
        return "#196127"

    # 7행 × 9열(63칸) grid
    cell = 14
    gap = 3
    cols = 9
    rows = 7

    svg_w = cols * (cell + gap)
    svg_h = rows * (cell + gap)

    svg = f'<svg width="{svg_w}" height="{svg_h}">'

    for idx, d in enumerate(dates):
        r = idx % rows
        c = idx // rows
        val = heatmap.get(str(d), 0)
        svg += f'<rect x="{c * (cell + gap)}" y="{r * (cell + gap)}" width="{cell}" height="{cell}" fill="{color(val)}" rx="3" />'

    svg += "</svg>"

    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)


# ---------------------------------------------------------
# 실행
# ---------------------------------------------------------
commits = get_commits()
today_solved, weekly_solved, weekly_goal, total_solved, cat_count, heatmap_data = parse_commit_info(commits)

# Donut 그래프 생성
generate_donut(os.path.join(ASSETS, "today.svg"), today_solved, 1, "solved")
generate_donut(os.path.join(ASSETS, "weekly.svg"), weekly_solved, weekly_goal, "solved")
generate_donut(os.path.join(ASSETS, "total.svg"), total_solved, total_solved if total_solved else 1, "solved")

generate_donut(os.path.join(ASSETS, "ikote.svg"), cat_count["이코테"], cat_count["이코테"] if cat_count["이코테"] else 1, "")
generate_donut(os.path.join(ASSETS, "programmers.svg"), cat_count["프로그래머스"], cat_count["프로그래머스"] if cat_count["프로그래머스"] else 1, "")
generate_donut(os.path.join(ASSETS, "boj.svg"), cat_count["BOJ"], cat_count["BOJ"] if cat_count["BOJ"] else 1, "")

# Heatmap 생성
generate_heatmap(os.path.join(ASSETS, "heatmap.svg"), heatmap_data)

# README 업데이트
with open(TEMPLATE, "r", encoding="utf-8") as f:
    txt = f.read()

txt = txt.replace("{{TODAY_COUNT}}", str(today_solved))
txt = txt.replace("{{WEEKLY_COUNT}}", str(weekly_solved))
txt = txt.replace("{{WEEKLY_GOAL}}", str(weekly_goal))
txt = txt.replace("{{TOTAL_SOLVED}}", str(total_solved))
txt = txt.replace("{{UPDATED_AT}}", str(datetime.datetime.now())[:16])
txt = txt.replace("{{USER}}", USER)
txt = txt.replace("{{REPO}}", REPO)

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write(txt)

print("README updated.")
