"""
section.py - A module for generating sections of a postmodern essay.
This module provides functions to create sections of an essay,
including headings and paragraphs.
It is designed to be used in conjunction with other modules
for generating essays, abstracts, and citations.
It includes functions to generate sections with headings,
paragraphs, and references.
It also includes a function to generate a section
with a specified number of paragraphs
and references.
"""

from paragraph import generate_paragraph
import random

def generate_section(heading, num_paragraphs, references):
    section_parts = [(f"## {heading}\n\n", None)]
    for _ in range(num_paragraphs):
        paragraph_parts = generate_paragraph("general", random.randint(2, 4), references)
        section_parts.extend(paragraph_parts)
        section_parts.append(("\n\n", None))
    return section_parts