import random
from sentence import generate_sentence
from data import philosophers, concepts, terms, philosopher_concepts

def generate_paragraph(template_type, num_sentences, references, forbidden_philosophers=[], forbidden_concepts=[], forbidden_terms=[]):
    paragraph_parts = []
    used_philosophers = set(forbidden_philosophers)
    used_concepts = set(forbidden_concepts)
    used_terms = set(forbidden_terms)
    for i in range(num_sentences):
        is_last_sentence = (i == num_sentences - 1)
        sentence_parts, used_items = generate_sentence(template_type, references, list(used_philosophers), list(used_concepts), list(used_terms), is_first_sentence=(i == 0))
        # Concatenate all text parts of this sentence with proper spacing
        sentence_text = ''
        for part in sentence_parts:
            text, citation = part
            if sentence_text:
                sentence_text += " " + text.strip()  # Add space before new part if not first
            else:
                sentence_text = text.strip()  # Start with the first part, stripped
        if not is_last_sentence:
            # Ensure there's a space after this sentence if it's not the last one
            if not sentence_text.endswith((' ', '.', '!', '?')):
                sentence_text += " "
        paragraph_parts.append((sentence_text, None))  # Add as a single part for the sentence
        used_philosophers.update([item for item in used_items if item in philosophers])
        used_concepts.update([item for item in used_items if item in concepts])
        used_terms.update([item for item in used_items if item in terms])
    # Add reflection with 70% chance
    if random.random() < 0.7 and used_concepts:
        concept = random.choice(list(used_concepts))
        associated_philosophers = [p for p in philosophers if p in philosopher_concepts and concept in philosopher_concepts[p][0]]
        if associated_philosophers:
            philosopher = random.choice(associated_philosophers)
            reflection = f"For further discussion on {concept}, see {philosopher}'s work."
            if paragraph_parts and not paragraph_parts[-1][0].endswith((' ', '.', '!', '?')):
                paragraph_parts.append((reflection + " ", None))  # Add space if needed
            else:
                paragraph_parts.append((reflection, None))
    return paragraph_parts