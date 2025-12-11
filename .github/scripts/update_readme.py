import os, re, math, datetime, subprocess
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
ASSETS = os.path.join(ROOT, "assets")
TEMPLATE = os.path.join(ROOT, "template_readme.md")
OUTPUT = os.path.join(ROOT, "README.md")

USER = os.environ.get("GITHUB_REPOSITORY", "").split("/")[0]
REPO = os.environ.get("GITHUB_REPOSITORY", "").split("/")[1]

os.makedirs(ASSETS, exist_ok=True)

# ------------------------------------------------------
# 1) Git commit log 가져오기
# ------------------------------------------------------
def get_commits():
    cmd = ["git", "log", "--since=60 days ago", "--pretty=%ad|%s", "--date=short"]
    lines = subprocess.check_output(cmd).decode().strip().split("\n")
    commits = []
    for ln in lines:
        if "|" not in ln:
            continue
        date, msg = ln.split("|", 1)
        commits.append({"date": date, "msg": msg.strip()})
    return commits


# ------------------------------------------------------
# 2) commit 정보 파싱
# ------------------------------------------------------
def parse_commit_info(commits):
    today = datetime.date.today()
    week_start = today - datetime.timedelta(days=today.weekday())

    today_solved = 0
    weekly_solved = 0
    total_solved = 0
    WEEKLY_GOAL = 10

    category = {"이코테": 0, "프로그래머스": 0, "BOJ": 0}
    heat = defaultdict(int)

    for c in commits:
        git_date = datetime.datetime.strptime(c["date"], "%Y-%m-%d").date()
        msg = c["msg"]

        m = re.search(r"(\d+)문제", msg)
        solved = int(m.group(1)) if m else 0

        total_solved += solved

        if git_date == today:
            today_solved += solved

        if git_date >= week_start:
            weekly_solved += solved

        if "이코테" in msg:
            category["이코테"] += solved
        elif "프로그래머스" in msg:
            category["프로그래머스"] += solved
        elif "BOJ" in msg or "boj" in msg.lower():
            category["BOJ"] += solved

        heat[str(git_date)] += solved

    return today_solved, weekly_solved, WEEKLY_GOAL, total_solved, category, heat


# ------------------------------------------------------
# 3) Donut SVG 생성
# ------------------------------------------------------
def generate_donut(path, value, goal, label):
    percent = 0 if goal == 0 else min(value / goal, 1)
    radius = 42
    C = 2 * math.pi * radius
    progress = percent * C

    svg = f"""
<svg width="140" height="140">
  <circle cx="70" cy="70" r="{radius}" stroke="#e6e6e6" stroke-width="10" fill="none"/>
  <circle cx="70" cy="70" r="{radius}" stroke="#4aa3ff" stroke-width="10"
    fill="none"
    stroke-dasharray="{progress} {C-progress}"
    transform="rotate(-90 70 70)"
    stroke-linecap="round"/>

  <text x="70" y="65" text-anchor="middle" font-size="20" fill="#333">{value}</text>
  <text x="70" y="90" text-anchor="middle" font-size="12" fill="#666">{label}</text>
</svg>
"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)


# ------------------------------------------------------
# 4) Heatmap SVG 생성
# ------------------------------------------------------
def generate_heatmap(path, heat):
    today = datetime.date.today()
    dates = [(today - datetime.timedelta(days=i)) for i in range(59, -1, -1)]
    maxv = max(heat.values()) if heat else 1

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

    svg_w = cols * (cell + gap) + 20
    svg_h = rows * (cell + gap) + 20

    svg = f'<svg width="{svg_w}" height="{svg_h}">'

    for idx, d in enumerate(dates):
        r = idx % rows
        c = idx // rows
        v = heat.get(str(d), 0)
        x = 10 + c * (cell + gap)
        y = 10 + r * (cell + gap)
        svg += f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" fill="{color(v)}" rx="3"/>'

    svg += "</svg>"

    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)


# ------------------------------------------------------
# 실행
# ------------------------------------------------------
commits = get_commits()
today_solved, weekly_solved, weekly_goal, total_solved, cat_count, heat_data = parse_commit_info(commits)

generate_donut(os.path.join(ASSETS, "today.svg"), today_solved, 1, "solved")
generate_donut(os.path.join(ASSETS, "weekly.svg"), weekly_solved, weekly_goal, "solved")
generate_donut(os.path.join(ASSETS, "total.svg"), total_solved, total_solved if total_solved else 1, "solved")

generate_donut(os.path.join(ASSETS, "ikote.svg"), cat_count["이코테"], cat_count["이코테"] or 1, "")
generate_donut(os.path.join(ASSETS, "programmers.svg"), cat_count["프로그래머스"], cat_count["프로그래머스"] or 1, "")
generate_donut(os.path.join(ASSETS, "boj.svg"), cat_count["BOJ"], cat_count["BOJ"] or 1, "")

generate_heatmap(os.path.join(ASSETS, "heatmap.svg"), heat_data)

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
