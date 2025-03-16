import random
from collections import Counter
from paragraph import generate_paragraph
from data import philosophers, concepts, italicized_terms, terms, contexts, adjectives
from quotes import quotes
from reference import generate_reference  # Assumed utility

TRIVIAL_WORDS = {"a", "an", "the", "into", "to", "of", "for", "on", "by", "with", "in", "and", "but", "or"}

def capitalize_italicized(word):
    """Capitalize the first letter of a word and apply italics if in italicized_terms."""
    # Capitalize the first letter
    if word and word[0].isalpha():
        capitalized = word[0].upper() + word[1:]
    else:
        capitalized = word
    # Apply italics if the word (lowercase) is in italicized_terms
    if capitalized.lower() in italicized_terms:
        return f"*{capitalized}*"
    return capitalized

def apply_title_case(title):
    """Applies academic title case, handling italicized terms."""
    title = title.strip()
    words = title.split()
    result = []
    capitalize_next = True
    for word in words:
        if capitalize_next or word.lower() not in TRIVIAL_WORDS:
            result.append(capitalize_italicized(word))
        else:
            result.append(word.lower())
        capitalize_next = word.endswith(":")
    return " ".join(result)

abstract_title_templates = [
    "The Abyss of Meaning: {concept} and {term} in Dialogue",
    "Fragments of Thought: Reflections on {philosopher}'s {concept}",
    "Echoes of {term}: A Postmodern Inquiry",
    "Navigating the Labyrinth: {concept} in {context}",
    "The Play of Signifiers: {term} and {concept}",
    "Disrupting the Center: {philosopher} and {term}",
    "Between the Lines: {concept} as {term}",
    "The Specter of {concept}: Haunting {context}",
    "Unraveling {term}: A {context} Perspective",
    "The Rhizomatic Web: {concept} and {term}"
]

def generate_section_title(section_parts):
    """Generate a section title based on content using abstract templates."""
    philosopher_count = Counter()
    concept_count = Counter()
    term_count = Counter()
    
    for part in section_parts:
        text = part.strip().replace("[citation]", "").replace("[reflection]", "").lower()
        text = text.replace(".", "").replace(",", "").replace("*", "")
        words = text.split()
        
        for ph in philosophers:
            if ph.lower() in text:
                philosopher_count[ph] += 1
        for word in words:
            if word in [c.lower() for c in concepts]:
                concept_count[word] += 1
            if word in [t.lower() for t in terms]:
                term_count[word] += 1
    
    top_philosophers = [ph for ph, _ in philosopher_count.most_common(1)]
    top_concepts = [c for c, _ in concept_count.most_common(1)]
    top_terms = [t for t, _ in term_count.most_common(1)]
    
    template = random.choice(abstract_title_templates)
    data = {}
    if '{concept}' in template:
        concept = top_concepts[0] if top_concepts else random.choice(concepts)
        data['concept'] = concept
    if '{term}' in template:
        term = top_terms[0] if top_terms else random.choice(terms)
        data['term'] = term
    if '{philosopher}' in template:
        philosopher = top_philosophers[0] if top_philosophers else random.choice(philosophers)
        data['philosopher'] = philosopher
    if '{context}' in template:
        data['context'] = random.choice(contexts)
    
    raw_title = template.format(**data)
    return apply_title_case(raw_title)

def generate_title():
    """Generate the essay title."""
    concept = random.choice(concepts)
    term = random.choice(terms)
    adjective = random.choice(adjectives)
    raw_title = f"unraveling {concept}: a {adjective} inquiry into {term}"
    return apply_title_case(raw_title)

def generate_essay():
    """Generate the full essay."""
    all_references = [generate_reference() for _ in range(12)]
    cited_references = []
    essay_parts = []
    mentioned_philosophers = set()
    used_concepts = set()
    used_terms = set()
    used_quotes = set()

    # Title
    title = generate_title()
    essay_parts.append(f"# {title}\n\n")

    # Introduction
    intro_text, intro_concepts, intro_terms = generate_paragraph(
        "introduction", random.randint(6, 8), all_references, mentioned_philosophers,
        used_quotes=used_quotes, all_references=all_references, cited_references=cited_references
    )
    essay_parts.append("## Introduction\n\n")
    essay_parts.append(intro_text + "\n\n")
    used_concepts.update(intro_concepts)
    used_terms.update(intro_terms)

    # Body sections
    num_body_sections = random.randint(3, 5)
    for _ in range(num_body_sections):
        section_paragraphs = []
        for _ in range(random.randint(2, 3)):
            paragraph_text, paragraph_concepts, paragraph_terms = generate_paragraph(
                "general", random.randint(6, 10), all_references, mentioned_philosophers,
                used_quotes=used_quotes, all_references=all_references, cited_references=cited_references
            )
            section_paragraphs.append(paragraph_text)
            used_concepts.update(paragraph_concepts)
            used_terms.update(paragraph_terms)
        section_title = generate_section_title(section_paragraphs)
        essay_parts.append(f"## {section_title}\n\n")
        essay_parts.append('\n\n'.join(section_paragraphs) + "\n\n")

    # Conclusion
    conclusion_text, _, _ = generate_paragraph(
        "conclusion", random.randint(6, 8), all_references, mentioned_philosophers,
        used_quotes=used_quotes, all_references=all_references, cited_references=cited_references
    )
    essay_parts.append("## Conclusion\n\n")
    essay_parts.append(conclusion_text + "\n\n")

    # References section
    essay_parts.append("## References\n\n")
    for i, ref in enumerate(cited_references, 1):
        essay_parts.append(f"[^{i}]: {ref}\n")

    essay_text = ''.join(essay_parts)
    return essay_text