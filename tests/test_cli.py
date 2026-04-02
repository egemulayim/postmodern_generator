import subprocess
import sys
import unittest
import os
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent


class CLITest(unittest.TestCase):
    def _run_interactive(self, user_input, timeout=90):
        return subprocess.run(
            [sys.executable, "main.py"],
            cwd=REPO_ROOT,
            input=user_input,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
            env={**os.environ, "TERM": "xterm"},
        )

    def test_help_describes_mode_rules_and_theme_listing(self):
        result = subprocess.run(
            [sys.executable, "main.py", "--help"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("--list-themes", result.stdout)
        self.assertIn("No arguments: interactive setup", result.stdout)
        self.assertIn("essays/", result.stdout)

    def test_list_themes_prints_available_themes_and_descriptions(self):
        result = subprocess.run(
            [sys.executable, "main.py", "--list-themes"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("Available themes:", result.stdout)
        self.assertIn("Digital Subjectivity", result.stdout)
        self.assertIn("Science and Technology Studies (STS)", result.stdout)

    def test_invalid_theme_suggests_list_themes(self):
        result = subprocess.run(
            [sys.executable, "main.py", "--theme", "Not A Real Theme"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )

        self.assertNotEqual(0, result.returncode)
        self.assertIn("Use --list-themes to see valid keys", result.stderr)

    def test_output_cannot_be_combined_with_no_export(self):
        result = subprocess.run(
            [sys.executable, "main.py", "--theme", "Digital Subjectivity", "--no-export", "--output", "essay.md"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )

        self.assertNotEqual(0, result.returncode)
        self.assertIn("--output cannot be used with --no-export", result.stderr)

    def test_zero_argument_run_uses_interactive_setup_and_can_skip_export(self):
        result = self._run_interactive("\n\n0\nn\n")

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("=== Postmodern Essay Generator ===", result.stdout)
        self.assertIn("Select metafiction level (1-3) [default: 2]:", result.stdout)
        self.assertIn("Select a theme number", result.stdout)
        self.assertIn("--- Generating Essay ---", result.stdout)
        self.assertIn("Do you want to export this essay as a Markdown (.md) file? [y/n]:", result.stdout)
        self.assertIn("Essay not exported.", result.stdout)

    def test_interactive_help_screen_returns_to_theme_selection(self):
        result = self._run_interactive("\n\nh\n\n0\nn\n")

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("Generate a postmodern essay. No arguments starts interactive setup", result.stdout)
        self.assertIn("--list-themes", result.stdout)
        self.assertGreaterEqual(result.stdout.count("Select a theme number"), 2)


if __name__ == "__main__":
    unittest.main()
