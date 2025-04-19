"""
citation_utils.py - A module for handling the citation system with academic conventions.
This module provides functions to generate various types of citations
including footnotes, inline citations, and bibliographic entries.
It also includes functions for generating citations with multiple authors,
page ranges, and theoretical emphasis.
"""

notes = []
note_counter = 1

def get_citation_note(reference):
    """
    Generate a citation note in a more academic format.
    Returns a properly formatted citation reference.
    """
    global note_counter
    note = f"{note_counter}. {reference}"
    notes.append(note)
    note_number = note_counter
    note_counter += 1
    return f"[{note_number}]"  # Academic-style bracket notation

def get_inline_citation(author, year):
    """
    Generate an inline citation in the format (Author, Year).
    This is a common academic citation style.
    """
    return f"({author}, {year})"

def get_ibid_citation(page_number=None):
    """
    Generate an 'ibid' citation, used when citing the same source again immediately.
    Optionally includes a page number.
    """
    if page_number:
        return f"(ibid., p. {page_number})"
    return "(ibid.)"

def get_op_cit_citation(author, page_number=None):
    """
    Generate an 'op. cit.' citation, used when citing a source that has been
    cited before, but not immediately preceding.
    """
    if page_number:
        return f"({author}, op. cit., p. {page_number})"
    return f"({author}, op. cit.)"

def get_cf_citation(author, year):
    """
    Generate a 'cf.' citation, used to compare with another source.
    """
    return f"(cf. {author}, {year})"

def get_see_also_citation(author, year):
    """
    Generate a 'see also' citation, used to refer to additional relevant sources.
    """
    return f"(see also {author}, {year})"

def generate_bibliography(references):
    """
    Generate a properly formatted bibliography from a list of references.
    """
    bibliography = ["## Bibliography\n"]
    for ref in references:
        bibliography.append(f"{ref}\n")
    return "\n".join(bibliography)

# Additional structures for citation patterns

# For complex citations with multiple authors
def get_multiple_author_citation(authors, year):
    """
    Format citations with multiple authors according to academic conventions.
    """
    if len(authors) == 1:
        return f"({authors[0]}, {year})"
    elif len(authors) == 2:
        return f"({authors[0]} and {authors[1]}, {year})"
    else:
        return f"({authors[0]} et al., {year})"

# For citations with page ranges
def get_citation_with_pages(author, year, start_page, end_page=None):
    """
    Format citations that include specific page references.
    """
    if end_page:
        return f"({author}, {year}: {start_page}-{end_page})"
    return f"({author}, {year}: {start_page})"

# For theoretical emphasis in citations
def get_theoretical_citation(author, year, concept):
    """
    Format citations that emphasize a theoretical concept from the cited work.
    """
    return f"({author}'s concept of '{concept}', {year})"