import os
import re
import json
import datetime
import pytz
import matplotlib.pyplot as plt
from matplotlib import font_manager, rcParams

USERNAME = "doHoaSen"
REPO = "StudyCodingTest"

TEMPLATE = "template_readme.md"
HISTORY = "solve_history.json"

ASSETS = "assets"
TREND_IMG = f"{ASSETS}/trend.png"

os.makedirs(ASSETS, exist_ok=True)

# -------------------- 폰트 설정 --------------------
font_manager.fontManager.addfont('/usr/share/fonts/truetype/nanum/NanumGothic.ttf')
rcParams['font.family'] = 'NanumGothic'


# -------------------- Java 파일 수 카운트 --------------------
def count_java(path):
    if not os.path.exists(path):
        return 0
    return sum(1 for r, _, f in os.walk(path) for ff in f if ff.endswith(".java"))

ikote_cnt = count_java("src/이코테_자바")
prog_cnt = count_java("src/programmers")
boj_cnt = count_java("src/BOJ")

total_cnt = ikote_cnt + prog_cnt + boj_cnt


# -------------------- Commit 파싱 --------------------
def extract_problems(text):
    return re.findall(r"- (.+)", text)


def parse_gitlog(log):
    solved = 0
    for entry in log.split("\n"):
        if "프로그래머스" not in entry and "이코테" not in entry and "BOJ" not in entry:
            continue
        try:
            commit_hash, msg = entry.split("|||")
            full = os.popen(f"git show {commit_hash}").read()
            solved += len(extract_problems(full))
        except:
            pass
    return solved


# -------------------- Today / Weekly --------------------
today_str = datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%Y-%m-%d")

today_log = os.popen(f'git log --since="{today_str}" --pretty=format:"%H|||%s"').read()
week_log = os.popen('git log --since="7 days ago" --pretty=format:"%H|||%s"').read()

today_solved = parse_gitlog(today_log)
weekly_solved = parse_gitlog(week_log)


# -------------------- 최근 7일 활동 내역 --------------------
recent = ""
git_recent = os.popen(
    'git log --since="7 days ago" --pretty=format:"%H|||%ad|||%s" --date=short'
).read()

for line in git_recent.split("\n"):
    if not line.strip():
        continue
    try:
        commit_hash, date, msg = line.split("|||")

        if not any(k in msg for k in ["프로그래머스", "이코테", "BOJ"]):
            continue

        full = os.popen(f"git show {commit_hash}").read()
        problems = extract_problems(full)

        cat = "프로그래머스" if "프로그래머스" in msg else "이코테" if "이코테" in msg else "BOJ"

        for p in problems:
            recent += f"| {date} | {cat} | {p.strip()} |\n"

    except:
        pass


# -------------------- Trend 그래프 --------------------
history = {}

if os.path.exists(HISTORY):
    with open(HISTORY, encoding="utf-8") as f:
        history = json.load(f)

history[today_str] = total_cnt

with open(HISTORY, "w", encoding="utf-8") as f:
    json.dump(history, f, indent=2, ensure_ascii=False)

dates = sorted(history.keys())
values = [history[d] for d in dates]

plt.figure(figsize=(8, 4))
plt.plot(dates, values, marker="o", color="#4ea3ff")
plt.title("최근 7일 누적 문제 풀이")
plt.grid(True, alpha=0.3)
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig(TREND_IMG, dpi=200)
plt.close()


# -------------------- Donut Chart --------------------
def donut(value, total, filename):
    percent = 0 if total == 0 else (value / total) * 100

    svg = f'''
<svg width="160" height="160" viewBox="0 0 42 42">
  <circle cx="21" cy="21" r="15.915" fill="#e6f3ff"/>
  <circle cx="21" cy="21" r="15.915"
    fill="transparent"
    stroke="#4ea3ff"
    stroke-width="4"
    stroke-dasharray="{percent} {100-percent}"
    transform="rotate(-90 21 21)"
  />
  <text x="50%" y="50%" dy=".3em" text-anchor="middle" font-size="8">{value}</text>
</svg>
'''
    with open(f"{ASSETS}/{filename}", "w", encoding="utf-8") as f:
        f.write(svg)

donut(ikote_cnt, total_cnt, "ikote.svg")
donut(prog_cnt, total_cnt, "programmers.svg")
donut(boj_cnt, total_cnt, "boj.svg")


# -------------------- Progress Bar --------------------
def bar(value, max_value, filename):
    percent = int((value / max_value) * 100) if max_value else 0
    svg = f'''
<svg width="260" height="26">
  <rect width="260" height="20" fill="#e6f3ff" rx="4"/>
  <rect width="{2.6 * percent}" height="20" fill="#4ea3ff" rx="4"/>
  <text x="130" y="14" text-anchor="middle" font-size="10">{value} / {max_value}</text>
</svg>
'''
    with open(f"{ASSETS}/{filename}", "w", encoding="utf-8") as f:
        f.write(svg)

bar(today_solved, 10, "today.svg")
bar(weekly_solved, 10, "weekly.svg")
bar(total_cnt, max(total_cnt, 1), "total.svg")


# -------------------- README 생성 --------------------
with open(TEMPLATE, encoding="utf-8") as f:
    template = f.read()

out = (
    template.replace("{{TODAY_SOLVED}}", str(today_solved))
    .replace("{{WEEKLY_SOLVED}}", str(weekly_solved))
    .replace("{{TOTAL_SOLVED}}", str(total_cnt))
    .replace("{{RECENT_ACTIVITY_TABLE}}", recent)
    .replace("{{USERNAME}}", USERNAME)
    .replace("{{REPO}}", REPO)
    .replace("{{LAST_UPDATE}}", datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%Y-%m-%d %H:%M"))
)

with open("README.md", "w", encoding="utf-8") as f:
    f.write(out)

print("README updated.")
