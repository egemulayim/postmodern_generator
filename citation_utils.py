"""
A module for handling the citation system with academic conventions.
This module provides functions to generate various types of citations
including inline citations, bibliographic entries, and MLA 9 formatted citations.
It also includes functions for generating citations with multiple authors,
page ranges, and theoretical emphasis.
"""

import re  # Added import for regex pattern matching

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
    return f"[^{note_number}]"  # Academic-style bracket notation

def get_inline_citation(author, year, page=None):
    """
    Generate an inline citation in MLA 9 format.
    
    Args:
        author (str): Author's last name
        year (str): Year of publication (not used in MLA style but kept for compatibility)
        page (str, optional): Page number for the citation
        
    Returns:
        str: MLA 9 formatted citation
    """
    # MLA style uses (Author Page) format without the year
    if page:
        return f"({author} {page})"
    else:
        # If no page number, just use author name
        return f"({author})"

def get_multi_author_inline_citation(authors, year, page=None):
    """
    Generate an MLA 9 style inline citation with multiple authors.
    
    Args:
        authors (list): List of author last names
        year (str): Year of publication (not used in MLA style but kept for compatibility)
        page (str, optional): Page number for the citation
        
    Returns:
        str: MLA 9 formatted citation
    """
    # Format based on number of authors
    if len(authors) == 1:
        author_text = authors[0]
    elif len(authors) == 2:
        author_text = f"{authors[0]} and {authors[1]}"
    else:
        author_text = f"{authors[0]} et al."
    
    # Include page number if available
    if page:
        return f"({author_text} {page})"
    else:
        return f"({author_text})"

def get_indirect_citation(original_author, secondary_author, page=None):
    """
    Generate an MLA 9 style indirect citation using "qtd. in" format.
    
    Args:
        original_author (str): Author being quoted
        secondary_author (str): Author in whose work the quote appears
        page (str, optional): Page number in the secondary work
        
    Returns:
        str: MLA 9 formatted indirect citation
    """
    if page:
        return f"({original_author}, qtd. in {secondary_author} {page})"
    else:
        return f"({original_author}, qtd. in {secondary_author})"

def get_ibid_citation(page_number=None):
    """
    Generate an 'ibid' citation, used when citing the same source again immediately.
    Note: MLA 9 does not use ibid., but this is maintained for compatibility.
    In MLA, you would repeat the author's name in subsequent citations.
    
    Args:
        page_number (str, optional): Page number for the citation
        
    Returns:
        str: Citation for repeated source
    """
    if page_number:
        return f"({page_number})"  # In MLA, just use the page number if author is clear from context
    return ""  # Empty if no page number - should be avoided

def get_op_cit_citation(author, page_number=None):
    """
    Generate an 'op. cit.' citation, used when citing a source that has been
    cited before, but not immediately preceding.
    Note: MLA 9 does not use "op. cit." - it always repeats the author name
    
    Args:
        author (str): Author last name
        page_number (str, optional): Page number for the citation
        
    Returns:
        str: MLA format citation
    """
    # In MLA, just use the regular author-page format for all citations
    if page_number:
        return f"({author} {page_number})"
    return f"({author})"

def get_cf_citation(author, year, page=None):
    """
    Generate a 'cf.' citation, used to compare with another source.
    
    Args:
        author (str): Author last name
        year (str): Year of publication (not used in MLA style but kept for compatibility)
        page (str, optional): Page number for the citation
        
    Returns:
        str: MLA format citation with "cf."
    """
    if page:
        return f"(cf. {author} {page})"
    return f"(cf. {author})"

def get_see_also_citation(author, year, page=None):
    """
    Generate a 'see also' citation, used to refer to additional relevant sources.
    
    Args:
        author (str): Author last name
        year (str): Year of publication (not used in MLA style but kept for compatibility)
        page (str, optional): Page number for the citation
        
    Returns:
        str: MLA format citation with "see also"
    """
    if page:
        return f"(see also {author} {page})"
    return f"(see also {author})"

def generate_works_cited(references):
    """
    Generate a properly formatted Works Cited section from a list of references.
    
    Args:
        references (list): List of reference strings
        
    Returns:
        str: Formatted Works Cited section
    """
    works_cited = ["## Works Cited\n"]
    for ref in references:
        # Format the reference for MLA style
        works_cited.append(f"{format_mla_reference(ref)}\n")
    return "\n".join(works_cited)

def format_mla_reference(reference):
    """
    Format a reference string according to MLA 9 guidelines.
    
    Args:
        reference (str): The reference string to format
        
    Returns:
        str: MLA 9 formatted reference
    """
    # Try to parse the reference to determine its type
    # This is a simple parsing function - a more complex implementation would handle
    # different reference types more comprehensively
    
    # First check for author and year
    author_year_match = re.match(r'^([^(]+)\(([0-9]{4})\)', reference)
    if author_year_match:
        author, year = author_year_match.groups()
        author = author.strip()
        
        # Check for book vs article
        rest = reference.split(")", 1)[1].strip()
        if rest.startswith(". *"):
            # Likely a book or journal article
            title_match = re.search(r'\*(.*?)\*', rest)
            if title_match:
                title = title_match.group(1)
                
                # Check if it's a journal article (contains volume and issue numbers)
                if re.search(r'[0-9]+\([0-9]+\)', rest):
                    # Journal article
                    journal_match = re.search(r'\*(.*?)\*\.\s*(.*?),\s*([0-9]+)\(([0-9]+)\),\s*(.*)', rest)
                    if journal_match:
                        title, journal, volume, issue, pages = journal_match.groups()
                        return f"{author} \"{title}.\" {journal}, vol. {volume}, no. {issue}, {year}, pp. {pages}"
                else:
                    # Book
                    publisher_match = re.search(r'\*(.*?)\*\.\s*(.*)', rest)
                    if publisher_match:
                        title, publisher = publisher_match.groups()
                        return f"{author} {title}. {publisher}"
    
    # If we couldn't parse it, return as is
    return reference

def get_citation_with_pages(author, year, start_page, end_page=None):
    """
    Format citations that include specific page references in MLA style.
    
    Args:
        author (str): Author last name
        year (str): Year of publication (not used in MLA style but kept for compatibility)
        start_page (str): Starting page number
        end_page (str, optional): Ending page number
        
    Returns:
        str: MLA format citation with page range
    """
    if end_page:
        return f"({author} {start_page}-{end_page})"
    return f"({author} {start_page})"

def get_theoretical_citation(author, year, concept, page=None):
    """
    Format citations that emphasize a theoretical concept from the cited work.
    
    Args:
        author (str): Author last name
        year (str): Year of publication (not used in MLA style but kept for compatibility)
        concept (str): Theoretical concept being referenced
        page (str, optional): Page number for the citation
        
    Returns:
        str: MLA format citation with theoretical concept
    """
    if page:
        return f"({author}'s concept of '{concept}', {page})"
    return f"({author}'s concept of '{concept}')"