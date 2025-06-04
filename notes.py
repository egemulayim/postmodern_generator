"""
A module for generating footnotes and bibliography entries
that maintain coherence with the main text of the essay.
This module provides a system for managing notes (footnotes) and bibliography entries.
It ensures coherence between the notes, the main text, and bibliography.
It includes functions to add citations, generate substantive notes,
and format bibliography entries.
It also provides functions to format notes and bibliography entries according to MLA 9 style guidelines.
"""

import random
import re
from json_data_provider import philosophers, concepts, terms, adjectives, philosopher_concepts
from json_data_provider import academic_journals, bibliography_title_templates
from json_data_provider import NON_STANDARD_AUTHOR_FORMATS
from json_data_provider import publishers as data_publishers, philosopher_key_works as data_philosopher_key_works
from capitalization import ensure_proper_capitalization_with_italics, italicize_terms_in_text, apply_title_case
from reference import strip_markdown_italics

# Placeholder definitions for variables used in this module but not sourced from data.py
# philosopher_key_works = {}  # REMOVE - Will use data_philosopher_key_works from data.py
# publishers = ["University Press", "Academic Books Inc."] # REMOVE - Will use data_publishers from data.py

class NoteSystem:
    """
    A system for managing notes (footnotes) and bibliography entries in a postmodern essay.
    This ensures coherence between the notes, the main text, and bibliography.
    Now implements MLA 9 style citations with Markdown footnote support.
    """
    
    def __init__(self):
        """Initialize the note system."""
        self.notes = [] # Stores tuples of (note_number, commentary_text, full_reference_string)
        self.works_cited = []
        self.citation_markers = {}  # Maps reference to note number for substantive notes
        self.page_numbers = {}  # Maps reference to page number(s)
        # Track which authors have multiple works
        self.author_work_count = {}  # Maps author to count of their works
        self.author_works = {}  # Maps author to dict of their works (title -> full reference)
        self.recently_used_note_templates = [] # For reducing immediate repetition of note commentary
        self.recently_used_formatted_commentaries = [] # Track recently *generated* commentaries
        # Enhanced template variety tracking
        self.recently_used_categories = []
        self.recently_used_template_content = []
        self.style = "endnotes"
    
    def reset(self):
        """Reset the note system to its initial state."""
        self.notes = []
        self.works_cited = []
        self.citation_markers = {}
        self.page_numbers = {}
        self.author_work_count = {}
        self.author_works = {}
        self.recently_used_note_templates = [] # Reset for new essay
        self.recently_used_formatted_commentaries = [] # Reset for new essay
        # Reset enhanced template variety tracking
        self.recently_used_categories = []
        self.recently_used_template_content = []
    
    def get_mentioned_philosophers(self):
        """Returns a list of philosophers who have been cited."""
        return list(self.author_work_count.keys())

    def _ensure_work_in_bibliography(self, reference_string):
        """
        Ensures a reference is in the bibliography and updates related tracking.
        
        Args:
            reference_string (str): The full bibliographic reference string.
        """
        full_author_name = self._extract_author_for_note(reference_string)
        title_key = self._extract_title_sorting_key(reference_string)

        if not self._is_duplicate_reference(reference_string):
            self.works_cited.append(reference_string)
            
            if full_author_name not in self.author_work_count:
                self.author_work_count[full_author_name] = 1
                self.author_works[full_author_name] = {}
            else:
                self.author_work_count[full_author_name] += 1
            
            if title_key: # Ensure title_key is not None before assignment
                self.author_works[full_author_name][title_key] = reference_string
        
        if reference_string not in self.page_numbers:
            self.page_numbers[reference_string] = random.randint(1, 300)

    def _create_parenthetical_citation_string(self, reference_string, original_author_for_indirect=None):
        """
        Creates the text for a parenthetical citation (e.g., (Author Page) or (Author, "Title" Page)).
        Ensures a non-empty, plausible parenthetical citation string is always returned.
        
        Args:
            reference_string (str): The full bibliographic reference string for the work being cited.
            original_author_for_indirect (str, optional): The name of the original author if this is
                                                            an indirect citation (qtd. in). Defaults to None.
                                                            
        Returns:
            str: The formatted parenthetical citation string.
        """
        if not reference_string: # Should not happen, but as a safeguard
            return "(Unknown Source)"

        full_author_name = self._extract_author_for_note(reference_string) or "Unknown Author"
        in_text_author = self._get_author_for_in_text_citation(full_author_name) or "Author"
        
        # Ensure title_key is a string, even if empty, to prevent errors with _get_short_title if None
        title_key_raw = self._extract_title_sorting_key(reference_string)
        title_key = str(title_key_raw) if title_key_raw is not None else ""

        page_num = self.page_numbers.get(reference_string, None)
        if page_num is None: # If not found or value was None
            page_num = random.randint(1,300) # Assign a random page if missing
        page_display = str(page_num) if page_num else "XX" # Ensure page is a string, "XX" if somehow still None/0

        current_author_work_count = self.author_work_count.get(full_author_name, 0)
        
        # Fallback for title components
        short_title_str = "Work"
        display_short_title_str = "Work"
        is_article_ref = False

        if title_key: # Only proceed if title_key is not an empty string
            is_article_ref = bool(re.search(r'\"\\s*[^\\\"]+?\\s*\"', reference_string))
            # Pass is_article_ref to _get_short_title
            raw_short_title = self._get_short_title(title_key, is_article_ref) # Expected to handle empty title_key gracefully
            if raw_short_title and isinstance(raw_short_title, str) and raw_short_title.strip():
                 short_title_str = raw_short_title.strip()
                 display_short_title_str = apply_title_case(short_title_str)
            # else, use default "Work"
        
        # Ensure short_title_str and display_short_title_str are not empty after processing
        if not short_title_str: short_title_str = "Work"
        if not display_short_title_str: display_short_title_str = "Work"


        # Ensure original_author_for_indirect is a string if provided
        indirect_author_display = str(original_author_for_indirect) if original_author_for_indirect else None

        try:
            if indirect_author_display: # Handling for "qtd. in"
                if current_author_work_count > 1 and title_key: # title_key check implies it's not empty
                    if is_article_ref:
                        return f'({indirect_author_display}, qtd. in {in_text_author}, "{display_short_title_str}" {page_display})'
                    else:
                        return f'({indirect_author_display}, qtd. in {in_text_author}, *{display_short_title_str}* {page_display})'
                else:
                    return f'({indirect_author_display}, qtd. in {in_text_author} {page_display})'
            else: # Standard parenthetical citation
                if current_author_work_count > 1 and title_key: # title_key check implies it's not empty
                    if is_article_ref:
                        return f'({in_text_author}, "{display_short_title_str}" {page_display})'
                    else:
                        return f'({in_text_author}, *{display_short_title_str}* {page_display})'
                else:
                    return f'({in_text_author} {page_display})'
        except Exception: # Ultimate fallback for any unexpected formatting error
            return f"({in_text_author or 'Author'} {page_display or 'XX'})"

    def add_citation(self, reference, context=None, is_quote_citation=False):
        """
        Add a citation. Manages bibliography and generates note/in-text marker.
        If is_quote_citation is True, always returns a parenthetical citation.
        If is_quote_citation is False (default), creates a substantive footnote and returns a marker [^N].
        """
        self._ensure_work_in_bibliography(reference)
        
        citation_to_embed_in_text = ""

        if is_quote_citation:
            citation_to_embed_in_text = self._create_parenthetical_citation_string(reference)
            
            # Even for quotes, if this is the first time we see this reference for note purposes,
            # and it's not yet in citation_markers, create a background substantive note.
            # This ensures _generate_substantive_note can still be called if other parts 
            # of the code expect a note to exist (e.g. for general commentary).
            if reference not in self.citation_markers:
                note_number = len(self.notes) + 1
                self.citation_markers[reference] = note_number # Mark as "seen" for footnote purposes
                commentary = self._generate_substantive_note(reference, context, note_number)
                self.notes.append((note_number, commentary, reference))
        else: # This is for general commentary notes (substantive footnotes)
            note_number = len(self.notes) + 1
            # For general notes, we always create a new note entry.
            # The citation_markers will point to the *first* note for that reference.
            if reference not in self.citation_markers:
                 self.citation_markers[reference] = note_number
            
            commentary = self._generate_substantive_note(reference, context, note_number)
            self.notes.append((note_number, commentary, reference))
            citation_to_embed_in_text = f"[^{note_number}]"
        
        # Ultimate fallback if somehow citation_to_embed_in_text is empty
        if not citation_to_embed_in_text:
            if is_quote_citation:
                # Attempt to get a very basic author string for a generic parenthetical
                fallback_author = self._get_author_for_in_text_citation(self._extract_author_for_note(reference) or "Author") or "Source"
                fallback_page = self.page_numbers.get(reference, "XX")
                citation_to_embed_in_text = f"({fallback_author} {fallback_page})"
            else:
                citation_to_embed_in_text = "[Citation Details Unavailable]" # Fallback for note marker

        return citation_to_embed_in_text
    
    def _get_short_title(self, title, is_article=False):
        """
        Create a shortened version of a title for in-text citations.
        Handles subtitles by prioritizing the main title (before a colon).
        
        Args:
            title (str): The full title
            is_article (bool): Whether this is an article (for formatting)
            
        Returns:
            str: A shortened title suitable for in-text citation
        """
        clean_title = title.strip()

        # Handle subtitles: if a colon is present, use the part before it as the main title for shortening.
        if ":" in clean_title:
            main_title_part = clean_title.split(":", 1)[0].strip()
            # Check if the main title part is substantial enough
            if len(main_title_part.split()) > 0:
                clean_title = main_title_part
        
        words = clean_title.split()
        
        if len(words) <= 4:
            return clean_title
        
        skip_words = ["the", "a", "an", "of", "in", "on", "for", "and", "or"]
        
        significant_words = []
        skipped_initial_article = False
        for i, word in enumerate(words):
            if i == 0 and word.lower() in skip_words and len(words) > len(skip_words):
                skipped_initial_article = True
                continue
            significant_words.append(word)
            if len(significant_words) >= (3 if skipped_initial_article or len(words) < 5 else 4):
                break
        
        short_title = " ".join(significant_words)
        
        short_title = re.sub(r'[:\.,;]$', '', short_title)
        
        return short_title
    
    def add_indirect_citation(self, original_author, secondary_reference, context=None):
        """
        Add an indirect citation. If new substantive note for secondary_reference, returns [^N].
        Otherwise, returns MLA "qtd. in" parenthetical.
        """
        self._ensure_work_in_bibliography(secondary_reference)

        citation_to_embed_in_text = ""
        # Check if a substantive note already exists for the secondary_reference
        # The decision to create a new note or a parenthetical "qtd. in"
        # depends on whether we've made a substantive comment on secondary_reference before.
        if secondary_reference not in self.citation_markers:
            note_number = len(self.notes) + 1
            self.citation_markers[secondary_reference] = note_number # Mark for future direct citations
            commentary = self._generate_substantive_note(secondary_reference, context, note_number)
            # The note is about the secondary_reference, but the in-text marker implies the indirect nature.
            self.notes.append((note_number, commentary, secondary_reference))
            # The note text itself might clarify "qtd. in" if desired, but the marker is for the secondary source's note.
            # For clarity, the in-text for a *new* substantive note on the secondary source should point to *that* note.
            # The commentary within this new note could elaborate on the "qtd. in original_author" aspect.
            # However, standard MLA for qtd. in is usually parenthetical.
            # Let's re-evaluate: if it's the *first time* we are citing secondary_reference substantively,
            # it gets its own note. The "qtd. in" appears in text.
            # If secondary_reference ALREADY has a note, then further "qtd. in" become purely parenthetical.

            # If we are creating a NEW substantive note for the secondary_reference,
            # the in-text marker should be for that new note.
            # The actual "qtd. in" phrasing is part of the parenthetical form.
            # The user asked: "If new substantive note for secondary_reference, returns [^N]."
            # This means if we haven't made a note about secondary_reference yet, we make one.
            citation_to_embed_in_text = f"[^{note_number}]"
            # The commentary in this note (note_number) should ideally reflect that it's being
            # introduced in the context of an indirect citation.
            # The current _generate_substantive_note doesn't have a direct way to signal this.
            # For now, the note will be a standard substantive note about secondary_reference.

        else: # secondary_reference already has a substantive note or has been cited before.
              # Subsequent indirect citations become parenthetical.
            citation_to_embed_in_text = self._create_parenthetical_citation_string(
                secondary_reference,
                original_author_for_indirect=original_author
            )
        
        return citation_to_embed_in_text
    
    def _extract_author_year(self, text):
        """Extract author and year from text using regex patterns."""
        # First try to match (Author, Year) or (Author Year) format
        author_year_match = re.search(r'\(([^,]+)(?:,\s*|\s+)(\d{4})\)', text)
        if author_year_match:
            return author_year_match.group(1).strip(), author_year_match.group(2)
            
        # Then try to match [Author, Year] format
        author_year_match = re.search(r'\[([^,]+)(?:,\s*|\s+)(\d{4})\]', text)
        if author_year_match:
            return author_year_match.group(1).strip(), author_year_match.group(2)
            
        # Finally try to match just author name
        author_match = re.search(r'\(([^,]+)\)', text)
        if author_match:
            return author_match.group(1).strip(), None
            
        return None, None
    
    def _is_duplicate_reference(self, reference):
        """
        Check if a reference is a duplicate of an existing one.
        
        Args:
            reference (str): The reference to check
        
        Returns:
            bool: True if duplicate found, False otherwise
        """
        author = self._extract_author_for_note(reference)
        title = self._extract_title_sorting_key(reference)
        
        for ref in self.works_cited:
            ref_author = self._extract_author_for_note(ref)
            ref_title = self._extract_title_sorting_key(ref)
            
            if author == ref_author and self._titles_are_similar(title, ref_title):
                return True
                
        return False
    
    def _titles_are_similar(self, title1, title2):
        """
        Compare two titles to determine if they are similar.
        
        Args:
            title1 (str): First title
            title2 (str): Second title
            
        Returns:
            bool: True if titles are similar, False otherwise
        """
        t1 = re.sub(r'[^\w\s]', '', title1.lower()) if title1 else ""
        t2 = re.sub(r'[^\w\s]', '', title2.lower()) if title2 else ""
        
        if not t1 or not t2:
            return False
            
        if t1 == t2:
            return True
            
        if t1 in t2 or t2 in t1:
            return True
            
        words1 = set(t1.split())
        words2 = set(t2.split())
        common_words = words1.intersection(words2)
        
        if len(words1) == 0 or len(words2) == 0:
            return False
        similarity_ratio = len(common_words) / max(len(words1), len(words2))
        return similarity_ratio > 0.6
    
    def _extract_title_sorting_key(self, reference):
        """
        Extract the title from a reference for sorting and ID generation (lowercase).
        Strips italics markers for the key itself.
        """
        # Try to extract the title for articles (in quotes)
        title_match = re.search(r'"\s*([^"]+?)\s*"', reference)
        if title_match:
            return title_match.group(1).lower() # Title is already plain text from group
        
        # Try for books (text after author. and before publisher/year details or another major section)
        # Example: Author. *Title*. Publisher, Year. OR Author. Title. Publisher, Year.
        # Matches text after first period and space, up to the next period preceding publisher/year info.
        # This regex attempts to capture the title part more accurately.
        # It looks for content after "Author." up to a period that's likely before publisher/year.
        # It allows for titles with colons, question marks etc.
        book_match = re.match(r'^[^\.]+\.\s+([^\.(]+(?:\([^)]+\))?[^.]*)\.', reference)
        if book_match:
            title = book_match.group(1).strip()
            # Remove italics markers (asterisks) and leading/trailing spaces/periods for sorting key
            return title.replace('*', '').strip('. ').lower()
        
        # Fallback if no clear title is found (should be rare for well-formed refs)
        return ""
    
    def _generate_substantive_note(self, reference, context, note_number):
        """
        Generate a substantive footnote that includes both a brief citation and additional commentary.
        The commentary is generated by _generate_commentary and is specific to the reference.
        
        Args:
            reference (str): The reference being cited
            context (dict): Context about the citation
            note_number (int): The note number (currently not directly used in commentary, but available)
        
        Returns:
            str: The formatted note text (commentary)
        """
        commentary = self._generate_commentary(reference, context)
        
        note_text = f"{commentary}" 
        
        return note_text
    
    def _extract_author_for_note(self, reference):
        """
        Extract author name from reference for use in note. (e.g. "Last, First M." or "hooks, bell")
        """
        # Try to match MLA 9 journal article format
        journal_match = re.match(r'^([^\.]+)\.\s*"[^\"]+".', reference)
        if journal_match:
            author = journal_match.group(1).strip()
            return author if author else "Unknown Author"
        
        # Try to match MLA 9 book format
        book_match = re.match(r'^([^\.]+)\.\s*([^\.]+)\.', reference)
        if book_match:
            author = book_match.group(1).strip()
            return author if author else "Unknown Author"
        
        # Legacy format fallback
        legacy_match = re.match(r'^([^(]+)', reference)
        if legacy_match:
            author = legacy_match.group(1).strip()
            return author if author else "Unknown Author"
        
        return "Unknown Author"
    
    def _format_author_for_commentary(self, author_name_str):
        """Formats an author name for use in note commentary (e.g., First Last). Ensures a plausible string."""
        if not author_name_str or not isinstance(author_name_str, str) or author_name_str.strip().lower() == "unknown author" or not author_name_str.strip():
            return "the author" # More generic fallback

        if author_name_str.lower() == "bell hooks":
            return "bell hooks"  # Ensure "bell hooks" for commentary

        author_name_str_lower = author_name_str.lower()
        for biblio_key, display_val in NON_STANDARD_AUTHOR_FORMATS.items():
            if biblio_key.lower() == author_name_str_lower:
                return display_val if display_val else "a noted scholar"
        
        processed_name = author_name_str.strip()
        if "," in processed_name:
            parts = processed_name.split(",", 1)
            last_name = parts[0].strip()
            first_middle_parts = parts[1].strip().split()
            if first_middle_parts and last_name:
                return " ".join(first_middle_parts) + " " + last_name
            elif last_name: 
                return last_name
            else: 
                return "a scholar"
        else:
            return processed_name if processed_name else "a noted thinker"

    def _get_author_for_in_text_citation(self, full_author_name):
        """Formats the author's name for in-text MLA citation (e.g., Lastname or special format)."""
        # full_author_name is expected in "Last, First" or special format like "hooks, bell"
        
        if full_author_name == "hooks, bell": # specific check for bibliography style "hooks, bell"
            return "hooks" # Return "hooks" for in-text parenthetical

        if not full_author_name or full_author_name == "Unknown Author":
            return "Unknown Author" # Should not happen if get_enhanced_citation is robust

        # Check against NON_STANDARD_AUTHOR_FORMATS if it contains other specific in-text formats
        # This part needs clarity on what NON_STANDARD_AUTHOR_FORMATS stores for in-text purposes.
        # For now, assuming it's mainly for display names or full bibliography names.
        # If NON_STANDARD_AUTHOR_FORMATS were to dictate in-text forms other than bell hooks:
        # lower_full_name = full_author_name.lower()
        # for name_in_list in NON_STANDARD_AUTHOR_FORMATS:
        #     if name_in_list.lower() == lower_full_name: # if it stores "Last, First" style
        #          # derive in-text from name_in_list
        #          pass 

        # Standard processing: Extract last name from "Last, First M."
        # Handles cases like "Smith, John Jr." or "de Beauvoir, Simone"
        name_parts = full_author_name.split(',')
        last_name_segment = name_parts[0].strip()

        # Further split last_name_segment if it contains spaces (e.g. "von Trapp")
        # We typically only want the primary last name for in-text.
        primary_last_name = last_name_segment.split()[-1]
        
        # Standard MLA practice is to capitalize the last name in parenthetical citations.
        # The user's request is specifically for "bell hooks" to be all lowercase.
        # Other authors should follow standard capitalization.
        return primary_last_name.capitalize()

    def _generate_commentary(self, reference, context):
        """Generate substantive commentary for a note based on context, aiming for variety and conciseness. Ensures a non-empty, meaningful string."""
        
        raw_current_author = self._extract_author_for_note(reference) # Fallback is "Unknown Author"
        ct_auth = self._format_author_for_commentary(raw_current_author) # Fallback is "the author"
        ct_auth_display = ct_auth if ct_auth != "the author" else "The author of the work cited"

        raw_another_philosopher = "another thinker" # Default
        valid_philosophers = [p for p in philosophers if p and isinstance(p, str) and p.strip()] if philosophers else []

        if valid_philosophers:
            if len(valid_philosophers) > 1:
                possible_others = [p for p in valid_philosophers if p != raw_current_author]
                if possible_others:
                    raw_another_philosopher = random.choice(possible_others)
                else: # current author was the only one, or not in list
                    raw_another_philosopher = random.choice(valid_philosophers)
            else: # Only one philosopher in the list
                raw_another_philosopher = valid_philosophers[0]
        else: # No philosophers in the global list
            raw_another_philosopher = "a notable scholar" # Fallback if global list is empty

        an_phil = self._format_author_for_commentary(raw_another_philosopher)
        an_phil_display = an_phil if an_phil != "the author" else "another scholar in the field"
        
        focus_topic = None
        related_topic = None
        
        # Contextual topic extraction (simplified)
        if context:
            current_context_topics = list(context.get('current_concepts_in_paragraph', [])) + \
                                   list(context.get('current_terms_in_paragraph', [])) + \
                                   list(context.get('concepts', [])) + \
                                   list(context.get('terms', []))
            current_context_topics = [t for t in current_context_topics if t and isinstance(t, str) and t.strip()] # Clean list
            if current_context_topics:
                focus_topic = random.choice(current_context_topics)
        
        # Fallback for focus_topic if not found from context
        if not focus_topic:
            global_topics = [t for t in (concepts or []) + (terms or []) if t and isinstance(t, str) and t.strip()]
            if global_topics:
                focus_topic = random.choice(global_topics)
            else:
                focus_topic = "the central theme" # Absolute fallback

        f_topic_display = focus_topic # Already a string or the fallback string

        # Determine related_topic
        possible_r_topics_all = [t for t in (concepts or []) + (terms or []) if t and isinstance(t, str) and t.strip() and t != focus_topic]
        if possible_r_topics_all:
            related_topic = random.choice(possible_r_topics_all)
        else:
            related_topic = "a relevant detail" # Absolute fallback
        
        r_topic_display = related_topic

        format_data = {
            'ct_auth': ct_auth_display,
            'an_phil': an_phil_display,
            'f_topic': f_topic_display,
            'r_topic': r_topic_display
        }

        master_template_list = { # Significantly expanded template variety for diverse note generation
            "elaboration": [
                f"{ct_auth_display}'s perspective on {f_topic_display} is particularly noteworthy here, especially in how it diverges from common interpretations.",
                f"This work offers an important elaboration of {f_topic_display}, particularly as it concerns {r_topic_display} and its contemporary relevance.",
                f"The nuanced treatment of {f_topic_display} in this source provides essential clarification often overlooked in broader discussions.",
                f"{ct_auth_display} develops a sophisticated framework for understanding {f_topic_display} that extends beyond traditional approaches.",
                f"The author's detailed analysis of {f_topic_display} reveals complexities that merit further consideration, especially regarding {r_topic_display}.",
                f"This reference expands on {f_topic_display} in ways that illuminate previously unexamined dimensions of {r_topic_display}.",
                f"{ct_auth_display}'s contribution here lies in unpacking the multilayered nature of {f_topic_display} and its relationship to {r_topic_display}."
            ],
            
            "contextualization": [
                f"This source provides important historical context for understanding {f_topic_display}, especially during its period of emergence and its impact on {r_topic_display}.",
                f"The historical significance of {f_topic_display} becomes clearer when situated within the broader intellectual context that {ct_auth_display} provides.",
                f"Understanding {f_topic_display} requires the kind of temporal perspective that this work supplies, particularly concerning {r_topic_display}.",
                f"{ct_auth_display} situates {f_topic_display} within its proper intellectual genealogy, revealing connections to {r_topic_display}.",
                f"The cultural and philosophical background necessary for comprehending {f_topic_display} is effectively established in this reference.",
                f"This work traces the evolution of thinking about {f_topic_display} and its gradual convergence with discussions of {r_topic_display}.",
                f"The contextual framework provided here is essential for grasping how {f_topic_display} relates to broader philosophical concerns with {r_topic_display}."
            ],
            
            "critique_comparison": [
                f"This source presents a contrasting viewpoint to {ct_auth_display} on {f_topic_display}, often attributed to scholars like {an_phil_display}, particularly concerning {r_topic_display}.",
                f"A critical assessment of {ct_auth_display}'s position on {f_topic_display} emerges when compared with alternative approaches to {r_topic_display}.",
                f"The limitations of conventional approaches to {f_topic_display} become apparent through this critical examination of {r_topic_display}.",
                f"{ct_auth_display} challenges prevailing interpretations of {f_topic_display}, offering a critique that extends to related discussions of {r_topic_display}.",
                f"This reference provides a counterpoint to mainstream views on {f_topic_display}, particularly where they intersect with {r_topic_display}.",
                f"The author's critical stance toward {f_topic_display} opens up alternative pathways for thinking about {r_topic_display}.",
                f"In questioning established assumptions about {f_topic_display}, this work reveals underlying tensions in how we approach {r_topic_display}."
            ],
            
            "methodological": [
                f"The methodological approach employed here for examining {f_topic_display} offers a model for similar investigations into {r_topic_display}.",
                f"{ct_auth_display}'s analytical framework provides valuable tools for approaching complex questions about {f_topic_display} and {r_topic_display}.",
                f"The research methodology demonstrated in this work establishes important precedents for studying {f_topic_display}.",
                f"This source exemplifies rigorous scholarship in its treatment of {f_topic_display}, particularly in relation to {r_topic_display}.",
                f"The systematic approach taken here toward {f_topic_display} could be productively applied to other areas, including {r_topic_display}.",
                f"{ct_auth_display}'s investigative method reveals dimensions of {f_topic_display} that previous approaches had overlooked.",
                f"The analytical precision with which this work examines {f_topic_display} sets a standard for discussions of {r_topic_display}."
            ],
            
            "theoretical_implications": [
                f"The theoretical implications of {ct_auth_display}'s work on {f_topic_display} extend well beyond immediate concerns with {r_topic_display}.",
                f"This reference opens up theoretical possibilities for {f_topic_display} that have broader significance for understanding {r_topic_display}.",
                f"The conceptual framework developed here for {f_topic_display} has ramifications for how we theorize {r_topic_display}.",
                f"{ct_auth_display} advances theoretical understanding of {f_topic_display} in ways that reshape discussions of {r_topic_display}.",
                f"The theoretical contributions of this work extend from its analysis of {f_topic_display} to broader questions about {r_topic_display}.",
                f"This source develops theoretical insights about {f_topic_display} that prove relevant to contemporary debates over {r_topic_display}.",
                f"The author's theoretical innovations regarding {f_topic_display} offer new perspectives on longstanding problems with {r_topic_display}."
            ],
            
            "interdisciplinary": [
                f"This work demonstrates the value of interdisciplinary approaches to {f_topic_display}, drawing connections to fields beyond traditional studies of {r_topic_display}.",
                f"{ct_auth_display} brings insights from multiple disciplines to bear on questions of {f_topic_display} and its relationship to {r_topic_display}.",
                f"The interdisciplinary perspective offered here enriches our understanding of both {f_topic_display} and {r_topic_display}.",
                f"By crossing disciplinary boundaries, this reference illuminates aspects of {f_topic_display} typically obscured in discussions of {r_topic_display}.",
                f"The author's interdisciplinary method reveals connections between {f_topic_display} and {r_topic_display} that disciplinary specialization often misses.",
                f"This work exemplifies the productive potential of interdisciplinary dialogue in addressing complex questions about {f_topic_display}.",
                f"The synthesis of different disciplinary perspectives on {f_topic_display} opens new avenues for exploring {r_topic_display}."
            ],
            
            "contemporary_relevance": [
                f"The contemporary relevance of {ct_auth_display}'s analysis of {f_topic_display} becomes particularly evident in current discussions of {r_topic_display}.",
                f"This work's treatment of {f_topic_display} speaks directly to present-day concerns about {r_topic_display}.",
                f"The enduring significance of this analysis lies in its applicability to contemporary questions surrounding {f_topic_display} and {r_topic_display}.",
                f"{ct_auth_display}'s insights into {f_topic_display} prove remarkably prescient given recent developments in {r_topic_display}.",
                f"The contemporary pertinence of this work stems from its sophisticated engagement with {f_topic_display} in relation to {r_topic_display}.",
                f"Current debates about {r_topic_display} would benefit from the perspective on {f_topic_display} that this reference provides.",
                f"The author's analysis of {f_topic_display} offers resources for addressing urgent contemporary questions about {r_topic_display}."
            ],
            
            "philosophical_foundations": [
                f"The philosophical foundations underlying {ct_auth_display}'s approach to {f_topic_display} merit examination, particularly as they inform discussions of {r_topic_display}.",
                f"This work's philosophical underpinnings provide important grounding for its treatment of {f_topic_display} and related questions about {r_topic_display}.",
                f"The foundational assumptions about {f_topic_display} that inform this analysis have significant implications for how we approach {r_topic_display}.",
                f"{ct_auth_display} articulates philosophical commitments regarding {f_topic_display} that shape the broader discourse on {r_topic_display}.",
                f"The philosophical framework employed here for understanding {f_topic_display} offers insights applicable to {r_topic_display}.",
                f"This reference's philosophical foundations illuminate deeper questions about the relationship between {f_topic_display} and {r_topic_display}.",
                f"The author's philosophical orientation toward {f_topic_display} provides a lens through which to examine {r_topic_display}."
            ],
            
            "empirical_evidence": [
                f"The empirical evidence presented here regarding {f_topic_display} substantiates claims that extend to broader questions about {r_topic_display}.",
                f"{ct_auth_display} marshals compelling evidence in support of positions on {f_topic_display} that have bearing on {r_topic_display}.",
                f"The evidentiary foundation of this work's claims about {f_topic_display} strengthens arguments concerning {r_topic_display}.",
                f"This reference provides empirical support for theoretical positions on {f_topic_display} that inform discussions of {r_topic_display}.",
                f"The evidence presented here challenges conventional assumptions about {f_topic_display} and, by extension, {r_topic_display}.",
                f"The author's careful attention to empirical detail in examining {f_topic_display} establishes credibility for claims about {r_topic_display}.",
                f"This work's empirical contributions to understanding {f_topic_display} have ramifications for how we study {r_topic_display}."
            ],
            
            "pedagogical": [
                f"This reference serves valuable pedagogical purposes in teaching about {f_topic_display}, particularly for students encountering {r_topic_display}.",
                f"{ct_auth_display}'s clear exposition of {f_topic_display} makes complex ideas accessible without sacrificing sophistication in addressing {r_topic_display}.",
                f"The pedagogical value of this work lies in its systematic introduction to key issues surrounding {f_topic_display} and {r_topic_display}.",
                f"This source provides an excellent starting point for students beginning to grapple with questions of {f_topic_display} in relation to {r_topic_display}.",
                f"The author's pedagogical sensitivity is evident in the careful way complex questions about {f_topic_display} are related to {r_topic_display}.",
                f"This work's educational significance extends beyond its immediate subject matter to broader pedagogical questions about teaching {f_topic_display}.",
                f"The clarity with which this reference presents difficult concepts about {f_topic_display} serves as a model for discussing {r_topic_display}."
            ],
            
            "historical_development": [
                f"The historical development of ideas about {f_topic_display} traced in this work illuminates the evolution of thinking about {r_topic_display}.",
                f"{ct_auth_display} charts the intellectual history of {f_topic_display} in ways that reveal its connections to {r_topic_display}.",
                f"This reference documents important moments in the development of scholarship on {f_topic_display} and its relationship to {r_topic_display}.",
                f"The genealogy of concepts related to {f_topic_display} presented here extends to contemporary discussions of {r_topic_display}.",
                f"This work traces intellectual lineages that connect historical treatments of {f_topic_display} to current approaches to {r_topic_display}.",
                f"The author's historical perspective on {f_topic_display} provides context essential for understanding debates about {r_topic_display}.",
                f"The development of scholarly discourse about {f_topic_display} documented here has parallels in the evolution of thinking about {r_topic_display}."
            ],
            
            "cross_cultural": [
                f"This work's cross-cultural perspective on {f_topic_display} reveals dimensions often overlooked in Western-centric discussions of {r_topic_display}.",
                f"{ct_auth_display} brings important cultural insights to bear on questions of {f_topic_display} that enrich understanding of {r_topic_display}.",
                f"The cultural specificity of approaches to {f_topic_display} highlighted here has implications for how we understand {r_topic_display} across contexts.",
                f"This reference demonstrates the value of examining {f_topic_display} from multiple cultural vantage points, especially regarding {r_topic_display}.",
                f"The author's attention to cultural variation in conceptions of {f_topic_display} opens new perspectives on {r_topic_display}.",
                f"This work challenges universal claims about {f_topic_display} by attending to cultural differences that extend to {r_topic_display}.",
                f"The cross-cultural analysis of {f_topic_display} provided here offers resources for more inclusive approaches to {r_topic_display}."
            ],
            
            "feminist_analysis": [
                f"The feminist analysis of {f_topic_display} offered here reveals gendered dimensions often invisible in discussions of {r_topic_display}.",
                f"{ct_auth_display} brings feminist insights to {f_topic_display} that have broader implications for understanding {r_topic_display}.",
                f"This work's feminist perspective on {f_topic_display} challenges masculinist assumptions in scholarship on {r_topic_display}.",
                f"The gendered analysis of {f_topic_display} presented here extends to important questions about {r_topic_display}.",
                f"This reference demonstrates how feminist approaches to {f_topic_display} can illuminate overlooked aspects of {r_topic_display}.",
                f"The author's feminist critique of traditional approaches to {f_topic_display} has ramifications for how we study {r_topic_display}.",
                f"This work contributes to feminist scholarship by examining {f_topic_display} in ways that connect to broader concerns with {r_topic_display}."
            ],
            
            "postcolonial_perspective": [
                f"The postcolonial perspective on {f_topic_display} developed here challenges colonial legacies in scholarship on {r_topic_display}.",
                f"{ct_auth_display} brings postcolonial insights to bear on {f_topic_display} that reshape understanding of {r_topic_display}.",
                f"This work's postcolonial analysis reveals how discussions of {f_topic_display} have been shaped by colonial frameworks affecting {r_topic_display}.",
                f"The decolonizing approach to {f_topic_display} offered here has implications for how we address {r_topic_display}.",
                f"This reference demonstrates the importance of postcolonial perspectives for understanding both {f_topic_display} and {r_topic_display}.",
                f"The author's postcolonial critique of Western approaches to {f_topic_display} opens alternative pathways for examining {r_topic_display}.",
                f"This work contributes to decolonizing scholarship through its treatment of {f_topic_display} in relation to {r_topic_display}."
            ],
            
            "phenomenological": [
                f"The phenomenological approach to {f_topic_display} employed here reveals experiential dimensions relevant to understanding {r_topic_display}.",
                f"{ct_auth_display} brings phenomenological insights to {f_topic_display} that illuminate the lived experience of {r_topic_display}.",
                f"This work's phenomenological analysis of {f_topic_display} attends to subjective aspects often neglected in discussions of {r_topic_display}.",
                f"The experiential focus of this analysis of {f_topic_display} provides important perspectives on {r_topic_display}.",
                f"This reference demonstrates the value of phenomenological approaches to {f_topic_display} for understanding {r_topic_display}.",
                f"The author's phenomenological sensitivity to {f_topic_display} reveals embodied dimensions of {r_topic_display}.",
                f"This work's attention to lived experience in relation to {f_topic_display} has implications for how we approach {r_topic_display}."
            ],
            
            "aesthetic_considerations": [
                f"The aesthetic dimensions of {f_topic_display} explored here connect to broader questions about the relationship between beauty and {r_topic_display}.",
                f"{ct_auth_display} attends to aesthetic aspects of {f_topic_display} that have often been overlooked in discussions of {r_topic_display}.",
                f"This work's aesthetic analysis of {f_topic_display} reveals sensory and affective dimensions relevant to {r_topic_display}.",
                f"The aesthetic framework employed here for understanding {f_topic_display} offers new perspectives on {r_topic_display}.",
                f"This reference demonstrates how aesthetic considerations inform both {f_topic_display} and related questions about {r_topic_display}.",
                f"The author's sensitivity to aesthetic questions surrounding {f_topic_display} enriches discussions of {r_topic_display}.",
                f"This work's aesthetic approach to {f_topic_display} illuminates affective and sensory dimensions of {r_topic_display}."
            ],
            
            "technological_implications": [
                f"The technological implications of {ct_auth_display}'s analysis of {f_topic_display} extend to contemporary questions about {r_topic_display} in digital contexts.",
                f"This work's examination of {f_topic_display} has relevance for understanding how technology shapes {r_topic_display}.",
                f"The relationship between technology and {f_topic_display} explored here provides insights applicable to {r_topic_display}.",
                f"{ct_auth_display} addresses technological dimensions of {f_topic_display} that connect to broader concerns about {r_topic_display}.",
                f"This reference anticipates technological developments relevant to both {f_topic_display} and {r_topic_display}.",
                f"The author's attention to technological mediation in discussions of {f_topic_display} has implications for {r_topic_display}.",
                f"This work's technological perspective on {f_topic_display} offers resources for addressing digital-age questions about {r_topic_display}."
            ],
            
            "ethical_dimensions": [
                f"The ethical implications of {ct_auth_display}'s treatment of {f_topic_display} extend to moral questions surrounding {r_topic_display}.",
                f"This work raises important ethical questions about {f_topic_display} that have bearing on how we approach {r_topic_display}.",
                f"The moral dimensions of {f_topic_display} highlighted here connect to broader ethical concerns with {r_topic_display}.",
                f"{ct_auth_display} attends to ethical aspects of {f_topic_display} often overlooked in discussions of {r_topic_display}.",
                f"This reference demonstrates the ethical stakes involved in how we understand {f_topic_display} in relation to {r_topic_display}.",
                f"The author's ethical analysis of {f_topic_display} provides moral resources for addressing questions about {r_topic_display}.",
                f"This work's attention to ethical dimensions of {f_topic_display} has implications for moral approaches to {r_topic_display}."
            ],
            
            "psychoanalytic": [
                f"The psychoanalytic insights into {f_topic_display} offered here reveal unconscious dimensions relevant to understanding {r_topic_display}.",
                f"{ct_auth_display} brings psychoanalytic theory to bear on {f_topic_display} in ways that illuminate {r_topic_display}.",
                f"This work's psychoanalytic approach to {f_topic_display} uncovers repressed aspects that connect to {r_topic_display}.",
                f"The unconscious dynamics of {f_topic_display} explored here have implications for how we understand {r_topic_display}.",
                f"This reference demonstrates the value of psychoanalytic perspectives for examining both {f_topic_display} and {r_topic_display}.",
                f"The author's psychoanalytic reading of {f_topic_display} reveals libidinal economies that inform {r_topic_display}.",
                f"This work's attention to unconscious processes in {f_topic_display} provides insights applicable to {r_topic_display}."
            ],
            
            "linguistic_analysis": [
                f"The linguistic analysis of {f_topic_display} provided here reveals discursive patterns that extend to discussions of {r_topic_display}.",
                f"{ct_auth_display} attends to language use in relation to {f_topic_display} that has implications for how we discuss {r_topic_display}.",
                f"This work's linguistic approach to {f_topic_display} illuminates semantic dimensions relevant to {r_topic_display}.",
                f"The discursive analysis of {f_topic_display} offered here connects to broader questions about language and {r_topic_display}.",
                f"This reference demonstrates how linguistic considerations inform understanding of both {f_topic_display} and {r_topic_display}.",
                f"The author's attention to rhetoric and discourse in discussions of {f_topic_display} has bearing on {r_topic_display}.",
                f"This work's linguistic sensitivity reveals how language shapes our understanding of {f_topic_display} and {r_topic_display}."
            ],
            
            "political_economy": [
                f"The political economic analysis of {f_topic_display} offered here reveals material conditions that shape {r_topic_display}.",
                f"{ct_auth_display} brings insights from political economy to bear on {f_topic_display} that illuminate {r_topic_display}.",
                f"This work's attention to economic dimensions of {f_topic_display} has implications for understanding {r_topic_display}.",
                f"The material analysis of {f_topic_display} provided here connects to broader questions about capitalism and {r_topic_display}.",
                f"This reference demonstrates how economic forces shape both {f_topic_display} and {r_topic_display}.",
                f"The author's political economic perspective on {f_topic_display} reveals class dynamics relevant to {r_topic_display}.",
                f"This work's analysis of power relations in {f_topic_display} extends to important questions about {r_topic_display}."
            ],
            
            "general_academic_comment": [
                f"{an_phil_display} also offers a complementary perspective on {f_topic_display} in their work on {r_topic_display}, which is touched upon in the cited reference.",
                f"The scholarly consensus on {f_topic_display} has evolved significantly, as this reference demonstrates in its treatment of {r_topic_display}.",
                f"Recent scholarship on {f_topic_display} has moved in directions that this work anticipates, particularly regarding {r_topic_display}.",
                f"The academic reception of ideas about {f_topic_display} continues to develop, as evidenced by ongoing discussions of {r_topic_display}.",
                f"This work contributes to a growing body of scholarship that examines {f_topic_display} in relation to {r_topic_display}.",
                f"The intellectual legacy of this analysis of {f_topic_display} can be traced in subsequent scholarship on {r_topic_display}.",
                f"Academic debate about {f_topic_display} has been enriched by the kind of analysis that this reference provides regarding {r_topic_display}."
            ]
        }

        chosen_template_str = ""
        try:
            # Use the enhanced _select_unique_template with the expanded template collection
            chosen_template_str = self._select_unique_template(master_template_list)
        except Exception:
            # Fallback: select randomly from available categories if the enhanced selection fails
            category_keys = [k for k,v in master_template_list.items() if v] # Only categories with templates
            if category_keys:
                chosen_category = random.choice(category_keys)
                chosen_template_str = random.choice(master_template_list[chosen_category])
            else:
                chosen_template_str = f"{ct_auth_display} provides further commentary on {f_topic_display}."

        final_commentary = ""
        try:
            final_commentary = chosen_template_str # Already formatted with f-string if from master_template_list
            # If chosen_template_str was a fallback non-f-string, it would need .format(**format_data)
            # The f-strings in master_template_list directly use the display variables.
        except Exception: 
            final_commentary = f"Please refer to the work by {ct_auth_display} for more on {f_topic_display}."

        if not final_commentary or not final_commentary.strip():
            final_commentary = f"The cited work offers further perspective on {f_topic_display}."
        
        if not final_commentary.endswith('.') and not final_commentary.endswith('?') and not final_commentary.endswith('!'):
            final_commentary += '.'
        
        return final_commentary

    def _get_alternative_reference(self, current_reference):
        """
        Find an alternative academic reference for comparison.

        Args:
            current_reference (str): The reference to find an alternative for.

        Returns:
            str: A formatted string for an alternative reference, or a placeholder if none found.
        """
        candidate_references = [ref for ref in self.works_cited if ref != current_reference]

        if not candidate_references:
            all_possible_works = []
            if 'philosopher_key_works' in globals() or 'philosopher_key_works' in locals():
                for author_works in data_philosopher_key_works.values():
                    all_possible_works.extend(author_works)
            
            candidate_references = [
                work for work in all_possible_works 
                if isinstance(work, dict) and work.get("title") and work.get("author") and
                   f"{work['author']}, {work['title']}" != current_reference
            ]
            
            if not candidate_references:
                return "another seminal work"

            selected_work_data = random.choice(candidate_references)
            author = selected_work_data.get("author", "Unknown Author")
            title = selected_work_data.get("title", "Untitled Work")
            
            if '"' in title:
                 formatted_title = title
            else:
                 formatted_title = f"*{title}*"
            return f"{author}, {formatted_title}"

        alternative_ref_full = random.choice(candidate_references)
        
        author = self._extract_author_for_note(alternative_ref_full)
        
        title_match = re.search(r', (\*[^\*]+\*|\"[^\"]+\"|[^,(]+(?:\([^)]+\))?)(?:, \d{4})?', alternative_ref_full)
        
        if title_match:
            title_part = title_match.group(1).strip()
            if not (title_part.startswith("*") and title_part.endswith("*")) and \
               not (title_part.startswith('"') and title_part.endswith('"')):
                # If it's not already an article title (quoted) or book title (italicized by asterisks),
                # assume it should be italicized as a book title for the purpose of this alternative ref.
                title_part = f"*{title_part}*"
            return f"{author}, {title_part}"
        
        # Fallback: if title extraction fails, generate a plausible book title for this author.
        # The 'author' variable here is already in "Last, First M." or special format.
        # We need the original author name as passed to get_enhanced_citation for philosopher_concepts lookup, if available.
        # However, _get_alternative_reference doesn't have direct access to that original name.
        # So, we'll generate a generic title for the extracted author.
        # We also don't know if it should be an article or book, book is a safer generic.
        generated_title = self._generate_book_title(author_name=author, existing_titles=[], philosopher_real_name=None)
        return f"{author}, *{apply_title_case(strip_markdown_italics(generated_title))}*"

    def _find_related_topics(self, focus_topic):
        """
        Finds related topics to a given focus_topic. 
        Prioritizes thematic clusters if available, then philosopher concepts, then general terms.
        """
        related_topics = []
        
        if not related_topics:
            try:
                from json_data_provider import philosopher_concepts # This import is fine
                for philosopher, concepts_list in philosopher_concepts.items(): # Renamed concepts to concepts_list
                    if focus_topic in concepts_list:
                        related_topics.extend([c for c in concepts_list if c != focus_topic])
            except ImportError:
                pass # philosopher_concepts should exist, but good to be safe
        
        if not related_topics: # Fallback to general concepts and terms
            # Ensure concepts and terms are available (they are loaded at module level in json_data_provider)
            # from json_data_provider import concepts, terms # Not needed if they are accessible
            general_concepts_sample = random.sample(concepts, min(3, len(concepts))) if concepts else []
            general_terms_sample = random.sample(terms, min(2, len(terms))) if terms else []
            related_topics.extend(general_concepts_sample)
            related_topics.extend(general_terms_sample)
        
        seen = set()
        unique_related = []
        for topic in related_topics:
            if topic not in seen:
                seen.add(topic)
                unique_related.append(topic)
        
        return unique_related

    def get_enhanced_citation(self, author_name, is_article, year, 
                              title_override=None, specific_year_override=None, is_article_override=None):
        """
        Generates a full bibliographic reference string.
        Accepts overrides for title, year, and article/book status for specific citations (e.g., from key works).
        Otherwise, tries to reuse existing work titles for an author or generates new ones.
        """
        formatted_author = author_name
        if author_name.lower() == "bell hooks":
            formatted_author = "hooks, bell"
        elif "," not in author_name:
            parts = author_name.split()
            if len(parts) > 1:
                formatted_author = f"{parts[-1]}, {' '.join(parts[:-1])}"
        
        author_period = "" if formatted_author.endswith(".") else "."

        current_year = specific_year_override if specific_year_override is not None else year
        
        is_definitely_article = False
        if is_article_override is not None:
            is_definitely_article = is_article_override
        else:
            is_definitely_article = is_article

        title_to_use = None
        if title_override:
            title_to_use = apply_title_case(title_override)
        else:
            # Attempt to get a key work first
            key_work_details = None
            # Ensure author_name is in the format expected by data_philosopher_key_works (usually "Last, First M.")
            # The `formatted_author` variable should already be in this format or a special format like "hooks, bell"
            if formatted_author in data_philosopher_key_works:
                author_key_works = data_philosopher_key_works[formatted_author]
                if author_key_works:
                    chosen_key_work = random.choice(author_key_works)
                    title_to_use = apply_title_case(chosen_key_work.get("title"))
                    # Override year and type if available from key work
                    if chosen_key_work.get("year"): # Ensure year is present
                        current_year = chosen_key_work.get("year")
                    if chosen_key_work.get("type"):
                        is_definitely_article = chosen_key_work.get("type") == "article"
                    # Store this choice to prevent immediate re-generation if possible
                    key_work_details = chosen_key_work # Keep details for later

            if not title_to_use: # If no key work was found or used
                existing_titles_for_author = []
                if formatted_author in self.author_works:
                    author_s_works_dict = self.author_works[formatted_author]
                    if author_s_works_dict:
                        for title_key in author_s_works_dict.keys():
                            existing_titles_for_author.append(title_key)
                        if existing_titles_for_author and random.random() < 0.75:
                            reused_title_key = random.choice(existing_titles_for_author)
                            title_to_use = apply_title_case(reused_title_key)

        if is_definitely_article:
            if not title_to_use:
                title_to_use = self._generate_article_title(author_name=formatted_author, existing_titles=existing_titles_for_author if not title_override else [], philosopher_real_name=author_name)
            
            journal_name = random.choice(academic_journals)
            volume = random.randint(1, 50)
            issue = random.randint(1, 12)
            start_page = random.randint(1, 100)
            end_page = start_page + random.randint(10, 45)
            reference = f"{formatted_author}{author_period} \"{apply_title_case(strip_markdown_italics(title_to_use))}.\" *{apply_title_case(strip_markdown_italics(journal_name))}*, vol. {volume}, no. {issue}, {current_year}, pp. {start_page}-{end_page}."
        else:
            if not title_to_use:
                title_to_use = self._generate_book_title(author_name=formatted_author, existing_titles=existing_titles_for_author if not title_override else [], philosopher_real_name=author_name)
            
            publisher = random.choice(data_publishers)
            reference = f"{formatted_author}{author_period} *{apply_title_case(strip_markdown_italics(title_to_use))}*. {publisher}, {current_year}."
        
        return reference

    def generate_notes_section(self):
        """Formats and returns the notes (as Markdown footnotes) and works cited section."""
        notes_string = "## Notes\n\n"
        if not self.notes:
            notes_string += "No substantive notes for this essay.\n\n"
        else:
            sorted_notes = sorted(self.notes, key=lambda x: x[0])
            for number, commentary, original_ref_str in sorted_notes:
                temp_commentary = ensure_proper_capitalization_with_italics(commentary)
                temp_commentary = italicize_terms_in_text(temp_commentary)
                formatted_commentary = temp_commentary.rstrip('\n')
                
                notes_string += f"[^{number}]: {formatted_commentary}\n"
            notes_string += "\n"

        works_cited_string = "## Works Cited\n\n"
        if not self.works_cited:
            works_cited_string += "No works cited for this essay.\n\n"
        else:
            unique_works_cited = sorted(list(set(self.works_cited)))
            for entry in unique_works_cited:
                temp_entry = ensure_proper_capitalization_with_italics(entry)
                formatted_entry = temp_entry.rstrip('\n')
                works_cited_string += f"{formatted_entry}\n\n" 
        
        return notes_string + works_cited_string

    def _generate_article_title(self, author_name=None, existing_titles=None, philosopher_real_name=None):
        """Generates a plausible academic article title, avoiding existing ones for the author if possible."""
        if existing_titles is None:
            existing_titles = []
        
        # Try to use concepts/terms related to the actual philosopher if available
        author_specific_concepts = []
        author_specific_terms = []
        if philosopher_real_name and philosopher_real_name in data_philosopher_key_works: # Check against the name used in data
            if philosopher_real_name in philosopher_concepts: # Direct check now
                author_data = philosopher_concepts[philosopher_real_name]
                if isinstance(author_data, dict):
                    author_specific_concepts = author_data.get('concepts', [])
                    author_specific_terms = author_data.get('terms', [])
                elif isinstance(author_data, list):
                    # If it's a flat list, assume all are concepts for now
                    # Or, you could try to distinguish them if there's a pattern or use all as concepts.
                    author_specific_concepts = author_data
                    # No specific terms identified from a flat list this way

        chosen_title = ""
        attempts = 0
        while attempts < 10:
            template = random.choice(bibliography_title_templates)
            core_concept = random.choice(author_specific_concepts) if author_specific_concepts else (random.choice(concepts) if concepts else "a key concept")
            core_term = random.choice(author_specific_terms) if author_specific_terms else (random.choice(terms) if terms else "a central term")
            
            philosopher_for_template_text = random.choice(philosophers) if philosophers else "a prominent thinker"
            if author_name and author_name != "Unknown Author" and philosophers and len(philosophers) > 1:
                formatted_author_of_work = self._format_author_for_commentary(author_name)
                possible_others = [p for p in philosophers if self._format_author_for_commentary(p) != formatted_author_of_work]
                if possible_others:
                    philosopher_for_template_text = random.choice(possible_others)
            
            formatted_philosopher_in_title = self._format_author_for_commentary(philosopher_for_template_text)

            title = template.format(
                concept=core_concept,
                term=core_term,
                philosopher=formatted_philosopher_in_title, 
                adj=random.choice(adjectives) if adjectives else "critical"
            )
            chosen_title = apply_title_case(title)
            
            is_new_theme = True 
            if existing_titles:
                 is_new_theme = not any(ex_title for ex_title in existing_titles if core_concept.lower() in ex_title or core_term.lower() in ex_title)
            
            if is_new_theme or not existing_titles:
                break
            attempts += 1
        return chosen_title if chosen_title else apply_title_case(f"A Study on {random.choice(concepts if concepts else ['the topic'])}")

    def _generate_book_title(self, author_name=None, existing_titles=None, philosopher_real_name=None):
        """Generates a plausible academic book title, avoiding existing ones for the author if possible."""
        if existing_titles is None:
            existing_titles = []

        # Try to use concepts/terms related to the actual philosopher if available
        author_specific_concepts = []
        author_specific_terms = []
        if philosopher_real_name and philosopher_real_name in data_philosopher_key_works: # Check against the name used in data
            if philosopher_real_name in philosopher_concepts: # Direct check now
                author_data = philosopher_concepts[philosopher_real_name]
                if isinstance(author_data, dict):
                    author_specific_concepts = author_data.get('concepts', [])
                    author_specific_terms = author_data.get('terms', [])
                elif isinstance(author_data, list):
                    author_specific_concepts = author_data

        chosen_title = ""
        attempts = 0
        while attempts < 10:
            template = random.choice(bibliography_title_templates)
            core_concept = random.choice(author_specific_concepts) if author_specific_concepts else (random.choice(concepts) if concepts else "a major theme")
            core_term = random.choice(author_specific_terms) if author_specific_terms else (random.choice(terms) if terms else "an important debate")

            philosopher_for_template_text = random.choice(philosophers) if philosophers else "a key figure"
            if author_name and author_name != "Unknown Author" and philosophers and len(philosophers) > 1:
                formatted_author_of_work = self._format_author_for_commentary(author_name)
                possible_others = [p for p in philosophers if self._format_author_for_commentary(p) != formatted_author_of_work]
                if possible_others:
                    philosopher_for_template_text = random.choice(possible_others)
            
            formatted_philosopher_in_title = self._format_author_for_commentary(philosopher_for_template_text)

            title = template.format(
                concept=core_concept,
                term=core_term,
                philosopher=formatted_philosopher_in_title, 
                adj=random.choice(adjectives) if adjectives else "significant"
            )
            chosen_title = apply_title_case(title)

            is_new_theme = True
            if existing_titles:
                is_new_theme = not any(ex_title for ex_title in existing_titles if core_concept.lower() in ex_title or core_term.lower() in ex_title)

            if is_new_theme or not existing_titles:
                break
            attempts += 1
        return chosen_title if chosen_title else apply_title_case(f"Rethinking {random.choice(concepts if concepts else ['the subject'])}")

    def _select_unique_template(self, templates_by_category):
        """
        Select a unique template string from a dictionary of template lists.
        Enhanced to provide much better variety by avoiding recently used categories and templates.
        Prioritizes category diversity and template uniqueness across the greatly expanded collection.

        Args:
            templates_by_category (dict): A dictionary where keys are category names and values are lists of template strings.
            
        Returns:
            str: A selected template string that maximizes variety.
        """
        if not templates_by_category:
            return "This citation provides additional perspective."

        available_categories = list(templates_by_category.keys())
        
        # Track recently used categories to encourage category diversity
        if not hasattr(self, 'recently_used_categories'):
            self.recently_used_categories = []
        
        # Track recently used template content to avoid immediate repetition
        if not hasattr(self, 'recently_used_template_content'):
            self.recently_used_template_content = []
        
        # First, try to select from categories not recently used
        unused_categories = [cat for cat in available_categories if cat not in self.recently_used_categories[-5:]]
        if not unused_categories:
            # If all categories have been used recently, reset and use all
            unused_categories = available_categories
            self.recently_used_categories = []
        
        # Try multiple attempts to find a unique template
        for attempt in range(min(20, len(available_categories) * 3)):
            # Prefer unused categories, but occasionally use any category for full variety
            if unused_categories and random.random() < 0.8:
                category_key = random.choice(unused_categories)
            else:
                category_key = random.choice(available_categories)
                
            template_list = templates_by_category.get(category_key, [])
            
            if template_list:
                template_str = random.choice(template_list)
                
                # Create a content fingerprint to avoid similar templates
                # Use first few words and template structure as fingerprint
                template_words = template_str.split()[:8] if len(template_str.split()) > 8 else template_str.split()
                content_fingerprint = " ".join(template_words).lower()
                
                # Check if this content is too similar to recently used ones
                is_too_similar = any(
                    len(set(content_fingerprint.split()) & set(recent.split())) > 4
                    for recent in self.recently_used_template_content[-10:]
                )
                
                if not is_too_similar:
                    # Update tracking
                    self.recently_used_categories.append(category_key)
                    if len(self.recently_used_categories) > 15:
                        self.recently_used_categories = self.recently_used_categories[-10:]
                    
                    self.recently_used_template_content.append(content_fingerprint)
                    if len(self.recently_used_template_content) > 20:
                        self.recently_used_template_content = self.recently_used_template_content[-15:]
                    
                    return template_str
        
        # If we couldn't find a unique template after many attempts, just pick one
        # This ensures we always return something even if variety isn't perfect
        category_key = random.choice(available_categories)
        template_list = templates_by_category.get(category_key, [])
        if template_list:
            selected_template = random.choice(template_list)
            
            # Still update tracking even for fallback selection
            self.recently_used_categories.append(category_key)
            if len(self.recently_used_categories) > 15:
                self.recently_used_categories = self.recently_used_categories[-10:]
                
            return selected_template

        return "This work is relevant to the discussion."