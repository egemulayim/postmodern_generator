import random
from citation_utils import get_citation_note
from data import philosophers, concepts, terms, philosopher_concepts, contexts

# Expanded introduction templates for variety and sophistication
introduction_templates = [
    "This paper explores the intricate relationship between {term} and {concept} within the discursive field of {context}.",
    "In recent scholarly endeavors, {term} has emerged as a focal point, particularly within the ambit of {context}.",
    "This study seeks to interrogate the modalities through which {concept} shapes {term} in {context}.",
    "The ensuing analysis situates {concept} within the broader epistemic terrain of {term} in {context}.",
    "It merits consideration that {concept} has assumed a pivotal role in elucidating {term} within {context}.",
    "Contemporary discourse increasingly gravitates toward {term}, especially when viewed through {context}.",
    "The confluence of {concept} and {term} yields novel insights into the fabric of {context}.",
    "By refracting {concept} through the prism of {term}, this paper enriches the discourse of {context}.",
    "To apprehend {term} fully, one must adopt a nuanced engagement with {concept} in {context}.",
    "This inquiry probes {concept}'s constitutive role in the reconfiguration of {term} within {context}."
]

# Expanded general templates with postmodern-inspired complexity
general_templates = [
    "{philosopher} posits that {concept} serves as a linchpin in reimagining {term}.",
    "For {philosopher}, {concept} destabilizes the sedimented meanings of {term}.",
    "Within the ambit of {term}, {concept} emerges as a site of epistemic rupture. [citation]",
    "{concept}, as {philosopher} delineates, reorients our engagement with {term}.",
    "{philosopher1} and {philosopher2} proffer divergent readings of {concept} vis-à-vis {term}.",
    "Certain critics aver that {philosopher}'s {concept} elides critical dimensions of {term}. [citation]",
    "Can {concept}, as {philosopher} contends, fully encapsulate the complexities of {term}?",
    "In {philosopher}'s corpus, {concept} casts a revelatory light upon {term}.",
    "{term} functions as the ground against which {philosopher} articulates {concept}.",
    "Through the lens of {concept}, {philosopher} interrogates the foundational axioms of {term}. [citation]",
    "{philosopher} embeds {concept} within the expansive discourse of {term}.",
    "The dialectical interplay of {concept} and {term} recurs throughout {philosopher}'s oeuvre.",
    "This analysis probes the différance inherent in {concept}, per {philosopher}, relative to {term}.",
    "In {philosopher}'s schema, {concept} constitutes a contested terrain for {term}.",
    "The trace of {concept} within {philosopher}'s texts unveils its imbrication with {term}."
]

# Expanded conclusion templates for cohesion and variety
conclusion_templates = [
    "In summation, this inquiry has elucidated the indelible role of {concept} in apprehending {term}.",
    "These findings bear profound implications for {context}, particularly through the prism of {concept}.",
    "To conclude, this analysis underscores the salience of {term} vis-à-vis {concept}.",
    "This study has demonstrated that {concept} fundamentally reconfigures our approach to {term} in {context}.",
    "Future scholarship might fruitfully explore {concept}'s ramifications for {term} within {context}.",
    "The symbiosis of {concept} and {term} proves essential to grasping {context}, as evidenced herein.",
    "By traversing {term} through {concept}, this paper augments our understanding of {context}.",
    "The results intimate that {concept} is a decisive vector in the constitution of {term} within {context}.",
    "This examination reveals {term}'s profound entanglement with {concept}, upending orthodoxies in {context}.",
    "Ultimately, these insights affirm that {concept} is indispensable to any rigorous study of {term} in {context}."
]

def capitalize_first_word(sentence):
    """Capitalizes the first letter of the first word in a sentence."""
    if not sentence:
        return sentence
    words = sentence.split()
    if words:
        words[0] = words[0].capitalize()
    return ' '.join(words)

def generate_sentence(template_type, references, forbidden_philosophers=[], forbidden_concepts=[], forbidden_terms=[]):
    """
    Generates a sentence based on the specified template type.

    Args:
        template_type (str): Type of sentence ("introduction", "general", "conclusion").
        references (list): List of citation references.
        forbidden_philosophers (list): Philosophers to exclude.
        forbidden_concepts (list): Concepts to exclude.
        forbidden_terms (list): Terms to exclude.

    Returns:
        tuple: (sentence_parts, used_items) where sentence_parts is a list of (text, citation) pairs,
               and used_items is a list of terms/concepts/philosophers used.
    """
    if template_type == "introduction":
        template = random.choice(introduction_templates)
        term = random.choice([t for t in terms if t not in forbidden_terms])
        concept = random.choice([c for c in concepts if c not in forbidden_concepts])
        context = random.choice(contexts)
        sentence = template.format(term=term, concept=concept, context=context)
    elif template_type == "conclusion":
        template = random.choice(conclusion_templates)
        term = random.choice([t for t in terms if t not in forbidden_terms])
        concept = random.choice([c for c in concepts if c not in forbidden_concepts])
        context = random.choice(contexts)
        sentence = template.format(term=term, concept=concept, context=context)
    else:  # general
        template = random.choice(general_templates)
        philosopher = random.choice([p for p in philosophers if p not in forbidden_philosophers])
        if philosopher in philosopher_concepts:
            related_concepts = [c for c in philosopher_concepts[philosopher] if c not in forbidden_concepts]
            concept = random.choice(related_concepts) if related_concepts else random.choice([c for c in concepts if c not in forbidden_concepts])
        else:
            concept = random.choice([c for c in concepts if c not in forbidden_concepts])
        term = random.choice([t for t in terms if t not in forbidden_terms])
        data = {
            'philosopher': philosopher,
            'concept': concept,
            'term': term,
            'philosopher1': philosopher,
            'philosopher2': random.choice([p for p in philosophers if p != philosopher and p not in forbidden_philosophers])
        }
        sentence = template.format(**data)

    # Handle citations
    if '[citation]' in sentence:
        reference = random.choice(references)
        citation_note = get_citation_note(reference)
        sentence = sentence.replace('[citation]', citation_note)

    # Ensure proper capitalization
    sentence = capitalize_first_word(sentence)

    # Normalize spacing
    sentence = ' '.join(sentence.split())

    return [(sentence, None)], [term, concept] if template_type in ['introduction', 'conclusion'] else [philosopher, concept, term]