"""
A module for generating academic references in a postmodern context.
This module creates a variety of academic references, including books, journal articles,
chapters in edited volumes, and conference papers.
The references are designed to reflect the complexity and depth of postmodern discourse,
while also adhering to MLA 9 style citation conventions.
It includes functions to generate titles, references, and work types,
as well as a function to generate a complete works cited.
"""

import random
import string
from json_data_provider import (philosophers as RAW_PHILOSOPHERS_FROM_DATA, concepts, terms, contexts, adjectives,
                               bibliography_title_templates, publishers, academic_journals,
                               conferences, locations, philosopher_key_works, NON_STANDARD_AUTHOR_FORMATS,
                               verbs, nouns, philosopher_concepts)
from capitalization import apply_title_case

# Create a cleaned, definitive list of philosophers for use within this module's fallbacks
CLEANED_PHILOSOPHERS_REF = [
    p for p in RAW_PHILOSOPHERS_FROM_DATA
    if p and isinstance(p, str) and len(p.strip().replace(".", "")) > 1
]
if not CLEANED_PHILOSOPHERS_REF:  # Fallback if cleaning results in an empty list
    CLEANED_PHILOSOPHERS_REF = ["Michel Foucault", "Judith Butler", "Jacques Derrida", "Slavoj Žižek"]

# Placeholder definitions for variables used in this module but not sourced from data.py
# REMOVE the local generic publishers list; we'll use the one from data.py
# publishers = ["Academic Press", "University Press", "Scholarly Books"] 

# Use slightly more varied placeholder names, or make it clear these are placeholders
first_names = ["Evelyn", "Alex", "Kai", "Sam", "Rowan", "Jordan", "Casey", "Morgan"]
last_names = ["Reed", "Hayes", "Chen", "Sinclair", "Al-Jamil", "Valerio", "Ortega", "Petrov"]

# From prominent philosophers to cite
# philosopher_names = [p.split()[-1] for p in philosophers] # No longer needed here directly if philosophers list is used

def strip_markdown_italics(text: str) -> str:
    """Remove markdown italics (asterisks or underscores) from a string."""
    if not isinstance(text, str): # Handle cases where text might not be a string
        return str(text)
    return text.replace('*', '').replace('_', '')

def generate_full_name():
    """Generate a complete author name."""
    first = random.choice(first_names)
    last = random.choice(last_names)
    return f"{last}, {first}"

def generate_title(fixed_philosopher=None, concept_hint=None, term_hint=None):
    """
    Generate an authentic, academic-sounding title using templates and word pools.
    Allows specifying a philosopher and concept to guide title generation.
    Ensures concepts/terms are appropriate for the given philosopher if one is specified.
    """
    philosopher_for_title = fixed_philosopher if fixed_philosopher else random.choice(CLEANED_PHILOSOPHERS_REF if CLEANED_PHILOSOPHERS_REF else ["Michel Foucault"])

    # Get concepts and terms specific to this philosopher
    philosopher_specific_concepts = philosopher_concepts.get(philosopher_for_title, [])
    # Using philosopher_specific_concepts also for terms for now, assuming terms are a subset or similar
    philosopher_specific_terms = philosopher_specific_concepts 

    concept_choice = "a key concept" # Default fallback
    if concept_hint and philosopher_specific_concepts and concept_hint in philosopher_specific_concepts:
        concept_choice = concept_hint
    elif concept_hint and not philosopher_specific_concepts: # Philosopher has no specific concepts, but hint given
        concept_choice = concept_hint # Use hint if it aligns with global concepts, or it's a general word
    elif philosopher_specific_concepts:
        concept_choice = random.choice(philosopher_specific_concepts)
    elif concepts: # Fallback to global concepts if philosopher has none and no valid hint
        concept_choice = random.choice(concepts)

    term_choice = "a central term" # Default fallback
    if term_hint and philosopher_specific_terms and term_hint in philosopher_specific_terms:
        term_choice = term_hint
    elif term_hint and not philosopher_specific_terms:
        term_choice = term_hint
    elif philosopher_specific_terms:
        term_choice = random.choice(philosopher_specific_terms)
    elif terms: # Fallback to global terms
        term_choice = random.choice(terms)

    # Attempt to choose a template that fits the available data (e.g., if no specific concepts for philosopher)
    # This is a simplified approach; more sophisticated template selection could be added.
    chosen_template = None
    if not philosopher_specific_concepts or not philosopher_specific_terms:
        # Try to find templates that don't require concepts or terms, or only philosopher
        simple_templates = [t for t in bibliography_title_templates if '{concept}' not in t and '{term}' not in t]
        if simple_templates:
            chosen_template = random.choice(simple_templates)
    if not chosen_template:
        chosen_template = random.choice(bibliography_title_templates)
    
    template = chosen_template
    keys_in_template = [item[1] for item in string.Formatter().parse(template) if item[1] is not None]

    format_args = {
        'verb': random.choice(verbs) if verbs else "explores",
        'noun': random.choice(nouns) if nouns else "discourse",
        'adj': random.choice(adjectives) if adjectives else "critical",
        'context': random.choice(contexts) if contexts else "contemporary thought",
        'philosopher': philosopher_for_title,
        'philosopher1': philosopher_for_title
    }

    # Populate concept/term related fields carefully
    if 'concept' in keys_in_template: format_args['concept'] = concept_choice
    if 'term' in keys_in_template: format_args['term'] = term_choice
    if 'concept1' in keys_in_template: format_args['concept1'] = concept_choice
    if 'term1' in keys_in_template: format_args['term1'] = term_choice

    if 'concept2' in keys_in_template:
        if philosopher_specific_concepts and len(philosopher_specific_concepts) > 1:
            format_args['concept2'] = random.choice([c for c in philosopher_specific_concepts if c != concept_choice] or philosopher_specific_concepts)
        elif concepts and concept_choice in concepts:
             format_args['concept2'] = random.choice([c for c in concepts if c != concept_choice] or concepts)
        else:
            format_args['concept2'] = random.choice(concepts) if concepts else "another key idea"
    
    if 'term2' in keys_in_template:
        if philosopher_specific_terms and len(philosopher_specific_terms) > 1:
            format_args['term2'] = random.choice([t for t in philosopher_specific_terms if t != term_choice] or philosopher_specific_terms)
        elif terms and term_choice in terms:
            format_args['term2'] = random.choice([t for t in terms if t != term_choice] or terms)
        else:
            format_args['term2'] = random.choice(terms) if terms else "another central notion"

    if 'philosopher2' in keys_in_template:
        other_philosophers = [p for p in CLEANED_PHILOSOPHERS_REF if p != philosopher_for_title]
        format_args['philosopher2'] = random.choice(other_philosophers) if other_philosophers else random.choice(CLEANED_PHILOSOPHERS_REF if CLEANED_PHILOSOPHERS_REF else ["Judith Butler"])
    
    # Ensure all keys required by the template are present in format_args, with generic fallbacks
    valid_args = {}
    for key in keys_in_template:
        if key in format_args:
            valid_args[key] = format_args[key]
        else: # Add generic fallback if a key required by template wasn't populated
            if key.startswith('concept'): valid_args[key] = "a relevant concept"
            elif key.startswith('term'): valid_args[key] = "a relevant term"
            elif key.startswith('philosopher'): valid_args[key] = random.choice(CLEANED_PHILOSOPHERS_REF if CLEANED_PHILOSOPHERS_REF else ["a thinker"])
            elif key == 'adj': valid_args[key] = "noteworthy"
            elif key == 'verb': valid_args[key] = "discusses"
            elif key == 'noun': valid_args[key] = "perspective"
            elif key == 'context': valid_args[key] = "its field"
            else: valid_args[key] = "an aspect" # Default for any other unexpected key

    raw_title = template.format(**valid_args)
    title = apply_title_case(raw_title)
    return title

def generate_reference(author_name=None, title_hint=None):
    """
    Generate a reference with a randomly selected work type in MLA 9 style format.
    If author_name is provided, that author will be used.
    If title_hint is provided, it will influence the title generation.
    
    Work types included:
        - Book
        - Journal article
        - Chapter in edited volume
        - Conference paper
    
    Returns:
        str: A formatted reference string following MLA 9 guidelines.
    """
    work_type = random.choice(["book", "journal", "chapter", "conference"])
    
    actual_author_name_for_reference = None
    title_concept_for_generation = None
    is_known_philosopher_author = False

    # Determine author name: if none, select a random one
    # THIS IS A CRITICAL FALLBACK - ENSURE IT CHOOSES FROM A CLEANED LIST
    if author_name is None:
        if CLEANED_PHILOSOPHERS_REF:
            author_name = random.choice(CLEANED_PHILOSOPHERS_REF)
        else:
            # Absolute fallback if CLEANED_PHILOSOPHERS_REF is somehow empty (should not happen)
            author_name = "Michel Foucault" # Default to a known good name
    elif not isinstance(author_name, str) or len(author_name.strip().replace(".","")) <=1:
        # If a bad author_name (e.g. single initial) was somehow passed, override it.
        if CLEANED_PHILOSOPHERS_REF:
            author_name = random.choice(CLEANED_PHILOSOPHERS_REF)
        else:
            author_name = "Judith Butler" # Different default for clarity

    if author_name:
        actual_author_name_for_reference = author_name
        # Format name as Last, First if it's a full name
        name_parts = actual_author_name_for_reference.split()
        if len(name_parts) > 1 and ',' not in actual_author_name_for_reference:
            author_display = f"{name_parts[-1]}, {' '.join(name_parts[:-1])}"
        else:
            author_display = actual_author_name_for_reference
        
        if actual_author_name_for_reference.lower() == "bell hooks":
            author_display = "hooks, bell"
        
        is_known_philosopher_author = actual_author_name_for_reference in CLEANED_PHILOSOPHERS_REF
        if is_known_philosopher_author and actual_author_name_for_reference in philosopher_key_works and philosopher_key_works[actual_author_name_for_reference]:
            title_concept_for_generation = random.choice(philosopher_key_works[actual_author_name_for_reference])
        elif title_hint:
            # Simplified: use the first part of the hint if it seems like a concept phrase
            title_concept_for_generation = title_hint.split(" and ")[0] if " and " in title_hint else title_hint

    else: # No author_name provided, 75% chance of using a philosopher from data
        if random.random() < 0.75:
            chosen_philosopher = random.choice(CLEANED_PHILOSOPHERS_REF if CLEANED_PHILOSOPHERS_REF else ["Jacques Derrida"])
            actual_author_name_for_reference = chosen_philosopher
            name_parts = chosen_philosopher.split()
            if len(name_parts) > 1:
                author_display = f"{name_parts[-1]}, {' '.join(name_parts[:-1])}"
            else:
                author_display = chosen_philosopher
            if chosen_philosopher.lower() == "bell hooks":
                author_display = "hooks, bell"
            
            is_known_philosopher_author = True
            if chosen_philosopher in philosopher_key_works and philosopher_key_works[chosen_philosopher]:
                title_concept_for_generation = random.choice(philosopher_key_works[chosen_philosopher])
            elif title_hint:
                 title_concept_for_generation = title_hint.split(" and ")[0] if " and " in title_hint else title_hint
        else:
            # Generate a plausible academic author name
            author_display = generate_full_name()
            actual_author_name_for_reference = author_display # Store for consistency, though not a philosopher
            if title_hint:
                title_concept_for_generation = title_hint.split(" and ")[0] if " and " in title_hint else title_hint
    
    # Title Generation
    if title_hint and len(title_hint.split()) > 3: # If hint is substantial, use it as title
        processed_title = apply_title_case(title_hint)
    else:
        # Generate title, using the determined author if they are a known philosopher
        # and any concept hint derived from title_hint or philosopher's specialties.
        philosopher_to_pass_to_title_gen = actual_author_name_for_reference if is_known_philosopher_author else None
        processed_title = generate_title(fixed_philosopher=philosopher_to_pass_to_title_gen, concept_hint=title_concept_for_generation)
    
    final_title = strip_markdown_italics(processed_title) # Ensure stripping always happens

    year = random.randint(1950, 2023)
    
    author_period = "" if author_display.endswith(".") else "."
    
    if work_type == "book":
        publisher = random.choice(publishers)
        # Italicize the entire title for books
        reference = f"{author_display}{author_period} *{final_title}*. {publisher}, {year}."
    
    elif work_type == "journal":
        raw_journal_name = random.choice(academic_journals)
        journal_name = strip_markdown_italics(raw_journal_name) # Strip italics from journal name
        volume = random.randint(1, 50)
        issue = random.randint(1, 12)
        start_page = random.randint(1, 100)
        end_page = start_page + random.randint(10, 45)
        # Journal article titles are in quotes, journal names are italicized
        reference = f'{author_display}{author_period} "{final_title}." *{journal_name}*, vol. {volume}, no. {issue}, {year}, pp. {start_page}-{end_page}.'
    
    elif work_type == "chapter":
        editor = generate_full_name()
        # Generate a book title, possibly using the same author/concept if relevant
        book_title_philosopher = actual_author_name_for_reference if is_known_philosopher_author and random.random() < 0.5 else None
        book_title_concept = title_concept_for_generation if random.random() < 0.5 else None
        raw_book_title = generate_title(fixed_philosopher=book_title_philosopher, concept_hint=book_title_concept)
        book_title = strip_markdown_italics(raw_book_title) # Strip italics from book title
        start_page = random.randint(1, 100)
        end_page = start_page + random.randint(10, 45)
        publisher = random.choice(publishers)
        # Chapter titles are in quotes, book titles are italicized
        reference = f'{author_display}{author_period} "{final_title}." *{book_title}*, edited by {editor}, {publisher}, {year}, pp. {start_page}-{end_page}.'
    
    elif work_type == "conference":
        conference_name = random.choice(conferences)
        location = random.choice(locations)
        start_date = random.randint(1, 28)
        month = random.choice(["Jan.", "Feb.", "Mar.", "Apr.", "May", "June", "July", "Aug.", "Sept.", "Oct.", "Nov.", "Dec."])
        reference = f'{author_display}{author_period} "{final_title}." {conference_name}, {location}, {start_date} {month} {year}.'
    
    return reference 