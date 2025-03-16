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

def generate_paragraph(template_type, num_sentences, references, forbidden_philosophers=[], forbidden_concepts=[], forbidden_terms=[], mentioned_philosophers=set(), used_quotes=set(), all_references=None, cited_references=[]):
    """
    Generate a paragraph by selecting sentences from a pool of generated sentences.

    Args:
        template_type (str): Type of paragraph ('introduction', 'general', or 'conclusion')
        num_sentences (int): Number of sentences desired in the paragraph
        references (list): List of references for citations (not used directly)
        forbidden_philosophers (list): Philosophers to exclude from generation
        forbidden_concepts (list): Concepts to exclude from generation
        forbidden_terms (list): Terms to exclude from generation
        mentioned_philosophers (set): Set of philosophers already mentioned in the text
        used_quotes (set): Quotes already used in the essay
        all_references (list): List of all possible references for citation
        cited_references (list): List of references cited so far in the essay

    Returns:
        tuple: (paragraph_str, used_concepts_in_paragraph, used_terms_in_paragraph)
               - paragraph_str (str): The generated paragraph
               - used_concepts_in_paragraph (set): Concepts used in the paragraph
               - used_terms_in_paragraph (set): Terms used in the paragraph
    """
    # Convert forbidden lists to sets
    forbidden_philosophers_set = set(forbidden_philosophers)
    forbidden_concepts_set = set(forbidden_concepts)
    forbidden_terms_set = set(forbidden_terms)

    used_phils_in_paragraph = set()
    used_concs_in_paragraph = set()
    used_trms_in_paragraph = set()

    pool_size = int(num_sentences * 1.5)
    sentence_pool = []
    used_data = []
    for _ in range(pool_size):
        sentence_parts, used_phils, used_concs, used_trms = generate_sentence(
            template_type, references, mentioned_philosophers,
            forbidden_philosophers_set | used_phils_in_paragraph,
            forbidden_concepts_set | used_concs_in_paragraph,
            forbidden_terms_set | used_trms_in_paragraph,
            used_quotes, all_references, cited_references
        )
        sentence_text, _ = sentence_parts[0]
        sentence_pool.append(sentence_text)
        used_data.append((used_phils, used_concs, used_trms))
        used_phils_in_paragraph.update(used_phils)
        used_concs_in_paragraph.update(used_concs)
        used_trms_in_paragraph.update(used_trms)

    selected_indices = random.sample(range(len(sentence_pool)), min(num_sentences, len(sentence_pool)))
    selected_sentences = [sentence_pool[i] for i in selected_indices]

    used_concepts_in_paragraph = set()
    used_terms_in_paragraph = set()
    for idx in selected_indices:
        _, used_concs, used_trms = used_data[idx]
        used_concepts_in_paragraph.update(used_concs)
        used_terms_in_paragraph.update(used_trms)

    paragraph_sentences = []
    for i, sentence in enumerate(selected_sentences):
        if i > 0:
            transitional_word = random.choice(transitional_words)
            paragraph_sentences.append(f"{transitional_word}, {sentence}")
        else:
            paragraph_sentences.append(sentence)
    paragraph_str = '. '.join(paragraph_sentences).strip() + '.'

    if random.random() < 0.2 and template_type == 'general':
        concept = random.choice([c for c in concepts if c not in forbidden_concepts])
        associated_philosophers = [p for p in philosophers if p in philosopher_concepts and concept in philosopher_concepts[p]]
        if associated_philosophers:
            philosopher = random.choice(associated_philosophers)
            philosopher_name = philosopher if philosopher not in mentioned_philosophers else philosopher.split()[-1]
            reflection = f"For further discussion on {concept}, see {philosopher_name}'s work."
            paragraph_str += ' ' + reflection

    return paragraph_str, used_concepts_in_paragraph, used_terms_in_paragraph