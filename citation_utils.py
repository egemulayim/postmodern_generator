notes = []
note_counter = 1

def get_citation_note(reference):
    global note_counter
    note = f"{note_counter}. {reference}"
    notes.append(note)
    note_number = note_counter
    note_counter += 1
    return f"[{note_number}]"  # Changed from f"({note_number})" to f"[{note_number}]"