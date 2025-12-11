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
TREND_IMG = f"{ASSETS}/trend.png"
os.makedirs(ASSETS, exist_ok=True)

# 한글 폰트 설정
font_manager.fontManager.addfont("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
plt.rc("font", family="DejaVu Sans")


# --------------------------------
# 유틸: 자바 파일 개수
# --------------------------------
def count_java_files(path):
    total = 0
    for root, _, files in os.walk(path):
        total += sum(1 for f in files if f.endswith(".java"))
    return total


ikote = count_java_files("src/이코테_자바")
programmers = count_java_files("src/programmers")
boj = count_java_files("src/BOJ") if os.path.exists("src/BOJ") else 0

total_solved = ikote + programmers + boj


# --------------------------------
# 문제명 파싱 (commit 메시지 기반)
# --------------------------------
def extract_problems(msg: str):
    results = []
    for line in msg.split("\n"):
        line = line.strip()
        # 문제명만 추출
        if line.startswith("- "):
            name = line[2:].strip()
            if 2 <= len(name) <= 60 and not re.search(r"[);}{=/]", name):
                results.append(name)
    return results


# --------------------------------
# 오늘 푼 문제
# --------------------------------
today = datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%Y-%m-%d")
today_solved = 0

raw = os.popen(f'git log --since="{today}" --pretty=format:"%B|||END"').read()
for block in raw.split("|||END"):
    problems = extract_problems(block)
    today_solved += len(problems)


# --------------------------------
# 최근 7일 문제
# --------------------------------
recent_rows = ""
weekly_solved = 0

week_raw = os.popen(
    'git log --since="7 days ago" --pretty=format:"%ad|||%B|||END" --date=short'
).read()

for block in week_raw.split("|||END"):
    if "|||" not in block:
        continue

    date, msg = block.split("|||", 1)
    problems = extract_problems(msg)

    if not problems:
        continue

    # 카테고리 구분
    if "프로그래머스" in msg:
        category = "프로그래머스"
    elif "이코테" in msg:
        category = "이코테"
    else:
        category = "BOJ"

    for p in problems:
        recent_rows += f"| {date} | {category} | {p} |\n"

    weekly_solved += len(problems)


# --------------------------------
# history.json 업데이트
# --------------------------------
history = {}
if os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, encoding="utf-8") as f:
        history = json.load(f)

history[today] = total_solved

with open(HISTORY_FILE, "w", encoding="utf-8") as f:
    json.dump(history, f, indent=2, ensure_ascii=False)


# --------------------------------
# 그래프 생성
# --------------------------------
dates = sorted(history.keys())
values = [history[d] for d in dates]

plt.figure(figsize=(8, 4))
plt.plot(dates, values, marker="o", linewidth=2, color="#40c463")
plt.grid(alpha=0.3)
plt.title("문제 풀이 누적 추세")
plt.xlabel("날짜")
plt.ylabel("누적 문제 수")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(TREND_IMG, dpi=200)
plt.close()


# --------------------------------
# SVG Progress Bar 생성
# --------------------------------
def make_svg(value, total, color, filename):
    pct = int((value / total) * 100) if total else 0
    fill_width = pct * 3  # 100% = 300px

    svg = f"""
<svg width="300" height="26">
  <rect x="0" y="10" width="300" height="10" fill="#e0e0e0" rx="5"/>
  <rect x="0" y="10" width="{fill_width}" height="10" fill="{color}" rx="5"/>
  <text x="150" y="9" font-size="12" text-anchor="middle" fill="#555">
    {value} / {total} ({pct}%)
  </text>
</svg>
"""
    with open(f"{ASSETS}/{filename}", "w", encoding="utf-8") as f:
        f.write(svg)


make_svg(today_solved, 10, "#ff6b6b", "today.svg")
make_svg(weekly_solved, 10, "#4c6ef5", "weekly.svg")
make_svg(total_solved, 500, "#40c463", "total.svg")


# --------------------------------
# README 업데이트
# --------------------------------
with open(README_TEMPLATE, encoding="utf-8") as f:
    readme = f.read()

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

with open("README.md", "w", encoding="utf-8") as f:
    f.write(new_readme)

print("Dashboard README updated successfully!")
