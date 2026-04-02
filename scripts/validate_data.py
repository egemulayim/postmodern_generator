"""
Validate the generator's JSON data contract.

This script is intentionally strict about theme schema drift because the
generator now relies on canonical theme fields without runtime shims.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent.parent / "data.json"

REQUIRED_ROOT_KEYS = (
    "philosophers",
    "concepts",
    "hybrid_concept_terms",
    "terms",
    "academic_vocab",
    "philosopher_concepts",
    "philosopher_key_works",
    "quotes",
    "thematic_clusters",
    "citation_relationships",
    "philosophical_movements",
)

REQUIRED_THEME_KEYS = (
    "description",
    "core_philosophers",
    "key_concepts",
    "relevant_terms",
    "context_phrases",
    "related_adjectives",
    "common_metaphors",
    "academic_sub_fields",
    "title_context_labels",
)

LEGACY_THEME_KEYS = (
    "philosophers",
    "keywords",
    "typical_phrasing",
    "academic_subfields",
)

TITLE_LABEL_WORD_LIMIT = 5


def load_data(data_path: Path = DATA_PATH) -> dict:
    """Load and parse the repository data file."""
    return json.loads(data_path.read_text(encoding="utf-8"))


def _validate_list_field(theme_name: str, theme: dict, field_name: str, errors: list[str]) -> None:
    value = theme.get(field_name)
    if not isinstance(value, list) or not value:
        errors.append(f"{theme_name}: `{field_name}` must be a non-empty list.")
        return
    for index, item in enumerate(value):
        if not isinstance(item, str) or not item.strip():
            errors.append(f"{theme_name}: `{field_name}[{index}]` must be a non-empty string.")


def _validate_root_string_list(field_name: str, value: object, errors: list[str]) -> None:
    if not isinstance(value, list) or not value:
        errors.append(f"`{field_name}` must be a non-empty list.")
        return
    for index, item in enumerate(value):
        if not isinstance(item, str) or not item.strip():
            errors.append(f"`{field_name}[{index}]` must be a non-empty string.")


def _normalize_movement_key(label: str) -> str:
    """Normalize movement labels to detect near-synonym duplicate buckets."""
    normalized = re.sub(r"[^a-z0-9]+", " ", label.lower()).strip()
    normalized_words: list[str] = []
    for word in normalized.split():
        if word.endswith("ies") and len(word) > 4:
            word = f"{word[:-3]}y"
        elif word.endswith("s") and len(word) > 4 and not word.endswith("ss"):
            word = word[:-1]
        normalized_words.append(word)
    return " ".join(normalized_words)


def validate_data(data: dict) -> tuple[list[str], list[str]]:
    """Return validation errors and warnings for the JSON data."""
    errors: list[str] = []
    warnings: list[str] = []

    for root_key in REQUIRED_ROOT_KEYS:
        if root_key not in data:
            errors.append(f"Missing root key: `{root_key}`.")

    if errors:
        return errors, warnings

    philosophers = set(data["philosophers"])
    concepts = set(data["concepts"])
    hybrid_concept_terms = set(data["hybrid_concept_terms"])
    terms = set(data["terms"])
    _validate_root_string_list("philosophers", data["philosophers"], errors)
    _validate_root_string_list("concepts", data["concepts"], errors)
    _validate_root_string_list("hybrid_concept_terms", data["hybrid_concept_terms"], errors)
    _validate_root_string_list("terms", data["terms"], errors)
    _validate_root_string_list("academic_vocab", data["academic_vocab"], errors)
    philosopher_concepts = data["philosopher_concepts"]
    philosopher_key_works = data["philosopher_key_works"]
    quotes = data.get("quotes", {})
    thematic_clusters = data["thematic_clusters"]
    citation_relationships = data["citation_relationships"]
    philosophical_movements = data["philosophical_movements"]

    if not isinstance(thematic_clusters, dict) or not thematic_clusters:
        errors.append("`thematic_clusters` must be a non-empty object.")
        return errors, warnings

    if not isinstance(citation_relationships, dict) or not citation_relationships:
        errors.append("`citation_relationships` must be a non-empty object.")
        return errors, warnings

    if not isinstance(philosophical_movements, dict) or not philosophical_movements:
        errors.append("`philosophical_movements` must be a non-empty object.")
        return errors, warnings

    unexpected_overlap = sorted((concepts & terms) - hybrid_concept_terms)
    missing_hybrid_overlap = sorted(hybrid_concept_terms - (concepts & terms))
    if unexpected_overlap:
        errors.append(
            "`concepts` and `terms` may overlap only for explicitly curated hybrid items; "
            f"unexpected overlap: {', '.join(unexpected_overlap)}."
        )
    if missing_hybrid_overlap:
        errors.append(
            "`hybrid_concept_terms` must exist in both `concepts` and `terms`; "
            f"missing overlap entries: {', '.join(missing_hybrid_overlap)}."
        )

    philosophers_with_citation_coverage = set()
    for philosopher_name, related_philosophers in citation_relationships.items():
        if not isinstance(philosopher_name, str) or not philosopher_name.strip():
            errors.append("`citation_relationships` keys must be non-empty strings.")
            continue
        if philosopher_name not in philosophers:
            errors.append(
                f"`citation_relationships` contains non-canonical source philosopher `{philosopher_name}`."
            )
            continue
        if not isinstance(related_philosophers, list) or not related_philosophers:
            errors.append(
                f"`citation_relationships[{philosopher_name}]` must be a non-empty list."
            )
            continue

        philosophers_with_citation_coverage.add(philosopher_name)
        seen_targets = set()
        for index, related_name in enumerate(related_philosophers):
            if not isinstance(related_name, str) or not related_name.strip():
                errors.append(
                    f"`citation_relationships[{philosopher_name}][{index}]` must be a non-empty string."
                )
                continue
            if related_name not in philosophers:
                errors.append(
                    f"`citation_relationships[{philosopher_name}]` contains non-canonical target "
                    f"`{related_name}`."
                )
                continue
            if related_name == philosopher_name:
                errors.append(
                    f"`citation_relationships[{philosopher_name}]` must not contain self-references."
                )
                continue
            if related_name in seen_targets:
                errors.append(
                    f"`citation_relationships[{philosopher_name}]` contains duplicate target "
                    f"`{related_name}`."
                )
                continue

            seen_targets.add(related_name)
            philosophers_with_citation_coverage.add(related_name)

    normalized_movement_names: dict[str, str] = {}
    philosophers_with_movement = set()
    for movement_name, movement_members in philosophical_movements.items():
        if not isinstance(movement_name, str) or not movement_name.strip():
            errors.append("`philosophical_movements` keys must be non-empty strings.")
            continue

        if not isinstance(movement_members, list) or not movement_members:
            errors.append(f"`philosophical_movements[{movement_name}]` must be a non-empty list.")
            continue

        normalized_name = _normalize_movement_key(movement_name)
        existing_name = normalized_movement_names.get(normalized_name)
        if existing_name and existing_name != movement_name:
            errors.append(
                "Near-duplicate movement buckets detected: "
                f"`{existing_name}` and `{movement_name}`."
            )
        else:
            normalized_movement_names[normalized_name] = movement_name

        seen_members = set()
        for index, philosopher_name in enumerate(movement_members):
            if not isinstance(philosopher_name, str) or not philosopher_name.strip():
                errors.append(
                    f"`philosophical_movements[{movement_name}][{index}]` must be a non-empty string."
                )
                continue
            if philosopher_name not in philosophers:
                errors.append(
                    f"`philosophical_movements[{movement_name}]` contains non-canonical philosopher "
                    f"`{philosopher_name}`."
                )
                continue
            if philosopher_name in seen_members:
                errors.append(
                    f"`philosophical_movements[{movement_name}]` contains duplicate philosopher "
                    f"`{philosopher_name}`."
                )
                continue

            seen_members.add(philosopher_name)
            philosophers_with_movement.add(philosopher_name)

    for theme_name, theme in thematic_clusters.items():
        if not isinstance(theme, dict):
            errors.append(f"{theme_name}: theme entry must be an object.")
            continue

        for legacy_key in LEGACY_THEME_KEYS:
            if legacy_key in theme:
                errors.append(f"{theme_name}: legacy theme key `{legacy_key}` must not be present.")

        for required_key in REQUIRED_THEME_KEYS:
            if required_key not in theme:
                errors.append(f"{theme_name}: missing required key `{required_key}`.")

        if "description" in theme and (not isinstance(theme["description"], str) or not theme["description"].strip()):
            errors.append(f"{theme_name}: `description` must be a non-empty string.")

        for list_field in REQUIRED_THEME_KEYS[1:]:
            if list_field in theme:
                _validate_list_field(theme_name, theme, list_field, errors)

        theme_overlap = sorted(set(theme.get("key_concepts", [])) & set(theme.get("relevant_terms", [])))
        if theme_overlap:
            errors.append(
                f"{theme_name}: `key_concepts` and `relevant_terms` must be locally disjoint; "
                f"overlap found: {', '.join(theme_overlap)}."
            )

        title_context_labels = theme.get("title_context_labels", [])
        if isinstance(title_context_labels, list):
            if not 4 <= len(title_context_labels) <= 8:
                errors.append(
                    f"{theme_name}: `title_context_labels` must contain 4-8 labels; found {len(title_context_labels)}."
                )
            for label in title_context_labels:
                if isinstance(label, str) and len(label.split()) > TITLE_LABEL_WORD_LIMIT:
                    errors.append(
                        f"{theme_name}: title label `{label}` exceeds the {TITLE_LABEL_WORD_LIMIT}-word limit."
                    )

        for philosopher in theme.get("core_philosophers", []):
            if philosopher not in philosophers:
                errors.append(f"{theme_name}: core philosopher `{philosopher}` is missing from `philosophers`.")
            if philosopher not in philosopher_concepts:
                errors.append(
                    f"{theme_name}: core philosopher `{philosopher}` is missing from `philosopher_concepts`."
                )
            if philosopher not in philosopher_key_works or not philosopher_key_works.get(philosopher):
                errors.append(
                    f"{theme_name}: core philosopher `{philosopher}` is missing from `philosopher_key_works`."
                )
            if philosopher not in philosophers_with_movement:
                errors.append(
                    f"{theme_name}: core philosopher `{philosopher}` is missing from `philosophical_movements`."
                )
            if philosopher not in philosophers_with_citation_coverage:
                errors.append(
                    f"{theme_name}: core philosopher `{philosopher}` is missing from `citation_relationships` coverage."
                )
            if philosopher not in quotes or not quotes.get(philosopher):
                warnings.append(
                    f"{theme_name}: core philosopher `{philosopher}` has no supporting quote entries."
                )

        for concept in theme.get("key_concepts", []):
            if concept not in concepts:
                errors.append(f"{theme_name}: key concept `{concept}` is missing from `concepts`.")

        for term in theme.get("relevant_terms", []):
            if term not in terms:
                errors.append(f"{theme_name}: relevant term `{term}` is missing from `terms`.")

    return errors, warnings


def main() -> int:
    """CLI entry point."""
    data = load_data()
    errors, warnings = validate_data(data)

    if errors:
        print("Data validation failed:")
        for error in errors:
            print(f"- {error}")
    else:
        print("Data validation passed.")

    if warnings:
        print("\nWarnings:")
        for warning in warnings:
            print(f"- {warning}")

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
