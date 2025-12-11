import os
import re
import json
import datetime
import pytz
import matplotlib.pyplot as plt
from matplotlib import rcParams

# 폰트 설정 (GitHub Actions용)
rcParams["font.family"] = "DejaVu Sans"

README_TEMPLATE = "README.md"
HISTORY_FILE = "solve_history.json"
ASSETS_DIR = "assets"

os.makedirs(ASSETS_DIR, exist_ok=True)

# ---------------- 파일 카운트 ----------------
def count_java(path):
    return sum(
        1 for _, _, files in os.walk(path)
        for f in files if f.endswith(".java")
    ) if os.path.exists(path) else 0


ikote = count_java("src/이코테_자바")
programmers = count_java("src/programmers")
boj = count_java("src/BOJ")

total = ikote + programmers + boj

# ---------------- 날짜 ----------------
today = datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%Y-%m-%d")

# ---------------- Commit 분석 ----------------
def get_recent_activity(days=7):
    cmd = f'git log --since="{days} days ago" --pretty=format:"%H|||%ad|||%s" --date=short'
    logs = os.popen(cmd).read().strip().split("\n")

    rows = ""

    for entry in logs:
        if not entry.strip():
            continue

        commit, date, msg = entry.split("|||")

        # commit message 예시:
        # 251210 프로그래머스: lv.1 3문제
        # - 크레인 인형뽑기 게임
        category = ""
        if "프로그래머스" in msg:
            category = "프로그래머스"
        elif "이코테" in msg:
            category = "이코테"
        elif "BOJ" in msg:
            category = "BOJ"
        else:
            continue

        detail = os.popen(f"git show {commit}").read()
        problems = re.findall(r"- (.+)", detail)

        for p in problems:
            rows += f"| {date} | {category} | {p.strip()} |\n"

    return rows


recent_table = get_recent_activity(7)

# ---------------- 누적 기록 JSON ----------------
if os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        history = json.load(f)
else:
    history = {}

history[today] = total
with open(HISTORY_FILE, "w", encoding="utf-8") as f:
    json.dump(history, f, ensure_ascii=False, indent=2)

# ---------------- 추세 그래프 ----------------
dates = sorted(history.keys())
values = [history[d] for d in dates]

plt.figure(figsize=(7,4))
plt.plot(dates, values, marker="o", color="#4ea5ff")
plt.title("최근 7일 누적 문제 그래프")
plt.xlabel("날짜")
plt.ylabel("누적 문제 수")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f"{ASSETS_DIR}/trend.png", dpi=200)
plt.close()

# ---------------- Donut Chart 생성 ----------------
def donut_svg(filename, percent):
    svg = f"""
<svg width="140" height="140" viewBox="0 0 36 36">
  <path d="M18 2
           a 16 16 0 1 1 0 32
           a 16 16 0 1 1 0 -32"
        fill="none"
        stroke="#eee"
        stroke-width="4"/>
  <path d="M18 2
           a 16 16 0 1 1 0 32"
        fill="none"
        stroke="#4ea5ff"
        stroke-width="4"
        stroke-dasharray="{percent}, 100"/>
  <text x="18" y="20" font-size="8" text-anchor="middle" fill="#4ea5ff">{percent}%</text>
</svg>
"""
    with open(f"{ASSETS_DIR}/{filename}", "w", encoding="utf-8") as f:
        f.write(svg)


# 비율 계산
ikote_rate = round((ikote / total) * 100) if total else 0
programmers_rate = round((programmers / total) * 100) if total else 0
boj_rate = round((boj / total) * 100) if total else 0

donut_svg("category_ikote.svg", ikote_rate)
donut_svg("category_programmers.svg", programmers_rate)
donut_svg("category_boj.svg", boj_rate)

# 기본 통계 SVG (오늘/주간/누적)
donut_svg("today.svg", 0)
donut_svg("weekly.svg", 0)
donut_svg("total.svg", round((total / 500) * 100))

# ---------------- README 업데이트 ----------------
with open(README_TEMPLATE, "r", encoding="utf-8") as f:
    readme = f.read()

updated = readme.replace("{{RECENT_ACTIVITY_TABLE}}", recent_table)\
                .replace("{{LAST_UPDATE}}", datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))

with open("README.md", "w", encoding="utf-8") as f:
    f.write(updated)

print("README updated!")
