import unittest

from scripts.validate_data import _normalize_movement_key, load_data, validate_data


class DataValidationTest(unittest.TestCase):
    def setUp(self):
        self.data = load_data()
        self.errors, self.warnings = validate_data(self.data)

    def test_data_validation_has_no_errors(self):
        self.assertEqual([], self.errors, "\n".join(self.errors))

    def test_priority_themes_use_canonical_theme_schema(self):
        required_keys = {
            "description",
            "core_philosophers",
            "key_concepts",
            "relevant_terms",
            "context_phrases",
            "related_adjectives",
            "common_metaphors",
            "academic_sub_fields",
            "title_context_labels",
        }
        legacy_keys = {"philosophers", "keywords", "typical_phrasing", "academic_subfields"}
        thematic_clusters = self.data["thematic_clusters"]

        for theme_name in (
            "Digital Subjectivity",
            "Queer Theory",
            "Science and Technology Studies (STS)",
        ):
            theme = thematic_clusters[theme_name]
            self.assertTrue(required_keys.issubset(theme.keys()), theme_name)
            self.assertTrue(theme.keys().isdisjoint(legacy_keys), theme_name)
            self.assertGreaterEqual(len(theme["title_context_labels"]), 4, theme_name)
            self.assertLessEqual(len(theme["title_context_labels"]), 8, theme_name)

    def test_academic_vocab_is_a_flat_string_list(self):
        academic_vocab = self.data["academic_vocab"]
        self.assertIsInstance(academic_vocab, list)
        self.assertTrue(academic_vocab)
        for entry in academic_vocab:
            self.assertIsInstance(entry, str)
            self.assertTrue(entry.strip())

    def test_concept_term_overlap_is_explicitly_curated(self):
        concepts = set(self.data["concepts"])
        terms = set(self.data["terms"])
        hybrids = set(self.data["hybrid_concept_terms"])

        self.assertTrue(hybrids)
        self.assertEqual(hybrids, concepts & terms)

        for entry in self.data["hybrid_concept_terms"]:
            self.assertIsInstance(entry, str)
            self.assertTrue(entry.strip())

    def test_theme_concepts_and_terms_are_locally_disjoint(self):
        for theme_name, theme in self.data["thematic_clusters"].items():
            overlap = set(theme["key_concepts"]) & set(theme["relevant_terms"])
            self.assertEqual(set(), overlap, theme_name)

    def test_theme_core_philosophers_have_movement_coverage(self):
        covered = set()
        for members in self.data["philosophical_movements"].values():
            covered.update(members)

        for theme_name, theme in self.data["thematic_clusters"].items():
            for philosopher in theme["core_philosophers"]:
                self.assertIn(philosopher, covered, f"{theme_name}: {philosopher}")

    def test_movement_taxonomy_uses_canonical_names_and_unique_labels(self):
        philosophers = set(self.data["philosophers"])
        normalized_names = {}

        for movement_name, members in self.data["philosophical_movements"].items():
            self.assertIsInstance(movement_name, str)
            self.assertTrue(movement_name.strip())
            self.assertIsInstance(members, list)
            self.assertTrue(members, movement_name)

            normalized_name = _normalize_movement_key(movement_name)
            self.assertNotIn(normalized_name, normalized_names, movement_name)
            normalized_names[normalized_name] = movement_name

            self.assertEqual(len(members), len(set(members)), movement_name)
            for philosopher in members:
                self.assertIn(philosopher, philosophers, f"{movement_name}: {philosopher}")

    def test_theme_core_philosophers_have_citation_relationship_coverage(self):
        covered = set(self.data["citation_relationships"])
        for members in self.data["citation_relationships"].values():
            covered.update(members)

        for theme_name, theme in self.data["thematic_clusters"].items():
            for philosopher in theme["core_philosophers"]:
                self.assertIn(philosopher, covered, f"{theme_name}: {philosopher}")

    def test_citation_relationships_use_canonical_names_and_unique_targets(self):
        philosophers = set(self.data["philosophers"])

        for philosopher, related in self.data["citation_relationships"].items():
            self.assertIsInstance(philosopher, str)
            self.assertTrue(philosopher.strip())
            self.assertIn(philosopher, philosophers, philosopher)
            self.assertIsInstance(related, list)
            self.assertTrue(related, philosopher)
            self.assertEqual(len(related), len(set(related)), philosopher)

            for related_philosopher in related:
                self.assertIn(related_philosopher, philosophers, f"{philosopher}: {related_philosopher}")
                self.assertNotEqual(philosopher, related_philosopher, philosopher)


if __name__ == "__main__":
    unittest.main()
