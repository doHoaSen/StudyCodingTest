import os
import re
import json
import datetime
import pytz
import matplotlib.pyplot as plt
import numpy as np

# 폰트 설정 (GitHub Actions용)
plt.rcParams["font.family"] = "DejaVu Sans"

ROOT = "."
TEMPLATE_FILE = "template_readme.md"
OUTPUT_README = "README.md"

ASSETS = os.path.join(ROOT, "assets")
os.makedirs(ASSETS, exist_ok=True)

# -------------------------
# 유틸 함수
# -------------------------
def count_java_files(path):
    if not os.path.exists(path):
        return 0
    return sum(f.endswith(".java") for _, _, fs in os.walk(path) for f in fs)

def parse_commits(days=60):
    """최근 N일간 커밋 수집 → 날짜별 문제 푼 수 계산"""
    log = os.popen(
        f'git log --since="{days} days ago" --pretty=format:"%ad|||%s" --date=short'
    ).read()

    stats = {}
    for line in log.split("\n"):
        if "프로그래머스" not in line and "이코테" not in line and "BOJ" not in line:
            continue

        try:
            date, msg = line.split("|||")
        except:
            continue

        # commit message: "251210 프로그래머스: lv.1 3문제"
        m = re.search(r"(\d+)문제", msg)
        solved = int(m.group(1)) if m else 1

        stats[date] = stats.get(date, 0) + solved

    return stats


# -------------------------
# 문제 카운트
# -------------------------
ikote = count_java_files("src/이코테_자바")
programmers = count_java_files("src/programmers")
boj = count_java_files("src/BOJ")

total = ikote + programmers + boj

# -------------------------
# 오늘 날짜 / 주간 통계
# -------------------------
today = datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%Y-%m-%d")
week_log = parse_commits(7)
today_solved = week_log.get(today, 0)
weekly_solved = sum(week_log.values())

# -------------------------
# Heatmap 데이터
# -------------------------
heatmap_data = parse_commits(60)

# -------------------------
# Donut Chart 생성
# -------------------------
def donut(value, label, filename, color="#4DB6E8"):
    fig, ax = plt.subplots(figsize=(3, 3))
    ax.pie(
        [value, 1],
        radius=1,
        colors=[color, "#E8F4FB"],
        startangle=90,
        counterclock=False,
        wedgeprops={"width": 0.35},
    )
    ax.text(0, 0, label, ha="center", va="center", fontsize=16)
    ax.set(aspect="equal")
    plt.savefig(os.path.join(ASSETS, filename), transparent=True)
    plt.close()


donut(today_solved, str(today_solved), "today.svg")
donut(weekly_solved, str(weekly_solved), "weekly.svg")
donut(total, str(total), "total.svg")
donut(total, "전체", "category_total.svg")

donut(ikote, str(ikote), "category_ikote.svg")
donut(programmers, str(programmers), "category_programmers.svg")
donut(boj, str(boj), "category_boj.svg")

# -------------------------
# Heatmap 생성
# -------------------------
def generate_heatmap(data, filename):
    dates = []
    values = []

    today = datetime.date.today()
    for i in range(60):
        d = today - datetime.timedelta(days=i)
        ds = d.strftime("%Y-%m-%d")
        dates.append(d)
        values.append(data.get(ds, 0))

    dates = dates[::-1]
    values = values[::-1]

    fig, ax = plt.subplots(figsize=(12, 2))
    vmax = max(values) if max(values) > 0 else 1

    cmap = plt.cm.get_cmap("Blues")
    colors = [cmap(v / vmax) for v in values]

    ax.bar(range(60), [1]*60, color=colors, width=1.0)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlim(0, 60)

    plt.savefig(os.path.join(ASSETS, filename), transparent=True)
    plt.close()


generate_heatmap(heatmap_data, "heatmap.svg")

# -------------------------
# README 생성
# -------------------------
with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
    template = f.read()

now = datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%Y-%m-%d %H:%M")

readme = (
    template.replace("{{TODAY_SOLVED}}", str(today_solved))
    .replace("{{WEEKLY_SOLVED}}", str(weekly_solved))
    .replace("{{TOTAL_SOLVED}}", str(total))
    .replace("{{LAST_UPDATE}}", now)
)

with open(OUTPUT_README, "w", encoding="utf-8") as f:
    f.write(readme)

print("README updated successfully.")
