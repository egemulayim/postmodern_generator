import json
import random
import re
import unittest
from pathlib import Path

from essay import generate_essay

REPO_ROOT = Path(__file__).resolve().parent.parent
FIXTURE_PATH = REPO_ROOT / "tests" / "fixtures" / "theme_surface_regressions.json"


def _load_fixture() -> dict:
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


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
    data_path = REPO_ROOT / "data.json"
    return json.loads(data_path.read_text(encoding="utf-8"))


def _distinct_theme_hits(text: str, theme: dict) -> int:
    haystack = text.lower()
    candidates = theme["key_concepts"] + theme["relevant_terms"]
    return sum(1 for candidate in candidates if candidate.lower() in haystack)


def _distinct_surface_hits(text: str, theme: dict) -> int:
    haystack = text.lower()
    candidates = theme["key_concepts"] + theme["relevant_terms"] + theme["core_philosophers"]
    return sum(1 for candidate in candidates if candidate.lower() in haystack)


class GenerationRegressionTest(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        self.fixture = _load_fixture()
        self.data = _load_data()

    def test_seeded_theme_surfaces_match_regression_fixture(self):
        for case in self.fixture["cases"]:
            with self.subTest(theme=case["theme"], seed=case["seed"]):
                random.seed(case["seed"])
                essay = generate_essay(
                    theme_key=case["theme"],
                    metafiction_level=case["metafiction_level"],
                )

                title_match = re.search(r"^# (.+)$", essay, flags=re.MULTILINE)
                keyword_match = re.search(r"^\*\*Keywords:\*\* (.+)$", essay, flags=re.MULTILINE)
                first_heading, first_body = _body_sections(essay)[0]
                first_paragraph = _normalize_whitespace(first_body.split("\n\n", 1)[0].strip())
                theme = self.data["thematic_clusters"][case["theme"]]

                actual = {
                    "title": title_match.group(1).strip() if title_match else "",
                    "keywords": sorted([
                        _normalize_keyword(keyword)
                        for keyword in keyword_match.group(1).split(",")
                        if _normalize_keyword(keyword)
                    ]) if keyword_match else [],
                }

                expected = {
                    "title": case["title"],
                    "keywords": case["keywords"],
                }

                self.assertEqual(
                    expected,
                    actual,
                    (
                        f"{case['theme']} seed {case['seed']} no longer matches the stored "
                        "surface regression fixture. If the change is intentional, refresh "
                        "tests/fixtures/theme_surface_regressions.json with "
                        "`python3 scripts/capture_surface_regressions.py`."
                    ),
                )

                self.assertGreaterEqual(
                    _distinct_surface_hits(first_heading, theme),
                    case["min_heading_surface_hits"],
                    (
                        f"{case['theme']} seed {case['seed']} first heading lost too much theme-local "
                        "surface detail compared with the stored regression baseline."
                    ),
                )
                self.assertGreaterEqual(
                    _distinct_theme_hits(first_paragraph, theme),
                    case["min_paragraph_theme_hits"],
                    (
                        f"{case['theme']} seed {case['seed']} first paragraph lost too much theme-local "
                        "content compared with the stored regression baseline."
                    ),
                )


if __name__ == "__main__":
    unittest.main()
