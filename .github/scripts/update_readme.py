import os
import re
import json
import datetime
import pytz
import matplotlib.pyplot as plt
from matplotlib import font_manager

# 경로 설정
README_TEMPLATE = "README.md"
HISTORY_FILE = "solve_history.json"
ASSETS = "assets"
TREND_IMG = f"{ASSETS}/trend.png"
os.makedirs(ASSETS, exist_ok=True)

# 한글 폰트 설정
font_manager.fontManager.addfont("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
plt.rc("font", family="DejaVu Sans")


# -------------------------
# 자바 파일 개수 집계
# -------------------------
def count_java_files(path):
    total = 0
    for root, _, files in os.walk(path):
        total += sum(1 for f in files if f.endswith(".java"))
    return total


ikote = count_java_files("src/이코테_자바")
programmers = count_java_files("src/programmers")
boj = count_java_files("src/BOJ") if os.path.exists("src/BOJ") else 0
total_solved = ikote + programmers + boj


# -------------------------
# 문제명 파싱 (★ commit 메시지 기반 ★)
# -------------------------
def extract_problems_from_commit_msg(msg):
    problems = []
    for line in msg.split("\n"):
        line = line.strip()
        if line.startswith("- "):
            name = line[2:].strip()
            if 2 <= len(name) <= 50:  # 정상적인 문제명 길이
                problems.append(name)
    return problems


# -------------------------
# 오늘 푼 문제
# -------------------------
today = datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%Y-%m-%d")
today_solved = 0

today_log = os.popen(f'git log --since="{today}" --pretty=format:"%H|||%B"').read()

for entry in today_log.split("\n\n"):
    if "|||" not in entry:
        continue
    commit_hash, msg = entry.split("|||", 1)
    problems = extract_problems_from_commit_msg(msg)
    today_solved += len(problems)


# -------------------------
# 최근 7일 활동
# -------------------------
recent_rows = ""
week_log = os.popen(
    'git log --since="7 days ago" --pretty=format:"%ad|||%B" --date=short'
).read()

weekly_solved = 0

for block in week_log.split("\n\n"):
    if "|||" not in block:
        continue

    date, msg = block.split("|||", 1)
    problems = extract_problems_from_commit_msg(msg)

    if problems:
        category = "프로그래머스" if "프로그래머스" in msg else "이코테" if "이코테" in msg else "BOJ"

        for p in problems:
            recent_rows += f"| {date} | {category} | {p} |\n"

        weekly_solved += len(problems)


# -------------------------
# 기록 파일(history.json)
# -------------------------
if os.path.exists(HISTORY_FILE):
    history = json.load(open(HISTORY_FILE, encoding="utf-8"))
else:
    history = {}

history[today] = total_solved
json.dump(history, open(HISTORY_FILE, "w", encoding="utf-8"), ensure_ascii=False, indent=2)


# -------------------------
# 그래프 생성
# -------------------------
dates = sorted(history.keys())
values = [history[d] for d in dates]

plt.figure(figsize=(8, 4))
plt.plot(dates, values, marker="o", color="#40c463")
plt.title("문제 풀이 누적 변화")
plt.xlabel("날짜")
plt.ylabel("누적 문제 수")
plt.grid(alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(TREND_IMG, dpi=200)
plt.close()


# -------------------------
# SVG progress bar 생성
# -------------------------
def svg_bar(value, total, color, filename):
    pct = min(100, int((value / total) * 100)) if total else 0
    w = int(3 * pct)
    svg = f"""
<svg width="300" height="26">
  <rect x="0" y="10" width="300" height="10" fill="#ddd" rx="5"/>
  <rect x="0" y="10" width="{w}" height="10" fill="{color}" rx="5"/>
  <text x="150" y="9" text-anchor="middle" font-size="12" fill="#555">
    {value}/{total} ({pct}%)
  </text>
</svg>
"""
    with open(f"{ASSETS}/{filename}", "w", encoding="utf-8") as f:
        f.write(svg)


svg_bar(today_solved, 10, "#ff6b6b", "today.svg")
svg_bar(weekly_solved, 10, "#4c6ef5", "weekly.svg")
svg_bar(total_solved, 300, "#40c463", "total.svg")


# -------------------------
# README 업데이트
# -------------------------
readme = open(README_TEMPLATE, encoding="utf-8").read()

now = datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%Y-%m-%d %H:%M")

new_readme = (
    readme.replace("{{TODAY_SOLVED}}", str(today_solved))
    .replace("{{WEEKLY_PROGRESS}}", str(weekly_solved))
    .replace("{{TOTAL_SOLVED}}", str(total_solved))
    .replace("{{IKOTE_COUNT}}", str(ikote))
    .replace("{{PROGRAMMERS_COUNT}}", str(programmers))
    .replace("{{BOJ_COUNT}}", str(boj))
    .replace("{{RECENT_ACTIVITY_TABLE}}", recent_rows)
    .replace("{{LAST_UPDATE}}", now)
)

open("README.md", "w", encoding="utf-8").write(new_readme)

print("README updated successfully!")

