from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
README = ROOT / "README.md"

QUESTION_RE = re.compile(
    r"^- \[[ xX]\] \[([^\]]+)\]"
    r"\(https://leetcode\.com/problems/([^/)]+)/?\)(.*)$"
)
TOPIC_RE = re.compile(r"^###\s+\d+\.")
PROGRESS_RE = re.compile(r"^\*\*Progress:\s*\d+/\d+\s+completed\*\*$")

# A problem counts as solved only if its LeetSync folder contains a Java file.
solved_slugs = set()

for folder in ROOT.iterdir():
    if folder.is_dir():
        match = re.match(r"^\d+-(.+)$", folder.name)
        if match and any(
            file.is_file() and file.suffix.lower() == ".java"
            for file in folder.rglob("*")
        ):
            solved_slugs.add(match.group(1))

lines = README.read_text(encoding="utf-8").splitlines()

# Remove old/duplicated dashboard content before the first topic heading.
first_topic = next(
    (i for i, line in enumerate(lines) if TOPIC_RE.match(line)),
    None
)

if first_topic is None:
    sys.exit("ERROR: Could not find topic headings in README.md.")

cleaned = []
for line in lines[:first_topic]:
    if (
        "DSA_PROGRESS_START" in line
        or "DSA_PROGRESS_END" in line
        or "Overall Progress:" in line
        or "problems solved" in line
        or "progress-bar.xyz" in line
    ):
        continue
    cleaned.append(line)

cleaned.extend(lines[first_topic:])

# Count questions and solved questions in each topic.
topic_counts = {}
current_topic = None
total = 0
completed = 0

for line in cleaned:
    if TOPIC_RE.match(line):
        current_topic = line
        topic_counts[current_topic] = [0, 0]
        continue

    match = QUESTION_RE.match(line)
    if match and current_topic:
        slug = match.group(2)
        is_solved = slug in solved_slugs
        topic_counts[current_topic][0] += 1
        topic_counts[current_topic][1] += int(is_solved)
        total += 1
        completed += int(is_solved)

if total != 150:
    sys.exit(
        f"ERROR: Expected 150 roadmap questions, found {total}. "
        "README was not modified."
    )

# Rebuild README with exactly one dashboard and one progress line per topic.
percentage = completed / total * 100
filled = round(percentage / 5)
bar = "█" * filled + "░" * (20 - filled)

dashboard = [
    "<!-- DSA_PROGRESS_START -->",
    f"**Overall Progress:** {completed}/{total} ({percentage:.1f}%)",
    f"`{bar}`",
    f"`{completed} / {total} problems solved`",
    "<!-- DSA_PROGRESS_END -->",
    "",
]

output = []
current_topic = None
dashboard_inserted = False

for line in cleaned:
    if TOPIC_RE.match(line):
        if not dashboard_inserted:
            output.extend(dashboard)
            dashboard_inserted = True

        current_topic = line
        output.append(line)
        done, count = topic_counts[current_topic]
        output.append(f"**Progress: {done}/{count} completed**")
        continue

    if PROGRESS_RE.match(line):
        continue

    match = QUESTION_RE.match(line)
    if match:
        title, slug, suffix = match.groups()
        checkbox = "x" if slug in solved_slugs else " "
        output.append(
            f"- [{checkbox}] [{title}]"
            f"(https://leetcode.com/problems/{slug}/){suffix}"
        )
    else:
        output.append(line)

README.write_text("\n".join(output) + "\n", encoding="utf-8")

print(f"\nREADME updated successfully.")
print(f"Overall progress: {completed}/{total} ({percentage:.1f}%)")
print("\nTopic progress:")

for topic, (count, done) in topic_counts.items():
    print(f"  {topic}: {done}/{count}")

print(f"\nJava solution folders detected: {len(solved_slugs)}")
