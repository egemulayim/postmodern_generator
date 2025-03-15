# paragraph.py
import random
from sentence import generate_sentence
from data import philosophers, concepts, terms, philosopher_concepts

# Extended list of transitional words
transitional_words = [
    "Moreover", "However", "In addition", "Furthermore", "Consequently",
    "Therefore", "Nonetheless", "Conversely", "Similarly", "Specifically",
    "Additionally", "Nevertheless", "On the other hand", "In contrast",
    "Accordingly", "As a result", "Hence", "Thus", "For instance", "Namely",
    "Meanwhile", "Alternatively", "Subsequently", "Indeed", "Likewise", "Concomitantly", "Still"
]

def generate_paragraph(template_type, num_sentences, references, forbidden_philosophers=[], forbidden_concepts=[], forbidden_terms=[], mentioned_philosophers=set()):
    """
    Generate a paragraph by selecting sentences from a pool of generated sentences.

    Args:
        template_type (str): Type of paragraph ('introduction', 'general', or 'conclusion')
        num_sentences (int): Number of sentences desired in the paragraph
        references (list): List of references for citations
        forbidden_philosophers (list): Philosophers to exclude from generation
        forbidden_concepts (list): Concepts to exclude from generation
        forbidden_terms (list): Terms to exclude from generation
        mentioned_philosophers (set): Set of philosophers already mentioned in the text

    Returns:
        str: A fully formed paragraph as a string
    """
    # Generate a pool of sentences (1.5 times the required number for diversity)
    pool_size = int(num_sentences * 1.5)
    sentence_pool = []
    for _ in range(pool_size):
        sentence_parts, _ = generate_sentence(template_type, references, mentioned_philosophers, forbidden_philosophers, forbidden_concepts, forbidden_terms)
        sentence_text, _ = sentence_parts[0]  # Unpack the tuple to get the sentence string
        sentence_pool.append(sentence_text)

    # Select the required number of sentences from the pool
    selected_sentences = random.sample(sentence_pool, num_sentences)

    # Construct the paragraph with transitional words
    if len(selected_sentences) > 1:
        paragraph_sentences = [selected_sentences[0]]  # First sentence without a transition
        for i in range(1, len(selected_sentences)):
            transitional_word = random.choice(transitional_words)
            sentence = selected_sentences[i]
            if sentence:
                sentence = sentence[0].lower() + sentence[1:]  # Lowercase the first letter after transition
            paragraph_sentences.append(f"{transitional_word}, {sentence}")
        paragraph_str = ' '.join(paragraph_sentences).strip()
    else:
        paragraph_str = selected_sentences[0] if selected_sentences else "This paragraph could not be generated."

    # Add a reflection sentence with 20% probability (only for 'general' paragraphs)
    if random.random() < 0.2 and template_type == 'general':
        concept = random.choice([c for c in concepts if c not in forbidden_concepts])
        associated_philosophers = [p for p in philosophers if p in philosopher_concepts and concept in philosopher_concepts[p]]
        if associated_philosophers:
            philosopher = random.choice(associated_philosophers)
            philosopher_name = philosopher if philosopher not in mentioned_philosophers else philosopher.split()[-1]
            reflection = f"For further discussion on {concept}, see {philosopher_name}'s work."
            paragraph_str += ' ' + reflection

    return paragraph_str