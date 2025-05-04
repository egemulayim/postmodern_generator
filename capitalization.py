"""
A module for handling proper capitalization and italicization in the generated essay.
This module ensures that philosopher names, titles, and specific terms are properly capitalized
and italicized according to academic conventions.
It also provides functions to format headings in title case and italicize terms
that should be italicized.
"""

import re
from data import philosophers, concepts, italicized_terms, terms

# These are words that should be lowercase in titles when they're not the first or last word
# Note: Words like "from", "with", "into", "over", etc. have 4+ letters 
# and should be capitalized in academic title case as per MLA 9 guidelines
LOWERCASE_WORDS = {
    # Articles
    "a", "an", "the", 
    # Coordinating conjunctions
    "and", "but", "or", "nor", "for", "so", "yet",
    # Short prepositions (fewer than 4 letters)
    "to", "of", "by", "at", "in", "on", "as",
    # Other short words that are typically lowercase in title case
    "via"
}

def ensure_proper_capitalization(text, capitalize_first=True):
    """
    Ensure proper capitalization of philosopher names and sentence beginnings.
    
    Args:
        text (str): The text to process
        capitalize_first (bool): Whether to capitalize the first letter of text and sentence beginnings
        
    Returns:
        str: The text with proper capitalization
    """
    if not text:
        return text
    
    # Capitalize philosopher names first
    for philosopher in philosophers:
        # Ensure we match whole words only and handle partial names (last names)
        full_name_pattern = r'\b' + re.escape(philosopher.lower()) + r'\b'
        text = re.sub(full_name_pattern, philosopher, text, flags=re.IGNORECASE)
        
        # Also handle last names only by splitting the philosopher name and matching the last part
        name_parts = philosopher.split()
        if len(name_parts) > 1:
            last_name = name_parts[-1]
            last_name_pattern = r'\b' + re.escape(last_name.lower()) + r'\b'
            text = re.sub(last_name_pattern, last_name, text, flags=re.IGNORECASE)
    
    # Handle special suffixes like "Jr." that should always be capitalized
    suffixes = ["Jr.", "Sr.", "III", "IV", "V", "VI"]
    for suffix in suffixes:
        suffix_pattern = r'\b' + re.escape(suffix.lower()) + r'\b'
        text = re.sub(suffix_pattern, suffix, text, flags=re.IGNORECASE)
    
    # Only handle sentence capitalization if requested
    if capitalize_first:
        # Capitalize first letter of the text
        if text and text[0].isalpha():
            text = text[0].upper() + text[1:]
        
        # Capitalize beginning of sentences, but be careful about initials
        # This regex looks for sentence endings followed by space and a word
        # But excludes patterns like "A. Smith" or "J.R.R. Tolkien"
        sentence_pattern = r'([.!?])\s+(?!([A-Z]\.)+\s)(\w)'
        
        def capitalize_match(match):
            punctuation = match.group(1)
            next_char = match.group(3)
            # Capitalize the next character if it's a letter
            if next_char.isalpha():
                return punctuation + ' ' + next_char.upper()
            return match.group(0)
        
        text = re.sub(sentence_pattern, capitalize_match, text)
    
    return text

def ensure_proper_capitalization_with_italics(text, capitalize_first=True):
    """
    Ensure proper capitalization while preserving existing italics.
    
    Args:
        text (str): The text to process with potential italics markers
        capitalize_first (bool): Whether to capitalize the first letter of text
        
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
            if (len(processed_parts) == 0 and capitalize_first) or (processed_parts and processed_parts[-1].rstrip().endswith(('.', '!', '?'))):
                if italicized_text and italicized_text[0].isalpha():
                    italicized_text = italicized_text[0].upper() + italicized_text[1:]
            processed_parts.append(f"*{italicized_text}*")
        else:
            # Regular text - apply full capitalization rules
            if len(processed_parts) == 0:  # If this is the first part
                processed_parts.append(ensure_proper_capitalization(part, capitalize_first=capitalize_first))
            else:  # For subsequent parts, we always capitalize the beginning of sentences
                processed_parts.append(ensure_proper_capitalization(part, capitalize_first=False))
    
    return ''.join(processed_parts)

# In capitalization.py, the issue with improper capitalization is in the apply_title_case function:

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
        
        # Special case for proper nouns (matching philosophers, concepts with capital letters)
        is_proper_noun = False
        for philosopher in philosophers:
            if clean_word.lower() in philosopher.lower().split():
                is_proper_noun = True
                break
        
        # Special handling for title words - in reference titles, we should capitalize most words
        # except for very small connector words when they're not the first word or last word
        is_small_word = clean_word in LOWERCASE_WORDS
        
        # In academic title case, always capitalize:
        # 1. First word of title or subtitle (after colon)
        # 2. Last word of title
        # 3. All nouns, pronouns, verbs, adjectives, adverbs
        # 4. All words of four or more letters
        
        # Only make lowercase:
        # - Articles (a, an, the)
        # - Short prepositions (in, on, for, etc.)
        # - Coordinating conjunctions (and, but, or, etc.)
        # - 'to' in infinitives
        
        # But only when they're not the first or last word
        
        should_capitalize = (capitalize_next or  # First word or after delimiter
                           not is_small_word or   # Not a small connector word
                           i == len(words) - 1 or # Last word
                           is_proper_noun or      # Proper noun
                           len(clean_word) >= 4)  # Word is 4+ letters
        
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
            if not is_proper_noun:
                if word and word[0].isalpha():
                    word = word.lower()
        
        result.append(word)
        capitalize_next = False  # Reset for next word unless it's after a delimiter
    
    # Join the words back together with modified delimiter handling
    formatted_title = ""
    for i, part in enumerate(result):
        if part in ['/', '-', '–', '—']:  # No spaces around slashes and dashes
            # No space before or after a slash or dash
            formatted_title = formatted_title.rstrip()
            formatted_title += part
        elif part == ':':  # Colon gets space after, but not before
            # No space before colon, space after (unless it's the last part)
            formatted_title = formatted_title.rstrip()
            formatted_title += part
            if i < len(result) - 1:
                formatted_title += " "
        else:
            # Regular word - add with space if not the first word and previous isn't a slash or dash
            if i > 0 and result[i-1] not in ['/', '-', '–', '—']:
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