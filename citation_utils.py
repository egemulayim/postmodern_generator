# citation_utils.py

notes = []  # List to store all citation notes
note_counter = 1  # Counter for numbering citations

def get_citation_note(reference):
    """
    Generates a citation note for the given reference and returns the note marker.
    
    Args:
        reference (str): The reference to be cited.
    
    Returns:
        str: The citation marker (e.g., "(1)").
    """
    global note_counter
    # Create a note like "1. Author, Title"
    note = f"{note_counter}. {reference}"
    notes.append(note)
    note_number = note_counter
    note_counter += 1
    return f"({note_number})"  # Returns something like "(1)"