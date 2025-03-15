import random
from sentence import generate_sentence
from data import philosophers, concepts, terms, philosopher_concepts

def generate_paragraph(template_type, num_sentences, references, forbidden_philosophers=[], forbidden_concepts=[], forbidden_terms=[]):
    paragraph_parts = []
    used_philosophers = set(forbidden_philosophers)
    used_concepts = set(forbidden_concepts)
    used_terms = set(forbidden_terms)
    for i in range(num_sentences):
        is_first = (i == 0)
        sentence_parts, used_items = generate_sentence(template_type, references, list(used_philosophers), list(used_concepts), list(used_terms), is_first_sentence=is_first)
        paragraph_parts.extend(sentence_parts)
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
            paragraph_parts.append((f"For further discussion, see [reflection].", reflection))
    return paragraph_parts