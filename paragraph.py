import random
from collections import Counter
from sentence import generate_sentence
from data import philosophers, concepts, terms, philosopher_concepts

# Extended list of transitional words
transitional_words = [
    "moreover", "however", "in addition", "furthermore", "consequently",
    "therefore", "nonetheless", "conversely", "similarly", "specifically",
    "additionally", "nevertheless", "on the other hand", "in contrast",
    "accordingly", "as a result", "hence", "thus", "for instance", "namely",
    "meanwhile", "alternatively", "subsequently", "indeed", "likewise", 
    "concomitantly", "still", "yet", "equally", "otherwise", "after all",
    "in other words", "as a matter of fact", "to that end", "in case as such"
]

def generate_paragraph(template_type, num_sentences, references, forbidden_philosophers=[], forbidden_concepts=[], forbidden_terms=[], mentioned_philosophers=set(), used_quotes=set(), all_references=None, cited_references=[]):
    """
    Generate a paragraph by selecting sentences from a pool, ensuring a central theme for coherence.

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

    # Find the most common concept or term for thematic focus
    all_concs = [c for _, concs, _ in used_data for c in concs]
    all_trms = [t for _, _, trms in used_data for t in trms]
    concept_counter = Counter(all_concs)
    term_counter = Counter(all_trms)
    most_common_concept = concept_counter.most_common(1)[0][0] if concept_counter else None
    most_common_term = term_counter.most_common(1)[0][0] if term_counter else None
    central_theme = most_common_concept or most_common_term

    # Select sentences with the central theme
    if central_theme:
        themed_sentences = [i for i, (_, concs, trms) in enumerate(used_data) if central_theme in concs or central_theme in trms]
        other_sentences = [i for i in range(len(sentence_pool)) if i not in themed_sentences]
        num_themed = max(1, num_sentences // 2)  # At least half should relate to the theme
        if len(themed_sentences) >= num_themed:
            selected_indices = random.sample(themed_sentences, num_themed)
            remaining = num_sentences - num_themed
            if remaining > 0:
                additional = random.sample(other_sentences, min(remaining, len(other_sentences)))
                selected_indices.extend(additional)
        else:
            selected_indices = themed_sentences[:]
            remaining = num_sentences - len(selected_indices)
            if remaining > 0:
                additional = random.sample(other_sentences, min(remaining, len(other_sentences)))
                selected_indices.extend(additional)
    else:
        selected_indices = random.sample(range(len(sentence_pool)), num_sentences)

    # Ensure exact number of sentences
    if len(selected_indices) < num_sentences:
        remaining_indices = [i for i in range(len(sentence_pool)) if i not in selected_indices]
        additional = random.sample(remaining_indices, min(num_sentences - len(selected_indices), len(remaining_indices)))
        selected_indices.extend(additional)

    selected_sentences = [sentence_pool[i] for i in selected_indices]

    used_concepts_in_paragraph = set()
    used_terms_in_paragraph = set()
    for idx in selected_indices:
        _, used_concs, used_trms = used_data[idx]
        used_concepts_in_paragraph.update(used_concs)
        used_terms_in_paragraph.update(used_trms)

    paragraph_sentences = []
    for i, sentence in enumerate(selected_sentences):
        # Ensure sentence ends with a period
        if not sentence.endswith('.'):
            sentence += '.'
        if i == 0:
            # Capitalize the first sentence
            if sentence:
                sentence = sentence[0].upper() + sentence[1:]
            paragraph_sentences.append(sentence)
        else:
            transitional_word = random.choice(transitional_words).capitalize()
            # Decapitalize the first word of the sentence after the transitional word, unless it's a proper noun
            words = sentence.split()
            if words and words[0].lower() not in terms and words[0].lower() not in concepts and words[0].lower() not in philosophers:
                sentence = words[0].lower() + ' ' + ' '.join(words[1:]) if len(words) > 1 else words[0].lower()
            paragraph_sentences.append(f"{transitional_word}, {sentence}")

    paragraph_str = ' '.join(paragraph_sentences)

    # Add reflection only for 'general' paragraphs with 20% chance
    if random.random() < 0.2 and template_type == 'general':
        concept = random.choice([c for c in concepts if c not in forbidden_concepts])
        associated_philosophers = [p for p in philosophers if p in philosopher_concepts and concept in philosopher_concepts[p]]
        if associated_philosophers:
            philosopher = random.choice(associated_philosophers)
            philosopher_name = philosopher if philosopher not in mentioned_philosophers else philosopher.split()[-1]
            reflection = f"for further discussion on {concept}, see {philosopher_name}'s work."
            # Capitalize reflection as a new sentence
            reflection = reflection[0].upper() + reflection[1:]
            paragraph_str += ' ' + reflection

    return paragraph_str, used_concepts_in_paragraph, used_terms_in_paragraph