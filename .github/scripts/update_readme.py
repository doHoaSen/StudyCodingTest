import json
import os
import datetime
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from pytz import timezone
import math

# ---------------------------
# PATH SETTINGS
# ---------------------------

ROOT = os.getcwd()
TEMPLATE_PATH = ".github/scripts/template_readme.md"
OUTPUT_README = "README.md"

ASSETS = "./assets"
TREND_IMAGE_PATH = f"{ASSETS}/trend.png"

DONUT_FILES = {
    "ikote": f"{ASSETS}/ikote.svg",
    "programmers": f"{ASSETS}/programmers.svg",
    "boj": f"{ASSETS}/boj.svg",
    "today": f"{ASSETS}/today.svg",
    "weekly": f"{ASSETS}/weekly.svg",
    "total": f"{ASSETS}/total.svg",
}

# ---------------------------
# LOAD FONTS (KOREAN FIX)
# ---------------------------
plt.rcParams['axes.unicode_minus'] = False

font_list = [
    "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
    "/usr/share/fonts/truetype/nanum/NanumGothicLight.ttf",
    "/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf"
]

for font in font_list:
    if os.path.exists(font):
        fm.fontManager.addfont(font)

plt.rc('font', family='NanumGothic')

# ---------------------------
# READ solve_history.json
# ---------------------------

with open("solve_history.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 최근 7일 기록
today = datetime.datetime.now(timezone("Asia/Seoul")).date()

daily_summary = {}
category_count = {"ikote": 0, "programmers": 0, "boj": 0}

recent_activity_rows = []
trend_dates = []
trend_counts = []

total_solved = 0

for d in data:
    date = datetime.datetime.strptime(d["date"], "%Y-%m-%d").date()

    # 카테고리 카운트
    category = d.get("category", "").lower()
    if "이코테" in category:
        category_count["ikote"] += 1
    elif "프로그래머스" in category:
        category_count["programmers"] += 1
    elif "boj" in category:
        category_count["boj"] += 1

    total_solved += 1

    # 최근 7일 누적
    if (today - date).days <= 6:
        trend_dates.append(str(date))
        trend_counts.append(total_solved)

    # 최근 활동 테이블
    if (today - date).days <= 6:
        for p in d["problems"]:
            recent_activity_rows.append(f"| {date} | {d['category']} | {p} |")

# ---------------------------
# TODAY & WEEKLY CALC
# ---------------------------

today_solved = sum(1 for d in data if d["date"] == str(today))

week_start = today - datetime.timedelta(days=today.weekday())
weekly_solved = sum(1 for d in data if week_start <= datetime.datetime.strptime(d["date"], "%Y-%m-%d").date() <= today)

# ---------------------------
# DRAW DONUT CHART FUNCTION
# ---------------------------

def draw_donut(value, total, outfile):
    if total == 0:
        percent = 0
    else:
        percent = round((value / total) * 100)

    # Light Blue theme
    main_color = "#4d8af0"
    bg_color = "#e6e6e6"

    fig, ax = plt.subplots(figsize=(2.2, 2.2))
    ax.pie(
        [percent, 100 - percent],
        colors=[main_color, bg_color],
        startangle=90,
        wedgeprops={'width': 0.28, 'edgecolor': 'white'}
    )
    ax.text(0, -0.05, f"{percent}%", ha='center', fontsize=13, color=main_color)
    plt.axis("equal")

    plt.savefig(outfile, transparent=True)
    plt.close()


# ---------------------------
# DRAW ALL DONUTS
# ---------------------------

draw_donut(today_solved, 1, DONUT_FILES["today"])
draw_donut(weekly_solved, 10, DONUT_FILES["weekly"])
draw_donut(total_solved, 500, DONUT_FILES["total"])

# category donut
total_category_sum = sum(category_count.values())
for key, file in DONUT_FILES.items():
    if key in ["today", "weekly", "total"]:
        continue
for k in ["ikote", "programmers", "boj"]:
    draw_donut(category_count[k], total_category_sum, DONUT_FILES[k])

# ---------------------------
# TREND GRAPH
# ---------------------------

if trend_dates:
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.plot(trend_dates, trend_counts, marker="o", color="#4d8af0")

    plt.xticks(rotation=45)
    ax.set_title("최근 7일 문제 풀이 추세")
    ax.set_ylabel("누적 문제 수")

    plt.tight_layout()
    plt.savefig(TREND_IMAGE_PATH, dpi=200)
    plt.close()

# ---------------------------
# TEMPLATE → README
# ---------------------------

with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
    template = f.read()

final_md = template.replace("{{TODAY_SOLVED}}", str(today_solved)) \
    .replace("{{WEEKLY_SOLVED}}", str(weekly_solved)) \
    .replace("{{TOTAL_SOLVED}}", str(total_solved)) \
    .replace("{{RECENT_ACTIVITY_TABLE}}", "\n".join(recent_activity_rows)) \
    .replace("{{LAST_UPDATE}}", str(today))

with open(OUTPUT_README, "w", encoding="utf-8") as f:
    f.write(final_md)

print("README updated.")
