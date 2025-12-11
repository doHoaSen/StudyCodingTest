import os
import re
import json
import datetime
import pytz
import matplotlib.pyplot as plt
from matplotlib import font_manager

README_FILE = "README.md"
HISTORY_FILE = "solve_history.json"

ASSETS = "assets"
os.makedirs(ASSETS, exist_ok=True)

TREND = f"{ASSETS}/trend.png"
TODAY_SVG = f"{ASSETS}/today.svg"
WEEKLY_SVG = f"{ASSETS}/weekly.svg"
TOTAL_SVG = f"{ASSETS}/total.svg"

# -----------------------------
# 1) Install Korean Font (Fix for GitHub Actions)
# -----------------------------
font_paths = [
    "/usr/share/fonts/opentype/nanum/NanumGothic.otf",
    "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
    "/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf"
]

valid_font_path = None
for p in font_paths:
    if os.path.exists(p):
        valid_font_path = p
        break

if valid_font_path:
    font_manager.fontManager.addfont(valid_font_path)
    plt.rc('font', family='NanumGothic')
else:
    plt.rc('font', family='DejaVu Sans')

# -----------------------------
# Count Java Files
# -----------------------------
def count_java(path):
    if not os.path.exists(path):
        return 0
    return sum(1 for _, _, files in os.walk(path) for f in files if f.endswith(".java"))

ikote = count_java("src/이코테_자바")
pro = count_java("src/programmers")
boj = count_java("src/BOJ")
total = ikote + pro + boj

# -----------------------------
# Extract Problems from commits
# -----------------------------
def extract_problems(text):
    lines = text.split("\n")
    result = []
    for line in lines:
        if line.startswith("- "):
            name = line[2:].strip()
            if not name.startswith("/") and len(name) < 50:
                result.append(name)
    return result

# -----------------------------
# Today solved
# -----------------------------
today = datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%Y-%m-%d")
today_log = os.popen(f'git log --since="{today}" --pretty=format:"%H|||%s"').read()

today_solved = 0
for entry in today_log.split("\n"):
    if not entry.strip():
        continue
    commit, msg = entry.split("|||")
    if not any(k in msg for k in ["프로그래머스", "이코테", "BOJ"]):
        continue
    full = os.popen(f"git show {commit}").read()
    today_solved += len(extract_problems(full))

# -----------------------------
# Weekly solved
# -----------------------------
week_log = os.popen('git log --since="7 days ago" --pretty=format:"%H|||%s"').read()
week_solved = 0

for entry in week_log.split("\n"):
    if not entry.strip():
        continue
    commit, msg = entry.split("|||")
    if not any(k in msg for k in ["프로그래머스", "이코테", "BOJ"]):
        continue
    full = os.popen(f"git show {commit}").read()
    week_solved += len(extract_problems(full))

week_progress = min(week_solved, 10)

# -----------------------------
# History for trend graph
# -----------------------------
if os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        history = json.load(f)
else:
    history = {}

history[today] = total

with open(HISTORY_FILE, "w", encoding="utf-8") as f:
    json.dump(history, f, indent=2, ensure_ascii=False)

# -----------------------------
# Trend Graph (7 days)
# -----------------------------
dates = sorted(history.keys())[-7:]
values = [history[d] for d in dates]

plt.figure(figsize=(8, 4))
plt.plot(dates, values, marker="o", color="#4A90E2")
plt.grid(True, alpha=0.3)
plt.title("최근 7일 누적 문제 그래프")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(TREND, dpi=200)
plt.close()

# -----------------------------
# Create light-blue SVG progress bars
# -----------------------------
def make_svg(value, max_value, path):
    pct = int((value / max_value) * 100)
    bar = int(240 * value / max_value)

    svg = f"""
<svg width="260" height="40">
  <rect width="240" height="10" x="10" y="18" rx="5" fill="#E6ECF5"/>
  <rect width="{bar}" height="10" x="10" y="18" rx="5" fill="#8AB6F9"/>
  <text x="130" y="15" font-size="12" text-anchor="middle">{value} / {max_value} ({pct}%)</text>
</svg>
"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)

make_svg(today_solved, 10, TODAY_SVG)
make_svg(week_solved, 10, WEEKLY_SVG)
make_svg(total, 500, TOTAL_SVG)

# -----------------------------
# Recent Activity Table
# -----------------------------
recent = ""

git_recent = os.popen(
    'git log --since="7 days ago" --pretty=format:"%H|||%ad|||%s" --date=short'
).read()

for entry in git_recent.split("\n"):
    if not entry.strip():
        continue
    commit, d, msg = entry.split("|||")
    if not any(k in msg for k in ["프로그래머스", "BOJ", "이코테"]):
        continue

    full = os.popen(f"git show {commit}").read()
    problems = extract_problems(full)

    for p in problems:
        recent += f"| {d} | {msg.split()[0]} | {p} |\n"

# -----------------------------
# Replace placeholders safely
# -----------------------------
def safe_replace(text, key, value):
    # "{{KEY}}", "{{ KEY }}", "{{KEY }}" 등 다양한 패턴 허용
    patterns = [
        f"{{{{{key}}}}}",
        f"{{{{ {key} }}}}",
        f"{{{{{key} }}}}",
        f"{{{{ {key}}}}}",
    ]
    for p in patterns:
        text = text.replace(p, value)
    return text

with open(README_FILE, "r", encoding="utf-8") as f:
    readme = f.read()

now = datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%Y-%m-%d %H:%M")

readme = safe_replace(readme, "TODAY_SOLVED", str(today_solved))
readme = safe_replace(readme, "WEEKLY_SOLVED", str(week_solved))
readme = safe_replace(readme, "TOTAL_SOLVED", str(total))
readme = safe_replace(readme, "IKOTE_COUNT", str(ikote))
readme = safe_replace(readme, "PROGRAMMERS_COUNT", str(pro))
readme = safe_replace(readme, "BOJ_COUNT", str(boj))
readme = safe_replace(readme, "RECENT_ACTIVITY_TABLE", recent)
readme = safe_replace(readme, "LAST_UPDATE", now)

with open(README_FILE, "w", encoding="utf-8") as f:
    f.write(readme)

print("Dashboard README updated.")
