import os
import re
import json
import datetime
import pytz
import matplotlib.pyplot as plt

README_TEMPLATE = "README.md"
HISTORY_FILE = "solve_history.json"
TREND_IMAGE_PATH = "assets/trend.png"

# Make sure assets folder exists
os.makedirs("assets", exist_ok=True)

def count_files(path):
    if not os.path.exists(path):
        return 0
    return sum(
        1 for root, dirs, files in os.walk(path)
        for f in files if f.endswith(".java")
    )

# ---- Problem Counts ----
ikote_count = count_files("src/이코테_자바")
programmers_lv1_count = count_files("src/프로그래머스_lv1")
boj_count = count_files("src/BOJ") if os.path.exists("src/BOJ") else 0

total_solved = ikote_count + programmers_lv1_count + boj_count

# ---- Today’s Solve Count ----
today = datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%Y-%m-%d")
today_solved = 0

today_log = os.popen(f'git log --since="{today}" --pretty=format:"%H|||%s"').read()

for entry in today_log.split("\n"):
    if not entry.strip():
        continue

    commit_hash, msg = entry.split("|||")

    if "프로그래머스" in msg or "BOJ" in msg:
        full_commit = os.popen(f'git show {commit_hash}').read()
        today_solved += len(re.findall(r"- (.+)", full_commit))

# ---- Weekly Progress ----
weekly_log = os.popen(
    'git log --since="7 days ago" --pretty=format:"%H|||%s"'
).read()

weekly_solved = 0

for entry in weekly_log.split("\n"):
    if not entry.strip():
        continue

    commit_hash, msg = entry.split("|||")

    if "프로그래머스" in msg or "BOJ" in msg:
        full_commit = os.popen(f'git show {commit_hash}').read()
        weekly_solved += len(re.findall(r"- (.+)", full_commit))

weekly_progress = min(weekly_solved, 10)

# ---- Load or Init History ----
if os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        history = json.load(f)
else:
    history = {}

# ---- Append Today's Data ----
history[today] = total_solved

with open(HISTORY_FILE, "w", encoding="utf-8") as f:
    json.dump(history, f, indent=2, ensure_ascii=False)

# ---- Trend Chart (line plot) ----
dates = sorted(history.keys())
values = [history[d] for d in dates]

plt.figure(figsize=(8, 4))
plt.plot(dates, values, marker="o", color="#40c463")
plt.title("Solved Trend", fontsize=16)
plt.xlabel("Date")
plt.ylabel("Total Solved")
plt.grid(True, alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(TREND_IMAGE_PATH, dpi=200)
plt.close()

# ---- Recent Activity Table ----
recent_rows = ""

git_log = os.popen(
    'git log --since="7 days ago" --pretty=format:"%H|||%ad|||%s" --date=short'
).read()

for entry in git_log.split("\n"):
    if not entry.strip():
        continue

    commit_hash, commit_date, message = entry.split("|||")

    token = message.split()[0]
    if re.match(r"\d{6}", token):
        yy, mm, dd = token[:2], token[2:4], token[4:6]
        formatted_date = f"20{yy}-{mm}-{dd}"
    else:
        formatted_date = commit_date

    if "프로그래머스" in message:
        category = "프로그래머스"
    elif "이코테" in message:
        category = "이코테"
    elif "BOJ" in message:
        category = "BOJ"
    else:
        category = "Unknown"

    full_commit = os.popen(f'git show {commit_hash}').read()
    problems = re.findall(r"- (.+)", full_commit)

    for p in problems:
        recent_rows += f"| {formatted_date} | {category} | {p.strip()} |\n"

# ---- Update README ----
with open(README_TEMPLATE, "r", encoding="utf-8") as f:
    readme = f.read()

now = datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%Y-%m-%d %H:%M")

new_readme = (
    readme.replace("14", str(total_solved))
    .replace("14", str(ikote_count))
    .replace("0", str(programmers_lv1_count))
    .replace("0", str(boj_count))
    .replace("0", str(today_solved))
    .replace("0", str(weekly_progress))
    .replace("| 2025-12-11 | Unknown | /dev/null |
| 2025-12-11 | Unknown | Problem Counts ---- |
| 2025-12-11 | Unknown | Today’s Solve Count ---- |
| 2025-12-11 | Unknown | (.+)", full_commit)) |
| 2025-12-11 | Unknown | Weekly Progress ---- |
| 2025-12-11 | Unknown | (.+)", full_commit)) |
| 2025-12-11 | Unknown | Load or Init History ---- |
| 2025-12-11 | Unknown | Append Today's Data ---- |
| 2025-12-11 | Unknown | Trend Chart (line plot) ---- |
| 2025-12-11 | Unknown | Recent Activity Table ---- |
| 2025-12-11 | Unknown | (.+)", full_commit) |
| 2025-12-11 | Unknown | Update README ---- |
| 2025-12-11 | Unknown | /dev/null |
| 2025-12-11 | Unknown | cron: "0 0 * * *" |
| 2025-12-11 | Unknown | uses: actions/checkout@v3 |
| 2025-12-11 | Unknown | uses: actions/setup-python@v4 |
| 2025-12-11 | Unknown | run: pip install pytz matplotlib |
| 2025-12-11 | Unknown | run: python .github/scripts/update_readme.py |
| 2025-12-11 | Unknown | run: | |
| 2025-12-11 | Unknown | /dev/null |
| 2025-12-11 | Unknown | /dev/null |
| 2025-12-11 | Unknown | /dev/null |
| 2025-12-11 | Unknown | /dev/null |
| 2025-12-11 | Unknown | /dev/null |
| 2025-12-11 | Unknown | /dev/null |
| 2025-12-11 | Unknown | Problem Counts ---- |
| 2025-12-11 | Unknown | Today’s Solve Count ---- |
| 2025-12-11 | Unknown | (.+)", full_commit)) |
| 2025-12-11 | Unknown | Weekly Progress ---- |
| 2025-12-11 | Unknown | (.+)", full_commit)) |
| 2025-12-11 | Unknown | Load or Init History ---- |
| 2025-12-11 | Unknown | Append Today's Data ---- |
| 2025-12-11 | Unknown | Trend Chart (line plot) ---- |
| 2025-12-11 | Unknown | Recent Activity Table ---- |
| 2025-12-11 | Unknown | (.+)", full_commit) |
| 2025-12-11 | Unknown | Update README ---- |
| 2025-12-11 | Unknown | /dev/null |
| 2025-12-11 | Unknown | /dev/null |
| 2025-12-11 | Unknown | /dev/null |
| 2025-12-11 | Unknown | /dev/null |
| 2025-12-11 | Unknown | /dev/null |
| 2025-12-11 | Unknown | /dev/null |
| 2025-12-11 | Unknown | /dev/null |
| 2025-12-11 | Unknown | /dev/null |
| 2025-12-11 | Unknown | '0'; |
| 2025-12-11 | Unknown | /dev/null |
| 2025-12-11 | Unknown | '0'; |
| 2025-12-11 | Unknown | /dev/null |
| 2025-12-11 | Unknown | 데이터 개수 N, 데이터 중 최대값의 크기 K |
| 2025-12-11 | Unknown | /dev/null |
| 2025-12-11 | Unknown | /dev/null |
| 2025-12-11 | Unknown | /dev/null |
| 2025-12-11 | Unknown | /dev/null |
| 2025-12-11 | Unknown | 1); |
| 2025-12-11 | Unknown | /dev/null |
| 2025-12-11 | Unknown | b[extIdx]); |
| 2025-12-11 | Unknown | b[sortIdx]); |
| 2025-12-11 | Unknown | /dev/null |
| 2025-12-11 | Unknown | idx; |
| 2025-12-11 | Unknown | map.getOrDefault(c, i+1); |
| 2025-12-11 | Unknown | /dev/null |
| 2025-12-11 | Unknown | /dev/null |
| 2025-12-11 | Unknown | /dev/null |
| 2025-12-11 | Unknown | '0'; |
| 2025-12-11 | Unknown | 1; |
| 2025-12-11 | Unknown | 1, scores.get(lastIndex-1) * 2); |
| 2025-12-11 | Unknown | 1; |
| 2025-12-11 | Unknown | /dev/null |
| 2025-12-11 | Unknown | /dev/null |
| 2025-12-11 | Unknown | 1 < section[i]){ |
| 2025-12-11 | Unknown | /dev/null |
| 2025-12-11 | Unknown | /dev/null |
| 2025-12-11 | Unknown | /dev/null |
| 2025-12-11 | Unknown | /dev/null |
| 2025-12-11 | Unknown | /dev/null |
| 2025-12-11 | Unknown | /dev/null |
| 2025-12-11 | Unknown | /dev/null |
| 2025-12-11 | Unknown | 1; j >= 0; j--) { |
| 2025-12-11 | Unknown | /dev/null |
| 2025-12-11 | Unknown | /dev/null |
| 2025-12-11 | Unknown | choice)); |
| 2025-12-11 | Unknown | 4)); |
| 2025-12-11 | Unknown | /dev/null |
| 2025-12-11 | Unknown | /dev/null |
| 2025-12-11 | Unknown | /dev/null |
| 2025-12-11 | Unknown | /dev/null |
| 2025-12-11 | Unknown | /dev/null |
| 2025-12-11 | Unknown | base + n) % 26 + base); |
| 2025-12-11 | Unknown | /dev/null |
| 2025-12-11 | Unknown | /dev/null |
| 2025-12-11 | Unknown | /dev/null |
| 2025-12-11 | Unknown | /dev/null |
| 2025-12-11 | Unknown | 1; i++){ |
| 2025-12-11 | Unknown | 1; |
| 2025-12-11 | Unknown | /dev/null |
| 2025-12-11 | Unknown | /dev/null |
| 2025-12-11 | Unknown | /dev/null |
| 2025-12-11 | Unknown | /dev/null |
| 2025-12-11 | Unknown | /dev/null |
| 2025-12-11 | Unknown | /dev/null |
| 2025-12-11 | Unknown | /dev/null |
| 2025-12-11 | Unknown | p.length() + 1; i++){ |
| 2025-12-11 | Unknown | /dev/null |
| 2025-12-11 | Unknown | /dev/null |
| 2025-12-11 | Unknown | 1) / 3; |
| 2025-12-11 | Unknown | 1) % 3; |
| 2025-12-11 | Unknown | 1) / 3; |
| 2025-12-11 | Unknown | 1) % 3; |
| 2025-12-11 | Unknown | tx) + Math.abs(fy - ty); |
| 2025-12-11 | Unknown | to); |
| 2025-12-11 | Unknown | /dev/null |
| 2025-12-11 | Unknown | /dev/null |
| 2025-12-11 | Unknown | 4) == 1 && |
| 2025-12-11 | Unknown | 3) == 2 && |
| 2025-12-11 | Unknown | 2) == 3 && |
| 2025-12-11 | Unknown | 1) == 1) { |
", recent_rows)
    .replace("2025-12-11 12:55", now)
)

with open("README.md", "w", encoding="utf-8") as f:
    f.write(new_readme)

print("README updated successfully!")
