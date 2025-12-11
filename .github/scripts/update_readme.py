import os
import re
import json
import datetime
import pytz
import matplotlib.pyplot as plt
from matplotlib import font_manager

README_TEMPLATE = "README.md"
HISTORY_FILE = "solve_history.json"
ASSETS_DIR = "assets"

TODAY_SVG = f"{ASSETS_DIR}/today.svg"
WEEKLY_SVG = f"{ASSETS_DIR}/weekly.svg"
TOTAL_SVG = f"{ASSETS_DIR}/total.svg"
TREND_IMAGE_PATH = f"{ASSETS_DIR}/trend.png"

os.makedirs(ASSETS_DIR, exist_ok=True)

# ----------------------------
# 0. Install Korean Font for Matplotlib
# ----------------------------
font_path = "/usr/share/fonts/truetype/nanum/NanumGothic.ttf"
if not os.path.exists(font_path):
    os.system("sudo apt-get update")
    os.system("sudo apt-get install -y fonts-nanum")

plt.rc("font", family="NanumGothic")

# ----------------------------
# Count Java files
# ----------------------------
def count_java(path):
    if not os.path.exists(path):
        return 0
    return sum(1 for _, _, files in os.walk(path) for f in files if f.endswith(".java"))


ikote_count = count_java("src/이코테_자바")
programmers_count = count_java("src/programmers")
boj_count = count_java("src/BOJ")
total_solved = ikote_count + programmers_count + boj_count


# ----------------------------
# Extract activity by parsing git commits
# ----------------------------
def extract_problems(commit_text):
    """문제 목록을 파싱 (코드 조각 제거)"""
    lines = commit_text.split("\n")
    results = []
    for line in lines:
        if line.startswith("- "):
            name = line.replace("- ", "").strip()
            if len(name) < 40 and not name.startswith("/"):
                results.append(name)
    return results


# ----------------------------
# Today solved
# ----------------------------
today = datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%Y-%m-%d")
today_log = os.popen(f'git log --since="{today}" --pretty=format:"%H|||%s"').read()

today_solved = 0
for entry in today_log.split("\n"):
    if not entry.strip():
        continue
    commit_hash, msg = entry.split("|||")
    if not any(k in msg for k in ["프로그램", "프로그래머스", "이코테", "BOJ"]):
        continue
    full_commit = os.popen(f"git show {commit_hash}").read()
    today_solved += len(extract_problems(full_commit))


# ----------------------------
# Weekly solved (limit 10)
# ----------------------------
weekly_log = os.popen('git log --since="7 days ago" --pretty=format:"%H|||%s"').read()
weekly_solved = 0

for entry in weekly_log.split("\n"):
    if not entry.strip():
        continue
    commit_hash, msg = entry.split("|||")
    if not any(k in msg for k in ["프로그래머스", "BOJ"]):
        continue
    full_commit = os.popen(f"git show {commit_hash}").read()
    weekly_solved += len(extract_problems(full_commit))

weekly_progress = min(weekly_solved, 10)


# ----------------------------
# Update history.json
# ----------------------------
if os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        history = json.load(f)
else:
    history = {}

history[today] = total_solved

with open(HISTORY_FILE, "w", encoding="utf-8") as f:
    json.dump(history, f, indent=2, ensure_ascii=False)


# ----------------------------
# Trend Chart (last 7 days)
# ----------------------------
sorted_dates = sorted(history.keys())[-7:]
values = [history[d] for d in sorted_dates]

plt.figure(figsize=(8, 4))
plt.plot(sorted_dates, values, marker="o", color="#4A90E2")
plt.title("최근 7일 누적 문제 그래프", fontsize=14)
plt.grid(True, alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(TREND_IMAGE_PATH, dpi=200)
plt.close()


# ----------------------------
# Create SVG Progress Bar (Light Blue Dashboard)
# ----------------------------
def make_svg(value, max_value, path):
    pct = int((value / max_value) * 100)
    bar_w = int((value / max_value) * 240)

    svg = f"""
<svg width="260" height="40" xmlns="http://www.w3.org/2000/svg">
  <rect x="10" y="18" width="240" height="10" rx="5" fill="#E6ECF5"/>
  <rect x="10" y="18" width="{bar_w}" height="10" rx="5" fill="#8AB6F9"/>
  <text x="130" y="15" font-size="12" text-anchor="middle" fill="#333">{value} / {max_value} ({pct}%)</text>
</svg>
"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)


make_svg(today_solved, 10, TODAY_SVG)
make_svg(weekly_solved, 10, WEEKLY_SVG)
make_svg(total_solved, 500, TOTAL_SVG)


# ----------------------------
# Recent Activity Table
# ----------------------------
recent_rows = ""

git_recent = os.popen(
    'git log --since="7 days ago" --pretty=format:"%H|||%ad|||%s" --date=short'
).read()

for entry in git_recent.split("\n"):
    if not entry.strip():
        continue
    commit_hash, d, msg = entry.split("|||")

    if not any(k in msg for k in ["프로그래머스", "BOJ", "이코테"]):
        continue

    full = os.popen(f"git show {commit_hash}").read()
    problems = extract_problems(full)

    for p in problems:
        recent_rows += f"| {d} | {msg.split()[0]} | {p} |\n"


# ----------------------------
# Apply to README.md
# ----------------------------
with open(README_TEMPLATE, "r", encoding="utf-8") as f:
    readme = f.read()

now = datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%Y-%m-%d %H:%M")

new_readme = (
    readme.replace("{{TODAY_SOLVED}}", str(today_solved))
    .replace("{{WEEKLY_SOLVED}}", str(weekly_solved))
    .replace("{{TOTAL_SOLVED}}", str(total_solved))
    .replace("{{IKOTE_COUNT}}", str(ikote_count))
    .replace("{{PROGRAMMERS_COUNT}}", str(programmers_count))
    .replace("{{BOJ_COUNT}}", str(boj_count))
    .replace("{{RECENT_ACTIVITY_TABLE}}", recent_rows)
    .replace("{{LAST_UPDATE}}", now)
)

with open("README.md", "w", encoding="utf-8") as f:
    f.write(new_readme)

print("README updated.")
