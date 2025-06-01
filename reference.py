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
from json_data_provider import (philosophers as RAW_PHILOSOPHERS_FROM_DATA, concepts, terms, adjectives,
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
first_names = ["Evelyn", "Alex", "Kai", "Sam", "Rowan", "Jordan", "Casey", "Morgan", "Taylor", "Drew"]
last_names = ["Reed", "Hayes", "Chen", "Sinclair", "Al-Jamil", "Valerio", "Ortega", "Petrov", "Kim", "Garcia"]

# From prominent philosophers to cite
# philosopher_names = [p.split()[-1] for p in philosophers] # No longer needed here directly if philosophers list is used

def strip_markdown_italics(text: str) -> str:
    """Remove markdown italics (asterisks or underscores) from a string."""
    if not isinstance(text, str): # Handle cases where text might not be a string
        return str(text)
    return text.replace('*', '').replace('_', '')

def generate_full_name():
    """Generate a complete author name. Ensures a non-empty, plausible name."""
    first = random.choice(first_names) if first_names else "Alex"
    last = random.choice(last_names) if last_names else "Researcher"
    return f"{last}, {first}"

def generate_title(fixed_philosopher=None, concept_hint=None, term_hint=None, coherence_manager=None):
    """
    Generate an authentic, academic-sounding title using templates and word pools.
    Allows specifying a philosopher and concept to guide title generation.
    Ensures concepts/terms are appropriate for the given philosopher if one is specified.
    Guarantees a non-empty, plausible title.
    """
    philosopher_for_title = fixed_philosopher
    if not philosopher_for_title:
        if CLEANED_PHILOSOPHERS_REF:
            philosopher_for_title = random.choice(CLEANED_PHILOSOPHERS_REF)
        else: # Absolute fallback for philosopher_for_title
            philosopher_for_title = "A. N. Thinker"


    # Get concepts and terms specific to this philosopher
    philosopher_specific_concepts = philosopher_concepts.get(philosopher_for_title, [])
    # Using philosopher_specific_concepts also for terms for now, assuming terms are a subset or similar
    philosopher_specific_terms = philosopher_specific_concepts

    concept_choice = "a key concept" # Default fallback
    if concept_hint and philosopher_specific_concepts and concept_hint in philosopher_specific_concepts:
        concept_choice = concept_hint
    elif concept_hint and not philosopher_specific_concepts: # Philosopher has no specific concepts, but hint given
        if concepts and concept_hint in concepts: # Check if hint is a globally known concept
             concept_choice = concept_hint
        else: # If hint is not in global concepts, use it as is (could be a general word)
             concept_choice = concept_hint if concept_hint else "an idea" # Ensure hint is not empty
    elif philosopher_specific_concepts:
        concept_choice = random.choice(philosopher_specific_concepts)
    elif concepts: # Fallback to global concepts if philosopher has none and no valid hint
        concept_choice = random.choice(concepts)
    else: # Absolute fallback if no concepts available
        concept_choice = "an important notion"


    term_choice = "a central term" # Default fallback
    if term_hint and philosopher_specific_terms and term_hint in philosopher_specific_terms:
        term_choice = term_hint
    elif term_hint and not philosopher_specific_terms:
        if terms and term_hint in terms: # Check if hint is a globally known term
            term_choice = term_hint
        else:
            term_choice = term_hint if term_hint else "a subject" # Ensure hint is not empty
    elif philosopher_specific_terms:
        term_choice = random.choice(philosopher_specific_terms)
    elif terms: # Fallback to global terms
        term_choice = random.choice(terms)
    else: # Absolute fallback
        term_choice = "a core subject"

    # Ensure template list is not empty
    current_title_templates = bibliography_title_templates if bibliography_title_templates else ["{Philosopher} on {Concept}: A Study of {Term}"]
    
    chosen_template = None
    if not philosopher_specific_concepts or not philosopher_specific_terms:
        simple_templates = [t for t in current_title_templates if '{concept}' not in t.lower() and '{term}' not in t.lower()]
        if simple_templates:
            chosen_template = random.choice(simple_templates)
    if not chosen_template:
        chosen_template = random.choice(current_title_templates)
    
    template = chosen_template
    keys_in_template = [item[1] for item in string.Formatter().parse(template) if item[1] is not None]

    context_for_title = "contemporary discourse" # Default
    if coherence_manager and coherence_manager.active_theme_key:
        theme_context = coherence_manager.get_theme_context_phrase()
        if theme_context:
            context_for_title = theme_context

    format_args = {
        'verb': random.choice(verbs) if verbs else "explores",
        'noun': random.choice(nouns) if nouns else "discourse",
        'adj': random.choice(adjectives) if adjectives else "critical",
        'context': context_for_title,
        'philosopher': philosopher_for_title, # Use the determined philosopher_for_title
        'philosopher1': philosopher_for_title,
    }

    # Populate concept/term related fields carefully, ensuring they are not empty
    if 'concept' in keys_in_template: format_args['concept'] = concept_choice if concept_choice else "analysis"
    if 'term' in keys_in_template: format_args['term'] = term_choice if term_choice else "framework"
    if 'concept1' in keys_in_template: format_args['concept1'] = concept_choice if concept_choice else "interpretation"
    if 'term1' in keys_in_template: format_args['term1'] = term_choice if term_choice else "perspective"

    if 'concept2' in keys_in_template:
        concept2_options = []
        if philosopher_specific_concepts and len(philosopher_specific_concepts) > 1:
            concept2_options = [c for c in philosopher_specific_concepts if c != concept_choice]
        if not concept2_options and concepts:
             concept2_options = [c for c in concepts if c != concept_choice]
        
        if concept2_options:
            format_args['concept2'] = random.choice(concept2_options)
        elif concepts: # if concept_choice was the only one, or no philosopher_specific
            format_args['concept2'] = random.choice(concepts)
        else: # absolute fallback for concept2
            format_args['concept2'] = "another key idea"
    
    if 'term2' in keys_in_template:
        term2_options = []
        if philosopher_specific_terms and len(philosopher_specific_terms) > 1:
            term2_options = [t for t in philosopher_specific_terms if t != term_choice]
        if not term2_options and terms:
            term2_options = [t for t in terms if t != term_choice]

        if term2_options:
            format_args['term2'] = random.choice(term2_options)
        elif terms:
            format_args['term2'] = random.choice(terms)
        else: # absolute fallback for term2
            format_args['term2'] = "another central notion"


    if 'philosopher2' in keys_in_template:
        other_philosophers = [p for p in CLEANED_PHILOSOPHERS_REF if p != philosopher_for_title] if CLEANED_PHILOSOPHERS_REF else []
        if other_philosophers:
            format_args['philosopher2'] = random.choice(other_philosophers)
        elif CLEANED_PHILOSOPHERS_REF: # Only one philosopher in list
            format_args['philosopher2'] = random.choice(CLEANED_PHILOSOPHERS_REF)
        else: # Absolute fallback
             format_args['philosopher2'] = "B. K. Critic"
    
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

    try: # Add try-except for the format operation itself
        raw_title = template.format(**valid_args)
    except KeyError: # Should not happen with the comprehensive valid_args, but as a safeguard
        raw_title = f"{valid_args.get('philosopher', 'Thinker')} on {valid_args.get('concept', 'Topic')}"
    except IndexError: # If template string is malformed, e.g. {}
        raw_title = f"{valid_args.get('philosopher', 'Thinker')} and {valid_args.get('term', 'Subject Matter')}"


    title = apply_title_case(raw_title if raw_title else "A Notable Contribution") # Ensure raw_title is not empty
    return title if title else "Untitled Work" # Final fallback for title

def generate_reference(author_name=None, title_hint=None, work_year=None, specific_work_type=None, coherence_manager=None):
    """
    Generate a reference with a randomly selected work type in MLA 9 style format.
    If author_name is provided, that author will be used.
    If title_hint is provided, it will influence the title generation.
    If work_year is provided, it will be used.
    If specific_work_type is provided, it will be used.
    Ensures a complete and plausible reference string is always returned.
    
    Work types included:
        - Book
        - Journal article
        - Chapter in edited volume
        - Conference paper
    
    Returns:
        str: A formatted reference string following MLA 9 guidelines.
    """
    work_type = specific_work_type if specific_work_type and specific_work_type in ["book", "journal", "chapter", "conference"] else random.choice(["book", "journal", "chapter", "conference"])
    
    actual_author_name_for_reference = None
    author_display = None
    is_known_philosopher_author = False
    title_concept_for_generation = None # Renamed from concept_hint for clarity within this scope


    # Section 1: Determine and Format Author Name
    if author_name and isinstance(author_name, str) and len(author_name.strip().replace(".", "")) > 1:
        actual_author_name_for_reference = author_name.strip()
    elif CLEANED_PHILOSOPHERS_REF:
        actual_author_name_for_reference = random.choice(CLEANED_PHILOSOPHERS_REF)
    else:
        actual_author_name_for_reference = "Foucault, Michel" # Ultimate fallback author

    # Format name as Last, First if it's not already (e.g. from CLEANED_PHILOSOPHERS_REF which are "First Last")
    name_parts = actual_author_name_for_reference.split()
    if len(name_parts) > 1 and ',' not in actual_author_name_for_reference:
        # Handle cases like "bell hooks" or "Judith Butler"
        if actual_author_name_for_reference.lower() in NON_STANDARD_AUTHOR_FORMATS:
            author_display = NON_STANDARD_AUTHOR_FORMATS[actual_author_name_for_reference.lower()]
        else:
            author_display = f"{name_parts[-1]}, {' '.join(name_parts[:-1])}"
    elif ',' in actual_author_name_for_reference : # Already in "Last, First" or "Last, F."
        author_display = actual_author_name_for_reference
    elif len(name_parts) == 1: # Single name (e.g. "Plato", or a last name was passed)
        author_display = actual_author_name_for_reference
    else: # Fallback if split results in unexpected parts (e.g. empty string was passed and somehow bypassed checks)
        author_display = "Critic, A."
        
    # Ensure author_display is not empty
    if not author_display: author_display = "Scholar, Anonymous"


    is_known_philosopher_author = actual_author_name_for_reference in CLEANED_PHILOSOPHERS_REF
    
    # Section 2: Determine Title Concept Hint for generate_title
    if title_hint and isinstance(title_hint, str) and len(title_hint.strip()) > 2 :
        title_concept_for_generation = title_hint.strip()
    elif is_known_philosopher_author and actual_author_name_for_reference in philosopher_key_works and philosopher_key_works[actual_author_name_for_reference]:
        # Try to get a key work title part as hint
        key_work_entry = random.choice(philosopher_key_works[actual_author_name_for_reference])
        if isinstance(key_work_entry, (list, tuple)) and len(key_work_entry) > 0:
            title_concept_for_generation = str(key_work_entry[0]) # Use title of key work
        elif isinstance(key_work_entry, str) : # If it's just a string title
            title_concept_for_generation = key_work_entry

    # Section 3: Generate Title
    # Pass the original full name of the philosopher if known, for better title generation context
    philosopher_for_title_gen = actual_author_name_for_reference if is_known_philosopher_author else None
    # If title_hint was substantial (e.g., seems like a full title already), use it directly after capitalization.
    if title_concept_for_generation and len(title_concept_for_generation.split()) > 4 : # Arbitrary threshold for "substantial"
        final_title_raw = title_concept_for_generation
    else: # Otherwise, generate a title based on hints or defaults.
        final_title_raw = generate_title(fixed_philosopher=philosopher_for_title_gen, concept_hint=title_concept_for_generation, term_hint=None, coherence_manager=coherence_manager)

    final_title = apply_title_case(final_title_raw if final_title_raw else "An Important Study")
    final_title = strip_markdown_italics(final_title) # Ensure stripping always happens
    if not final_title: final_title = "Untitled Analysis" # Ultimate fallback for title

    # Section 4: Determine Year
    year = work_year if isinstance(work_year, int) and 1000 <= work_year <= 2050 else random.randint(1950, 2024)

    # Section 5: Construct Reference String based on work_type
    author_suffix = "" if author_display.endswith(".") or author_display.endswith("?") or author_display.endswith("!") else "."
    
    # Default values for components to ensure they are always defined
    default_publisher = "University Press"
    default_journal_name = "Journal of Postmodern Inquiry"
    default_editor_name = "Editor, Collective"
    default_book_title_for_chapter = "Foundational Essays"
    default_conference_name = "Annual Conference on Critical Thought"
    default_location = "New York"

    reference = ""

    if work_type == "book":
        publisher = random.choice(publishers) if publishers else default_publisher
        reference = author_display + author_suffix + " *" + final_title + "*. " + publisher + ", " + str(year) + "."
    
    elif work_type == "journal":
        journal_name = random.choice(academic_journals) if academic_journals else default_journal_name
        volume = random.randint(1, 50)
        issue = random.randint(1, 4)
        start_page = random.randint(1, 100)
        end_page = start_page + random.randint(5, 30)
        # MLA: "Title of Article." *Title of Journal*, vol. X, no. Y, Year, pp. Z-ZZ.
        reference = (author_display + author_suffix + 
                     ' "' + final_title + '." ' +
                     '*' + journal_name + '*, ' +
                     'vol. ' + str(volume) + ', ' +
                     'no. ' + str(issue) + ', ' +
                     str(year) + ', ' +
                     'pp. ' + str(start_page) + '-' + str(end_page) + '.')
    
    elif work_type == "chapter":
        editor_name = generate_full_name() # Generate a plausible editor name
        editor_suffix = "" if editor_name.endswith(".") else "."
        
        book_title_raw = generate_title(fixed_philosopher=None, concept_hint="Collected Works", coherence_manager=coherence_manager)
        book_title_italicized = "*" + apply_title_case(strip_markdown_italics(book_title_raw)) + "*"
        
        publisher = random.choice(publishers) if publishers else default_publisher
        start_page = random.randint(1, 200)
        end_page = start_page + random.randint(10, 40)
        # MLA: "Title of Chapter." *Title of Book*, edited by Editor Name(s), Publisher, Year, pp. Z-ZZ.
        reference = (author_display + author_suffix +
                     ' "' + final_title + '." ' +
                     book_title_italicized + ', ' +
                     'edited by ' + editor_name + editor_suffix + ' ' +
                     publisher + ', ' +
                     str(year) + ', ' +
                     'pp. ' + str(start_page) + '-' + str(end_page) + '.')

    elif work_type == "conference":
        conference_name = random.choice(conferences) if conferences else default_conference_name
        conference_location = random.choice(locations) if locations else default_location
        conference_date_day = random.randint(1,28)
        conference_date_month = random.choice(['Jan.', 'Feb.', 'Mar.', 'Apr.', 'May', 'Jun.', 'Jul.', 'Aug.', 'Sep.', 'Oct.', 'Nov.', 'Dec.'])
        # MLA: "Title of Presentation." *Name of Conference*, Location, Date. Type of Presentation.
        # For simplicity, "Paper presented at the" implies type.
        reference = (author_display + author_suffix +
                     ' "' + final_title + '." ' +
                     '*' + conference_name + '*, ' + # Italicize conference name as per some MLA examples for formally published proceedings.
                                                     # If it's just a presentation, no italics for conf name, but this is a common style for outputs.
                     conference_location + ', ' +
                     str(conference_date_day) + ' ' + conference_date_month + ' ' + str(year) + '. Conference Presentation.')
    
    else: # Should not happen with current work_type logic, but as a fallback
        reference = f"{author_display}{author_suffix} *{final_title}*. Unknown Source, {year}."

    return reference if reference else f"{author_display}. *Untitled Work*. Default Press, {year}." 