"""
A module for generating academic references in a postmodern context.
This module creates a variety of academic references, including books, journal articles,
chapters in edited volumes, and conference papers.
The references are designed to reflect the complexity and depth of postmodern discourse,
while also adhering to academic citation conventions.
It includes functions to generate titles, references, and work types,
as well as a function to generate a complete bibliography.
"""

import random
from data import philosophers, concepts, terms, contexts, adjectives

# Expanded word pools for authentic and varied titles
verbs = [
    "explore", "investigate", "analyze", "examine", "deconstruct", "reimagine", 
    "critique", "interrogate", "unveil", "disrupt", "reconstruct", "transcend", 
    "subvert", "recontextualize", "problematize", "theorize", "synthesize", 
    "elucidate", "illuminate", "dismantle", "reframe", "negotiate", "navigate", 
    "articulate", "destabilize", "reconceptualize", "foreground", "situate", 
    "trace", "map", "chart", "survey", "assess", "evaluate", "appraise", 
    "revisit", "reassess", "reconsider", "rethink", "reimagine", "re-envision"
]

nouns = [
    "discourse", "narrative", "paradigm", "framework", "lens", "perspective", 
    "approach", "methodology", "ontology", "epistemology", "hegemony", 
    "subjectivity", "agency", "identity", "power", "resistance", "subversion", 
    "transgression", "alterity", "difference", "multiplicity", "plurality", 
    "complexity", "ambiguity", "contradiction", "paradox", "dialectic", 
    "interplay", "intersection", "convergence", "divergence", "tension", 
    "rupture", "disruption", "transformation", "evolution", "genealogy", 
    "archaeology", "cartography", "topography", "landscape", "terrain", 
    "milieu", "context", "situation", "condition", "circumstance", "conjuncture"
]

prepositions = ["of", "in", "through", "beyond", "against", "within", "across", "between", "amidst", "towards"]

conjunctions = ["and", "or", "but", "yet", "while", "as", "through"]

# Title templates for variety and academic plausibility
title_templates = [
    "{verb} the {noun}: {adjective} {concept} in {context}",
    "{adjective} {noun}: {verb} {term} through {concept}",
    "towards a {adjective} {noun} of {concept}",
    "{verb} {term}: a {adjective} inquiry",
    "the {noun} of {concept}: {verb} {term} in {context}",
    "{concept} and {term}: {verb} the {noun}",
    "beyond {term}: {verb} {concept} in {context}",
    "{verb} the {noun}: {concept} as {term}",
    "the {adjective} {noun}: {verb} {concept} and {term}",
    "{concept} in {context}: {verb} the {noun} of {term}"
]

# Work type-specific elements for realistic references
publishers = [
    "Oxford University Press", "Cambridge University Press", "Harvard University Press", 
    "MIT Press", "Routledge", "Palgrave Macmillan", "University of Chicago Press", 
    "Princeton University Press", "Yale University Press", "Stanford University Press"
]

journals = [
    "Critical Inquiry", "Cultural Studies", "Theory, Culture & Society", 
    "Postmodern Culture", "Social Text", "New Literary History", 
    "boundary 2", "Public Culture", "Differences", "October"
]

conferences = [
    "International Conference on Postmodernism", "Symposium on Cultural Theory", 
    "Annual Meeting of the Modern Language Association", "Conference on Postcolonial Studies", 
    "Workshop on Critical Theory", "Seminar on Continental Philosophy", 
    "Colloquium on Literary Criticism", "Forum on Social Theory", 
    "Congress on Cultural Studies", "Summit on Philosophy and Literature"
]

locations = [
    "New York", "London", "Paris", "Berlin", "Tokyo", "Sydney", 
    "Toronto", "Chicago", "San Francisco", "Amsterdam"
]

# Author and editor names for variety
authors = [
    "Smith, J.", "Johnson, A.", "Williams, B.", "Brown, C.", "Davis, D.", 
    "Miller, E.", "Wilson, F.", "Moore, G.", "Taylor, H.", "Anderson, I.", 
    "Thomas, K.", "Jackson, L.", "White, M.", "Harris, N.", "Martin, O.", 
    "Thompson, P.", "Garcia, Q.", "Martinez, R.", "Robinson, S.", "Clark, T."
]

editors = [
    "Lee, U.", "Walker, V.", "Hall, W.", "Allen, X.", "Young, Y.", 
    "King, Z.", "Wright, A.", "Lopez, B.", "Hill, C.", "Scott, D."
]

def generate_title():
    """
    Generate an authentic, academic-sounding title using templates and word pools.
    
    Returns:
        str: A capitalized title string.
    """
    template = random.choice(title_templates)
    verb = random.choice(verbs)
    noun = random.choice(nouns)
    adjective = random.choice(adjectives)
    concept = random.choice(concepts)
    term = random.choice(terms)
    context = random.choice(contexts)
    
    title = template.format(
        verb=verb.capitalize(),
        noun=noun,
        adjective=adjective,
        concept=concept,
        term=term,
        context=context
    )
    return title

def generate_reference():
    """
    Generate a reference with a randomly selected work type and an enhanced title.
    
    Work types included:
        - Book
        - Journal article
        - Chapter in edited volume
        - Conference paper
    
    Returns:
        str: A formatted reference string.
    """
    work_type = random.choice(["book", "journal", "chapter", "conference"])
    author = random.choice(authors)
    year = random.randint(1950, 2023)
    title = generate_title()
    
    if work_type == "book":
        publisher = random.choice(publishers)
        reference = f"{author} ({year}). *{title}*. {publisher}."
    
    elif work_type == "journal":
        journal_name = random.choice(journals)
        volume = random.randint(1, 50)
        issue = random.randint(1, 12)
        pages = f"{random.randint(1, 100)}-{random.randint(101, 200)}"
        reference = f"{author} ({year}). *{title}*. {journal_name}, {volume}({issue}), {pages}."
    
    elif work_type == "chapter":
        editor = random.choice(editors)
        book_title = generate_title()  # Separate title for the edited volume
        pages = f"{random.randint(1, 100)}-{random.randint(101, 200)}"
        publisher = random.choice(publishers)
        reference = f"{author} ({year}). *{title}*. In {editor} (Ed.), *{book_title}* (pp. {pages}). {publisher}."
    
    elif work_type == "conference":
        conference_name = random.choice(conferences)
        location = random.choice(locations)
        reference = f"{author} ({year}). *{title}*. {conference_name}, {location}."
    
    return reference