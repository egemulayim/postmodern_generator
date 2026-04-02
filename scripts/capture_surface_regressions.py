"""
Capture representative seeded surface regressions for noisy themes.

This snapshot intentionally records only the highest-visibility surfaces
that have been most prone to theme drift:

- title
- abstract keywords
- first body heading
- first body paragraph

The fixture is meant to preserve the current qualitative baseline so future
changes can be evaluated against concrete seeded outputs instead of memory.
"""

from __future__ import annotations

import argparse
import json
import random
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from essay import generate_essay

DEFAULT_OUTPUT = REPO_ROOT / "tests" / "fixtures" / "theme_surface_regressions.json"
DATA_PATH = REPO_ROOT / "data.json"

CASES = [
    ("Science and Technology Studies (STS)", 42),
    ("Science and Technology Studies (STS)", 314),
    ("Speculative Realism and Object-Oriented Ontology", 42),
    ("Speculative Realism and Object-Oriented Ontology", 314),
    ("Technology, Media, and Culture", 42),
    ("Technology, Media, and Culture", 314),
    ("Psychoanalysis and Culture", 42),
    ("Psychoanalysis and Culture", 314),
    ("Power and Knowledge", 42),
    ("Power and Knowledge", 314),
    ("Digital Subjectivity", 42),
    ("Digital Subjectivity", 314),
]


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


def _normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _normalize_keyword(keyword: str) -> str:
    return keyword.strip().strip("*").strip()


def _load_data() -> dict:
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))


def _distinct_theme_hits(text: str, theme: dict) -> int:
    haystack = text.lower()
    candidates = theme["key_concepts"] + theme["relevant_terms"]
    return sum(1 for candidate in candidates if candidate.lower() in haystack)


def _distinct_surface_hits(text: str, theme: dict) -> int:
    haystack = text.lower()
    candidates = theme["key_concepts"] + theme["relevant_terms"] + theme["core_philosophers"]
    return sum(1 for candidate in candidates if candidate.lower() in haystack)


def capture_cases() -> dict:
    data = _load_data()
    cases = []
    for theme_name, seed in CASES:
        random.seed(seed)
        essay = generate_essay(theme_key=theme_name, metafiction_level="moderate")
        theme = data["thematic_clusters"][theme_name]
        title_match = re.search(r"^# (.+)$", essay, flags=re.MULTILINE)
        keyword_match = re.search(r"^\*\*Keywords:\*\* (.+)$", essay, flags=re.MULTILINE)
        first_heading, first_body = _body_sections(essay)[0]
        first_paragraph = _normalize_whitespace(first_body.split("\n\n", 1)[0].strip())
        keywords = [
            _normalize_keyword(keyword)
            for keyword in keyword_match.group(1).split(",")
            if _normalize_keyword(keyword)
        ] if keyword_match else []
        cases.append(
            {
                "theme": theme_name,
                "seed": seed,
                "metafiction_level": "moderate",
                "title": title_match.group(1).strip() if title_match else "",
                "keywords": sorted(keywords),
                # Leave a small buffer for sentence-assembly variance across Python processes.
                "min_heading_surface_hits": max(1, _distinct_surface_hits(first_heading, theme) - 2),
                "min_paragraph_theme_hits": max(7, _distinct_theme_hits(first_paragraph, theme) - 4),
                "reference_first_heading": first_heading,
                "reference_first_paragraph": first_paragraph,
            }
        )

    return {"cases": cases}


def main() -> int:
    parser = argparse.ArgumentParser(description="Capture seeded theme-surface regression fixtures.")
    parser.add_argument(
        "--output",
        default=str(DEFAULT_OUTPUT),
        help="Path to the JSON fixture file to write.",
    )
    args = parser.parse_args()

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(capture_cases(), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote regression fixture to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
