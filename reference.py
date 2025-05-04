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
from data import philosophers, concepts, terms, contexts, adjectives
from capitalization import apply_title_case

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
    "Princeton University Press", "Yale University Press", "Stanford University Press",
    "Columbia University Press", "Duke University Press", "Cornell University Press",
    "University of Minnesota Press", "Verso Books", "University of California Press"
]

journals = [
    "Critical Inquiry", "Cultural Studies", "Theory, Culture & Society", 
    "Postmodern Culture", "Social Text", "New Literary History", 
    "boundary 2", "Public Culture", "Differences", "October",
    "Cultural Critique", "Diacritics", "Philosophy Today", "Signs",
    "Journal of Philosophy", "Continental Philosophy Review"
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

# First and last names for constructing complete author names
first_names = [
    "John", "Sarah", "Michael", "Catherine", "David", "Elizabeth", "Robert", "Jennifer",
    "Thomas", "Maria", "James", "Emily", "William", "Laura", "Richard", "Alice",
    "Joseph", "Hannah", "Charles", "Margaret", "Daniel", "Rebecca", "Matthew", "Julia",
    "Anthony", "Patricia", "Christopher", "Susan", "Andrew", "Karen", "George", "Anna",
    "Edward", "Helen", "Paul", "Lisa", "Mark", "Michelle", "Donald", "Amanda",
    "Steven", "Melissa", "Kenneth", "Stephanie", "Brian", "Nicole", "Kevin", "Angela",
    "Jason", "Christina", "Roger", "Victoria", "Adrian", "Alexandra", "Benjamin", "Natalie",
    "Gregory", "Sophia", "Ronald", "Olivia", "Timothy", "Emma", "Nicholas", "Claire",
    "Peter", "Abigail", "Samuel", "Megan", "Raymond", "Jessica", "Frank", "Rachel",
    "Gary", "Samantha", "Jeffrey", "Danielle", "Stephen", "Grace", "Harold", "Lily",
    "Jonathan", "Chloe", "Harry", "Sofia", "Scott", "Eleanor", "Jack", "Zoe",
    "Lawrence", "Stella", "Frederick", "Audrey", "Raymond", "Leah", "Alan", "Violet",
    "Arthur", "Nora", "Philip", "Isabella", "Eric", "Lucy", "Francis", "Amelia",
    "Walter", "Harper", "Zachary", "Charlotte", "Louis", "Penelope", "Albert", "Elizabeth"
]

last_names = [
    "Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson",
    "Moore", "Taylor", "Anderson", "Thomas", "Jackson", "White", "Harris", "Martin",
    "Thompson", "Garcia", "Martinez", "Robinson", "Clark", "Rodriguez", "Lewis", "Lee",
    "Walker", "Hall", "Allen", "Young", "Hernandez", "King", "Wright", "Lopez",
    "Hill", "Scott", "Green", "Adams", "Baker", "Gonzalez", "Nelson", "Carter",
    "Mitchell", "Perez", "Roberts", "Turner", "Phillips", "Campbell", "Parker", "Evans",
    "Edwards", "Collins", "Stewart", "Sanchez", "Morris", "Rogers", "Reed", "Cook",
    "Morgan", "Bell", "Murphy", "Bailey", "Rivera", "Cooper", "Richardson", "Cox",
    "Howard", "Ward", "Torres", "Peterson", "Gray", "Ramirez", "James", "Watson",
    "Brooks", "Kelly", "Sanders", "Price", "Bennett", "Wood", "Barnes", "Ross",
    "Henderson", "Coleman", "Jenkins", "Perry", "Powell", "Long", "Patterson", "Hughes",
    "Flores", "Washington", "Butler", "Simmons", "Foster", "Gonzales", "Bryant",
    "Alexander", "Russell", "Griffin", "Diaz", "Hayes", "Myers", "Ford", "Hamilton",
    "Graham", "Sullivan", "Wallace", "Woods", "Cole", "West", "Jordan", "Owens",
    "Reynolds", "Fisher", "Ellis", "Harrison", "Gibson", "Mcdonald", "Cruz", "Marshall"
]

# From prominent philosophers to cite
philosopher_names = [p.split()[-1] for p in philosophers]  # Get last names of philosophers

def generate_full_name():
    """Generate a complete author name."""
    first = random.choice(first_names)
    last = random.choice(last_names)
    return f"{last}, {first}"

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
    
    raw_title = template.format(
        verb=verb,
        noun=noun,
        adjective=adjective,
        concept=concept,
        term=term,
        context=context
    )
    
    # Apply proper title case
    title = apply_title_case(raw_title)
    return title

def generate_reference():
    """
    Generate a reference with a randomly selected work type in MLA 9 style format.
    
    Work types included:
        - Book
        - Journal article
        - Chapter in edited volume
        - Conference paper
    
    Returns:
        str: A formatted reference string following MLA 9 guidelines.
    """
    work_type = random.choice(["book", "journal", "chapter", "conference"])
    
    # Decide if the author should be a philosopher or a generated name
    if random.random() < 0.5:  # 50% chance of using a philosopher
        philosopher = random.choice(philosophers)
        # Format name as Last, First
        name_parts = philosopher.split()
        if len(name_parts) > 1:
            author = f"{name_parts[-1]}, {' '.join(name_parts[:-1])}"
        else:
            author = philosopher
            
        # Special case for bell hooks (always lowercase)
        if philosopher.lower() == "bell hooks":
            author = "hooks, bell"
    else:
        # Generate a plausible academic author name
        author = generate_full_name()
    
    year = random.randint(1950, 2023)
    title = generate_title()
    
    # Format in MLA 9 style - careful with period handling
    # Check if author already ends with a period
    author_period = "" if author.endswith(".") else "."
    
    if work_type == "book":
        publisher = random.choice(publishers)
        # MLA 9 Book format: Author. Title. Publisher, Year.
        reference = f"{author}{author_period} {title}. {publisher}, {year}."
    
    elif work_type == "journal":
        journal_name = random.choice(journals)
        volume = random.randint(1, 50)
        issue = random.randint(1, 12)
        start_page = random.randint(1, 100)
        end_page = start_page + random.randint(10, 45)
        # MLA 9 Journal article format: Author. "Title." Journal Name, vol. Volume, no. Issue, Year, pp. Pages.
        reference = f"{author}{author_period} \"{title}.\" {journal_name}, vol. {volume}, no. {issue}, {year}, pp. {start_page}-{end_page}."
    
    elif work_type == "chapter":
        editor = generate_full_name()
        book_title = generate_title()  # Separate title for the edited volume
        start_page = random.randint(1, 100)
        end_page = start_page + random.randint(10, 45)
        publisher = random.choice(publishers)
        # MLA 9 Chapter format: Author. "Chapter Title." Book Title, edited by Editor, Publisher, Year, pp. Pages.
        reference = f"{author}{author_period} \"{title}.\" {book_title}, edited by {editor}, {publisher}, {year}, pp. {start_page}-{end_page}."
    
    elif work_type == "conference":
        conference_name = random.choice(conferences)
        location = random.choice(locations)
        start_date = random.randint(1, 28)
        month = random.choice(["Jan.", "Feb.", "Mar.", "Apr.", "May", "June", "July", "Aug.", "Sept.", "Oct.", "Nov.", "Dec."])
        # MLA 9 Conference paper format: Author. "Title." Conference Name, Location, Day Month Year.
        reference = f"{author}{author_period} \"{title}.\" {conference_name}, {location}, {start_date} {month} {year}."
    
    return reference