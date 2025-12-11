import os
import re
import json
import datetime
import pytz
import matplotlib.pyplot as plt
from math import pi

# ─────────────────────────────────────────────
# 기본 설정
# ─────────────────────────────────────────────
README_TEMPLATE = "README.md"
HISTORY_FILE = "solve_history.json"
ASSETS_DIR = "assets"
TREND_IMAGE_PATH = f"{ASSETS_DIR}/trend.png"

os.makedirs(ASSETS_DIR, exist_ok=True)

# Korean Font 설정 (NanumGothic)
plt.rcParams["font.family"] = "NanumGothic"
plt.rcParams["axes.unicode_minus"] = False


# ─────────────────────────────────────────────
# 파일 수 카운팅
# ─────────────────────────────────────────────
def count_java_files(path):
    if not os.path.exists(path):
        return 0
    return sum(1 for _, _, files in os.walk(path) for f in files if f.endswith(".java"))


ikote_count = count_java_files("src/이코테_자바")
programmers_count = count_java_files("src/programmers")
boj_count = count_java_files("src/BOJ")

total_solved = ikote_count + programmers_count + boj_count


# ─────────────────────────────────────────────
# 최근 일자 계산
# ─────────────────────────────────────────────
today = datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%Y-%m-%d")
week_ago = (datetime.datetime.now(pytz.timezone("Asia/Seoul"))
            - datetime.timedelta(days=7)).strftime("%Y-%m-%d")


# ─────────────────────────────────────────────
# 문제명 정제 함수
# ─────────────────────────────────────────────
def clean_problem_name(name):
    name = name.strip()

    # 쓰레기 문자열 제거
    if len(name) < 2:
        return None
    if re.fullmatch(r"[\)\(\]\[]+", name):
        return None
    if name.startswith("/dev"):
        return None
    if len(name) > 30:  # 너무 긴 코드 조각 배제
        return None

    return name


# ─────────────────────────────────────────────
# 최근 7일 commit 로그 추출
# ─────────────────────────────────────────────
log = os.popen(
    f'git log --since="{week_ago}" --pretty=format:"%H|||%ad|||%s" --date=short'
).read()

recent_rows = ""

for entry in log.split("\n"):
    if not entry.strip():
        continue

    commit_hash, commit_date, msg = entry.split("|||")

    # 문제 관련 commit만 필터링
    if not any(k in msg for k in ["프로그래머스", "이코테", "BOJ"]):
        continue

    full_commit = os.popen(f"git show {commit_hash}").read()

    problems = re.findall(r"- (.+)", full_commit)

    for p in problems:
        cleaned = clean_problem_name(p)
        if cleaned:
            if "프로그래머스" in msg:
                recent_rows += f"| {commit_date} | 프로그래머스 | {cleaned} |\n"
            elif "이코테" in msg:
                recent_rows += f"| {commit_date} | 이코테 | {cleaned} |\n"
            elif "BOJ" in msg:
                recent_rows += f"| {commit_date} | BOJ | {cleaned} |\n"


# ─────────────────────────────────────────────
# 오늘 푼 문제 수 계산
# ─────────────────────────────────────────────
today_solved = recent_rows.count(today)


# ─────────────────────────────────────────────
# solve_history.json 업데이트
# ─────────────────────────────────────────────
if os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        history = json.load(f)
else:
    history = {}

history[today] = total_solved

with open(HISTORY_FILE, "w", encoding="utf-8") as f:
    json.dump(history, f, indent=2, ensure_ascii=False)


# ─────────────────────────────────────────────
# SVG 원형 게이지 생성 함수
# ─────────────────────────────────────────────
def create_svg(filename, percent, label):
    radius = 45
    circumference = 2 * pi * radius
    progress = circumference * (percent / 100)

    svg_content = f"""
    <svg width="140" height="140" viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
        <circle cx="60" cy="60" r="{radius}" fill="none" stroke="#e6e6e6" stroke-width="10"/>
        <circle cx="60" cy="60" r="{radius}" fill="none"
            stroke="#4C9CFF" stroke-width="10"
            stroke-dasharray="{progress} {circumference-progress}"
            stroke-linecap="round"
            transform="rotate(-90 60 60)"
        />
        <text x="60" y="60" text-anchor="middle" font-size="20" fill="#4C9CFF" dy="6">{percent}%</text>
        <text x="60" y="90" text-anchor="middle" font-size="12" fill="#555">{label}</text>
    </svg>
    """

    with open(f"{ASSETS_DIR}/{filename}", "w", encoding="utf-8") as f:
        f.write(svg_content)


# ─────────────────────────────────────────────
# 카테고리 비율 계산
# ─────────────────────────────────────────────
total_for_ratio = max(total_solved, 1)

cat_ratio = round((ikote_count / total_for_ratio) * 100)
prog_ratio = round((programmers_count / total_for_ratio) * 100)
boj_ratio = round((boj_count / total_for_ratio) * 100)

# SVG 생성
create_svg("today.svg", today_solved * 10, "오늘 푼 문제")
create_svg("weekly.svg", min(today_solved * 10, 100), "주간 목표")
create_svg("total.svg", min(total_solved / 5, 100), "누적 해결률")
create_svg("categories.svg", prog_ratio, "프로그래머스 비율")


# ─────────────────────────────────────────────
# 추세 그래프 생성
# ─────────────────────────────────────────────
dates = sorted(history.keys())
values = [history[d] for d in dates]

plt.figure(figsize=(8, 4))
plt.plot(dates, values, marker="o", color="#4C9CFF")
plt.title("최근 7일 누적 문제 그래프")
plt.xlabel("날짜")
plt.ylabel("해결 수")
plt.grid(True, alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(TREND_IMAGE_PATH, dpi=200)
plt.close()


# ─────────────────────────────────────────────
# README 업데이트
# ─────────────────────────────────────────────
with open(README_TEMPLATE, "r", encoding="utf-8") as f:
    readme = f.read()

now = datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%Y-%m-%d %H:%M")

new_readme = (
    readme.replace("{{RECENT_ACTIVITY_TABLE}}", recent_rows)
          .replace("{{LAST_UPDATE}}", now)
)

with open("README.md", "w", encoding="utf-8") as f:
    f.write(new_readme)

print("README updated.")
