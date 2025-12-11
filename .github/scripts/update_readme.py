import os
import re
import json
import datetime
import pytz
import matplotlib.pyplot as plt
from matplotlib import font_manager


# ==============================
# 기본 설정
# ==============================
README_TEMPLATE = "README.md"
HISTORY_FILE = "solve_history.json"
ASSETS_DIR = "assets"
TREND_IMAGE_PATH = f"{ASSETS_DIR}/trend.png"

os.makedirs(ASSETS_DIR, exist_ok=True)

# 한글 폰트 설정 (GitHub Actions에서도 깨지지 않도록)
font_manager.fontManager.addfont("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
plt.rc("font", family="DejaVu Sans")


# ==============================
# 유틸 함수
# ==============================
def count_java_files(path):
    if not os.path.exists(path):
        return 0
    return sum(
        1 for _, _, files in os.walk(path) for f in files if f.endswith(".java")
    )


def generate_svg_progress(value, total, color, filename):
    percent = int((value / total) * 100) if total else 0

    svg = f"""
<svg width="300" height="28" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="12" width="300" height="10" fill="#e0e0e0" rx="5"/>
  <rect x="0" y="12" width="{3*percent}" height="10" fill="{color}" rx="5"/>
  <text x="150" y="10" font-size="12" text-anchor="middle" fill="#555">
    {value} / {total} ({percent}%)
  </text>
</svg>
"""
    with open(f"{ASSETS_DIR}/{filename}", "w", encoding="utf-8") as f:
        f.write(svg)


# ==============================
# 카테고리 파일 수 계산
# ==============================
ikote_count = count_java_files("src/이코테_자바")
programmers_count = count_java_files("src/programmers")
boj_count = count_java_files("src/BOJ")

total_solved = ikote_count + programmers_count + boj_count


# ==============================
# 오늘 푼 문제 수
# ==============================
today = datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%Y-%m-%d")
today_solved = 0

today_logs = os.popen(
    f'git log --since="{today}" --pretty=format:"%H|||%s"'
).read()

for row in today_logs.split("\n"):
    if not row.strip():
        continue

    commit_hash, msg = row.split("|||")

    if not any(k in msg for k in ["프로그래머스", "이코테", "BOJ"]):
        continue

    full_commit = os.popen(f"git show {commit_hash}").read()
    problems = re.findall(r"- (.+)", full_commit)
    today_solved += len(problems)


# ==============================
# 주간 푼 문제 수
# ==============================
weekly_logs = os.popen(
    'git log --since="7 days ago" --pretty=format:"%H|||%s"'
).read()

weekly_solved = 0

for row in weekly_logs.split("\n"):
    if not row.strip():
        continue

    commit_hash, msg = row.split("|||")

    if not any(k in msg for k in ["프로그래머스", "BOJ"]):
        continue

    full_commit = os.popen(f"git show {commit_hash}").read()
    weekly_solved += len(re.findall(r"- (.+)", full_commit))

weekly_progress = min(weekly_solved, 10)


# ==============================
# 기록 파일(history)
# ==============================
if os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        history = json.load(f)
else:
    history = {}

history[today] = total_solved

with open(HISTORY_FILE, "w", encoding="utf-8") as f:
    json.dump(history, f, ensure_ascii=False, indent=2)


# ==============================
# 누적 그래프 생성
# ==============================
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
plt.savefig(TREND_IMAGE_PATH, dpi=200)
plt.close()


# ==============================
# 최근 7일 Activity 추출
# ==============================
recent_activity = ""

logs = os.popen(
    'git log --since="7 days ago" --pretty=format:"%H|||%ad|||%s" --date=short'
).read()

for row in logs.split("\n"):
    if not row.strip():
        continue

    commit_hash, date, msg = row.split("|||")

    if not any(k in msg for k in ["프로그래머스", "이코테", "BOJ"]):
        continue

    full = os.popen(f"git show {commit_hash}").read()
    problems = re.findall(r"- (.+)", full)

    for p in problems:
        recent_activity += f"| {date} | {msg.split()[1]} | {p} |\n"


# ==============================
# SVG Progress Bar 생성
# ==============================
generate_svg_progress(today_solved, 10, "#ff6b6b", "today.svg")
generate_svg_progress(weekly_progress, 10, "#4c6ef5", "weekly.svg")
generate_svg_progress(total_solved, 500, "#40c463", "total.svg")


# ==============================
# README 갱신
# ==============================
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
    .replace("{{RECENT_ACTIVITY_TABLE}}", recent_activity)
    .replace("{{LAST_UPDATE}}", now)
)

with open("README.md", "w", encoding="utf-8") as f:
    f.write(new_readme)

print("README updated successfully!")
