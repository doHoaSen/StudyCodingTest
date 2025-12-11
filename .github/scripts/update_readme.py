import os
import re
import json
import datetime
import pytz
import matplotlib.pyplot as plt
from matplotlib import font_manager

README_TEMPLATE = "README.md"
HISTORY_FILE = "solve_history.json"
ASSETS = "assets"

os.makedirs(ASSETS, exist_ok=True)

# ------------------- FONT FIX -------------------
font_paths = [
    "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
    "/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf",
]

for fp in font_paths:
    if os.path.exists(fp):
        font_manager.fontManager.addfont(fp)

plt.rc("font", family="NanumGothic")

# ----------------- FILE COUNT -----------------
def count_java_files(path):
    return sum(
        1 for _, _, files in os.walk(path)
        for f in files if f.endswith(".java")
    ) if os.path.exists(path) else 0

ikote = count_java_files("src/이코테_자바")
programmers = count_java_files("src/programmers")
boj = count_java_files("src/BOJ")

total_solved = ikote + programmers + boj

# ----------------- PROGRESS CALC -----------------
today = datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%Y-%m-%d")

today_solved = 0
weekly_solved = 0

git_today = os.popen(f'git log --since="{today}" --pretty=format:"%H|||%s"').read()
git_week = os.popen('git log --since="7 days ago" --pretty=format:"%H|||%s"').read()

def extract_problems(commit_hash):
    """Commit 안의 문제 리스트 추출 ('- 문제명' 패턴)"""
    full = os.popen(f"git show {commit_hash}").read()
    return re.findall(r"- (.+)", full)

for entry in git_today.split("\n"):
    if not entry.strip():
        continue
    commit_hash, _ = entry.split("|||")
    today_solved += len(extract_problems(commit_hash))

for entry in git_week.split("\n"):
    if not entry.strip():
        continue
    commit_hash, _ = entry.split("|||")
    weekly_solved += len(extract_problems(commit_hash))

weekly_progress = min(weekly_solved, 10)

# ----------------- HISTORY GRAPH -----------------
history = {}
if os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        history = json.load(f)

history[today] = total_solved

with open(HISTORY_FILE, "w", encoding="utf-8") as f:
    json.dump(history, f, indent=2, ensure_ascii=False)

# ----------------- TREND GRAPH -----------------
dates = sorted(history.keys())
values = [history[d] for d in dates]

plt.figure(figsize=(8, 4))
plt.plot(dates, values, marker="o", color="#4da3ff", linewidth=2)
plt.title("최근 7일 문제 풀이 추세")
plt.xlabel("날짜")
plt.ylabel("누적 문제 수")
plt.grid(alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f"{ASSETS}/trend.png", dpi=200)
plt.close()

# ----------------- DONUT CHART -----------------
def generate_donut(name, value, total):
    percent = (value / total * 100) if total > 0 else 0
    remain = 100 - percent

    fig, ax = plt.subplots(figsize=(2.6, 2.6))
    ax.pie(
        [percent, remain],
        colors=["#4da3ff", "#d9eaff"],
        startangle=90,
        wedgeprops={"width": 0.3},
    )
    ax.text(0, 0, f"{int(percent)}%", ha="center", va="center", fontsize=16)
    plt.tight_layout()
    plt.savefig(f"{ASSETS}/{name}_donut.svg", format="svg")
    plt.close()

generate_donut("ikote", ikote, total_solved)
generate_donut("programmers", programmers, total_solved)
generate_donut("boj", boj, total_solved)

# ----------------- RECENT ACTIVITY -----------------
recent_rows = ""
git_log = os.popen(
    'git log --since="7 days ago" --pretty=format:"%H|||%ad|||%s" --date=short'
).read()

for entry in git_log.split("\n"):
    if not entry.strip():
        continue

    commit_hash, commit_date, msg = entry.split("|||")
    problems = extract_problems(commit_hash)

    # commit 메시지 기준 카테고리 추출
    if "프로그래머스" in msg:
        category = "프로그래머스"
    elif "이코테" in msg:
        category = "이코테"
    elif "BOJ" in msg:
        category = "BOJ"
    else:
        continue

    for p in problems:
        recent_rows += f"| {commit_date} | {category} | {p.strip()} |\n"

# ----------------- UPDATE README -----------------
with open(README_TEMPLATE, "r", encoding="utf-8") as f:
    readme = f.read()

now = datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%Y-%m-%d %H:%M")

processed = (
    readme.replace("{{TODAY_SOLVED}}", str(today_solved))
    .replace("{{WEEKLY_PROGRESS}}", str(weekly_progress))
    .replace("{{TOTAL_SOLVED}}", str(total_solved))
    .replace("{{IKOTE_COUNT}}", str(ikote))
    .replace("{{PROGRAMMERS_COUNT}}", str(programmers))
    .replace("{{BOJ_COUNT}}", str(boj))
    .replace("{{RECENT_ACTIVITY_TABLE}}", recent_rows)
    .replace("{{LAST_UPDATE}}", now)
)

with open("README.md", "w", encoding="utf-8") as f:
    f.write(processed)

print("README updated.")
