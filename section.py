# section.py
from paragraph import generate_paragraph
import random

def generate_section(heading, num_paragraphs, references):
    section_parts = [(f"## {heading}\n\n", None)]
    for _ in range(num_paragraphs):
        paragraph_parts = generate_paragraph("general", random.randint(2, 4), references)
        section_parts.extend(paragraph_parts)
        section_parts.append(("\n\n", None))
    return section_parts