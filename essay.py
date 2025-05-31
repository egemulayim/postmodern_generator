"""
A module for coherent essay structure and generation.
This module generates a full essay with coherent sections,
properly formatted citations, and a works cited section.
It includes functions for generating titles, sections, and
abstracts, as well as managing notes and references.
It also ensures proper capitalization and formatting
of headings and terms.
The citation system follows MLA 9 style guidelines.
"""

import random
import metafiction
from coherence import EssayCoherence
from paragraph import generate_paragraph
from json_data_provider import philosophers, concepts, terms, philosopher_concepts, contexts, thematic_clusters
from reference import generate_reference
from capitalization import (
    ensure_proper_capitalization_with_italics, 
    format_headings_with_title_case,
    italicize_terms_in_text,
    apply_title_case
)
from notes import NoteSystem
from abstract_generator import generate_enhanced_abstract

# Import the reset function
from citation_utils import reset_citation_globals

import re
from collections import Counter

# Define constants for sentence counts per paragraph
MIN_SENTENCES_PER_PARAGRAPH = 7
MAX_SENTENCES_PER_PARAGRAPH = 10
MIN_PARAGRAPHS_PER_SECTION = 2 # Define if not already defined
MAX_PARAGRAPHS_PER_SECTION = 4 # Define if not already defined

def extract_themes_from_title(raw_title, concepts, terms):
    """
    Extract key concepts and terms from the title for thematic consistency.
    
    Args:
        raw_title (str): The raw title string
        concepts (list): Available concepts list
        terms (list): Available terms list
        
    Returns:
        dict: Dictionary of title themes (concepts, terms, related concepts)
    """
    # Initialize dictionary to store themes
    title_themes = {
        'primary_concepts': [],
        'primary_terms': [],
        'related_concepts': []
    }
    
    # First, try to find any concepts or terms explicitly mentioned in the title
    for concept in concepts:
        if concept.lower() in raw_title.lower():
            title_themes['primary_concepts'].append(concept)
    
    for term in terms:
        if term.lower() in raw_title.lower():
            title_themes['primary_terms'].append(term)
    
    # Try pattern matching if explicit matches are insufficient
    if len(title_themes['primary_concepts']) < 2:
        # Common patterns in title templates - updated to capture multi-word concepts
        concept_patterns = [
            r'of ([\w\s-]+?)(?::|,| and| in|$)',  # captures concepts after 'of '
            r'([\w\s-]+?)(?: and|:) ', # captures concepts before ' and ' or ':'
            r'^([\w\s-]+?)(?::|,)', # captures concepts at the beginning of the title, before ':' or ','
            r'([\w\s-]+?):' # captures concepts followed by a colon
        ]
        
        # Try each pattern
        for pattern in concept_patterns:
            matches = re.findall(pattern, raw_title)
            if matches:
                for match in matches:
                    if isinstance(match, tuple):
                        for group in match:
                            if group and any(concept.lower() == group.lower() for concept in concepts):
                                matching_concept = next(c for c in concepts if c.lower() == group.lower())
                                title_themes['primary_concepts'].append(matching_concept)
                    elif isinstance(match, str) and any(concept.lower() == match.lower() for concept in concepts):
                        matching_concept = next(c for c in concepts if c.lower() == match.lower())
                        title_themes['primary_concepts'].append(matching_concept)
    
    # Similar approach for terms
    if len(title_themes['primary_terms']) < 2:
        term_patterns = [
            r': ([\w\s-]+?)(?: in|$)', # captures terms after ': '
            r'([\w\s-]+?) in the', # captures terms before ' in the'
            r'([\w\s-]+?):' # captures terms before ':'
        ]
        
        for pattern in term_patterns:
            matches = re.findall(pattern, raw_title)
            if matches:
                for match in matches:
                    if isinstance(match, tuple):
                        for group in match:
                            if group and any(term.lower() == group.lower() for term in terms):
                                matching_term = next(t for t in terms if t.lower() == group.lower())
                                title_themes['primary_terms'].append(matching_term)
                    elif isinstance(match, str) and any(term.lower() == match.lower() for term in terms):
                        matching_term = next(t for t in terms if t.lower() == match.lower())
                        title_themes['primary_terms'].append(matching_term)
    
    # If we still don't have enough themes, add some random ones
    # but with less weight than the ones directly from the title
    if len(title_themes['primary_concepts']) < 2:
        additional_concepts = random.sample([c for c in concepts if c not in title_themes['primary_concepts']], 
                                           min(2, len(concepts)))
        title_themes['related_concepts'].extend(additional_concepts)
    
    if len(title_themes['primary_terms']) < 2:
        title_themes['primary_terms'].extend(
            random.sample([t for t in terms if t not in title_themes['primary_terms']], 
                          min(2, len(terms)))
        )
    
    # Deduplicate
    title_themes['primary_concepts'] = list(set(title_themes['primary_concepts']))
    title_themes['primary_terms'] = list(set(title_themes['primary_terms']))
    title_themes['related_concepts'] = list(set(title_themes['related_concepts']))
    
    return title_themes

def find_relevant_philosophers(concepts, terms, philosopher_concepts):
    """
    Find philosophers most associated with given concepts and terms.
    
    Args:
        concepts (list): List of concepts to match
        terms (list): List of terms to match
        philosopher_concepts (dict): Dictionary mapping philosophers to their concepts
        
    Returns:
        list: Philosophers most relevant to the given concepts and terms
    """
    relevant_philosophers = []
    
    # Find philosophers associated with concepts
    for concept in concepts:
        for philosopher, philo_concepts in philosopher_concepts.items():
            if concept in philo_concepts:
                relevant_philosophers.append(philosopher)
    
    # If we found relevant philosophers, return them, otherwise return empty list
    if relevant_philosophers:
        return list(set(relevant_philosophers))  # Deduplicate
    else:
        return []

def generate_title(coherence_manager):
    """
    Generate a more sophisticated and thematically coherent title.
    
    Args:
        coherence_manager: The EssayCoherence instance to use for theme management
    
    Returns:
        str: A formatted title
    """
    # Get primary themes for consistency
    primary_concept = coherence_manager.get_weighted_concept()
    primary_term = coherence_manager.get_weighted_term()
    
    # More sophisticated title templates
    title_templates = [
        f"The {random.choice(['Dialectic', 'Discourse', 'Problematic', 'Aporia', 'Paradox'])} of {primary_concept}: {random.choice(['Toward', 'Towards', 'Interrogating', 'Rethinking', 'Reimagining'])} {primary_term}",
        f"{primary_concept} and {primary_term}: {random.choice(['Beyond', 'After', 'Against', 'Within', 'Between'])} {coherence_manager.get_related_concept(primary_concept)}",
        f"{random.choice(['Deconstructing', 'Problematizing', 'Negotiating', 'Tracing', 'Mapping'])} {primary_concept}: {primary_term} in the Age of {coherence_manager.get_oppositional_concept(primary_concept)}",
        f"The {random.choice(['Impossibility', 'Possibility', 'Crisis', 'Politics', 'Poetics'])} of {primary_term}: {primary_concept} and its {random.choice(['Discontents', 'Others', 'Afterlives', 'Limits', 'Futures'])}",
        f"{primary_concept}/{primary_term}: {random.choice(['Towards', 'Beyond', 'After', 'Against'])} a {random.choice(['Critical', 'Radical', 'Deconstructive', 'Post-Dialectical', 'Non-Representational'])} Theory",
        f"{random.choice(['Reading', 'Writing', 'Theorizing', 'Thinking', 'Performing'])} {primary_concept} {random.choice(['After', 'Through', 'Against', 'With', 'Beyond'])} {primary_term}",
        f"{random.choice(['The End of', 'After', 'Beyond', 'Against', 'Rethinking'])} {primary_concept}: {primary_term} in the Era of {coherence_manager.get_related_concept(primary_concept)}"
    ]
    
    raw_title = random.choice(title_templates)
    
    # Record usage of concepts and terms in the title
    coherence_manager.record_usage(
        concepts=[primary_concept, coherence_manager.get_related_concept(primary_concept)],
        terms=[primary_term]
    )
    
    return raw_title

def generate_essay(theme_key=None):
    """Generate the full essay with enhanced internal reasoning, proper capitalization, and coherent notes."""
    # Reset global citation state before generating a new essay
    reset_citation_globals()

    # Initialize coherence manager for thematic unity
    coherence_manager = EssayCoherence(theme_key=theme_key)
    
    # Initialize note system for managing citations and bibliography
    note_system = NoteSystem()
    note_system.reset() # Reset note system state
    
    essay_parts = []
    used_quotes = set()

    # Title with greater sophistication
    raw_title = generate_title(coherence_manager)
    # Apply title case without running through the regular capitalization system
    title = apply_title_case(raw_title)
    essay_parts.append(f"# {title}\n\n")
    
    # Extract the main themes from the title for consistent usage
    title_themes = extract_themes_from_title(raw_title, concepts, terms)
    
    # Prioritize these title themes in the coherence manager
    coherence_manager.prioritize_title_themes(title_themes)
    
    # Find philosophers most associated with title themes
    relevant_philosophers = find_relevant_philosophers(
        title_themes['primary_concepts'] + title_themes['related_concepts'],
        title_themes['primary_terms'],
        philosopher_concepts
    )
    # Ensure relevant_philosophers is not empty, if so, pick some random ones
    if not relevant_philosophers:
        relevant_philosophers = random.sample(philosophers, min(3, len(philosophers)))
    
    # Generate a more comprehensive abstract with keywords that reference title themes
    abstract = generate_enhanced_abstract(coherence_manager, title_themes, essay_theme_key=theme_key)
    
    # Apply capitalization fix to the abstract
    abstract = ensure_proper_capitalization_with_italics(abstract)
    
    # Apply italicization to terms
    abstract = italicize_terms_in_text(abstract)
    
    essay_parts.append(abstract) # Removed unnecessary extra '\n'
    essay_parts.append("## Introduction\n\n") # Then "## Introduction" followed by two newlines (for a blank line)

    # Body sections with dialectical development
    num_body_sections = random.randint(3, 5)
    
    # Create a dialectical progression for section themes
    # Start with a primary concept from the title if available
    starting_concept = (title_themes['primary_concepts'][0] if title_themes['primary_concepts'] 
                       else coherence_manager.primary_concepts[0] if coherence_manager.primary_concepts 
                       else random.choice(concepts))
    
    dialectic = coherence_manager.develop_dialectic(starting_concept, num_steps=num_body_sections - 1)

    # Determine paragraph counts for Intro and Conclusion first (1-3 paragraphs each)
    actual_num_intro_paragraphs = random.randint(1, 3)
    actual_num_conclusion_paragraphs = random.randint(1, 3)
    max_intro_conclusion_length = max(actual_num_intro_paragraphs, actual_num_conclusion_paragraphs)

    # Pre-calculate paragraph counts for Body Sections.
    # Body sections must be at least one paragraph longer than the longer of intro/conclusion,
    # and a maximum of 5 paragraphs.
    temp_body_section_paragraph_counts = []
    for _ in range(num_body_sections):
        lower_bound_body = max_intro_conclusion_length + 1
        # Ensure lower_bound is not greater than upper_bound (5).
        # Since max_intro_conclusion_length is at most 3, lower_bound_body is at most 4.
        # So random.randint(lower_bound_body, 5) is always valid.
        num_paragraphs_for_this_body_section = random.randint(lower_bound_body, 5)
        temp_body_section_paragraph_counts.append(num_paragraphs_for_this_body_section)
    
    # Introduction with more theoretical sophistication
    intro_theme = coherence_manager.get_section_theme() 
    intro_context = {
        'section': 'introduction',
        'title_themes': title_themes,
        'relevant_philosophers': relevant_philosophers
    }
    # actual_num_intro_paragraphs (defined above) will be used to generate the intro paragraphs
    intro_paragraphs_content = []
    for _ in range(actual_num_intro_paragraphs):
        paragraph_text, used_concepts, used_terms = generate_paragraph(
            "introduction", random.randint(7, 9), 
            used_quotes=used_quotes, note_system=note_system, context=intro_context,
            coherence_manager=coherence_manager
        )
        # Capitalize and italicize paragraph text
        paragraph_text = ensure_proper_capitalization_with_italics(paragraph_text)
        paragraph_text = italicize_terms_in_text(paragraph_text)
        intro_paragraphs_content.append(paragraph_text)
        coherence_manager.record_usage(concepts=used_concepts, terms=used_terms) # Ensure usage is recorded
    
    essay_parts.append("\n".join(intro_paragraphs_content) + "\n\n") # Join paragraphs with one newline, then two newlines after the section

    # Generate body sections
    for i, body_section_theme_concept in enumerate(dialectic):
        # Determine actual number of paragraphs for this body section based on pre-calculated counts
        actual_num_paragraphs_for_section = temp_body_section_paragraph_counts[i]

        section_theme = coherence_manager.get_section_theme(specific_concept=body_section_theme_concept)
        
        # Create context for the section
        section_context = {
            'section': f'body_section_{i+1}',
            'title_themes': title_themes,
            'relevant_philosophers': relevant_philosophers,
            'section_theme_concept': body_section_theme_concept 
        }

        # Generate paragraphs for the current section
        section_paragraphs = []
        for para_idx in range(actual_num_paragraphs_for_section):
            paragraph_text, used_concepts, used_terms = generate_paragraph(
                f"body_section_{i+1}", 
                random.randint(MIN_SENTENCES_PER_PARAGRAPH, MAX_SENTENCES_PER_PARAGRAPH),
                used_quotes=used_quotes, 
                note_system=note_system,
                context=section_context,
                coherence_manager=coherence_manager
            )
            # Capitalize and italicize paragraph text
            paragraph_text = ensure_proper_capitalization_with_italics(paragraph_text)
            paragraph_text = italicize_terms_in_text(paragraph_text)
            section_paragraphs.append(paragraph_text)
            coherence_manager.record_usage(concepts=used_concepts, terms=used_terms) # Ensure usage is recorded
        
        # Generate section title (now using the corrected theme)
        section_title_text = generate_section_title(
            section_paragraphs, coherence_manager, section_theme, title_themes=title_themes
        )
        # Format section title with ## and a single space, then add to essay_parts
        essay_parts.append(f"## {section_title_text}\n\n") # Section title followed by two newlines (for a blank line)
        essay_parts.append("\n".join(section_paragraphs) + "\n\n") # Join paragraphs with one newline, then two newlines after the section

    # Conclusion with more theoretical sophistication
    conclusion_theme = coherence_manager.get_section_theme(is_conclusion=True)
    conclusion_context = {
        'section': 'conclusion',
        'title_themes': title_themes,
        'relevant_philosophers': relevant_philosophers
    }
    # actual_num_conclusion_paragraphs will be used to generate the conclusion paragraphs
    conclusion_paragraphs_content = []
    for _ in range(actual_num_conclusion_paragraphs):
        paragraph_text, used_concepts, used_terms = generate_paragraph(
            "conclusion", random.randint(7, 9), 
            used_quotes=used_quotes, note_system=note_system, context=conclusion_context,
            coherence_manager=coherence_manager
        )
        # Capitalize and italicize paragraph text
        paragraph_text = ensure_proper_capitalization_with_italics(paragraph_text)
        paragraph_text = italicize_terms_in_text(paragraph_text)
        conclusion_paragraphs_content.append(paragraph_text)
        coherence_manager.record_usage(concepts=used_concepts, terms=used_terms) # Ensure usage is recorded
    
    essay_parts.append("## Conclusion\n\n") # Add "## Conclusion" title with two newlines after (for a blank line)
    essay_parts.append("\n".join(conclusion_paragraphs_content) + "\n\n") # Join paragraphs, then two newlines

    # Generate Notes section and Works Cited section from a single call
    full_notes_and_works_cited = note_system.generate_notes_section()
    if full_notes_and_works_cited and full_notes_and_works_cited.strip():
        essay_parts.append(full_notes_and_works_cited)
    
    return "".join(essay_parts)

def generate_section_title(section_paragraphs, coherence_manager, section_theme, title_themes=None):
    """
    Generate a sophisticated, context-aware section title using a template.
    Ensures the title is relevant to the section's content and overall essay themes.
    """
    # Base template for titles to ensure diversity and theoretical framing
    templates = [
        "{concept1}: {philosopher1} and the Poetics of {concept2} and {term1}",
        "The Politics of {concept1}: {philosopher1}, {term1}, and the {context1} of {concept2}",
        "Deconstructing {term1}: {philosopher1} on {concept1} in the Age of {concept2}",
        "Beyond {concept1}: {philosopher1}, {term2}, and the Crisis of {term1}",
        "Rethinking {concept1}: {philosopher1}'s {term1} in Dialogue with {concept2}",
        "{concept1} and Its Discontents: {philosopher1}, {concept2}, and the Future of {term1}",
        "The Limits of {term1}: {philosopher1}, {concept2}, and the Question of {concept1}",
        "Interrogating {concept1}: {philosopher1}, {term1}, and the Necropolitics of {concept2}",
        "{term1} Revisited: {philosopher1}, {concept2}, and the Hauntology of {concept1}",
        "The {context1} of {concept1}: {philosopher1}, {term1}, and Postmodernity's {concept2}"
    ]
    
    # Get primary concepts and terms from the section theme
    # These will be prioritized for the title
    primary_concept = section_theme.get('primary_concept', random.choice(concepts))
    primary_term = section_theme.get('primary_term', random.choice(terms))
    
    # Get other concepts and terms, trying to use title_themes for relevance if available
    secondary_concept = random.choice(title_themes['primary_concepts'] + title_themes['related_concepts'] if title_themes and (title_themes['primary_concepts'] + title_themes['related_concepts']) else concepts)
    secondary_term = random.choice(title_themes['primary_terms'] if title_themes and title_themes['primary_terms'] else terms)

    # Ensure distinct concepts and terms
    while secondary_concept == primary_concept:
        secondary_concept = random.choice(concepts)
    while secondary_term == primary_term:
        secondary_term = random.choice(terms)
        
    # Select a relevant philosopher
    # Prefer philosophers linked to the primary concept of the section, or from title_themes
    relevant_philosophers_for_section = find_relevant_philosophers([primary_concept], [primary_term], philosopher_concepts)
    if not relevant_philosophers_for_section and title_themes:
        relevant_philosophers_for_section = find_relevant_philosophers(
            title_themes['primary_concepts'] + title_themes['related_concepts'],
            title_themes['primary_terms'],
            philosopher_concepts
        )
    
    philosopher = random.choice(relevant_philosophers_for_section if relevant_philosophers_for_section else philosophers)

    # Choose a random context
    context = random.choice(contexts)

    # Choose a random template
    template = random.choice(templates)
    
    # Fill the template
    raw_section_title = template.format(
        concept1=primary_concept,
        concept2=secondary_concept,
        term1=primary_term,
        term2=secondary_term,
        philosopher1=philosopher,
        context1=context
    )
    
    # Apply title case to the raw section title
    section_title = apply_title_case(raw_section_title)
    
    # Italicize terms within the title if any exist
    section_title = italicize_terms_in_text(section_title)
    
    return section_title # Return just the processed title string, newlines handled in generate_essay