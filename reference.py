import random
from data import first_names, last_names, years, publishers, title_words, generate_title  # Added generate_title

# Different types of works and their citation formats
work_types = [
    "book", "journal_article", "book_section", "conference_talk", "symposium_talk"
]

def generate_reference():
    """
    Generates a random reference with varied work types and citation styles.
    
    Returns:
        str: Formatted reference string based on work type.
    """
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    author = f"{last_name}, {first_name[0]}."
    year = random.choice(years)
    
    # Generate title (two random words from title_words)
    title = generate_title()  # Now properly imported from data.py
    
    work_type = random.choice(work_types)
    
    if work_type == "book":
        publisher = random.choice(publishers)
        return f"{author} ({year}). *{title}*. {publisher}."
    
    elif work_type == "journal_article":
        journal = random.choice(["Journal of Postmodern Studies", "Cultural Critique", "Postcolonial Review",
                               "Critical Theory Quarterly", "Gender Studies Journal", "Media and Society",
                               "Philosophy Today", "Literary Theory Review", "Anthropocene Studies",
                               "Neoliberalism and Culture"])
        volume = random.randint(1, 50)
        issue = random.randint(1, 4)
        pages = f"{random.randint(1, 100)}-{random.randint(101, 200)}"
        return f"{author} ({year}). *{title}*. {journal}, {volume}({issue}), {pages}."
    
    elif work_type == "book_section":
        editor_first = random.choice(first_names)
        editor_last = random.choice(last_names)
        editor = f"{editor_last}, {editor_first[0]}."
        book_title = generate_title()  # Generate a new title for the book
        publisher = random.choice(publishers)
        pages = f"{random.randint(1, 100)}-{random.randint(101, 200)}"
        return f"{author} ({year}). *{title}*. In {editor} (Ed.), *{book_title}* (pp. {pages}). {publisher}."
    
    elif work_type == "conference_talk":
        conference = random.choice(["Annual Conference on Postmodern Theory", "International Symposium on Critical Theory",
                                  "Global Forum on Cultural Studies", "Conference on Postcolonial Literature",
                                  "Symposium on Gender and Media", "Philosophy Congress", "Literary Theory Summit",
                                  "Anthropocene Research Meeting", "Neoliberalism Conference", "Digital Humanities Forum"])
        location = random.choice(["New York", "London", "Paris", "Berlin", "Tokyo", "Sydney", "Toronto", "Amsterdam",
                                "Boston", "Chicago", "San Francisco", "Los Angeles", "Seattle", "Washington D.C.",
                                "Online"])
        return f"{author} ({year}). *{title}*. {conference}, {location}."
    
    else:  # symposium_talk
        symposium = random.choice(["Symposium on Postmodernism", "International Symposium on Poststructuralism",
                                 "Global Symposium on Cultural Critique", "Symposium on Queer Theory",
                                 "Postcolonial Studies Symposium", "Gender and Technology Symposium",
                                 "Philosophy and Ethics Symposium", "Literary Theory Workshop",
                                 "Anthropocene and Ecology Symposium", "Neoliberalism and Society Symposium"])
        location = random.choice(["New York", "London", "Paris", "Berlin", "Tokyo", "Sydney", "Toronto", "Amsterdam",
                                "Boston", "Chicago", "San Francisco", "Los Angeles", "Seattle", "Washington D.C.",
                                "Online"])
        return f"{author} ({year}). *{title}*. {symposium}, {location}."