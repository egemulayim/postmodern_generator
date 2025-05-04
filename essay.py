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
from data import philosophers, concepts
from reference import generate_reference
from capitalization import (
    ensure_proper_capitalization_with_italics, 
    format_headings_with_title_case,
    italicize_terms_in_text,
    apply_title_case
)
from notes import NoteSystem
from abstract_generator import generate_enhanced_abstract

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

    # Generate a more comprehensive abstract with keywords
    abstract = generate_enhanced_abstract(coherence_manager)
    
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
    
    # Create a basic context for the introduction
    intro_context = {
        'section': 'introduction'
    }
    
    # Generate the introduction paragraph
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
    starting_concept = coherence_manager.primary_concepts[0] if coherence_manager.primary_concepts else random.choice(concepts)
    dialectic = coherence_manager.develop_dialectic(starting_concept, num_steps=num_body_sections - 1)
    
    for i in range(num_body_sections):
        # Get a thematic focus for this section that continues the dialectic
        section_theme = coherence_manager.get_section_theme()
        if i < len(dialectic):
            section_theme['concept'] = dialectic[i]
        
        section_paragraphs = []
        section_concepts = set()
        section_terms = set()
        num_paragraphs = random.randint(2, 3)
        
        for j in range(num_paragraphs):
            # Create context for this paragraph
            paragraph_context = {
                'concepts': set() if j == 0 else section_concepts,
                'terms': set() if j == 0 else section_terms,
                'section': section_theme.get('concept', 'general'),
                'philosophers': [section_theme.get('philosopher'), section_theme.get('related_philosopher')]
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
        
        # Generate a section title and apply title case appropriately
        raw_section_title = generate_section_title(section_paragraphs, coherence_manager, section_theme)
        section_title = apply_title_case(raw_section_title)
        
        essay_parts.append(f"## {section_title}\n\n")
        essay_parts.append('\n\n'.join(section_paragraphs) + "\n\n")

    # Conclusion with enhanced self-reference
    conclusion_context = {
        'concepts': coherence_manager.primary_concepts[:2],
        'terms': coherence_manager.primary_terms[:2],
        'section': 'conclusion'
    }
    
    conclusion_text, conclusion_concepts, conclusion_terms = generate_paragraph(
        "conclusion", random.randint(6, 8), all_references,
        used_quotes=used_quotes, note_system=note_system, context=conclusion_context
    )
    
    coherence_manager.record_usage(concepts=conclusion_concepts, terms=conclusion_terms)
    
    # Add metafictional conclusion
    metafictional_conclusion = metafiction.generate_metafictional_conclusion(
        coherence_manager.used_concepts, coherence_manager.used_terms
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

def generate_section_title(section_parts, coherence_manager, section_theme):
    """
    Generate a section title based on content and thematic focus.
    
    Args:
        section_parts: The content of the section
        coherence_manager: The EssayCoherence instance
        section_theme: The thematic focus for the section
    
    Returns:
        str: A raw section title (will be formatted with title case later)
    """
    philosopher = section_theme.get('philosopher', random.choice(philosophers))
    concept = section_theme.get('concept', coherence_manager.get_weighted_concept())
    term = section_theme.get('term', coherence_manager.get_weighted_term())
    
    # More sophisticated section title templates
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
    
    title = random.choice(section_templates)
    
    # Record usage
    coherence_manager.record_usage(
        philosophers=[philosopher],
        concepts=[concept],
        terms=[term]
    )
    
    # Return raw title (will be formatted with title case later)
    return title