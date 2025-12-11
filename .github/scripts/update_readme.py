import os
import re
import json
import datetime
import pytz
import matplotlib.pyplot as plt
from matplotlib import font_manager

# -------------------------
# 기본 경로 설정
# -------------------------
README_TEMPLATE = "README.md"
HISTORY_FILE = "solve_history.json"
ASSETS = "assets"
TREND_IMG = f"{ASSETS}/trend.png"

os.makedirs(ASSETS, exist_ok=True)

# 한글 폰트 설정
font_manager.fontManager.addfont("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
plt.rc("font", family="DejaVu Sans")


# -------------------------
# 유틸: 자바 파일 카운트
# -------------------------
def count_java_files(path):
    if not os.path.exists(path):
        return 0
    total = 0
    for root, _, files in os.walk(path):
        total += sum(1 for f in files if f.endswith(".java"))
    return total


# -------------------------
# 유틸: SVG Progress Bar 생성
# -------------------------
def generate_svg(value, total, color, filename):
    percent = int((value / total) * 100) if total else 0
    bar_width = int(3 * percent)

    svg = f"""
<svg width="300" height="28" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="12" width="300" height="10" fill="#e0e0e0" rx="5"/>
  <rect x="0" y="12" width="{bar_width}" height="10" fill="{color}" rx="5"/>
  <text x="150" y="10" font-size="12" text-anchor="middle" fill="#555">
    {value} / {total} ({percent}%)
  </text>
</svg>
"""
    with open(f"{ASSETS}/{filename}", "w", encoding="utf-8") as f:
        f.write(svg)


# -------------------------
# 카테고리별 파일 수
# -------------------------
ikote = count_java_files("src/이코테_자바")
programmers = count_java_files("src/programmers")
boj = count_java_files("src/BOJ")

total_solved = ikote + programmers + boj


# -------------------------
# 오늘 푼 문제 수
# -------------------------
today = datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%Y-%m-%d")
today_solved = 0

today_log = os.popen(f'git log --since="{today}" --pretty=format:"%H|||%s"').read()

for row in today_log.split("\n"):
    if not row.strip():
        continue
    commit_hash, msg = row.split("|||")

    # 문제 풀이 commit만 처리
    if not any(k in msg for k in ["프로그래머스", "이코테", "BOJ"]):
        continue

    diff = os.popen(f"git show {commit_hash}").read()

    # 문제 제목만 추출하는 패턴
    problems = re.findall(r"- ([가-힣A-Za-z0-9\[\]\(\) ]{2,50})", diff)
    today_solved += len(problems)


# -------------------------
# 최근 7일 문제 풀이
# -------------------------
recent_rows = ""
week_log = os.popen(
    'git log --since="7 days ago" --pretty=format:"%H|||%ad|||%s" --date=short'
).read()

for row in week_log.split("\n"):
    if not row.strip():
        continue

    commit_hash, date, msg = row.split("|||")

    if not any(k in msg for k in ["프로그래머스", "이코테", "BOJ"]):
        continue

    diff = os.popen(f"git show {commit_hash}").read()
    titles = re.findall(r"- ([가-힣A-Za-z0-9\[\]\(\) ]{2,50})", diff)

    if "프로그래머스" in msg:
        category = "프로그래머스"
    elif "이코테" in msg:
        category = "이코테"
    else:
        category = "BOJ"

    for t in titles:
        recent_rows += f"| {date} | {category} | {t} |\n"


# -------------------------
# history.json 업데이트
# -------------------------
if os.path.exists(HISTORY_FILE):
    history = json.load(open(HISTORY_FILE, encoding="utf-8"))
else:
    history = {}

history[today] = total_solved
json.dump(history, open(HISTORY_FILE, "w", encoding="utf-8"), ensure_ascii=False, indent=2)


# -------------------------
# 누적 그래프 생성
# -------------------------
dates = sorted(history.keys())
values = [history[d] for d in dates]

plt.figure(figsize=(8, 4))
plt.plot(dates, values, marker="o", color="#40c463")
plt.grid(alpha=0.3)
plt.title("문제 풀이 누적 변화")
plt.xlabel("날짜")
plt.ylabel("누적 문제 수")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(TREND_IMG, dpi=200)
plt.close()


# -------------------------
# SVG 생성
# -------------------------
generate_svg(today_solved, 10, "#ff6b6b", "today.svg")
generate_svg(min(len(values), 10), 10, "#4c6ef5", "weekly.svg")
generate_svg(total_solved, 500, "#40c463", "total.svg")


# -------------------------
# README 업데이트
# -------------------------
readme = open(README_TEMPLATE, encoding="utf-8").read()

now = datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%Y-%m-%d %H:%M")

new_readme = (
    readme.replace("{{TODAY_SOLVED}}", str(today_solved))
    .replace("{{WEEKLY_PROGRESS}}", str(len(values)))
    .replace("{{TOTAL_SOLVED}}", str(total_solved))
    .replace("{{IKOTE_COUNT}}", str(ikote))
    .replace("{{PROGRAMMERS_COUNT}}", str(programmers))
    .replace("{{BOJ_COUNT}}", str(boj))
    .replace("{{RECENT_ACTIVITY_TABLE}}", recent_rows)
    .replace("{{LAST_UPDATE}}", now)
)

open("README.md", "w", encoding="utf-8").write(new_readme)

print("README updated successfully!")
