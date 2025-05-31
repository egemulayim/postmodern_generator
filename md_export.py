"""
A module for exporting the generated essay to a .md file.
This module exports the generated essay to a .md file in the 'essays' directory.
It also includes essay generation configuration at the top of the file.
"""

import os

def export_to_markdown(essay_content, filename=None, essay_config=None):
    """Exports the given essay content to a .md file in the 'essays' directory.

    The 'essays' directory will be created if it doesn't exist.
    Includes essay generation configuration at the top of the file.

    Args:
        essay_content (str): The content of the essay to export.
        filename (str, optional): The desired filename. If None, prompts the user.
        essay_config (dict, optional): Dictionary containing generation config (seed, theme, date).
    """
    while True:
        if not filename:
            fn_input = input("Enter the filename for the .md file (e.g., my_essay.md), or leave blank to skip: ").strip()
            if not fn_input: # User skipped
                print("Markdown export skipped.")
                return False # Indicate skipped
            filename = fn_input

        # Ensure the 'essays' directory exists
        output_dir = "essays"
        if not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir)
                print(f"Created directory: {output_dir}")
            except OSError as e:
                print(f"Error creating directory {output_dir}: {e}")
                # Allow user to skip if directory creation fails
                skip_choice = input("Failed to create output directory. Skip export? (yes/no): ").strip().lower()
                if skip_choice in ["yes", "y"]:
                    print("Markdown export skipped.")
                    return False
                else:
                    print("Cannot proceed without output directory. Export aborted.")
                    return False
        
        # Prepend directory to filename
        filepath = os.path.join(output_dir, filename)

        if not filepath.endswith(".md"):
            filepath += ".md"
            print(f"Filename amended to: {filepath}")
        
        try:
            # Prepare config header
            config_header = ""
            if essay_config:
                config_header += f"---\n"
                config_header += f"Seed: {essay_config.get('seed_used', 'N/A')}\n"
                config_header += f"Theme: {essay_config.get('theme_selected', 'N/A')}\n"
                config_header += f"Generated: {essay_config.get('generation_date', 'N/A')}\n"
                config_header += f"---\n\n"
            
            full_content_to_write = config_header + essay_content

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(full_content_to_write)
            print(f"Essay successfully exported to {filepath}")
            return True # Indicate success
        except IOError as e:
            print(f"Error exporting essay to {filepath}: {e}")
            # Allow user to retry with a different filename or skip
            retry_choice = input("Would you like to try a different filename or skip exporting? (retry/skip): ").strip().lower()
            if retry_choice == "skip":
                print("Markdown export skipped.")
                return False # Indicate skipped
            elif retry_choice == "retry":
                filename = None # Reset filename to prompt again
                continue # Loop back to ask for filename
            else:
                print("Invalid choice. Skipping export.")
                return False # Default to skip on invalid choice
        break # Should only be reached on successful write or if user chose to skip from error 