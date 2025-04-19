"""
A module for generating metafictional elements in generated essays.
This module provides functions to create metafictional elements
that can be inserted into academic writing, particularly in the context of
postmodern philosophy and theory.
It includes functions to generate metafictional elements for paragraphs,
insert them into existing text, and create metafictional conclusions.
The metafictional elements are designed to reflect the self-referential nature
of postmodern discourse, often questioning the very frameworks and methodologies
they employ.
It also includes a function to generate a metafictional conclusion
that references concepts and terms used in the essay.
This module is intended to enhance the complexity and depth of
academic writing, particularly in the context of postmodern philosophy.
It is designed to be used in conjunction with other modules
for generating essays, abstracts, and citations.
"""

import random
from data import concepts, terms, philosophers

def generate_metafictional_element():
    """Generate a metafictional element for use in abstracts or introductions."""
    templates = [
        "It bears asking whether this line of reasoning merely reproduces existing paradigms.",
        "This analysis acknowledges its own complicity in the very discourses it critiques.",
        "In doing so, this paper inevitably participates in the economy of academic knowledge production it seeks to interrogate.",
        "The inherent contradictions of such an approach will become apparent as the argument unfolds.",
        "To what extent can this investigation escape the very logic it seeks to critique?",
        "This paper remains aware of the paradox inherent in employing theoretical tools to critique those same tools.",
        "In articulating these critiques, I acknowledge the impossibility of a position fully exterior to the systems under examination.",
        "The methodology employed here is necessarily implicated in the structures it attempts to analyze.",
        "This text performs the very tensions it describes.",
        "Such an approach raises questions about the possibility of critical distance in theoretical discourse."
    ]
    
    return random.choice(templates)

def insert_metafiction_in_paragraph(paragraph_text):
    """Insert a metafictional element into an existing paragraph appropriately."""
    # Don't add metafiction if the paragraph already contains it
    metafictional_indicators = [
        "this essay", "this text", "this paper", "this analysis", 
        "in writing", "the author", "inevitably", "implicated", 
        "complicit", "paradox", "entangled", "self-reflexive"
    ]
    
    if any(indicator in paragraph_text.lower() for indicator in metafictional_indicators):
        return paragraph_text
    
    # Different types of metafictional elements to insert
    metafictional_templates = [
        "The reflexive awareness that {concept} both enables and delimits this analysis does not escape the author.",
        "This paragraph, in its attempt to elucidate {term}, inevitably falls into the trap of {concept}.",
        "As we examine {concept}, we become implicated in the very {term} we seek to critique.",
        "Writing about {concept} and {term} necessarily involves a certain disciplinary complicity.",
        "This text, in attempting to analyze {term}, becomes yet another instance of academic {concept}.",
        "The author acknowledges the impossibility of standing outside the {concept} being described.",
        "In theorizing {term}, this analysis participates in the economy of {concept} it seeks to interrogate.",
        "{philosopher} might note that this very paragraph performs the logic of {concept} it describes.",
        "Even as we critique {concept}, we cannot escape its structuring effects on our analysis of {term}.",
        "This attempt to theorize {term} is itself caught within the web of {concept}."
    ]
    
    # Select a random concept, term, and philosopher to populate the template
    concept = random.choice(concepts)
    term = random.choice([t for t in terms if t != concept])
    philosopher = random.choice(philosophers)
    
    metafictional_text = random.choice(metafictional_templates).format(
        concept=concept,
        term=term,
        philosopher=philosopher
    )
    
    # Add the metafictional element at an appropriate place
    sentences = paragraph_text.split(". ")
    if len(sentences) <= 2:
        # For short paragraphs, add at the end
        return paragraph_text + " " + metafictional_text + "."
    else:
        # For longer paragraphs, insert at a reasonable position
        insert_position = random.randint(len(sentences) // 2, len(sentences) - 1)
        sentences.insert(insert_position, metafictional_text)
        return ". ".join(sentences)

def generate_metafictional_conclusion(concepts_used, terms_used):
    """
    Generate a metafictional conclusion that references concepts and terms used in the essay.
    
    Args:
        concepts_used (set): Set of concepts used in the essay
        terms_used (set): Set of terms used in the essay
    
    Returns:
        str: A metafictional conclusion statement
    """
    # Select relevant concepts and terms
    concept = random.choice(list(concepts_used)) if concepts_used else random.choice(concepts)
    term = random.choice(list(terms_used)) if terms_used else random.choice(terms)
    
    conclusion_templates = [
        f"In attempting to conclude this essay, we find ourselves caught in the very {concept} we sought to analyze, a testament to its pervasive influence.",
        f"This essay, in its attempt to map {concept}, has perhaps only succeeded in demonstrating the complexity and elusiveness of {term}.",
        f"The intertextuality of this analysis reflects the inherent complexity of the relationship between {concept} and {term}.",
        f"If there is a conclusion to be drawn from our examination of {term}, it is perhaps that {concept} continues to resist theoretical closure.",
        f"As this paper draws to a close—a closure that is always provisional—we are left not with answers about {concept} and {term}, but with more refined questions.",
        f"The paradox, of course, is that in critiquing {concept}, this essay has enacted the very {term} it has sought to problematize.",
        f"To conclude, if such a gesture is possible, is to acknowledge that any engagement with {concept} necessarily participates in the very {term} it seeks to elucidate.",
        f"What emerges from this investigation is not a definitive account of {concept}, but a recognition of its irreducible entanglement with {term}.",
        f"The reflexivity required to analyze {concept} inevitably implicates this text in the economy of {term} it has attempted to critique.",
        f"Perhaps the most significant insight to emerge from this analysis is the recognition that {concept} and {term} remain sites of productive undecidability."
    ]
    
    return random.choice(conclusion_templates)