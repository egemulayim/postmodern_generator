import random
from collections import Counter
from paragraph import generate_paragraph
from data import philosophers, concepts, terms, contexts, adjectives
from reference import generate_reference

# List of trivial words (not capitalized unless first word or after a colon)
TRIVIAL_WORDS = {"a", "an", "the", "into", "to", "of", "for", "on", "by", "with", "in", "and", "but", "or"}

def apply_title_case(title):
    """Applies academic title case to a string."""
    words = title.split()
    result = []
    capitalize_next = True  # Capitalize the first word

    for word in words:
        if capitalize_next or word.lower() not in TRIVIAL_WORDS:
            result.append(word.capitalize())
        else:
            result.append(word.lower())
        # Capitalize the next word if this one ends with a colon
        capitalize_next = word.endswith(":")

    return " ".join(result)

def generate_section_title(section_parts):
    philosopher_count = Counter()
    concept_count = Counter()
    term_count = Counter()
    
    for part in section_parts:
        text = part[0] if isinstance(part, tuple) else part
        # Remove placeholders
        text = text.replace("[citation]", "").replace("[reflection]", "").strip()
        # Normalize text to handle punctuation
        text = text.replace(".", "").replace(",", "").lower()
        words = text.split()
        
        # Check for philosopher names (which might be multi-word)
        for ph in philosophers:
            ph_lower = ph.lower()
            if ph_lower in text:
                philosopher_count[ph] += 1
        
        # Check for concepts and terms (assuming they are single words)
        for word in words:
            word_lower = word.lower()
            if word_lower in [c.lower() for c in concepts]:
                concept_count[word] += 1
            if word_lower in [t.lower() for t in terms]:
                term_count[word] += 1
    
    # Get the most common items
    top_philosophers = [ph for ph, _ in philosopher_count.most_common(2)]
    top_concepts = [c for c, _ in concept_count.most_common(2)]
    top_terms = [t for t, _ in term_count.most_common(2)]
    
    # If no specific content is found, use a generic title
    if not (top_philosophers or top_concepts or top_terms):
        raw_title = "Speculative Reflections"
    else:
        # Title templates
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
        
        # Fill template with top items
        philosopher = random.choice(top_philosophers) if top_philosophers else "Contemporary Theory"
        concept = random.choice(top_concepts) if top_concepts else "Postmodernism"
        term = random.choice(top_terms) if top_terms else "Discourse"
        context = random.choice(contexts)  # Use contexts list for variety
        
        raw_title = template.format(philosopher=philosopher, concept=concept, term=term, context=context)
    
    # Apply title case to the raw title
    return apply_title_case(raw_title)

def generate_title():
    concept = random.choice(concepts)
    term = random.choice(terms)
    adjective = random.choice(adjectives)
    raw_title = f"unraveling {concept}: a {adjective} inquiry into {term}"
    # Apply title case to the raw title
    return apply_title_case(raw_title)

def generate_essay():
    references = [generate_reference() for _ in range(12)]
    essay_parts = []

    # Title
    title = generate_title()
    essay_parts.append((f"# {title}\n\n", None))

    # Introduction: 6-8 sentences
    intro_parts = generate_paragraph("introduction", random.randint(6, 8), references)
    essay_parts.append(("## Introduction\n\n", None))
    essay_parts.extend(intro_parts)
    essay_parts.append(("\n\n", None))

    # Body sections: 3-5 sections with 2-3 paragraphs each, 6-10 sentences per paragraph
    num_body_sections = random.randint(3, 5)
    for _ in range(num_body_sections):
        section_parts = []
        for _ in range(random.randint(2, 3)):  # 2-3 paragraphs per section
            paragraph_parts = generate_paragraph("general", random.randint(6, 10), references)
            section_parts.extend(paragraph_parts)
        section_title = generate_section_title(section_parts)  # Generate dynamic title with title case
        essay_parts.append((f"## {section_title}\n\n", None))
        essay_parts.extend(section_parts)
        essay_parts.append(("\n\n", None))

    # Conclusion: 6-8 sentences
    conclusion_parts = generate_paragraph("conclusion", random.randint(6, 8), references)
    essay_parts.append(("## Conclusion\n\n", None))
    essay_parts.extend(conclusion_parts)
    essay_parts.append(("\n\n", None))

    # Notes section
    notes_section = "## Notes\n\n"
    for i, ref in enumerate(references, 1):
        notes_section += f"{i}. {ref}\n"
    essay_parts.append((notes_section, None))

    # Combine everything
    essay_text = "".join([part[0] for part in essay_parts])
    return essay_text