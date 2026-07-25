#!/usr/bin/env python3
"""
Auto-generate the root README.md with an up-to-date problem index table.
Scans all topic folders, parses solution READMEs, and builds the master table.
Now supports multiple solution files and languages per problem.
"""

import os
import re
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
README_PATH = os.path.join(REPO_ROOT, "README.md")

# Directories to ignore
IGNORE_DIRS = {".git", ".github", ".gitkeep", "__pycache__", "scripts", "assets"}

# Difficulty mapping
DIFFICULTY_MAP = {
    "easy": "🟢 Easy",
    "medium": "🟡 Medium",
    "hard": "🔴 Hard",
}

# Language detection from file extensions
EXTENSION_TO_LANGUAGE = {
    ".py": "Python",
    ".cpp": "C++",
    ".cxx": "C++",
    ".cc": "C++",
    ".java": "Java",
    ".js": "JavaScript",
    ".ts": "TypeScript",
    ".go": "Go",
    ".rs": "Rust",
    ".swift": "Swift",
    ".kt": "Kotlin",
}

# Language icons for badges
LANGUAGE_ICONS = {
    "Python": "![Python](https://img.shields.io/badge/-Python-3776AB?logo=python&logoColor=white)",
    "C++": "![C++](https://img.shields.io/badge/-C++-00599C?logo=c%2B%2B&logoColor=white)",
    "Java": "![Java](https://img.shields.io/badge/-Java-ED8B00?logo=openjdk&logoColor=white)",
    "JavaScript": "![JavaScript](https://img.shields.io/badge/-JavaScript-F7DF1E?logo=javascript&logoColor=black)",
    "TypeScript": "![TypeScript](https://img.shields.io/badge/-TypeScript-3178C6?logo=typescript&logoColor=white)",
    "Go": "![Go](https://img.shields.io/badge/-Go-00ADD8?logo=go&logoColor=white)",
    "Rust": "![Rust](https://img.shields.io/badge/-Rust-000000?logo=rust&logoColor=white)",
    "Swift": "![Swift](https://img.shields.io/badge/-Swift-FA7343?logo=swift&logoColor=white)",
    "Kotlin": "![Kotlin](https://img.shields.io/badge/-Kotlin-7F52FF?logo=kotlin&logoColor=white)",
}


def detect_languages_from_files(root):
    """Detect languages by scanning solution files in the problem folder."""
    languages = []
    if os.path.isdir(root):
        for f in os.listdir(root):
            ext = os.path.splitext(f)[1].lower()
            if ext in EXTENSION_TO_LANGUAGE:
                lang = EXTENSION_TO_LANGUAGE[ext]
                if lang not in languages:
                    languages.append(lang)
    return languages


def parse_problem_readme(readme_path):
    """Extract problem metadata from a solution's README.md."""
    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract problem number from title (e.g., "# 3658. GCD of Odd and Even Sums")
    title_match = re.search(r"^#\s+(\d+)\.\s+(.+)$", content, re.MULTILINE)
    number = title_match.group(1) if title_match else "???"
    title = title_match.group(2).strip() if title_match else "Unknown"

    # Extract topic (e.g., "**Topic:** Math")
    topic_match = re.search(r"\*\*Topic:\*\*\s*(.+)", content)
    topic = topic_match.group(1).strip() if topic_match else "Unknown"

    # Extract difficulty (e.g., "**Difficulty:** Easy")
    diff_match = re.search(r"\*\*Difficulty:\*\*\s*(.+)", content)
    difficulty_raw = diff_match.group(1).strip().lower() if diff_match else "unknown"
    difficulty = DIFFICULTY_MAP.get(difficulty_raw, f"⚪ {difficulty_raw.title()}")

    return number, title, difficulty, topic


def scan_solutions():
    """Walk the repo tree and collect all problem solutions."""
    solutions = []

    for root, dirs, _ in os.walk(REPO_ROOT):
        # Skip ignored dirs
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS and not d.startswith(".")]

        # Check if this directory contains a README.md
        if "README.md" in os.listdir(root):
            # Ensure it's a problem folder (has a number prefix like "3658_...")
            folder_name = os.path.basename(root)
            if re.match(r"^\d+_", folder_name):
                readme_path = os.path.join(root, "README.md")
                try:
                    number, title, difficulty, topic = parse_problem_readme(readme_path)

                    # Detect languages from actual solution files
                    languages = detect_languages_from_files(root)

                    # Find all solution files (not README.md)
                    solution_files = sorted([
                        f
                        for f in os.listdir(root)
                        if f.endswith((".py", ".cpp", ".cxx", ".cc", ".java", ".js", ".ts", ".go", ".rs", ".swift", ".kt"))
                    ])

                    # Relative paths for links
                    rel_folder = os.path.relpath(root, REPO_ROOT).replace("\\", "/")

                    solutions.append(
                        {
                            "number": number,
                            "title": title,
                            "difficulty": difficulty,
                            "topic": topic,
                            "languages": languages,
                            "solution_files": solution_files,
                            "folder": rel_folder,
                            "readme": f"{rel_folder}/README.md",
                        }
                    )
                except Exception as e:
                    print(f"⚠️  Error parsing {readme_path}: {e}")

    # Sort by problem number
    solutions.sort(key=lambda s: int(s["number"]) if s["number"].isdigit() else 0)
    return solutions


def generate_readme(solutions):
    """Generate the full README.md content."""
    # Count stats
    total = len(solutions)
    easy_count = sum(1 for s in solutions if "Easy" in s["difficulty"])
    medium_count = sum(1 for s in solutions if "Medium" in s["difficulty"])
    hard_count = sum(1 for s in solutions if "Hard" in s["difficulty"])
    topics = sorted(set(s["topic"] for s in solutions))

    # Collect all unique languages across all solutions
    all_languages_set = set()
    for s in solutions:
        for lang in s["languages"]:
            all_languages_set.add(lang)
    all_languages = sorted(all_languages_set)

    # Build the table rows
    table_rows = []
    for s in solutions:
        # Build language badges string
        if s["languages"]:
            lang_badges = " & ".join(
                LANGUAGE_ICONS.get(lang, lang) for lang in s["languages"]
            )
        else:
            lang_badges = "Unknown"

        # Build solution file links - direct links to each solution file
        if s["solution_files"]:
            solution_links = []
            for sf in s["solution_files"]:
                ext = os.path.splitext(sf)[1].lower()
                lang_label = EXTENSION_TO_LANGUAGE.get(ext, "Solution")
                solution_links.append(f"[{lang_label}]({s['folder']}/{sf})")
            solution_link = " & ".join(solution_links)
        else:
            solution_link = f"[View]({s['readme']})"

        problem_link = f"[{s['number']}. {s['title']}]({s['folder']}/)"
        table_rows.append(
            f"| {s['number']} | {problem_link} | {s['difficulty']} | {s['topic']} | {lang_badges} | {solution_link} | ✅ |"
        )

    table_body = "\n".join(table_rows) if table_rows else "| | *No solutions yet* | | | | | |"

    # Build the README
    readme = f"""# 🧠 LeetCode Solutions

![Problems Solved](https://img.shields.io/badge/Solved-{total}-brightgreen)
![Easy](https://img.shields.io/badge/Easy-{easy_count}-brightgreen)
![Medium](https://img.shields.io/badge/Medium-{medium_count}-yellow)
![Hard](https://img.shields.io/badge/Hard-{hard_count}-red)
![Languages](https://img.shields.io/badge/Languages-{len(all_languages)}-blue)
![GitHub last commit](https://img.shields.io/github/last-commit/rakshika2639/leetcode-solutions)

A curated collection of my LeetCode problem solutions, organized by topic. Each solution includes a detailed explanation, complexity analysis, and key takeaways to reinforce learning.

> 🔄 This README is **automatically updated** via GitHub Actions whenever new solutions are pushed.

---

## 📊 Progress Overview

| Metric | Count |
|--------|:-----:|
| ✅ Total Solved | **{total}** |
| 🟢 Easy | **{easy_count}** |
| 🟡 Medium | **{medium_count}** |
| 🔴 Hard | **{hard_count}** |
| 📚 Topics Covered | **{len(topics)}** |
| 💻 Languages Used | **{len(all_languages)}** |

---

## 📋 Problem Index

| # | Problem | Difficulty | Topic | Language | Solution | Status |
|---|---------|:----------:|-------|:--------:|:--------:|:------:|
{table_body}
| | **Total** | | | | | **{total}** |

---

## 🗂️ Repository Structure

```
leetcode-solutions/
├── README.md               ← You are here (auto-generated)
├── .github/workflows/      ← CI/CD for auto-updating this README
├── scripts/                ← Generation scripts
└── Topic_Name/             ← Organized by topic (e.g., Math, Arrays)
    └── Problem_Number_Title/
        ├── README.md       ← Problem explanation, approach & complexity
        ├── solution.py     ← Solution in Python (and/or other languages)
        └── solution.cpp    ← Solution in C++
```

---

## 🚀 How to Navigate

1. **By Topic** — Each folder groups problems by their primary topic (e.g., `Math/`, `Arrays/`, `String/`).
2. **By Problem** — Click any problem number in the table above to jump directly to its solution folder.
3. **By Language** — Filter solutions by language.

---

## 🛠️ Languages Used

"""

    # Languages section
    lang_rows = []
    for lang in all_languages:
        count = sum(1 for s in solutions if lang in s["languages"])
        icon = LANGUAGE_ICONS.get(lang, lang)
        lang_rows.append(f"| {icon} | {count} |")
    lang_table = "\n".join(lang_rows) if lang_rows else "| None | 0 |"

    readme += f"""| Language | Problems |
|:--------:|:--------:|
{lang_table}

---

## 📈 Topics Covered

"""

    # Topics section
    topic_rows = []
    for topic in topics:
        count = sum(1 for s in solutions if s["topic"] == topic)
        topic_rows.append(f"- **{topic}** — {count} problem(s)")
    topic_section = "\n".join(topic_rows) if topic_rows else "- *No topics yet*"

    readme += f"""{topic_section}

---

## 🎯 Next Goals

- [ ] Solve problems across more topics
- [ ] Add multiple language solutions per problem
- [ ] Include video walkthrough links
- [ ] Maintain a weekly streak

---

<div align="center">

**Happy Coding!** ✨

⭐ Star this repo if you find it helpful!

</div>
"""

    return readme


def main():
    print("🔍 Scanning repository for solutions...")
    solutions = scan_solutions()
    print(f"   Found {len(solutions)} solution(s)")

    print("📝 Generating README...")
    new_readme = generate_readme(solutions)

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_readme)

    print(f"✅ README.md updated successfully at {README_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

