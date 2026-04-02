import json
import random
import re
import subprocess
import sys
import unittest
from pathlib import Path

from essay import generate_essay

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = REPO_ROOT / "data.json"
ESSAYS_DIR = REPO_ROOT / "essays"


def _load_data():
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))


def _count_footnotes(text: str) -> int:
    return len(re.findall(r"^\[\^\d+\]:", text, flags=re.MULTILINE))


def _body_headings(text: str) -> list[str]:
    headings = re.findall(r"^## (.+)$", text, flags=re.MULTILINE)
    excluded = {"Abstract", "Introduction", "Conclusion", "Notes", "Works Cited"}
    return [heading for heading in headings if heading not in excluded]


def _body_sections(text: str) -> list[tuple[str, str]]:
    matches = list(re.finditer(r"^## (.+)$", text, flags=re.MULTILINE))
    excluded = {"Abstract", "Introduction", "Conclusion", "Notes", "Works Cited"}
    sections = []
    for index, match in enumerate(matches):
        heading = match.group(1)
        if heading in excluded:
            continue
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections.append((heading, text[start:end].strip()))
    return sections


def _heading_word_count(heading: str) -> int:
    cleaned = re.sub(r"[*(),:/-]", " ", heading)
    return len([word for word in cleaned.split() if word])


def _distinct_theme_hits(text: str, theme: dict) -> int:
    haystack = text.lower()
    candidates = theme["key_concepts"] + theme["relevant_terms"]
    return sum(1 for candidate in candidates if candidate.lower() in haystack)


def _distinct_surface_hits(text: str, theme: dict) -> int:
    haystack = text.lower()
    candidates = theme["key_concepts"] + theme["relevant_terms"] + theme["core_philosophers"]
    return sum(1 for candidate in candidates if candidate.lower() in haystack)


def _extract_markdown_section(text: str, heading: str) -> str:
    match = re.search(
        rf"^## {re.escape(heading)}\n\n(.*?)(?=^## |\Z)",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )
    return match.group(1).strip() if match else ""


def _essay_title(text: str) -> str:
    match = re.search(r"^# (.+)$", text, flags=re.MULTILINE)
    return match.group(1).strip() if match else ""


def _abstract_keywords(text: str) -> list[str]:
    match = re.search(r"^\*\*Keywords:\*\* (.+)$", text, flags=re.MULTILINE)
    if not match:
        return []
    return [keyword.strip() for keyword in match.group(1).split(",") if keyword.strip()]


class GenerationSmokeTest(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        self.data = _load_data()
        ESSAYS_DIR.mkdir(exist_ok=True)

    def test_seeded_themes_stay_within_note_and_heading_limits(self):
        for theme_name in (
            "Digital Subjectivity",
            "Queer Theory",
            "Science and Technology Studies (STS)",
            "Power and Knowledge",
        ):
            with self.subTest(theme=theme_name):
                random.seed(42)
                essay = generate_essay(theme_key=theme_name, metafiction_level="moderate")

                self.assertIn("## Abstract", essay)
                self.assertIn("## Introduction", essay)
                self.assertIn("## Conclusion", essay)
                self.assertIn("## Notes", essay)
                self.assertIn("## Works Cited", essay)
                self.assertGreater(len(essay.split("## Introduction", 1)[0]), 100)
                self.assertLessEqual(_count_footnotes(essay), 36)

                headings = _body_headings(essay)
                self.assertTrue(headings, f"{theme_name}: expected at least one generated body heading.")
                for heading in headings:
                    self.assertLessEqual(_heading_word_count(heading), 16, heading)

                hits = _distinct_theme_hits(essay, self.data["thematic_clusters"][theme_name])
                self.assertGreaterEqual(
                    hits,
                    4,
                    f"{theme_name}: expected at least 4 distinct theme concept/term hits, found {hits}.",
                )

    def test_cli_no_export_runs_non_interactively(self):
        result = subprocess.run(
            [sys.executable, "main.py", "--seed", "42", "--theme", "Digital Subjectivity", "--no-export"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("Essay not exported (--no-export specified).", result.stdout)

    def test_cli_export_auto_generates_filename_without_prompt(self):
        before = set(path.name for path in ESSAYS_DIR.glob("*.md"))
        result = subprocess.run(
            [sys.executable, "main.py", "--seed", "42", "--theme", "Digital Subjectivity", "--export"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
        self.assertEqual(0, result.returncode, result.stderr)
        after = set(path.name for path in ESSAYS_DIR.glob("*.md"))
        created = sorted(after - before)
        self.assertTrue(created, "Expected --export to create a markdown file.")
        for filename in created:
            (ESSAYS_DIR / filename).unlink(missing_ok=True)

    def test_theme_surfaces_stay_local_in_high_visibility_sections(self):
        for theme_name in (
            "Technology, Media, and Culture",
            "Science and Technology Studies (STS)",
            "Speculative Realism and Object-Oriented Ontology",
            "Psychoanalysis and Culture",
        ):
            with self.subTest(theme=theme_name):
                random.seed(314)
                essay = generate_essay(theme_key=theme_name, metafiction_level="moderate")
                theme = self.data["thematic_clusters"][theme_name]

                title = _essay_title(essay)
                self.assertGreaterEqual(
                    _distinct_surface_hits(title, theme),
                    1,
                    f"{theme_name}: expected the essay title to contain at least one theme-local surface hit.",
                )

                keywords = _abstract_keywords(essay)
                self.assertGreaterEqual(
                    sum(
                        1 for keyword in keywords
                        if keyword.lower() in {
                            candidate.lower()
                            for candidate in (
                                theme["key_concepts"] + theme["relevant_terms"] + theme["core_philosophers"]
                            )
                        }
                    ),
                    3,
                    f"{theme_name}: expected at least three abstract keywords from the active theme.",
                )

                introduction = _extract_markdown_section(essay, "Introduction")
                self.assertGreaterEqual(
                    _distinct_theme_hits(introduction, theme),
                    2,
                    f"{theme_name}: expected the introduction to retain at least two distinct theme hits.",
                )

                sections = _body_sections(essay)
                self.assertTrue(sections, f"{theme_name}: expected at least one generated body section.")
                first_heading, first_section_body = sections[0]
                self.assertGreaterEqual(
                    _distinct_surface_hits(first_heading, theme),
                    1,
                    f"{theme_name}: expected the first body heading to contain at least one theme-local surface hit.",
                )

                first_paragraph = first_section_body.split("\n\n", 1)[0].strip()
                self.assertGreaterEqual(
                    _distinct_theme_hits(first_paragraph, theme),
                    2,
                    f"{theme_name}: expected the first body paragraph to retain at least two distinct theme hits.",
                )


if __name__ == "__main__":
    unittest.main()
