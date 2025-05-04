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
from data import philosophers, concepts, terms, philosopher_concepts, contexts
from reference import generate_reference
from capitalization import (
    ensure_proper_capitalization_with_italics, 
    format_headings_with_title_case,
    italicize_terms_in_text,
    apply_title_case
)
from notes import NoteSystem
from abstract_generator import generate_enhanced_abstract

import re
from collections import Counter

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
        # Common patterns in title templates
        concept_patterns = [
            r'of (\w+):', r'(\w+) and', r'^(\w+):', r'(\w+):',
            r'(\w+) in the', r'(\w+) of', r'(\w+)/(\w+)'
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
            r': (\w+) in', r'(\w+) in the', r'(\w+):', r'/(\w+):',
            r'(\w+) and its', r'(\w+) in the Era'
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

def generate_essay():
    """Generate the full essay with enhanced internal reasoning, proper capitalization, and coherent notes."""
    # Initialize coherence manager for thematic unity
    coherence_manager = EssayCoherence()
    
    # Initialize note system for managing citations and bibliography
    note_system = NoteSystem()
    
    # Generate references
    all_references = [generate_reference() for _ in range(15)]
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
    
    # Generate a more comprehensive abstract with keywords that reference title themes
    abstract = generate_enhanced_abstract(coherence_manager, title_themes)
    
    # Apply capitalization fix to the abstract
    abstract = ensure_proper_capitalization_with_italics(abstract)
    
    # Apply italicization to terms
    abstract = italicize_terms_in_text(abstract)
    
    essay_parts.append(abstract)

    # Initialize empty sets for tracking concepts and terms
    intro_concepts = set()
    intro_terms = set()

    # Introduction with more theoretical sophistication
    intro_theme = coherence_manager.get_section_theme()
    
    # Create a context for the introduction that includes title themes
    intro_context = {
        'section': 'introduction',
        'title_themes': title_themes,
        'relevant_philosophers': relevant_philosophers
    }
    
    # Generate the introduction paragraph with title themes emphasized
    intro_text, intro_concepts, intro_terms = generate_paragraph(
        "introduction", random.randint(7, 9), all_references, 
        used_quotes=used_quotes, note_system=note_system, context=intro_context
    )
    
    # Add metafictional element to introduction
    intro_text = metafiction.insert_metafiction_in_paragraph(intro_text)
    
    # Apply capitalization fix
    intro_text = ensure_proper_capitalization_with_italics(intro_text)
    
    # Apply italicization to terms
    intro_text = italicize_terms_in_text(intro_text)
    
    essay_parts.append("## Introduction\n\n")
    essay_parts.append(intro_text + "\n\n")
    
    # Record usage
    coherence_manager.record_usage(concepts=intro_concepts, terms=intro_terms)

    # Body sections with dialectical development
    num_body_sections = random.randint(3, 5)
    
    # Create a dialectical progression for section themes
    # Start with a primary concept from the title if available
    starting_concept = (title_themes['primary_concepts'][0] if title_themes['primary_concepts'] 
                       else coherence_manager.primary_concepts[0] if coherence_manager.primary_concepts 
                       else random.choice(concepts))
    
    dialectic = coherence_manager.develop_dialectic(starting_concept, num_steps=num_body_sections - 1)
    
    for i in range(num_body_sections):
        # Get a thematic focus for this section that continues the dialectic
        section_theme = coherence_manager.get_section_theme()
        
        # Always use a concept from the dialectic for stronger coherence
        if i < len(dialectic):
            section_theme['concept'] = dialectic[i]
        
        # Try to use a term from the title themes
        if title_themes['primary_terms'] and random.random() < 0.7:
            section_theme['term'] = random.choice(title_themes['primary_terms'])
            
        # Try to use a philosopher relevant to the title themes
        if relevant_philosophers and random.random() < 0.7:
            section_theme['philosopher'] = random.choice(relevant_philosophers)
            
        # For the related philosopher, try to find someone who has written on similar themes
        if section_theme.get('philosopher') and relevant_philosophers:
            potential_related = [p for p in relevant_philosophers if p != section_theme['philosopher']]
            if potential_related:
                section_theme['related_philosopher'] = random.choice(potential_related)
        
        section_paragraphs = []
        section_concepts = set()
        section_terms = set()
        num_paragraphs = random.randint(2, 3)
        
        for j in range(num_paragraphs):
            # Create context for this paragraph that includes title themes and section theme
            paragraph_context = {
                'concepts': set() if j == 0 else section_concepts,
                'terms': set() if j == 0 else section_terms,
                'section': section_theme.get('concept', 'general'),
                'philosophers': [section_theme.get('philosopher'), section_theme.get('related_philosopher')],
                'title_themes': title_themes,
                'relevant_philosophers': relevant_philosophers,
                'section_theme': section_theme
            }
            
            paragraph_text, paragraph_concepts, paragraph_terms = generate_paragraph(
                "general", random.randint(6, 10), all_references,
                used_quotes=used_quotes, note_system=note_system, context=paragraph_context
            )
            
            # Add metafictional elements with decreasing probability
            if j == num_paragraphs - 1 or random.random() < 0.4:
                paragraph_text = metafiction.insert_metafiction_in_paragraph(paragraph_text)
            
            # Apply capitalization fix
            paragraph_text = ensure_proper_capitalization_with_italics(paragraph_text)
            
            # Apply italicization to terms
            paragraph_text = italicize_terms_in_text(paragraph_text)
            
            section_paragraphs.append(paragraph_text)
            section_concepts.update(paragraph_concepts)
            section_terms.update(paragraph_terms)
            coherence_manager.record_usage(concepts=paragraph_concepts, terms=paragraph_terms)
        
        # Generate a section title that relates to both the main title and section content
        raw_section_title = generate_section_title(section_paragraphs, coherence_manager, 
                                                 section_theme, title_themes)
        section_title = apply_title_case(raw_section_title)
        
        essay_parts.append(f"## {section_title}\n\n")
        essay_parts.append('\n\n'.join(section_paragraphs) + "\n\n")

    # Conclusion with enhanced self-reference
    # Use primary concepts and terms from the title for the conclusion
    conclusion_context = {
        'concepts': title_themes['primary_concepts'][:2] if title_themes['primary_concepts'] 
                   else coherence_manager.primary_concepts[:2],
        'terms': title_themes['primary_terms'][:2] if title_themes['primary_terms'] 
                else coherence_manager.primary_terms[:2],
        'section': 'conclusion',
        'title_themes': title_themes,
        'relevant_philosophers': relevant_philosophers
    }
    
    conclusion_text, conclusion_concepts, conclusion_terms = generate_paragraph(
        "conclusion", random.randint(6, 8), all_references,
        used_quotes=used_quotes, note_system=note_system, context=conclusion_context
    )
    
    coherence_manager.record_usage(concepts=conclusion_concepts, terms=conclusion_terms)
    
    # Add metafictional conclusion that references title themes
    metafictional_conclusion = metafiction.generate_metafictional_conclusion(
        title_themes['primary_concepts'] + title_themes['related_concepts'],
        title_themes['primary_terms']
    )
    conclusion_text += ' ' + metafictional_conclusion
    
    # Apply capitalization fix
    conclusion_text = ensure_proper_capitalization_with_italics(conclusion_text)
    
    # Apply italicization to terms
    conclusion_text = italicize_terms_in_text(conclusion_text)
    
    essay_parts.append("## Conclusion\n\n")
    essay_parts.append(conclusion_text + "\n\n")

    # Generate Works Cited and Notes sections
    notes_section = note_system.generate_notes_section()
    works_cited_section = note_system.generate_works_cited_section()
    
    # Add Notes first, then Works Cited - per MLA 9 guidelines
    if notes_section:
        essay_parts.append(notes_section)

    if works_cited_section:
        essay_parts.append(works_cited_section)
    
    # Combine all parts into the essay text
    essay_text = ''.join(essay_parts)
    
    # Final pass: ensure all headings have proper title case
    essay_text = format_headings_with_title_case(essay_text)
    
    return essay_text

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

def generate_section_title(section_paragraphs, coherence_manager, section_theme, title_themes=None):
    """
    Generate a section title based on content and thematic focus, related to main title.
    
    Args:
        section_paragraphs: The content of the section
        coherence_manager: The EssayCoherence instance
        section_theme: The thematic focus for the section
        title_themes (dict): Themes from the main title
        
    Returns:
        str: A raw section title (will be formatted with title case later)
    """
    # Use philosopher from section theme or pick a relevant one
    philosopher = section_theme.get('philosopher', random.choice(philosophers))
    
    # Use concept from section theme (which should already be from the dialectic progression)
    concept = section_theme.get('concept', coherence_manager.get_weighted_concept())
    
    # Use term from title themes if available, otherwise from section theme
    if title_themes and title_themes['primary_terms'] and random.random() < 0.7:
        term = random.choice(title_themes['primary_terms'])
    else:
        term = section_theme.get('term', coherence_manager.get_weighted_term())
    
    # More sophisticated section title templates that relate to main themes
    section_templates = [
        f"{philosopher} and the Politics of {concept}",
        f"The {random.choice(['Dialectic', 'Discourse', 'Problematic'])} of {concept} in {philosopher}'s Theory of {term}",
        f"{concept} as {term}: {random.choice(['Reading', 'Rethinking', 'Reimagining'])} {philosopher}",
        f"{random.choice(['Beyond', 'After', 'Against'])} {concept}: {philosopher} on {term}",
        f"{term} and its {random.choice(['Discontents', 'Others', 'Limits'])}: {philosopher}'s {concept}",
        f"The {random.choice(['Question', 'Problem', 'Aporia'])} of {term} in {philosopher}'s {concept}",
        f"{philosopher}'s {concept}: {random.choice(['Toward', 'Towards', 'Beyond'])} a Theory of {term}",
        f"{concept}/{term}: {philosopher} and the {random.choice(['Politics', 'Poetics', 'Ethics'])} of {random.choice(['Difference', 'Identity', 'Representation', 'Resistance'])}",
        f"{term} in the Age of {concept}: {random.choice(['Reading', 'Rethinking', 'Reimagining'])} {philosopher}",
        f"The {random.choice(['End', 'Death', 'Future', 'Return'])} of {concept}: {philosopher} and {term}"
    ]
    
    # If we have title themes, add some templates that specifically reference them
    if title_themes and title_themes['primary_concepts']:
        primary_title_concept = title_themes['primary_concepts'][0]
        title_specific_templates = [
            f"{concept} and {primary_title_concept}: {philosopher}'s Intervention",
            f"Rethinking {term} through {primary_title_concept}: {philosopher}'s Approach",
            f"{philosopher} on {concept}: Implications for {primary_title_concept}",
            f"The Relation of {concept} to {primary_title_concept} in {philosopher}'s Work"
        ]
        # Add these templates with a higher chance of selection
        for _ in range(3):  # Add multiple times to increase probability
            section_templates.append(random.choice(title_specific_templates))
    
    title = random.choice(section_templates)
    
    # Record usage
    coherence_manager.record_usage(
        philosophers=[philosopher],
        concepts=[concept],
        terms=[term]
    )
    
    return title