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
from json_data_provider import philosophers, concepts, terms, philosopher_concepts, thematic_clusters
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

# Define constants for sentence counts per paragraph
MIN_SENTENCES_PER_PARAGRAPH = 7
MAX_SENTENCES_PER_PARAGRAPH = 10
MIN_PARAGRAPHS_PER_SECTION = 2 # Define if not already defined
MAX_PARAGRAPHS_PER_SECTION = 4 # Define if not already defined

def extract_themes_from_title(raw_title, concepts, terms, coherence_manager=None):
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

    title_themes['primary_concepts'] = list(dict.fromkeys(title_themes['primary_concepts']))
    title_themes['primary_terms'] = [
        term for term in dict.fromkeys(title_themes['primary_terms'])
        if term not in title_themes['primary_concepts']
    ]
    
    # If we still don't have enough themes, add some random ones
    # but with less weight than the ones directly from the title
    if len(title_themes['primary_concepts']) < 2:
        preferred_concepts = (
            coherence_manager.active_theme_data.get('key_concepts', [])
            if coherence_manager and coherence_manager.active_theme_key
            else concepts
        )
        available_additional_concepts = [c for c in preferred_concepts if c not in title_themes['primary_concepts']]
        if not available_additional_concepts:
            available_additional_concepts = [c for c in concepts if c not in title_themes['primary_concepts']]
        additional_concepts = random.sample(
            available_additional_concepts,
            min(2, len(available_additional_concepts))
        )
        title_themes['related_concepts'].extend(additional_concepts)
    
    if len(title_themes['primary_terms']) < 2:
        preferred_terms = (
            coherence_manager.active_theme_data.get('relevant_terms', [])
            if coherence_manager and coherence_manager.active_theme_key
            else terms
        )
        available_additional_terms = [
            t for t in preferred_terms
            if t not in title_themes['primary_terms'] and t not in title_themes['primary_concepts']
        ]
        if not available_additional_terms:
            available_additional_terms = [
                t for t in terms
                if t not in title_themes['primary_terms'] and t not in title_themes['primary_concepts']
            ]
        title_themes['primary_terms'].extend(
            random.sample(available_additional_terms, min(2, len(available_additional_terms)))
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
    # Keep title construction tightly theme-local whenever an active theme exists.
    primary_concept = coherence_manager.get_surface_concept()
    primary_term = coherence_manager.get_surface_term(exclude={primary_concept})

    theme_local_concepts = []
    if coherence_manager.active_theme_key:
        theme_local_concepts = [
            concept for concept in coherence_manager.active_theme_data.get('key_concepts', [])
            if concept != primary_concept
        ]

    secondary_concept = None
    if theme_local_concepts:
        secondary_concept = coherence_manager.get_weighted_concept(
            exclude={primary_concept},
            subset=theme_local_concepts
        )
    if not secondary_concept:
        secondary_concept = (
            coherence_manager.get_related_concept(primary_concept, exclude={primary_concept})
            or coherence_manager.get_surface_concept(exclude={primary_concept}, fallback_to_general=False)
            or coherence_manager.get_surface_concept(exclude={primary_concept})
        )

    oppositional_concept = None
    if theme_local_concepts:
        oppositional_concept = coherence_manager.get_weighted_concept(
            exclude={primary_concept, secondary_concept},
            subset=[concept for concept in theme_local_concepts if concept != secondary_concept]
        )
    if not oppositional_concept:
        oppositional_concept = (
            coherence_manager.get_oppositional_concept(primary_concept, exclude={primary_concept})
            or coherence_manager.get_surface_concept(exclude={primary_concept, secondary_concept}, fallback_to_general=False)
            or coherence_manager.get_surface_concept(exclude={primary_concept, secondary_concept})
        )

    title_context = coherence_manager.get_theme_title_context_label() or primary_term

    # More sophisticated title templates
    title_templates = [
        f"The {title_context} of {primary_concept}: {random.choice(['Toward', 'Towards', 'Interrogating', 'Rethinking', 'Reimagining'])} {primary_term}",
        f"{primary_concept} and {primary_term}: {random.choice(['Beyond', 'After', 'Against', 'Within', 'Between'])} {secondary_concept}",
        f"{random.choice(['Deconstructing', 'Problematizing', 'Negotiating', 'Tracing', 'Mapping'])} {primary_concept}: {primary_term} in {title_context}",
        f"The {random.choice(['Impossibility', 'Possibility', 'Crisis', 'Politics', 'Poetics'])} of {primary_term}: {primary_concept} and its {random.choice(['Discontents', 'Others', 'Afterlives', 'Limits', 'Futures'])}",
        f"{primary_concept}/{primary_term}: {random.choice(['Towards', 'Beyond', 'After', 'Against'])} {title_context}",
        f"{random.choice(['Reading', 'Writing', 'Theorizing', 'Thinking', 'Performing'])} {primary_concept} {random.choice(['After', 'Through', 'Against', 'With', 'Beyond'])} {primary_term}",
        f"{random.choice(['The End of', 'After', 'Beyond', 'Against', 'Rethinking'])} {primary_concept}: {primary_term} and {secondary_concept}"
    ]
    
    raw_title = random.choice(title_templates)
    
    # Record usage of concepts and terms in the title
    coherence_manager.record_usage(
        concepts=[primary_concept, secondary_concept, oppositional_concept],
        terms=[primary_term]
    )
    
    return raw_title

def generate_essay(theme_key=None, metafiction_level='moderate'):
    """Generate the full essay with enhanced internal reasoning, proper capitalization, and coherent notes."""
    # Initialize coherence manager for thematic unity
    coherence_manager = EssayCoherence(theme_key=theme_key)
    
    # Initialize note system for managing citations and bibliography
    note_system = NoteSystem(coherence_manager=coherence_manager)
    note_system.reset() # Reset note system state
    
    essay_parts = []
    used_quotes = set() # Initialize used_quotes here

    # Title with greater sophistication
    raw_title = generate_title(coherence_manager)
    # Apply title case without running through the regular capitalization system
    title = apply_title_case(raw_title)
    essay_parts.append(f"# {title}\n\n")
    
    # Extract the main themes from the title for consistent usage
    title_themes = extract_themes_from_title(raw_title, concepts, terms, coherence_manager=coherence_manager)
    
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

    # Body sections with dialectical development - determine count early for intro context
    num_body_sections = random.randint(3, 5)

    # Start with a primary concept from the title if available
    starting_concept = (title_themes['primary_concepts'][0] if title_themes['primary_concepts']
                       else coherence_manager.get_surface_concept()
                       if coherence_manager
                       else coherence_manager.primary_concepts[0] if coherence_manager.primary_concepts 
                       else random.choice(concepts))
    
    # Generate Introduction section
    num_intro_paragraphs = random.randint(1, 2)  # Usually 1-2 paragraphs for introduction
    coherence_manager.advance_section()  # Track introduction section
    
    for intro_index in range(num_intro_paragraphs):
        num_sentences = random.randint(MIN_SENTENCES_PER_PARAGRAPH - 2, MAX_SENTENCES_PER_PARAGRAPH - 1)
        if num_sentences < 4: num_sentences = 4  # Ensure introduction is substantial
        
        # Introduction context includes overall essay themes and relevant philosophers
        intro_context = {
            'section_index': 0,  # Introduction is the first section
            'total_sections': num_body_sections + 2,  # intro + body + conclusion
            'theme_concept': starting_concept,  # Use the starting concept that will drive the essay
            'theme_term': coherence_manager.get_surface_term(exclude={starting_concept}),
            'title_themes': title_themes,
            'relevant_philosophers': relevant_philosophers,
            'is_introduction': True,  # Flag to help paragraph generation recognize this as introduction
            'force_theme_local': True,
            'paragraph_id': f"introduction-{intro_index}"
        }
        
        intro_paragraph, intro_concepts, intro_philosophers = generate_paragraph(
            template_type='introduction',  # Use introduction template type
            num_sentences=num_sentences,
            mentioned_philosophers=note_system.get_mentioned_philosophers(),
            used_quotes=used_quotes,
            note_system=note_system,
            context=intro_context,
            coherence_manager=coherence_manager
        )
        essay_parts.append(intro_paragraph + "\n\n")
        
        # Record usage for introduction elements
        if intro_concepts:
            coherence_manager.record_usage(concepts=intro_concepts)
        if intro_philosophers:
            coherence_manager.record_usage(philosophers=intro_philosophers)
    
    # Generate the sequence of concepts for body sections using the advanced dialectic
    section_concepts = coherence_manager.develop_dialectic(starting_concept, num_steps=num_body_sections)

    # Ensure section_concepts has enough items, pad if necessary with weighted concepts
    # This is a safeguard in case develop_dialectic returns fewer than num_body_sections.
    if len(section_concepts) < num_body_sections:
        needed = num_body_sections - len(section_concepts)
        for _ in range(needed):
            # Exclude concepts already in the progression to ensure variety
            fallback_concept = coherence_manager.get_surface_concept(exclude=set(section_concepts))
            if fallback_concept:
                section_concepts.append(fallback_concept)
            else:
                # If still no fallback, pick any concept not already used (very rare)
                available_fallbacks = [c for c in concepts if c not in section_concepts]
                if available_fallbacks:
                    section_concepts.append(random.choice(available_fallbacks))
                else: # Absolute last resort, repeat last concept (should almost never happen)
                    section_concepts.append(section_concepts[-1] if section_concepts else random.choice(concepts))

    section_counter = 0
    for i in range(num_body_sections):
        section_theme_concept = section_concepts[i]
        section_counter += 1
        section_paragraphs = []
        num_paragraphs_in_section = random.randint(MIN_PARAGRAPHS_PER_SECTION, MAX_PARAGRAPHS_PER_SECTION)
        
        # Advance section tracking in coherence manager
        coherence_manager.advance_section()
        
        # Refresh theme weights periodically to maintain thematic coherence
        if i > 0 and i % 2 == 0:  # Every second section
            coherence_manager.refresh_theme_weights()
        
        # Context for this section, including the main concept for the section
        # and philosophers relevant to the overall essay title
        section_context = {
            'section_index': i + 1,
            'total_sections': num_body_sections,
            'theme_concept': section_theme_concept, # The core concept for this section from dialectic
            'title_themes': title_themes, # Overall title themes for broader context
            'relevant_philosophers': relevant_philosophers, # Philosophers from title
            'section_length': num_paragraphs_in_section,
            'essay_length': num_body_sections + 2  # intro + body + conclusion
        }

        for j in range(num_paragraphs_in_section):
            num_sentences = random.randint(MIN_SENTENCES_PER_PARAGRAPH, MAX_SENTENCES_PER_PARAGRAPH)
            paragraph_context = section_context.copy()
            paragraph_context['paragraph_id'] = f"section-{i + 1}-paragraph-{j}"
            paragraph_context['force_theme_local'] = (j == 0)
            if j == 0:
                paragraph_context['theme_term'] = coherence_manager.get_surface_term(exclude={section_theme_concept})
            # Pass coherence_manager and section_context to paragraph generation
            paragraph_text, paragraph_concepts, paragraph_philosophers = generate_paragraph(
                template_type='general', 
                num_sentences=num_sentences, 
                forbidden_philosophers=[], # Manage forbidden items at a higher level or within paragraph if needed
                forbidden_concepts=[c for c in section_concepts if c != section_theme_concept], # Avoid other section themes strongly
                mentioned_philosophers=note_system.get_mentioned_philosophers(),
                used_quotes=used_quotes, # Pass used_quotes
                note_system=note_system,
                context=paragraph_context, # Pass section-specific context
                coherence_manager=coherence_manager
            )
            section_paragraphs.append(paragraph_text)
            
            # Record usage of concepts and philosophers from the paragraph for weight adjustment
            if paragraph_concepts:
                coherence_manager.record_usage(concepts=paragraph_concepts)
                # Detect dialectical moments for each concept used
                for concept in paragraph_concepts:
                    coherence_manager.detect_dialectical_moment(concept, paragraph_text)
            if paragraph_philosophers:
                coherence_manager.record_usage(philosophers=paragraph_philosophers)
            
            # Enhanced metafictional element insertion with contextual awareness
            dialectical_context = coherence_manager.get_dialectical_context()
            section_context_for_meta = {
                'section_length': num_paragraphs_in_section,
                'essay_length': num_body_sections + 2,
                'metafiction_count_this_section': coherence_manager.metafiction_count_per_section[coherence_manager.section_index]
            }
            
            meta_text = metafiction.insert_metafiction_in_paragraph(
                section_paragraphs[-1], 
                theme_key=theme_key, 
                coherence_manager=coherence_manager,
                metafiction_level=metafiction_level,
                section_context=section_context_for_meta,
                dialectical_context=dialectical_context
            )
            if meta_text != section_paragraphs[-1]:  # Metafiction was added
                section_paragraphs[-1] = meta_text
                coherence_manager.record_metafiction_usage()

        # Generate section title based on content and section theme
        section_title_text = generate_section_title(section_paragraphs, coherence_manager, section_theme_concept, title_themes)
        essay_parts.append(f"## {section_title_text}\n\n")
        essay_parts.extend([p + "\n\n" for p in section_paragraphs])

    # Conclusion
    essay_parts.append("## Conclusion\n\n")
    coherence_manager.advance_section()  # Track conclusion section
    num_conclusion_paragraphs = random.randint(1, MAX_PARAGRAPHS_PER_SECTION -1) # Typically 1-2 paragraphs
    for conclusion_index in range(num_conclusion_paragraphs):
        num_sentences = random.randint(MIN_SENTENCES_PER_PARAGRAPH -1, MAX_SENTENCES_PER_PARAGRAPH -1)
        if num_sentences < 3: num_sentences = 3 # Ensure conclusion is not too short
        
        # Conclusion context can be simpler or refer to overall themes
        conclusion_context = {
            'section_index': num_body_sections + 1, # After last body section
            'total_sections': num_body_sections + 1, # Intro + Body + Conclusion
            'theme_concept': coherence_manager.get_weighted_concept(subset=coherence_manager.used_concepts or None),
            'theme_term': coherence_manager.get_surface_term(),
            'title_themes': title_themes,
            'relevant_philosophers': relevant_philosophers,
            'paragraph_id': f"conclusion-{conclusion_index}"
        }
        
        conclusion_paragraph, conclusion_concepts, conclusion_philosophers = generate_paragraph(
            template_type='conclusion', 
            num_sentences=num_sentences, 
            mentioned_philosophers=note_system.get_mentioned_philosophers(),
            used_quotes=used_quotes, # Pass used_quotes
            note_system=note_system,
            context=conclusion_context,
            coherence_manager=coherence_manager
        )
        essay_parts.append(conclusion_paragraph + "\n\n")
        
        # Record usage for conclusion elements too
        if conclusion_concepts:
            coherence_manager.record_usage(concepts=conclusion_concepts)
        if conclusion_philosophers:
            coherence_manager.record_usage(philosophers=conclusion_philosophers)
    
    # Add a final metafictional statement to the conclusion if desired
    # Store the last conclusion paragraph without trailing newlines for potential concatenation
    last_conclusion_paragraph = essay_parts.pop().rstrip() if essay_parts and essay_parts[-1].endswith("\n\n") else ""
    
    if num_conclusion_paragraphs > 0: # Ensure there was a conclusion paragraph to begin with
        current_conclusion_content = last_conclusion_paragraph
    else: # If no regular conclusion paragraphs were generated, start fresh
        current_conclusion_content = ""
        # Generate a basic conclusion paragraph if none exists and metafiction is added
        final_meta = metafiction.generate_metafictional_conclusion(
            coherence_manager.used_concepts, 
            coherence_manager.used_terms, 
            theme_key=theme_key, 
            coherence_manager=coherence_manager,
            metafiction_level=metafiction_level
        )
        if final_meta:  # Only proceed if metafiction was generated
            num_sentences = random.randint(MIN_SENTENCES_PER_PARAGRAPH - 2, MAX_SENTENCES_PER_PARAGRAPH - 2)
            if num_sentences < 2: num_sentences = 2
            conclusion_context = {
                'section_index': num_body_sections,
                'total_sections': num_body_sections + 1,
                'theme_concept': coherence_manager.get_weighted_concept(subset=coherence_manager.used_concepts or None),
                'title_themes': title_themes,
                'relevant_philosophers': relevant_philosophers
            }
            base_conclusion_paragraph, base_conclusion_concepts, base_conclusion_philosophers = generate_paragraph(
                template_type='conclusion',
                num_sentences=num_sentences,
                mentioned_philosophers=note_system.get_mentioned_philosophers(),
                used_quotes=used_quotes,
                note_system=note_system,
                context=conclusion_context,
                coherence_manager=coherence_manager
            )
            current_conclusion_content = base_conclusion_paragraph
            
            # Record usage for fallback conclusion elements too
            if base_conclusion_concepts:
                coherence_manager.record_usage(concepts=base_conclusion_concepts)
            if base_conclusion_philosophers:
                coherence_manager.record_usage(philosophers=base_conclusion_philosophers)

    # Enhanced metafictional conclusion generation
    final_meta = metafiction.generate_metafictional_conclusion(
        coherence_manager.used_concepts, 
        coherence_manager.used_terms, 
        theme_key=theme_key, 
        coherence_manager=coherence_manager,
        metafiction_level=metafiction_level
    )
    if final_meta:  # Only add if metafiction was generated
        processed_final_meta = ensure_proper_capitalization_with_italics(italicize_terms_in_text(final_meta))
        if current_conclusion_content:
             # Add a space only if current_conclusion_content is not empty
            current_conclusion_content += " " + processed_final_meta
        else:
            current_conclusion_content = processed_final_meta

    if current_conclusion_content: # Only append if there's something to append
        essay_parts.append(current_conclusion_content + "\n\n")

    # Works Cited / Bibliography
    notes_and_bibliography_section = note_system.generate_notes_section()
    if notes_and_bibliography_section:
        essay_parts.append(notes_and_bibliography_section)
    
    return "".join(essay_parts)

def generate_section_title(section_paragraphs, coherence_manager, section_theme_concept, title_themes=None):
    """
    Generate a sophisticated, context-aware section title using a template.
    Ensures the title is relevant to the section's content and overall essay themes.
    """
    templates = [
        "{concept1} and {term1}",
        "{concept1} in {context1}",
        "{philosopher1} on {concept1}",
        "{concept1}, {term1}, and {context1}",
        "{concept1} Beyond {term1}",
        "The {context1} of {concept1}"
    ]
    
    # section_theme_concept is the primary concept for this section's title
    primary_concept = section_theme_concept
    
    # Get a primary term related to the primary_concept or from coherence_manager
    if coherence_manager:
        primary_term = (
            coherence_manager.get_surface_term(exclude={primary_concept}, fallback_to_general=False)
            or coherence_manager.get_surface_term(exclude={primary_concept})
            or coherence_manager.get_weighted_term(exclude={primary_concept})
        )
    else:
        primary_term = random.choice([t for t in terms if t != primary_concept] or terms)

    if not primary_term: # Absolute fallback if term selection failed
        primary_term = random.choice([t for t in terms if t != primary_concept] or terms)

    # Get other concepts and terms, trying to use title_themes for relevance if available
    secondary_concept_candidates = []
    if title_themes:
        secondary_concept_candidates.extend(title_themes.get('primary_concepts', []))
        secondary_concept_candidates.extend(title_themes.get('related_concepts', []))
    if coherence_manager and coherence_manager.active_theme_key:
        secondary_concept_candidates.extend(coherence_manager.active_theme_data.get('key_concepts', []))
    # Filter out the primary_concept from candidates
    secondary_concept_candidates = [c for c in secondary_concept_candidates if c != primary_concept]
    if not secondary_concept_candidates: # Fallback if title_themes didn't provide suitable candidates
        if coherence_manager and coherence_manager.active_theme_key:
            secondary_concept_candidates = [
                c for c in coherence_manager.active_theme_data.get('key_concepts', [])
                if c != primary_concept
            ]
        if not secondary_concept_candidates:
            secondary_concept_candidates = [c for c in concepts if c != primary_concept]
    
    secondary_concept = random.choice(secondary_concept_candidates if secondary_concept_candidates else concepts) # Final fallback to all concepts

    secondary_term_candidates = []
    if title_themes:
        secondary_term_candidates.extend(title_themes.get('primary_terms', []))
    if coherence_manager and coherence_manager.active_theme_key:
        secondary_term_candidates.extend(coherence_manager.active_theme_data.get('relevant_terms', []))
    # Filter out the primary_term and concepts used as terms
    secondary_term_candidates = [t for t in secondary_term_candidates if t != primary_term and t != primary_concept and t != secondary_concept]
    if not secondary_term_candidates: # Fallback
        if coherence_manager and coherence_manager.active_theme_key:
            secondary_term_candidates = [
                t for t in coherence_manager.active_theme_data.get('relevant_terms', [])
                if t != primary_term and t != primary_concept and t != secondary_concept
            ]
        if not secondary_term_candidates:
            secondary_term_candidates = [t for t in terms if t != primary_term and t != primary_concept and t != secondary_concept]

    secondary_term = random.choice(secondary_term_candidates if secondary_term_candidates else terms) # Final fallback to all terms
        
    # Select a relevant philosopher
    # Prefer philosophers linked to the primary concept of the section, or from title_themes
    relevant_philosophers_for_section = find_relevant_philosophers([primary_concept], [primary_term], philosopher_concepts)
    if coherence_manager and coherence_manager.active_theme_key:
        active_theme_philosophers = set(coherence_manager.active_theme_data.get('core_philosophers', []))
        theme_relevant_philosophers = [
            philosopher for philosopher in relevant_philosophers_for_section
            if philosopher in active_theme_philosophers
        ]
        if theme_relevant_philosophers:
            relevant_philosophers_for_section = theme_relevant_philosophers
    if not relevant_philosophers_for_section and title_themes:
        relevant_philosophers_for_section = find_relevant_philosophers(
            title_themes.get('primary_concepts', []) + title_themes.get('related_concepts', []),
            title_themes.get('primary_terms', []),
            philosopher_concepts
        )
        if coherence_manager and coherence_manager.active_theme_key:
            active_theme_philosophers = set(coherence_manager.active_theme_data.get('core_philosophers', []))
            theme_relevant_philosophers = [
                philosopher for philosopher in relevant_philosophers_for_section
                if philosopher in active_theme_philosophers
            ]
            if theme_relevant_philosophers:
                relevant_philosophers_for_section = theme_relevant_philosophers

    philosopher = (
        random.choice(relevant_philosophers_for_section)
        if relevant_philosophers_for_section
        else coherence_manager.get_surface_philosopher() if coherence_manager
        else random.choice(philosophers)
    )

    context_word = coherence_manager.get_theme_title_context_label() if coherence_manager else None
    if not context_word:
        context_word = "theory"

    invalid_contexts = [phrase.lower() for phrase in coherence_manager.active_theme_data.get('context_phrases', [])] if coherence_manager and coherence_manager.active_theme_data else []

    for _ in range(5):
        template = random.choice(templates)
        raw_section_title = template.format(
            concept1=primary_concept,
            concept2=secondary_concept,
            term1=primary_term,
            term2=secondary_term,
            philosopher1=philosopher,
            context1=context_word
        )
        section_title = italicize_terms_in_text(apply_title_case(raw_section_title))
        cleaned_title = re.sub(r'[*"]', '', section_title)
        if len(cleaned_title.split()) > 16:
            continue
        if "(" in cleaned_title or ")" in cleaned_title:
            continue
        if any(phrase and phrase in cleaned_title.lower() for phrase in invalid_contexts):
            continue
        return section_title

    fallback_title = f"{primary_concept} and {primary_term}"
    return italicize_terms_in_text(apply_title_case(fallback_title))
