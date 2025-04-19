"""
A module for handling proper capitalization and italicization in the generated essay.
This module ensures that philosopher names, titles, and specific terms are properly capitalized
and italicized according to academic conventions.
It also provides functions to format headings in title case and italicize terms
that should be italicized.
"""

import re
from data import philosophers, concepts, italicized_terms, terms

# Words that should not be capitalized in titles unless they're the first or last word
LOWERCASE_WORDS = {
    "a", "an", "the", "and", "but", "or", "nor", "for", "so", "yet", 
    "to", "of", "by", "at", "from", "with", "in", "on", "upon", "as", "into",
    "like", "over", "against", "through", "after", "during", "since", "before",
    "between", "under", "within", "along", "following", "across", "behind",
    "beyond", "plus", "except", "but", "up", "out", "around", "down", "off", "above"
}

def ensure_proper_capitalization(text):
    """
    Ensure proper capitalization of philosopher names and sentence beginnings.
    
    Args:
        text (str): The text to process
        
    Returns:
        str: The text with proper capitalization
    """
    if not text:
        return text
    
    # Always capitalize first letter of text
    if text and text[0].isalpha():
        text = text[0].upper() + text[1:]
    
    # Capitalize philosopher names
    for philosopher in philosophers:
        # Ensure we match whole words only
        pattern = r'\b' + re.escape(philosopher.lower()) + r'\b'
        text = re.sub(pattern, philosopher, text, flags=re.IGNORECASE)
    
    # Capitalize beginning of sentences
    sentences = re.split(r'([.!?]\s+)', text)
    result = []
    
    for i in range(len(sentences)):
        if i % 2 == 0:  # This is a sentence, not a separator
            if sentences[i] and len(sentences[i]) > 0:
                # Make sure the first word is capitalized if it's alphabetic
                first_word_match = re.match(r'^\s*(\w+)', sentences[i])
                if first_word_match:
                    first_word = first_word_match.group(1)
                    capitalized = first_word[0].upper() + first_word[1:] if first_word and first_word[0].isalpha() else first_word
                    sentences[i] = re.sub(r'^\s*\w+', lambda m: ' ' * (m.start() - m.start()) + capitalized, sentences[i])
        result.append(sentences[i])
    
    return ''.join(result)

def ensure_proper_capitalization_with_italics(text):
    """
    Ensure proper capitalization while preserving existing italics.
    
    Args:
        text (str): The text to process with potential italics markers
        
    Returns:
        str: The text with proper capitalization and preserved italics
    """
    if not text:
        return text
    
    # Split the text by italics markers to preserve them
    parts = re.split(r'(\*[^*]+\*)', text)
    
    # Process each part separately
    processed_parts = []
    for part in parts:
        if part.startswith('*') and part.endswith('*'):
            # This is an italicized part - preserve it but capitalize if needed
            italicized_text = part[1:-1]  # Remove asterisks
            # Only capitalize first letter if it's a title or beginning of sentence
            if len(processed_parts) == 0 or processed_parts[-1].rstrip().endswith(('.', '!', '?')):
                if italicized_text and italicized_text[0].isalpha():
                    italicized_text = italicized_text[0].upper() + italicized_text[1:]
            processed_parts.append(f"*{italicized_text}*")
        else:
            # Regular text - apply full capitalization rules
            processed_parts.append(ensure_proper_capitalization(part))
    
    return ''.join(processed_parts)

def apply_title_case(title):
    """
    Apply academic title case to a title string, handling italicized terms properly.
    Also handles special cases like words after slashes and colons.
    
    Args:
        title (str): The title string to process
        
    Returns:
        str: The title with proper capitalization
    """
    if not title:
        return title
    
    # Special handling for splitting by both spaces and certain delimiters that should have
    # capitalization after them (colon, slash, etc.)
    # We'll preserve the delimiters in the split results
    split_pattern = r'(\s+|(?<=[:/\-–—])|(?=[:/\-–—]))'
    raw_parts = re.split(split_pattern, title)
    
    # Recombine parts into words, keeping track of delimiters
    words = []
    current_word = ""
    for part in raw_parts:
        if not part.strip():  # This is whitespace
            if current_word:
                words.append(current_word)
                current_word = ""
            continue
        elif part in [':', '/', '-', '–', '—']:  # This is a delimiter
            if current_word:
                words.append(current_word)
                words.append(part)
                current_word = ""
            else:
                words.append(part)
        else:
            current_word += part
    
    # Add the last word if there is one
    if current_word:
        words.append(current_word)
    
    # Process each word and delimiter for proper case
    result = []
    capitalize_next = True  # Start with capitalization and after delimiters
    
    for i, word in enumerate(words):
        # Check if this is a delimiter
        if word in [':', '/', '-', '–', '—']:
            result.append(word)
            capitalize_next = True  # Capitalize the word after a delimiter
            continue
        
        # Remove any punctuation for checking against lowercase words
        clean_word = re.sub(r'[^\w\s]', '', word.lower())
        
        # Conditions for capitalizing:
        # 1. First word or word after a delimiter
        # 2. Not in the lowercase list or it's the last word
        # 3. Last word in the title
        should_capitalize = (capitalize_next or 
                           clean_word not in LOWERCASE_WORDS or 
                           i == len(words) - 1)
        
        if should_capitalize:
            # Capitalize first letter if it's a letter
            if word and word[0].isalpha():
                if word.startswith('*') and len(word) > 1:
                    # Handle words that start with asterisk (italics)
                    if word[1].isalpha():
                        word = f"*{word[1].upper()}{word[2:]}"
                else:
                    word = word[0].upper() + word[1:]
        else:
            # Make lowercase unless it's a proper noun
            is_proper_noun = any(philosopher.lower() in word.lower() for philosopher in philosophers)
            if not is_proper_noun:
                if word and word[0].isalpha():
                    word = word.lower()
        
        result.append(word)
        capitalize_next = False  # Reset for next word unless it's after a delimiter
    
    # Join the words back together
    formatted_title = ""
    for i, part in enumerate(result):
        if part in [':', '/', '-', '–', '—']:
            # No space before a delimiter, space after (unless it's the last part)
            formatted_title = formatted_title.rstrip()
            formatted_title += part
            if i < len(result) - 1:
                formatted_title += " "
        else:
            # Regular word - add with space if not the first word
            if i > 0 and not result[i-1] in [':', '/', '-', '–', '—']:
                formatted_title += " "
            formatted_title += part
    
    return formatted_title

def format_headings_with_title_case(text):
    """
    Format all headings in the text with title case.
    
    Args:
        text (str): The full text containing markdown headings
        
    Returns:
        str: The text with properly capitalized headings
    """
    # Match markdown headings (## Title)
    heading_pattern = r'^(#{1,6})\s+(.+)$'
    
    lines = text.split('\n')
    for i, line in enumerate(lines):
        match = re.match(heading_pattern, line.strip())
        if match:
            heading_level, heading_text = match.groups()
            # Apply title case to the heading text
            formatted_heading = apply_title_case(heading_text)
            lines[i] = f"{heading_level} {formatted_heading}"
    
    return '\n'.join(lines)

def italicize_terms_in_text(text):
    """
    Italicize terms in the text that should be italicized.
    
    Args:
        text (str): The text to process
        
    Returns:
        str: The text with italicized terms
    """
    if not text:
        return text
        
    # Only italicize terms that aren't already italicized
    # First, find all already italicized sections to exclude them
    italicized_sections = []
    for match in re.finditer(r'\*([^*]+)\*', text):
        italicized_sections.append((match.start(), match.end()))
    
    # For each term that should be italicized
    for term in italicized_terms:
        # Look for the term with word boundaries
        pattern = r'\b' + re.escape(term) + r'\b'
        
        # Find all occurrences
        for match in re.finditer(pattern, text, re.IGNORECASE):
            start, end = match.span()
            
            # Check if this match is already within an italicized section
            already_italicized = False
            for section_start, section_end in italicized_sections:
                if start >= section_start and end <= section_end:
                    already_italicized = True
                    break
            
            # If not already italicized, add asterisks around it
            if not already_italicized:
                matched_text = match.group(0)
                replacement = f"*{matched_text}*"
                
                # Update the text
                text = text[:start] + replacement + text[end:]
                
                # Update the positions of all subsequent italicized sections
                shift = len(replacement) - len(matched_text)
                italicized_sections = [(s if s < start else s + shift, 
                                       e if e < start else e + shift) 
                                      for s, e in italicized_sections]
                
                # Add this new italicized section
                italicized_sections.append((start, start + len(replacement)))
                
                # Since we modified the string, we need to adjust our search position
                # This is necessary because we're searching in the original string
                # but modifying it as we go
                break
    
    return text