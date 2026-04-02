"""
Main entry point for the postmodern essay generator.
This script generates a postmodern essay with optional random seed and theme selection.
It uses the `essay` module to create the essay content and includes
academic citation conventions.
"""

from essay import generate_essay
from json_data_provider import thematic_clusters # Import thematic_clusters to list available themes
from md_export import export_to_markdown # Import the new export function
import sys
import random # Ensure random is imported for seed setting and potential random theme choice
import datetime # For timestamping the export
import argparse # Import argparse
import os # Add os import for clearing screen
import re
from textwrap import dedent


def get_available_themes():
    """Return the canonical CLI ordering for theme keys."""
    return sorted(thematic_clusters.keys(), key=str.casefold)


def format_theme_listing(available_themes=None, include_descriptions=False, numbered=False):
    """Format available themes for CLI or interactive display."""
    themes = available_themes or get_available_themes()
    lines = []
    for index, theme_key in enumerate(themes, start=1):
        prefix = f"{index}. " if numbered else "- "
        lines.append(f"{prefix}{theme_key}")
        if include_descriptions:
            description = thematic_clusters.get(theme_key, {}).get('description', 'No description available.')
            lines.append(f"   {description}")
    return "\n".join(lines)


def build_parser():
    """Build the canonical CLI parser for the essay generator."""
    description = (
        "Generate a postmodern essay. No arguments starts interactive setup; "
        "any CLI argument runs non-interactively."
    )
    epilog = dedent(
        """\
        Mode rules:
          No arguments: interactive setup
          Any CLI argument: non-interactive run

        Theme discovery:
          python main.py --list-themes

        Export behavior:
          --export writes to essays/
          --output <filename> implies --export and writes inside essays/
          --no-export skips export entirely

        Examples:
          python main.py --help
          python main.py --list-themes
          python main.py --seed 42 --theme "Digital Subjectivity"
          python main.py --theme "Queer Theory" --export
          python main.py --theme "Digital Subjectivity" --export --output digital-subjectivity.md
          python main.py --seed 314 --theme "Power and Knowledge" --metafiction subtle --no-export
        """
    )
    parser = argparse.ArgumentParser(
        description=description,
        epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--seed", type=int, help="An integer seed for reproducible generation.")
    parser.add_argument(
        "--theme",
        type=str,
        help="A specific theme key for the essay. Use --list-themes to inspect valid keys.",
    )
    parser.add_argument(
        "--list-themes",
        action="store_true",
        help="Print available themes with descriptions and exit.",
    )
    parser.add_argument(
        "--metafiction",
        type=str,
        choices=['subtle', 'moderate', 'highly_self_aware'],
        default='moderate',
        help="Set the level of metafictional self-awareness (default: moderate).",
    )

    export_group = parser.add_mutually_exclusive_group()
    export_group.add_argument(
        "--export",
        action="store_true",
        help="Export the essay as Markdown to essays/ after generation.",
    )
    export_group.add_argument(
        "--no-export",
        action="store_true",
        help="Skip export and do not prompt for export after generation.",
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Filename only for Markdown export inside essays/. Implies --export.",
    )
    return parser


def validate_output_filename_argument(parser, output_filename):
    """Validate the --output CLI argument and keep its contract filename-only."""
    if output_filename is None:
        return None

    candidate = output_filename.strip()
    if not candidate:
        parser.error("--output requires a non-empty filename.")

    if os.path.basename(candidate) != candidate:
        parser.error("--output expects a filename only; files are always written inside essays/.")

    return candidate

def get_user_seed():
    """Prompt the user to enter a seed or choose random generation."""
    while True:
        seed_input = input("Enter a number for a specific seed value or press Enter to generate from a random seed: ")
        if not seed_input:  
            return None  
        try:
            seed_value = int(seed_input)
            return seed_value
        except ValueError:
            print("Invalid input. Seed must be a number or empty for random generation.")

def show_theme_info(available_themes):
    """Displays detailed information about each available theme."""
    os.system('cls' if os.name == 'nt' else 'clear')
    print("--- Theme Information ---")
    if not available_themes:
        print("No themes available to display information for.")
    else:
        print(format_theme_listing(available_themes, include_descriptions=True, numbered=True))
    input("\nPress Enter to return to theme selection...")

def show_help_info():
    """Display CLI help information using the canonical parser output."""
    print()
    build_parser().print_help()
    input("\nPress Enter to continue...")

def get_metafiction_level():
    """Prompt the user to select metafiction level."""
    metafiction_options = {
        1: 'subtle',
        2: 'moderate', 
        3: 'highly_self_aware'
    }
    
    descriptions = {
        'subtle': 'Minimal, strategic placement (~8% of paragraphs)',
        'moderate': 'Balanced self-reflexivity (~15% of paragraphs)', 
        'highly_self_aware': 'Frequent, experimental placement (~25% of paragraphs)'
    }
    
    while True:
        print("\nMetafiction Level Options:")
        print("  1. Subtle - " + descriptions['subtle'])
        print("  2. Moderate - " + descriptions['moderate'])
        print("  3. Highly Self-Aware - " + descriptions['highly_self_aware'])
        
        choice = input("Select metafiction level (1-3) [default: 2]: ").strip()
        
        if not choice:  # Default to moderate
            return 'moderate'
        
        try:
            choice_num = int(choice)
            if choice_num in metafiction_options:
                selected_level = metafiction_options[choice_num]
                print(f"Selected metafiction level: {selected_level}")
                return selected_level
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
        except ValueError:
            print("Invalid input. Please enter a number 1-3 or press Enter for default.")

def interactive_setup():
    """Handle the complete interactive setup flow with navigation options."""
    print("=== Postmodern Essay Generator ===")
    print("Tip: Use 'python main.py --help' or 'python main.py --list-themes' for the non-interactive interface.")
    print()
    
    # Get initial seed
    user_seed = get_user_seed()
    
    # Get initial metafiction level
    user_metafiction_level = get_metafiction_level()
    
    # Theme selection with navigation options
    available_themes = get_available_themes()
    result = _select_theme_with_navigation(
        available_themes, None, user_seed, user_metafiction_level
    )
    
    # Handle the return values properly
    if len(result) == 4:
        chosen_theme_key, theme_selection_prompt, final_seed, final_metafiction = result
    else:
        chosen_theme_key, theme_selection_prompt = result
        final_seed = user_seed
        final_metafiction = user_metafiction_level
    
    return final_seed, final_metafiction, chosen_theme_key

def _select_theme_with_navigation(available_themes, current_theme_key=None, current_seed=None, current_metafiction='moderate'):
    """Enhanced theme selection with navigation options to change seed and metafiction level."""
    chosen_theme_key = None
    theme_selection_prompt = None

    if current_theme_key:
        if current_theme_key in available_themes:
            chosen_theme_key = current_theme_key
            print(f"Using chosen theme: {chosen_theme_key}")
            theme_selection_prompt = chosen_theme_key
            return chosen_theme_key, theme_selection_prompt
        else:
            print(f"Warning: Theme '{current_theme_key}' not found. Available themes are: {available_themes}")
            chosen_theme_key = random.choice(available_themes)
            print(f"Falling back to random theme: {chosen_theme_key}")
            theme_selection_prompt = chosen_theme_key
            return chosen_theme_key, theme_selection_prompt
    else:
        # Interactive selection loop with navigation
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            
            # Display current settings
            seed_display = current_seed if current_seed is not None else "Random"
            print(f"Current Settings: Seed = {seed_display}, Metafiction = {current_metafiction}")
            print()
            
            print("Available themes:")
            print("  0. Random Theme")
            for i, th_key in enumerate(available_themes):
                print(f"  {i+1}. {th_key}")
            print()
            print("Navigation Options:")
            print("  s. Change seed")
            print("  m. Change metafiction level")
            print("  i. Theme information")
            print("  h. CLI help")

            max_theme_option = len(available_themes)
            choice = input(f"Select a theme number (0-{max_theme_option}), or option (s/m/i/h): ").strip().lower()

            if choice == 's':
                # Go back to seed selection
                print("\n--- Seed Selection ---")
                new_seed = get_user_seed()
                current_seed = new_seed
                continue
            elif choice == 'm':
                # Go back to metafiction selection
                print("\n--- Metafiction Level Selection ---")
                new_metafiction = get_metafiction_level()
                current_metafiction = new_metafiction
                continue
            elif choice == 'i':
                show_theme_info(available_themes)
                continue
            elif choice == 'h':
                show_help_info()
                continue

            try:
                choice_num = int(choice)
                if choice_num == 0:
                    chosen_theme_key = random.choice(available_themes)
                    print(f"Randomly selected theme: {chosen_theme_key}")
                    theme_selection_prompt = f"Randomly selected: {chosen_theme_key}"
                    break
                elif 1 <= choice_num <= max_theme_option:
                    chosen_theme_key = available_themes[choice_num-1]
                    theme_selection_prompt = chosen_theme_key
                    break
                else:
                    print("Invalid choice. Please try again.")
                    input("Press Enter to continue...")
            except ValueError:
                print("Invalid input. Please enter a number, 's', 'm', 'i', or 'h'.")
                input("Press Enter to continue...")
    
    # Return theme and updated settings
    return chosen_theme_key, theme_selection_prompt, current_seed, current_metafiction

def _select_theme_simple(available_themes, current_theme_key=None):
    """Simplified theme selection wrapper for generate_with_seed_and_theme."""
    if current_theme_key:
        if current_theme_key in available_themes:
            print(f"Using chosen theme: {current_theme_key}")
            return current_theme_key, current_theme_key
        raise ValueError(f"Theme key '{current_theme_key}' is not valid.")
    else:
        # For non-interactive usage, just pick random
        chosen_theme_key = random.choice(available_themes)
        print(f"No theme specified; randomly selected: {chosen_theme_key}")
        return chosen_theme_key, f"Randomly selected: {chosen_theme_key}"

def slugify_filename_part(value):
    """Convert a label into a filesystem-safe filename fragment."""
    normalized = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return normalized or "untitled"

def build_output_filename(theme_key, seed, generation_time):
    """Build a deterministic non-interactive export filename."""
    theme_part = slugify_filename_part(theme_key or "random-theme")
    timestamp = generation_time.strftime("%Y%m%d-%H%M%S")
    return f"{theme_part}-seed-{seed}-{timestamp}.md"

def generate_with_seed_and_theme(seed=None, theme_key=None, export_option=None, metafiction_level='moderate', output_filename=None, interactive=False):
    """Generate an essay with an optional random seed and theme."""
    final_seed_used = None # Initialize here
    if seed is not None: # Specific seed provided by user or args
        random.seed(seed)
        print(f"Using provided seed: {seed}")
        final_seed_used = seed # Assign user-provided seed
    else: # No seed provided, generate one
        current_seed = random.randint(1, 1000000)
        random.seed(current_seed)
        print(f"Using generated seed: {current_seed}")
        final_seed_used = current_seed # Ensure the randomly generated seed is captured

    available_themes = get_available_themes()
    chosen_theme_key, theme_selection_prompt = _select_theme_simple(available_themes, theme_key)

    generation_time = datetime.datetime.now()

    essay_config = {
        "seed_used": final_seed_used, # Now correctly includes random seed value
        "theme_selected": theme_selection_prompt, # Now correctly formatted for export
        "generation_date": generation_time.strftime("%Y-%m-%d %H:%M:%S"),
        "metafiction_level": metafiction_level
    }

    print(f"\n--- Generating Essay ---")
    print(f"Active theme set to: {chosen_theme_key}, Seed: {final_seed_used}")
    essay_content = generate_essay(theme_key=chosen_theme_key, metafiction_level=metafiction_level)
    print(essay_content)

    # Handle export based on CLI option or prompt user
    if export_option == "export":
        filename = output_filename or build_output_filename(chosen_theme_key, final_seed_used, generation_time)
        export_to_markdown(
            essay_content,
            filename=filename,
            essay_config=essay_config,
            interactive=False
        )
    elif export_option == "no-export":
        print("Essay not exported (--no-export specified).")
    else:
        if not interactive:
            print("Essay not exported (non-interactive CLI run without --export).")
            return
        # Ask the user if they want to export the essay (interactive mode)
        while True:
            export_choice = input("Do you want to export this essay as a Markdown (.md) file? [y/n]: ").strip().lower()
            if export_choice.startswith('y'):
                export_to_markdown(essay_content, essay_config=essay_config, interactive=True)
                break
            elif export_choice.startswith('n'):
                print("Essay not exported.")
                break
            else:
                print("Invalid choice. Please enter 'y' or 'n'.")

def main(argv=None):
    """CLI entry point."""
    parser = build_parser()
    args = parser.parse_args(argv)
    cli_args_provided = len(argv) > 0 if argv is not None else len(sys.argv) > 1

    if args.list_themes:
        print("Available themes:\n")
        print(format_theme_listing(include_descriptions=True, numbered=True))
        return 0

    user_seed = args.seed
    user_theme_key = args.theme
    user_metafiction_level = args.metafiction
    output_filename = validate_output_filename_argument(parser, args.output)

    if args.no_export and output_filename:
        parser.error("--output cannot be used with --no-export.")
    
    # Determine export option
    export_option = None
    if output_filename:
        export_option = "export"
    elif args.export:
        export_option = "export"
    elif args.no_export:
        export_option = "no-export"
    
    available_themes = get_available_themes()

    if args.theme and args.theme not in available_themes:
        parser.error(
            f"Theme key '{args.theme}' is not valid. "
            f"Use --list-themes to see valid keys."
        )

    # Only fall back to interactive setup when the program is launched with no CLI arguments at all.
    if not cli_args_provided:
        user_seed, user_metafiction_level, user_theme_key = interactive_setup()

    generate_with_seed_and_theme(
        seed=user_seed,
        theme_key=user_theme_key,
        export_option=export_option,
        metafiction_level=user_metafiction_level,
        output_filename=output_filename,
        interactive=not cli_args_provided
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
