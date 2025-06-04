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
        # thematic_clusters is available globally from json_data_provider import
        for i, theme_key in enumerate(available_themes):
            description = thematic_clusters.get(theme_key, {}).get('description', 'No description available.')
            print(f"\n{i+1}. Theme: {theme_key}")
            print(f"  Description: {description}")
    input("\nPress Enter to return to theme selection...")

def show_help_info():
    """Display CLI help information."""
    print("\n--- CLI Help ---")
    print("You can also use command-line arguments for faster generation:")
    print("  python main.py --help                     Show all available options")
    print("  python main.py --seed 42                  Use specific seed")
    print("  python main.py --theme \"Digital Subjectivity\"  Use specific theme")
    print("  python main.py --metafiction subtle       Set metafiction level")
    print("  python main.py --export                   Auto-export as Markdown")
    print("  python main.py --no-export               Skip export")
    print("  python main.py --seed 42 --theme \"Queer Theory\" --export")
    print("                                            Combine multiple options")
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
    print("Tip: Use 'python main.py --help' to see all command-line options for faster generation.")
    print()
    
    # Get initial seed
    user_seed = get_user_seed()
    
    # Get initial metafiction level
    user_metafiction_level = get_metafiction_level()
    
    # Theme selection with navigation options
    available_themes = list(thematic_clusters.keys())
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
        else:
            print(f"Warning: Theme '{current_theme_key}' not found. Available themes are: {available_themes}")
            chosen_theme_key = random.choice(available_themes)
            print(f"Falling back to random theme: {chosen_theme_key}")
            return chosen_theme_key, chosen_theme_key
    else:
        # For non-interactive usage, just pick random
        chosen_theme_key = random.choice(available_themes)
        print(f"No theme specified, randomly selected: {chosen_theme_key}")
        return chosen_theme_key, f"Randomly selected: {chosen_theme_key}"

def generate_with_seed_and_theme(seed=None, theme_key=None, export_option=None, metafiction_level='moderate'):
    """Generate an essay with an optional random seed and theme."""
    final_seed_used = None # Initialize here
    if seed is not None: # Specific seed provided by user or args
        random.seed(seed)
        print(f"Using random seed: {seed}")
        final_seed_used = seed # Assign user-provided seed
    else: # No seed provided, generate one
        current_seed = random.randint(1, 1000000)
        random.seed(current_seed)
        print(f"Using randomly generated seed for this run: {current_seed}")
        final_seed_used = current_seed # Ensure the randomly generated seed is captured

    available_themes = list(thematic_clusters.keys())
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
        export_to_markdown(essay_content, essay_config=essay_config)
    elif export_option == "no-export":
        print("Essay not exported (--no-export specified).")
    else:
        # Ask the user if they want to export the essay (interactive mode)
        while True:
            export_choice = input("Do you want to export this essay as a Markdown (.md) file? [y/n]: ").strip().lower()
            if export_choice.startswith('y'):
                export_to_markdown(essay_content, essay_config=essay_config)
                break
            elif export_choice.startswith('n'):
                print("Essay not exported.")
                break
            else:
                print("Invalid choice. Please enter 'y' or 'n'.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a postmodern essay.")
    parser.add_argument("--seed", type=int, help="An integer seed for random generation.")
    parser.add_argument("--theme", type=str, help="A specific theme key for the essay.")
    parser.add_argument("--metafiction", type=str, choices=['subtle', 'moderate', 'highly_self_aware'], 
                       default='moderate', 
                       help="Set the level of metafictional self-awareness (default: moderate).")
    
    # Add export control arguments (mutually exclusive)
    export_group = parser.add_mutually_exclusive_group()
    export_group.add_argument("--export", action="store_true", 
                            help="Automatically export the essay as a Markdown file after generation.")
    export_group.add_argument("--no-export", action="store_true", 
                            help="Skip export and don't prompt for export after generation.")
    
    args = parser.parse_args()

    user_seed = args.seed
    user_theme_key = args.theme
    user_metafiction_level = args.metafiction
    
    # Determine export option
    export_option = None
    if args.export:
        export_option = "export"
    elif args.no_export:
        export_option = "no-export"
    
    available_themes = list(thematic_clusters.keys())

    if args.theme and args.theme not in available_themes:
        print(f"Error: Theme key '{args.theme}' is not valid.")
        print(f"Available themes are: {available_themes}")
        sys.exit(1)

    # If no CLI arguments are provided for seed, theme, and default metafiction, use interactive setup
    if user_seed is None and user_theme_key is None and user_metafiction_level == 'moderate':
        user_seed, user_metafiction_level, user_theme_key = interactive_setup()

    generate_with_seed_and_theme(seed=user_seed, theme_key=user_theme_key, export_option=export_option, metafiction_level=user_metafiction_level)