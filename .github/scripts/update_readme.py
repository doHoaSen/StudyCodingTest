import os
import re
import math
import datetime
import pytz
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
# 1) Commit 로그 가져오기 (timestamp 기반)
# ---------------------------------------------------------
def get_commits():
    cmd = [
        "git",
        "log",
        "--since=60 days ago",
        "--pretty=%H|%s"
    ]
    out = subprocess.check_output(cmd).decode().strip().split("\n")

    commits = []
    for line in out:
        if "|" not in line:
            continue

        sha, msg = line.split("|", 1)

        ts = subprocess.check_output(
            ["git", "show", "-s", "--format=%ct", sha]
        ).decode().strip()

        commit_date = datetime.datetime.utcfromtimestamp(int(ts)).date()

        commits.append({
            "date": commit_date,
            "msg": msg.strip()
        })

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

    cat_count = {"이코테": 0, "프로그래머스": 0, "BOJ": 0}
    heatmap = defaultdict(int)

    for c in commits:
        commit_date = c["date"]
        msg = c["msg"]

        # YYMMDD 패턴이 있는 커밋만 처리
        match = re.match(r"(\d{6})\s+(.+)", msg)
        if not match:
            continue

        # N문제 파싱
        num_match = re.search(r"(\d+)문제", msg)
        solved = int(num_match.group(1)) if num_match else 0

        # 오늘/주간/누적
        if commit_date == today:
            today_solved += solved
        if commit_date >= week_start:
            weekly_solved += solved

        total_solved += solved
        heatmap[str(commit_date)] += solved

        # 카테고리 카운트
        if "이코테" in msg:
            cat_count["이코테"] += solved
        if "프로그래머스" in msg:
            cat_count["프로그래머스"] += solved
        if "BOJ" in msg or "boj" in msg.lower():
            cat_count["BOJ"] += solved

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
<svg width="160" height="160">
  <circle cx="80" cy="80" r="{radius}" stroke="#e5e7eb" stroke-width="12" fill="none"/>
  <circle cx="80" cy="80" r="{radius}"
    stroke="#4aa3ff" stroke-width="12" fill="none"
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
def generate_heatmap(path, data):
    today = datetime.date.today()
    dates = [(today - datetime.timedelta(days=i)) for i in range(59, -1, -1)]

    max_val = max(data.values()) if data else 1

    cell = 18
    gap = 4
    rows = 7
    cols = math.ceil(len(dates) / rows)

    svg_w = cols * (cell + gap)
    svg_h = rows * (cell + gap)

    def color(v):
        if v == 0: return "#ebedf0"
        if v < 2: return "#c6e48b"
        if v < 5: return "#7bc96f"
        if v < 10: return "#239a3b"
        return "#196127"

    svg = f'<svg width="{svg_w}" height="{svg_h}">'

    for idx, d in enumerate(dates):
        r = idx % rows
        c = idx // rows
        val = data.get(str(d), 0)
        svg += f'<rect x="{c*(cell+gap)}" y="{r*(cell+gap)}" width="{cell}" height="{cell}" fill="{color(val)}" rx="3"/>'

    svg += '</svg>'

    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)


# ---------------------------------------------------------
# 실행
# ---------------------------------------------------------
commits = get_commits()
today_solved, weekly, weekly_goal, total, cat, heatmap_data = parse_commit_info(commits)

generate_donut(os.path.join(ASSETS, "today.svg"), today_solved, 1, "solved")
generate_donut(os.path.join(ASSETS, "weekly.svg"), weekly, weekly_goal, "solved")
generate_donut(os.path.join(ASSETS, "total.svg"), total, total if total else 1, "solved")

generate_donut(os.path.join(ASSETS, "ikote.svg"), cat["이코테"], max(cat["이코테"], 1), "")
generate_donut(os.path.join(ASSETS, "programmers.svg"), cat["프로그래머스"], max(cat["프로그래머스"], 1), "")
generate_donut(os.path.join(ASSETS, "boj.svg"), cat["BOJ"], max(cat["BOJ"], 1), "")

generate_heatmap(os.path.join(ASSETS, "heatmap.svg"), heatmap_data)

KST = pytz.timezone("Asia/Seoul")
updated = datetime.datetime.now(KST).strftime("%Y-%m-%d %H:%M")

with open(TEMPLATE, "r", encoding="utf-8") as f:
    txt = f.read()

txt = txt.replace("{{TODAY_COUNT}}", str(today_solved))
txt = txt.replace("{{WEEKLY_COUNT}}", str(weekly))
txt = txt.replace("{{WEEKLY_GOAL}}", str(weekly_goal))
txt = txt.replace("{{TOTAL_SOLVED}}", str(total))
txt = txt.replace("{{UPDATED_AT}}", updated)
txt = txt.replace("{{USER}}", USER)
txt = txt.replace("{{REPO}}", REPO)

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write(txt)

print("README updated.")
