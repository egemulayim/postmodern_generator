import random
from collections import Counter
from paragraph import generate_paragraph
from data import philosophers, concepts, terms, contexts, adjectives
from quotes import quotes
from reference import generate_reference  # Assumed utility

TRIVIAL_WORDS = {"a", "an", "the", "into", "to", "of", "for", "on", "by", "with", "in", "and", "but", "or"}

def apply_title_case(title):
    """Applies academic title case."""
    title = title.strip()
    words = title.split()
    result = []
    capitalize_next = True
    for word in words:
        if capitalize_next or word.lower() not in TRIVIAL_WORDS:
            result.append(word.capitalize())
        else:
            result.append(word.lower())
        capitalize_next = word.endswith(":")
    return " ".join(result)

def generate_section_title(section_parts):
    """Generate a section title based on content."""
    philosopher_count = Counter()
    concept_count = Counter()
    term_count = Counter()
    
    for part in section_parts:
        text = part.strip().replace("[citation]", "").replace("[reflection]", "").lower()
        text = text.replace(".", "").replace(",", "")
        words = text.split()
        
        for ph in philosophers:
            if ph.lower() in text:
                philosopher_count[ph] += 1
        for word in words:
            if word in [c.lower() for c in concepts]:
                concept_count[word] += 1
            if word in [t.lower() for t in terms]:
                term_count[word] += 1
    
    top_philosophers = [ph for ph, _ in philosopher_count.most_common(2)]
    top_concepts = [c for c, _ in concept_count.most_common(2)]
    top_terms = [t for t, _ in term_count.most_common(2)]
    
    if not (top_philosophers or top_concepts or top_terms):
        raw_title = "Speculative Reflections"
    else:
        templates = [
            "Exploring {concept} in {philosopher}'s Thought",
            "{term} and Its Implications for {concept}",
            "A {context}-Based Inquiry into {concept}",
            "{philosopher} and the Dynamics of {term}",
            "The Role of {term} in {philosopher}'s Philosophy",
            "{concept}: A {context} Perspective",
            "Re-examining {concept} Through {philosopher}'s Lens",
            "Intersections of {term} and {concept} in {context}",
            "Critical Reflections on {concept} in the Work of {philosopher}"
        ]
        template = random.choice(templates)
        philosopher = random.choice(top_philosophers) if top_philosophers else "Contemporary Theory"
        concept = random.choice(top_concepts) if top_concepts else "Postmodernism"
        term = random.choice(top_terms) if top_terms else "Discourse"
        context = random.choice(contexts)
        raw_title = template.format(philosopher=philosopher, concept=concept, term=term, context=context)
    
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
    all_references = [generate_reference() for _ in range(12)]  # List of all possible references
    cited_references = []  # List to track references cited in the essay
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

    # References section with footnote definitions
    essay_parts.append("## Notes\n\n")
    for i, ref in enumerate(cited_references, 1):
        essay_parts.append(f"[^{i}]: {ref}\n")

    # Combine everything
    essay_text = ''.join(essay_parts)
    return essay_text