import random
from sentence import generate_sentence
from data import philosophers, concepts, terms, philosopher_concepts

def generate_paragraph(template_type, num_sentences, references, forbidden_philosophers=[], forbidden_concepts=[], forbidden_terms=[]):
    """
    Generates a paragraph consisting of multiple sentences.
    
    Args:
        template_type (str): Type of sentence templates to use.
        num_sentences (int): Number of sentences in the paragraph.
        references (list): List of citation references.
        forbidden_philosophers (list): Philosophers to exclude.
        forbidden_concepts (list): Concepts to exclude.
        forbidden_terms (list): Terms to exclude.
    
    Returns:
        str: The generated paragraph.
    """
    paragraph_sentences = []
    used_philosophers = set(forbidden_philosophers)
    used_concepts = set(forbidden_concepts)
    used_terms = set(forbidden_terms)
    for i in range(num_sentences):
        # Always set is_first_sentence to True to capitalize each sentence's first word
        sentence_parts, used_items = generate_sentence(template_type, references, list(used_philosophers), list(used_concepts), list(used_terms), is_first_sentence=True)
        # Collect only the text parts
        text = ''
        for part in sentence_parts:
            text += part[0] + ' '
        paragraph_sentences.append(text.strip())
        used_philosophers.update([item for item in used_items if item in philosophers])
        used_concepts.update([item for item in used_items if item in concepts])
        used_terms.update([item for item in used_items if item in terms])
    
    # Join all sentences with spaces to form the paragraph, ensuring proper spacing
    paragraph_str = ' '.join(paragraph_sentences).strip()
    
    # Add reflection with 70% chance
    if random.random() < 0.7 and used_concepts:
        concept = random.choice(list(used_concepts))
        associated_philosophers = [p for p in philosophers if p in philosopher_concepts and concept in philosopher_concepts[p]]
        if associated_philosophers:
            philosopher = random.choice(associated_philosophers)
            reflection = f"For further discussion on {concept}, see {philosopher}'s work."
            paragraph_str += ' ' + reflection
    
    return paragraph_str