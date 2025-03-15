# reference.py
import random
from data import first_names, last_names, adjectives, nouns, theories, contexts, publishers

class Reference:
    def __init__(self, author, year, title, publisher):
        self.author = author
        self.year = year
        self.title = title
        self.publisher = publisher

    def __str__(self):
        return f"{self.author} ({self.year}). {self.title}. {self.publisher}"

def generate_reference():
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    author = f"{last_name}, {first_name[0]}."
    year = random.randint(1960, 2023)
    adjective = random.choice(adjectives)
    noun = random.choice(nouns)
    theory = random.choice(theories)
    context = random.choice(contexts)
    title = f"{adjective} {noun}: {theory} in {context}"
    publisher = random.choice(publishers)
    return Reference(author, year, title, publisher)