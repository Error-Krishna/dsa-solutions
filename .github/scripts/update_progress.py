import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
README = ROOT / "README.md"

START = "<!-- DSA_PROGRESS_START -->"
END = "<!-- DSA_PROGRESS_END -->"

TABLE_ROW = re.compile(
    r"^\|\s*(\d+)\s*\|\s*\[([^\]]+)\]"
    r"\(https://leetcode\.com/problems/([^/)]+)/?\)"
    r"\s*\|\s*(Easy|Medium|Hard)\s*\|$"
)

TASK_ROW = re.compile(
    r"^-\s*\[[ xX]\]\s*\[([^\]]+)\]"
    r"\(https://leetcode\.com/problems/([^/)]+)/?\)"
    r"\s+—\s+(Easy|Medium|Hard)$"
)

SECTION = re.compile(r"^###\s+(\d+)\.\s+(.+?)(?:\s+—\s+\d+\s+Problems)?$")
PROGRESS = re.compile(r"^\*\*Progress:\s*\d+/\d+\s+completed\*\*$")


def get_solved_slugs():
    solved = set()

    for folder in ROOT.iterdir():
        if not folder.is_dir():
            continue

        match = re.match(r"^\d+-(.+)$", folder.name)

        if not match:
            continue

        # Only count actual LeetSync solution folders.
        if list(folder.glob("*.java")):
            solved.add(match.group(1).lower())

    return solved


def update():
    if not README.exists():
        raise FileNotFoundError("Root README.md does not exist.")

    solved = get_solved_slugs()
    lines = README.read_text(encoding="utf-8").splitlines()

    if not any(line.startswith("## 📚 DSA Roadmap") for line in lines):
        raise ValueError("DSA Roadmap heading was not found.")

    if START not in lines or END not in lines:
        raise ValueError("Progress markers are missing from README.md.")

    output = []
    topic_counts = []
    current_topic = None
    total = 0
    completed = 0

    for line in lines:
        if line == START:
            output.append(START)
            output.append(f"**Overall Progress:** {completed}/{total} (0%)")
            output.append(END)
            continue

        if line == END:
            # Replace the temporary dashboard with final values.
            output[-2:] = [
                f"**Overall Progress:** {completed}/{total} "
                f"({round(completed / total * 100, 1) if total else 0}%)",
                f"`{completed} / {total} problems solved`",
                f"![Progress](https://progress-bar.xyz/"
                f"{round(completed / total * 100, 1) if total else 0}"
                f"/?width=400)",
                END,
            ]
            continue

        section = SECTION.match(line)

        if section:
            current_topic = {
                "name": line,
                "total": 0,
                "completed": 0,
            }
            topic_counts.append(current_topic)
            output.append(line)
            continue

        if current_topic and PROGRESS.match(line):
            continue

        if current_topic:
            match = TABLE_ROW.match(line)
            task = TASK_ROW.match(line)

            if match:
                _, title, slug, difficulty = match.groups()
            elif task:
                title, slug, difficulty = task.groups()
            else:
                if line.startswith("|") and (
                    re.match(r"^\|\s*#\s*\|", line)
                    or re.match(r"^\|\s*:?-{2,}", line)
                ):
                    continue

                output.append(line)
                continue

            is_solved = slug.lower() in solved
            current_topic["total"] += 1
            total += 1

            if is_solved:
                current_topic["completed"] += 1
                completed += 1

            checkbox = "x" if is_solved else " "
            output.append(
                f"- [{checkbox}] [{title}]"
                f"(https://leetcode.com/problems/{slug}/)"
                f" — {difficulty}"
            )
            continue

        output.append(line)

    if total != 150:
        raise ValueError(
            f"Expected 150 roadmap questions, found {total}. "
            "No README changes were written."
        )

    # Add topic progress directly below each topic heading.
    final_lines = []
    topic_index = 0

    for line in output:
        final_lines.append(line)

        if topic_index < len(topic_counts):
            topic = topic_counts[topic_index]

            if line == topic["name"]:
                final_lines.append(
                    f"**Progress: {topic['completed']}/"
                    f"{topic['total']} completed**"
                )
                topic_index += 1

    README.write_text(
        "\n".join(final_lines) + "\n",
        encoding="utf-8",
    )

    print("\n========== PROGRESS REPORT ==========")
    for topic in topic_counts:
        print(
            f"{topic['completed']:2}/{topic['total']:2} "
            f"- {topic['name'].replace('### ', '')}"
        )

    percentage = round(completed / total * 100, 1)
    print("-------------------------------------")
    print(f"TOTAL: {completed}/{total} ({percentage}%)")
    print("README updated successfully.")
    print("=====================================")


if __name__ == "__main__":
    update()
