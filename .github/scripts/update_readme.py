import os
import re
import json
import datetime
import pytz
import matplotlib.pyplot as plt

README_TEMPLATE = "README.md"
HISTORY_FILE = "solve_history.json"

ASSETS = "assets"
TREND_IMAGE_PATH = f"{ASSETS}/trend.png"

os.makedirs(ASSETS, exist_ok=True)


# ---------------------- Helper Functions ----------------------
def count_java_files(path):
    if not os.path.exists(path):
        return 0
    return sum(1 for _, _, files in os.walk(path) for f in files if f.endswith(".java"))


def svg_progress_bar(filename, value, max_value, bar_color="#4CAF50"):
    percent = int((value / max_value) * 100) if max_value > 0 else 0
    bar_width = int(3 * percent)

    svg = f"""
<svg width="300" height="30" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="10" width="300" height="10" fill="#ddd" rx="5"/>
  <rect x="0" y="10" width="{bar_width}" height="10" fill="{bar_color}" rx="5"/>
  <text x="150" y="25" font-size="12" text-anchor="middle" fill="#333">
    {value} / {max_value} ({percent}%)
  </text>
</svg>
"""
    with open(f"{ASSETS}/{filename}", "w", encoding="utf-8") as f:
        f.write(svg)


# ---------------------- Count ----------------------
ikote_count = count_java_files("src/이코테_자바")
programmers_count = count_java_files("src/programmers")
boj_count = count_java_files("src/BOJ")

total_solved = ikote_count + programmers_count + boj_count


# ---------------------- Today Solve Count ----------------------
today = datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%Y-%m-%d")

today_solved = 0
today_log = os.popen(f'git log --since="{today}" --pretty=format:"%s"').read()

for msg in today_log.split("\n"):
    if any(k in msg for k in ["프로그래머스", "이코테", "BOJ"]):
        today_solved += 1


# ---------------------- Weekly Solve Count ----------------------
weekly_solved = 0
weekly_log = os.popen('git log --since="7 days ago" --pretty=format:"%s"').read()

for msg in weekly_log.split("\n"):
    if any(k in msg for k in ["프로그래머스", "이코테", "BOJ"]):
        weekly_solved += 1

weekly_progress = min(weekly_solved, 10)


# ---------------------- Save History ----------------------
if os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        history = json.load(f)
else:
    history = {}

history[today] = total_solved

with open(HISTORY_FILE, "w", encoding="utf-8") as f:
    json.dump(history, f, indent=2, ensure_ascii=False)


# ---------------------- Generate Trend Chart ----------------------
dates = sorted(history.keys())
values = [history[d] for d in dates]

plt.figure(figsize=(8, 4))
plt.plot(dates, values, marker="o", color="#40c463")
plt.title("최근 문제 풀이 추세", fontsize=14)
plt.xlabel("날짜")
plt.ylabel("누적 문제 수")
plt.grid(True, alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(TREND_IMAGE_PATH, dpi=200)
plt.close()


# ---------------------- Recent 7 days activity ----------------------
recent_rows = ""
git_recent = os.popen(
    'git log --since="7 days ago" --pretty=format:"%ad|||%s" --date=short'
).read()

for row in git_recent.split("\n"):
    if not any(k in row for k in ["프로그래머스", "이코테", "BOJ"]):
        continue

    date, msg = row.split("|||")
    msg = msg.strip()

    if "프로그래머스" in msg:
        category = "프로그래머스"
    elif "이코테" in msg:
        category = "이코테"
    else:
        category = "BOJ"

    problem = (
        msg.replace("프로그래머스", "")
        .replace("이코테", "")
        .replace("BOJ", "")
        .strip()
    )

    recent_rows += f"| {date} | {category} | {problem} |\n"


# ---------------------- Generate SVG Progress Bars ----------------------
svg_progress_bar("today.svg", today_solved, 10, "#ff9800")
svg_progress_bar("weekly.svg", weekly_progress, 10, "#3f51b5")
svg_progress_bar("total.svg", total_solved, 500, "#4CAF50")


# ---------------------- Replace README ----------------------
with open(README_TEMPLATE, "r", encoding="utf-8") as f:
    readme = f.read()

now = datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%Y-%m-%d %H:%M")

new_readme = (
    readme.replace("{{TODAY_SOLVED}}", str(today_solved))
    .replace("{{WEEKLY_PROGRESS}}", str(weekly_progress))
    .replace("{{TOTAL_SOLVED}}", str(total_solved))
    .replace("{{IKOTE_COUNT}}", str(ikote_count))
    .replace("{{PROGRAMMERS_COUNT}}", str(programmers_count))
    .replace("{{BOJ_COUNT}}", str(boj_count))
    .replace("{{RECENT_ACTIVITY_TABLE}}", recent_rows)
    .replace("{{LAST_UPDATE}}", now)
)

with open("README.md", "w", encoding="utf-8") as f:
    f.write(new_readme)

print("README updated successfully!")
