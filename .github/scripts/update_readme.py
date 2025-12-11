import os
import re
import json
import datetime
import pytz
import matplotlib.pyplot as plt

README_TEMPLATE = "README.md"
HISTORY_FILE = "solve_history.json"
TREND_IMAGE_PATH = "assets/trend.png"

# Ensure assets folder exists
os.makedirs("assets", exist_ok=True)


# ---------------- Java 파일 자동 카운트 함수 ----------------
def count_java_files(path):
    if not os.path.exists(path):
        return 0
    return sum(
        1
        for _, _, files in os.walk(path)
        for f in files
        if f.endswith(".java")
    )


# 카테고리별 집계
ikote_count = count_java_files("src/이코테_자바")
programmers_count = count_java_files("src/programmers")
boj_count = count_java_files("src/BOJ")

total_solved = ikote_count + programmers_count + boj_count


# ---------------- Today Solve Count ----------------
today = datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%Y-%m-%d")
today_solved = 0

today_log = os.popen(f'git log --since="{today}" --pretty=format:"%H|||%s"').read()

for entry in today_log.split("\n"):
    if not entry.strip():
        continue

    commit_hash, msg = entry.split("|||")

    if not any(k in msg for k in ["프로그래머스", "BOJ", "이코테"]):
        continue

    full_commit = os.popen(f'git show {commit_hash}').read()
    problems = re.findall(r"- (.+)", full_commit)
    today_solved += len(problems)


# ---------------- Weekly Progress ----------------
weekly_log = os.popen('git log --since="7 days ago" --pretty=format:"%H|||%s"').read()
weekly_solved = 0

for entry in weekly_log.split("\n"):
    if not entry.strip():
        continue

    commit_hash, msg = entry.split("|||")

    if not any(k in msg for k in ["프로그래머스", "BOJ", "이코테"]):
        continue

    full_commit = os.popen(f'git show {commit_hash}').read()
    weekly_solved += len(re.findall(r"- (.+)", full_commit))

weekly_progress = min(weekly_solved, 10)


# ---------------- Load / Init history ----------------
if os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        history = json.load(f)
else:
    history = {}

history[today] = total_solved
with open(HISTORY_FILE, "w", encoding="utf-8") as f:
    json.dump(history, f, indent=2, ensure_ascii=False)


# ---------------- Trend Chart ----------------
dates = sorted(history.keys())
values = [history[d] for d in dates]

plt.figure(figsize=(8, 4))
plt.plot(dates, values, marker="o", color="#40c463")
plt.title("문제 풀이 추세 그래프", fontsize=16)
plt.xlabel("날짜")
plt.ylabel("총 누적 해결 문제 수")
plt.grid(True, alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(TREND_IMAGE_PATH, dpi=200)
plt.close()


# ---------------- Recent Activity ----------------
recent_rows = ""

git_log = os.popen(
    'git log --since="7 days ago" --pretty=format:"%H|||%ad|||%s" --date=short'
).read()

for entry in git_log.split("\n"):
    if not entry.strip():
        continue

    commit_hash, commit_date, msg = entry.split("|||")

    if not any(k in msg for k in ["프로그래머스", "이코테", "BOJ"]):
        continue

    if "프로그래머스" in msg:
        category = "프로그래머스"
    elif "이코테" in msg:
        category = "이코테"
    elif "BOJ" in msg:
        category = "BOJ"
    else:
        continue

    full_commit = os.popen(f'git show {commit_hash}').read()
    problems = re.findall(r"- (.+)", full_commit)

    for p in problems:
        recent_rows += f"| {commit_date} | {category} | {p.strip()} |\n"


# ---------------- Replace README Template ----------------
with open(README_TEMPLATE, "r", encoding="utf-8") as f:
    readme = f.read()

now = datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%Y-%m-%d %H:%M")

new_readme = (
    readme.replace("{{TOTAL_SOLVED}}", str(total_solved))
    .replace("{{IKOTE_COUNT}}", str(ikote_count))
    .replace("{{PROGRAMMERS_COUNT}}", str(programmers_count))
    .replace("{{BOJ_COUNT}}", str(boj_count))
    .replace("{{TODAY_SOLVED}}", str(today_solved))
    .replace("{{WEEKLY_PROGRESS}}", str(weekly_progress))
    .replace("{{RECENT_ACTIVITY_TABLE}}", recent_rows)
    .replace("{{LAST_UPDATE}}", now)
)

with open("README.md", "w", encoding="utf-8") as f:
    f.write(new_readme)

print("README updated successfully!")
