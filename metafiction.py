"""
A module for generating metafictional elements in generated essays.
This module provides functions to create metafictional elements
that can be inserted into academic writing, particularly in the context of
postmodern philosophy and theory.
It includes functions to generate metafictional elements for paragraphs,
insert them into existing text, and create metafictional conclusions.
The metafictional elements are designed to reflect the self-referential nature
of postmodern discourse, often questioning the very frameworks and methodologies
they employ.
It also includes a function to generate a metafictional conclusion
that references concepts and terms used in the essay.
This module is intended to enhance the complexity and depth of
academic writing, particularly in the context of postmodern philosophy.
It is designed to be used in conjunction with other modules
for generating essays, abstracts, and citations.
"""

import random
import re
from json_data_provider import (
    concepts, terms, philosophers, 
    METAFICTIONAL_TEMPLATES, METAFICTIONAL_CONCLUSIONS,
    thematic_clusters # Added for theme-specific metafiction
)
# It's generally better to pass coherence_manager as an argument if it's used extensively
# from coherence import EssayCoherence # Avoid direct import if passing as arg

def generate_metafictional_element(theme_key=None, coherence_manager=None):
    """Generate a metafictional element, potentially themed, for use in abstracts or introductions."""
    templates = [
        "It bears asking whether this line of reasoning merely reproduces existing paradigms.",
        "This analysis acknowledges its own complicity in the very discourses it critiques.",
        "In doing so, this paper inevitably participates in the economy of academic knowledge production it seeks to interrogate.",
        "The inherent contradictions of such an approach will become apparent as the argument unfolds.",
        "To what extent can this investigation escape the very logic it seeks to critique?",
        "This paper remains aware of the paradox inherent in employing theoretical tools to critique those same tools.",
        "In articulating these critiques, I acknowledge the impossibility of a position fully exterior to the systems under examination.",
        "The methodology employed here is necessarily implicated in the structures it attempts to analyze.",
        "This text performs the very tensions it describes.",
        "Such an approach raises questions about the possibility of critical distance in theoretical discourse."
    ]
    
    # Theme-specific additions (could be expanded in data.py)
    if theme_key and theme_key in thematic_clusters:
        theme_data = thematic_clusters[theme_key]
        if theme_key == "Technology, Media, and Culture":
            templates.append("This textual analysis ironically attempts to grasp a digitally saturated, post-literate condition.")
        elif theme_key == "Power and Knowledge":
            templates.append("The very act of articulating this critique of power is itself a discursive move within a field of power.")
        elif theme_key == "Decoloniality and Postcolonial Studies":
            templates.append("Can this analysis, framed within Western academic discourse, truly decenter dominant epistemologies?")

    chosen_template = random.choice(templates)

    # If coherence_manager is available, try to make it more specific
    if coherence_manager:
        # These are placeholders for more specific concept/term selection if template uses them
        # The generic templates above mostly don't, but future ones might.
        mf_concept = coherence_manager.get_weighted_concept()
        mf_term = coherence_manager.get_weighted_term(exclude={mf_concept})
        # Example of how a more complex template *could* be formatted:
        # if "{concept}" in chosen_template: chosen_template = chosen_template.format(concept=mf_concept, term=mf_term)

    return chosen_template

def insert_metafiction_in_paragraph(paragraph_text, theme_key=None, coherence_manager=None):
    """Insert a metafictional element into an existing paragraph appropriately, considering theme."""
    metafictional_indicators = [
        "this essay", "this text", "this paper", "this analysis", 
        "in writing", "the author", "inevitably", "implicated", 
        "complicit", "paradox", "entangled", "self-reflexive",
        # Added from generate_metafictional_element to avoid double-dipping
        "reproduces existing paradigms", "discourses it critiques", "economy of academic knowledge production",
        "logic it seeks to critique", "theoretical tools to critique", "systems under examination"
    ]
    
    if any(indicator in paragraph_text.lower() for indicator in metafictional_indicators):
        return paragraph_text
    
    # Select a random concept, term, and philosopher to populate the template
    # Prioritize from theme if coherence_manager and theme are available
    mf_concept = random.choice(concepts)
    mf_term = random.choice([t for t in terms if t != mf_concept])
    mf_philosopher = random.choice(philosophers)

    if coherence_manager:
        mf_concept = coherence_manager.get_weighted_concept()
        mf_term = coherence_manager.get_weighted_term(exclude={mf_concept})
        mf_philosopher = coherence_manager.get_weighted_philosopher()
        if coherence_manager.active_theme_key: # Further bias if theme is active
            theme_data = coherence_manager.active_theme_data
            if theme_data.get('key_concepts') and random.random() < 0.7:
                mf_concept = random.choice(theme_data['key_concepts'])
            if theme_data.get('relevant_terms') and random.random() < 0.7:
                mf_term = random.choice([t for t in theme_data['relevant_terms'] if t != mf_concept])
            if theme_data.get('core_philosophers') and random.random() < 0.7:
                mf_philosopher = random.choice(theme_data['core_philosophers'])
    
    # Use METAFICTIONAL_TEMPLATES from data.py
    # We could also add theme-specific templates here if desired
    metafictional_text_template = random.choice(METAFICTIONAL_TEMPLATES)
    try:
        metafictional_text = metafictional_text_template.format(
            concept=mf_concept,
            term=mf_term,
            philosopher=mf_philosopher
        )
    except KeyError: # If template doesn't use all keys, or uses different ones
        # Fallback for simpler templates or if formatting fails
        metafictional_text = "This text self-consciously reflects on its own discursive construction."
        if "{concept}" in metafictional_text_template: # Attempt partial format
            try: metafictional_text = metafictional_text_template.format(concept=mf_concept, term=random.choice(terms), philosopher=random.choice(philosophers))
            except: pass # Ignore if still fails

    if paragraph_text.endswith('.'):
        paragraph_text = paragraph_text[:-1]

    sentences = re.split(r'(?<=[.?!])\s+(?=[A-Z])|(?<=[.?!])$\s*', paragraph_text.strip())
    sentences = [s.strip() for s in sentences if s.strip()]

    if not sentences:
         return metafictional_text

    if len(sentences) <= 1:
        if sentences and not sentences[-1].endswith(tuple('.!?')):
            return sentences[-1] + ". " + metafictional_text
        elif sentences:
            return sentences[-1] + " " + metafictional_text
        else:
            return metafictional_text
    else:
        insert_position = random.randint(len(sentences) // 2, len(sentences) - 1)
        if not sentences[insert_position -1].endswith(tuple('.!?')):
            sentences[insert_position -1] += '.'
        sentences.insert(insert_position, metafictional_text)
        return " ".join(sentences)

def generate_metafictional_conclusion(concepts_used, terms_used, theme_key=None, coherence_manager=None):
    """
    Generate a metafictional conclusion, potentially themed.
    Args:
        concepts_used (set): Set of concepts used in the essay.
        terms_used (set): Set of terms used in the essay.
        theme_key (str, optional): The active theme key.
        coherence_manager (EssayCoherence, optional): The coherence manager instance.
    Returns:
        str: A metafictional conclusion statement
    """
    mf_concept = random.choice(list(concepts_used)) if concepts_used else random.choice(concepts)
    mf_term = random.choice(list(terms_used)) if terms_used else random.choice(terms)

    if coherence_manager:
        mf_concept = coherence_manager.get_weighted_concept(exclude=terms_used if terms_used else None)
        mf_term = coherence_manager.get_weighted_term(exclude=concepts_used.union({mf_concept}) if concepts_used else {mf_concept})
        if coherence_manager.active_theme_key:
            theme_data = coherence_manager.active_theme_data
            if theme_data.get('key_concepts') and random.random() < 0.8:
                potential_concepts = [c for c in theme_data['key_concepts'] if c in concepts_used]
                if potential_concepts: mf_concept = random.choice(potential_concepts)
            if theme_data.get('relevant_terms') and random.random() < 0.8:
                potential_terms = [t for t in theme_data['relevant_terms'] if t in terms_used and t != mf_concept]
                if potential_terms: mf_term = random.choice(potential_terms)
    
    # Fallback if mf_term became same as mf_concept due to limited themed choices
    if mf_concept == mf_term:
        mf_term = random.choice([t for t in (list(terms_used) if terms_used else terms) if t != mf_concept] or terms)

    # Use the imported templates from data.py
    # Consider adding theme-specific conclusion templates to data.py
    conclusion_template = random.choice(METAFICTIONAL_CONCLUSIONS)
    
    try:
        return conclusion_template.format(concept=mf_concept, term=mf_term)
    except KeyError: # Fallback if formatting fails
        return f"Ultimately, the very attempt to delineate {mf_concept} from {mf_term} underscores the constructed nature of this theoretical endeavor."