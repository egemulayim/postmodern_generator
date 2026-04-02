import random
import unittest

from notes import NoteSystem


class NoteSystemTest(unittest.TestCase):
    def test_known_philosopher_uses_curated_key_work_titles(self):
        random.seed(7)
        note_system = NoteSystem()

        reference = note_system.get_enhanced_citation(
            "Wendy Hui Kyong Chun",
            is_article=False,
            year=2000,
        )

        title = note_system._extract_title_sorting_key(reference)
        self.assertIn(
            title,
            {"updating to remain the same"},
            reference,
        )

    def test_existing_reference_is_reused_for_matching_author_and_title(self):
        note_system = NoteSystem()
        existing_reference = (
            "Chun, Wendy Hui Kyong. *Updating To Remain The Same*. "
            "Duke University Press, 2016."
        )
        note_system._ensure_work_in_bibliography(existing_reference)

        reference = note_system.get_enhanced_citation(
            "Wendy Hui Kyong Chun",
            is_article=False,
            year=2000,
            title_override="Updating to Remain the Same",
        )

        self.assertEqual(existing_reference, reference)


if __name__ == "__main__":
    unittest.main()
