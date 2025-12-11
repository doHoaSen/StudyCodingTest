import os
import re
import json
import datetime
import pytz

# Repo name 자동 감지
REPO = os.popen("git config --get remote.origin.url").read().strip()
REPO = REPO.replace("https://github.com/", "").replace(".git", "")

ROOT = "."
ASSETS = "assets"
os.makedirs(ASSETS, exist_ok=True)

TEMPLATE = "template_readme.md"
README = "README.md"
HISTORY = "solve_history.json"

# ------------ Java file counter ------------
def count_java(path):
    if not os.path.exists(path):
        return 0
    return sum(
        1 for _, _, files in os.walk(path) for f in files if f.endswith(".java")
    )

ikote = count_java("src/이코테_자바")
programmers = count_java("src/programmers")
boj = count_java("src/BOJ") if os.path.exists("src/BOJ") else 0
total = ikote + programmers + boj

# ------------ Today / weekly solved (file based) ------------
today_str = datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%Y-%m-%d")

def get_git_changes(since):
    """Count modified Java files since given date."""
    log = os.popen(f'git log --since="{since}" --name-only --pretty=format:').read()
    return sum(1 for line in log.split("\n") if line.strip().endswith(".java"))

today_solved = get_git_changes(today_str)
weekly_solved = get_git_changes("7 days ago")
if weekly_solved > 10:
    weekly_solved = 10

# ------------ Save history for heatmap ------------
today_date = datetime.date.today().isoformat()

if os.path.exists(HISTORY):
    history = json.load(open(HISTORY, "r", encoding="utf-8"))
else:
    history = {}

history[today_date] = total
json.dump(history, open(HISTORY, "w", encoding="utf-8"), indent=2)

# ------------ Donut Chart Generator ------------
def donut_svg(value, total):
    percent = 0 if total == 0 else (value / total) * 100
    dash = f"{percent} {100 - percent}"

    return f'''
<svg width="160" height="160" viewBox="0 0 36 36" xmlns="http://www.w3.org/2000/svg">
  <circle cx="18" cy="18" r="15.9155"
      fill="none" stroke="#e6e6e6" stroke-width="3"/>
  <circle cx="18" cy="18" r="15.9155"
      fill="none" stroke="#4ea3ff" stroke-width="3"
      stroke-dasharray="{dash}" stroke-linecap="round"
      transform="rotate(-90 18 18)"/>

  <text x="18" y="18" font-size="7" fill="#222"
        text-anchor="middle" dominant-baseline="central"
        font-family="DejaVu Sans">{value}</text>

  <text x="18" y="23" font-size="3.5" fill="#666"
        text-anchor="middle" font-family="DejaVu Sans">
      solved
  </text>
</svg>
'''

# Save donut SVGs
open(f"{ASSETS}/today.svg", "w").write(donut_svg(today_solved, 10))
open(f"{ASSETS}/weekly.svg", "w").write(donut_svg(weekly_solved, 10))
open(f"{ASSETS}/total.svg", "w").write(donut_svg(total, 500))
open(f"{ASSETS}/category_total.svg", "w").write(donut_svg(total, total or 1))
open(f"{ASSETS}/ikote.svg", "w").write(donut_svg(ikote, total or 1))
open(f"{ASSETS}/programmers.svg", "w").write(donut_svg(programmers, total or 1))
open(f"{ASSETS}/boj.svg", "w").write(donut_svg(boj, total or 1))

# ------------ Heatmap SVG ------------
def heatmap_svg(history):
    """Generate 60-day heatmap like GitHub style."""
    today = datetime.date.today()
    days = [today - datetime.timedelta(days=i) for i in range(59, -1, -1)]

    # Normalize values
    vals = [history.get(d.isoformat(), 0) for d in days]
    maxv = max(vals) if max(vals) > 0 else 1

    # Color scale
    def color(v):
        level = int((v / maxv) * 4)
        colors = ["#ebedf0", "#c6e48b", "#7bc96f", "#239a3b", "#196127"]
        return colors[level]

    svg = '<svg width="700" height="120" xmlns="http://www.w3.org/2000/svg">'
    x = 10
    y = 20
    for i, day in enumerate(days):
        v = vals[i]
        svg += f'<rect x="{x}" y="{y}" width="10" height="10" fill="{color(v)}"/>'
        x += 12
    svg += "</svg>"
    return svg

open(f"{ASSETS}/heatmap.svg", "w").write(heatmap_svg(history))

# ------------ Build README ------------
last_update = datetime.datetime.now(
    pytz.timezone("Asia/Seoul")
).strftime("%Y-%m-%d %H:%M")

readme = open(TEMPLATE, "r", encoding="utf-8").read()
readme = (
    readme.replace("{{TODAY_SOLVED}}", str(today_solved))
    .replace("{{WEEKLY_SOLVED}}", str(weekly_solved))
    .replace("{{TOTAL_SOLVED}}", str(total))
    .replace("{{IKOTE_COUNT}}", str(ikote))
    .replace("{{PROGRAMMERS_COUNT}}", str(programmers))
    .replace("{{BOJ_COUNT}}", str(boj))
    .replace("{{LAST_UPDATE}}", last_update)
    .replace("{{REPO}}", REPO)
)

open(README, "w", encoding="utf-8").write(readme)

print("README updated.")
