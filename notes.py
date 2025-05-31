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
        self.used_template_patterns = set()  # Track used template pattern types
        self.used_template_fingerprints = set()  # Track specific template structures
        self.page_numbers = {}  # Maps reference to page number(s)
        # Track which authors have multiple works
        self.author_work_count = {}  # Maps author to count of their works
        self.author_works = {}  # Maps author to dict of their works (title -> full reference)
        self.recently_used_note_templates = [] # For reducing immediate repetition of note commentary
        self.recently_used_formatted_commentaries = [] # Track recently *generated* commentaries
        self.style = "endnotes"
    
    def reset(self):
        """Reset the note system to its initial state."""
        self.notes = []
        self.works_cited = []
        self.citation_markers = {}
        self.used_template_patterns = set()
        self.used_template_fingerprints = set()
        self.page_numbers = {}
        self.author_work_count = {}
        self.author_works = {}
        self.recently_used_note_templates = [] # Reset for new essay
        self.recently_used_formatted_commentaries = [] # Reset for new essay
    
    def add_citation(self, reference, context=None):
        """
        Add a citation. If it's the first substantive mention, a footnote marker [^N] is returned.
        Otherwise, a standard MLA parenthetical citation (Author Page) is returned.
        """
        full_author_name = self._extract_author_for_note(reference)
        in_text_author = self._get_author_for_in_text_citation(full_author_name)
        title_key = self._extract_title_sorting_key(reference)
        
        if not self._is_duplicate_reference(reference):
            self.works_cited.append(reference)
            
            if full_author_name not in self.author_work_count:
                self.author_work_count[full_author_name] = 1
                self.author_works[full_author_name] = {}
            else:
                self.author_work_count[full_author_name] += 1
            
            self.author_works[full_author_name][title_key] = reference
        
        if reference not in self.page_numbers:
            self.page_numbers[reference] = random.randint(1, 300)
        page_num = self.page_numbers[reference]
        
        citation_to_embed_in_text = ""
        if reference not in self.citation_markers:
            note_number = len(self.notes) + 1
            self.citation_markers[reference] = note_number
            
            commentary = self._generate_substantive_note(reference, context, note_number)
            self.notes.append((note_number, commentary, reference))
            citation_to_embed_in_text = f"[^{note_number}]"
        else:
            current_author_work_count = self.author_work_count.get(full_author_name, 0)
            if current_author_work_count > 1:
                is_article = bool(re.search(r'\"\s*[^\"]+?\s*\"', reference))
                short_title = self._get_short_title(title_key, is_article)
                display_short_title = apply_title_case(short_title)
                if is_article:
                    citation_to_embed_in_text = f"({in_text_author}, \"{display_short_title}\" {page_num})"
                else:
                    citation_to_embed_in_text = f"({in_text_author}, *{display_short_title}* {page_num})"
            else:
                citation_to_embed_in_text = f"({in_text_author} {page_num})"
        
        return citation_to_embed_in_text
    
    def _get_short_title(self, title, is_article=False):
        """
        Create a shortened version of a title for in-text citations.
        
        Args:
            title (str): The full title
            is_article (bool): Whether this is an article (for formatting)
            
        Returns:
            str: A shortened title suitable for in-text citation
        """
        clean_title = title.strip()
        
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
        full_secondary_author_name = self._extract_author_for_note(secondary_reference)
        in_text_secondary_author = self._get_author_for_in_text_citation(full_secondary_author_name)
        title_key = self._extract_title_sorting_key(secondary_reference)

        if not self._is_duplicate_reference(secondary_reference):
            self.works_cited.append(secondary_reference)
            if full_secondary_author_name not in self.author_work_count:
                self.author_work_count[full_secondary_author_name] = 1
                self.author_works[full_secondary_author_name] = {}
            else:
                self.author_work_count[full_secondary_author_name] += 1
            self.author_works[full_secondary_author_name][title_key] = secondary_reference
        
        if secondary_reference not in self.page_numbers:
            self.page_numbers[secondary_reference] = random.randint(1, 300)
        page_num = self.page_numbers[secondary_reference]
        
        citation_to_embed_in_text = ""
        if secondary_reference not in self.citation_markers:
            note_number = len(self.notes) + 1
            self.citation_markers[secondary_reference] = note_number
            commentary = self._generate_substantive_note(secondary_reference, context, note_number)
            self.notes.append((note_number, commentary, secondary_reference))
            citation_to_embed_in_text = f"[^{note_number}]"
        else:
            current_secondary_author_work_count = self.author_work_count.get(full_secondary_author_name, 0)
            if current_secondary_author_work_count > 1:
                is_article = bool(re.search(r'\"\s*[^\"]+?\s*\"', secondary_reference))
                short_title = self._get_short_title(title_key, is_article)
                display_short_title = apply_title_case(short_title)
                if is_article:
                    citation_to_embed_in_text = f"({original_author}, qtd. in {in_text_secondary_author}, \"{display_short_title}\" {page_num})"
                else:
                    citation_to_embed_in_text = f"({original_author}, qtd. in {in_text_secondary_author}, *{display_short_title}* {page_num})"
            else:
                citation_to_embed_in_text = f"({original_author}, qtd. in {in_text_secondary_author} {page_num})"
        
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
            return author
        
        # Try to match MLA 9 book format
        book_match = re.match(r'^([^\.]+)\.\s*([^\.]+)\.', reference)
        if book_match:
            author = book_match.group(1).strip()
            return author
        
        # Legacy format fallback
        legacy_match = re.match(r'^([^(]+)', reference)
        if legacy_match:
            author = legacy_match.group(1).strip()
            return author
        
        return "Unknown Author"
    
    def _format_author_for_commentary(self, author_name_str):
        """Formats an author name for use in note commentary (e.g., First Last)."""
        if not author_name_str or author_name_str == "Unknown Author":
            return "an author"

        if author_name_str.lower() == "bell hooks":
            return "bell hooks"  # Ensure "bell hooks" for commentary

        # For other non-standard names, use the format from NON_STANDARD_AUTHOR_FORMATS
        # This assumes NON_STANDARD_AUTHOR_FORMATS stores the desired display format.
        if author_name_str.lower() in [name.lower() for name in NON_STANDARD_AUTHOR_FORMATS]:
            for name_in_list in NON_STANDARD_AUTHOR_FORMATS:
                if name_in_list.lower() == author_name_str.lower():
                    return name_in_list # Return the exact stored version

        # Standard formatting for other authors (First Last or Last, First -> First Last)
        author_name_str = author_name_str.strip()
        if "," in author_name_str:
            parts = author_name_str.split(",", 1)
            last_name = parts[0].strip()
            first_middle_parts = parts[1].strip().split()
            return " ".join(first_middle_parts) + " " + last_name
        else:
            # Assumes input is already in "First Last" or just "Last" if single name
            return author_name_str

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
        """Generate substantive commentary for a note based on context, aiming for variety and conciseness."""
        
        raw_current_author = self._extract_author_for_note(reference)
        raw_another_philosopher = random.choice(philosophers) if philosophers else "another thinker"

        if raw_current_author and raw_current_author != "Unknown Author" and philosophers and len(philosophers) > 1:
            possible_others = [p for p in philosophers if p != raw_current_author]
            if possible_others:
                raw_another_philosopher = random.choice(possible_others)
        
        ct_auth = self._format_author_for_commentary(raw_current_author)
        an_phil = self._format_author_for_commentary(raw_another_philosopher)
        
        focus_topic = None
        related_topic = None
        
        if context:
            # Prioritize concepts from the immediate context if available
            current_concepts = context.get('current_concepts_in_paragraph', [])
            current_terms = context.get('current_terms_in_paragraph', [])

            if current_concepts:
                focus_topic = random.choice(list(current_concepts))
            elif current_terms:
                focus_topic = random.choice(list(current_terms))
            # Fallback to broader context concepts/terms
            elif context.get('concepts') and isinstance(context['concepts'], list) and context['concepts']:
                focus_topic = random.choice(list(context['concepts']))
            elif context.get('terms') and isinstance(context['terms'], list) and context['terms']:
                focus_topic = random.choice(list(context['terms']))
        
        if focus_topic:
            related_topics_list = self._find_related_topics(focus_topic)
            if related_topics_list:
                related_topic = random.choice(related_topics_list)
        
        if focus_topic:
            f_topic = focus_topic
        elif concepts: # Global concepts list
            f_topic = random.choice(concepts)
        elif terms: # Global terms list
            f_topic = random.choice(terms)
        else:
            f_topic = "the central theme"

        # Ensure related_topic is different from focus_topic and is meaningful
        possible_r_topics_all = [t for t in terms if t != f_topic] + [c for c in concepts if c != f_topic]
        if related_topic and related_topic == f_topic: # If _find_related_topics returned the same topic
            related_topic = None

        if not related_topic and possible_r_topics_all:
            r_topic = random.choice(possible_r_topics_all)
        elif not related_topic: # Fallback if no other distinct topic can be found
            generic_related_topics = ["a secondary aspect", "a related field", "a connected idea", "another dimension", "a broader discussion", "a tangential point", "an underlying assumption", "a contrasting perspective"]
            r_topic = random.choice([grt for grt in generic_related_topics if grt != f_topic])
        else:
            r_topic = related_topic


        master_template_list = {
            "elaboration": [
                f"{ct_auth}'s perspective on {f_topic} is particularly noteworthy here, especially in how it diverges from common interpretations.",
                f"This work offers an important elaboration of {f_topic}, particularly as it concerns {r_topic} and its contemporary relevance.",
                f"The idea of {f_topic} is developed with considerable nuance by {ct_auth} in the work cited, challenging previous understandings.",
                f"This text further elaborates on {f_topic}, critically connecting it to the broader implications of {r_topic}.",
                f"{ct_auth}'s treatment of {f_topic} here provides crucial detail, particularly regarding its influence on the study of {r_topic}.",
                f"One might note {ct_auth}'s specific emphasis on {f_topic} within this work, which reframes its relationship with {r_topic}.",
                f"The cited text explores {f_topic} in depth, offering a unique lens on {r_topic}."
            ],
            "contextualization": [
                f"This source provides important historical context for understanding {f_topic}, especially during its period of emergence and its impact on {r_topic}.",
                f"The intellectual context for {f_topic}, particularly regarding its complex interplay with {r_topic}, is significantly illuminated by this work.",
                f"This reference situates {ct_auth}'s argument on {f_topic} within a broader scholarly debate, one that often involves thinkers like {an_phil} and their views on {r_topic}.",
                f"To understand {f_topic} more fully, {ct_auth}'s work here offers necessary contextualization, particularly when considering the arguments surrounding {r_topic}.",
                f"Consider {an_phil}'s contemporaneous work on {r_topic}; it offers a wider view of the intellectual currents surrounding {f_topic} and {ct_auth}'s contribution.",
                f"{ct_auth}'s analysis of {f_topic} is best understood by considering the prevailing discussions on {r_topic} at the time.",
                f"The work cited is pivotal for grasping the historical significance of {f_topic} in relation to {r_topic}."
            ],
            "critique_comparison": [
                f"This source presents a contrasting viewpoint to {ct_auth} on {f_topic}, often attributed to scholars like {an_phil}, particularly concerning {r_topic}.",
                f"For an alternative interpretation of {f_topic}, consult {an_phil}'s critical work on {r_topic}, which questions some of {ct_auth}'s assumptions.",
                f"This reference provides a critical engagement with {ct_auth}'s main thesis on {f_topic}, which notably diverges from {an_phil}'s position on {r_topic}.",
                f"This text by {ct_auth} engages with themes similar to {an_phil}'s work on {r_topic}, but from a distinctly different theoretical standpoint on {f_topic}.",
                f"A contrasting analysis of {f_topic}, especially in relation to {r_topic}, is presented by {an_phil}, thereby challenging {ct_auth}'s conclusions.",
                f"{ct_auth}'s argument regarding {f_topic} can be juxtaposed with {an_phil}'s treatment of {r_topic} to reveal differing theoretical commitments.",
                f"While {ct_auth} emphasizes {f_topic}, {an_phil} offers a compelling counter-argument focusing on {r_topic}."
            ],
            "foundational_methodological": [
                f"This citation is foundational to {ct_auth}'s subsequent line of argument concerning {f_topic} and its complex relation to {r_topic}.",
                f"Elaboration of the theoretical basis for {f_topic}, as utilized by {ct_auth} in dialogue with {an_phil}'s work on {r_topic}, can be found here.",
                f"Methodological considerations concerning the study of {f_topic} are detailed by {ct_auth} in this source, often contrasted with {an_phil}'s approach to {r_topic}.",
                f"See here for the foundational methodology {ct_auth} applies to {f_topic}, which significantly informs their broader work on {r_topic} and its implications.",
                f"The methodological framework {ct_auth} employs for {f_topic} is crucial for understanding their conclusions about {r_topic}.",
                f"This work details {ct_auth}'s specific methodology regarding {f_topic}, differentiating it from {an_phil}'s research on {r_topic}."
            ],
            "influence_relevance": [
                f"{ct_auth}'s work on {f_topic} had a significant reception, profoundly influencing subsequent discussions on {r_topic} by scholars such as {an_phil}.",
                f"The continuing relevance of {ct_auth}'s original work on {f_topic} is demonstrated by its frequent citation in contemporary studies of {r_topic} and beyond.",
                f"This text by {ct_auth} was influential in shaping debates around {f_topic}, including critical responses from thinkers like {an_phil} concerning {r_topic}.",
                f"The broader implications of {f_topic}, as explored by {ct_auth}, are discussed in this text, particularly in relation to {r_topic} and {an_phil}'s theories on similar subjects.",
                f"The impact of {ct_auth}'s theories on {f_topic} can be seen in how {an_phil} later approached {r_topic}.",
                f"This work's reception shows the widespread influence of {ct_auth}'s ideas on {f_topic}, particularly within discussions of {r_topic}."
            ],
            "general_academic_comment": [
                f"See also the related discussion of {f_topic} by {an_phil} in their work on {r_topic}, which offers a complementary perspective found in this reference.",
                f"The development of {ct_auth}'s thought on {f_topic} is evident here, especially when considering their engagement with {r_topic} and the contrasting views of {an_phil}.",
                f"This reference by {ct_auth} provides further essential context on {f_topic} and its intrinsic connection to {r_topic}, a point also touched upon by {an_phil}.",
                f"This work is illustrative of a broader trend in analyzing {f_topic}, also seen in {an_phil}'s critical examinations of {r_topic} and its contemporary manifestations.",
                f"The nuances of {ct_auth}'s position on {f_topic} are explored in depth here, often touching upon {r_topic} as discussed by {an_phil} in different contexts.",
                f"It is worth noting {ct_auth}'s contribution to the discourse on {f_topic}, which complements {an_phil}'s analysis of {r_topic}.",
                f"The cited passage is particularly relevant for understanding {ct_auth}'s stance on {f_topic} vis-à-vis {r_topic}."
            ],
             "specific_focus": [
                f"{ct_auth}, in this particular text, focuses on the implications of {f_topic} for {r_topic}.",
                f"The primary argument in this cited work by {ct_auth} revolves around {f_topic} and its direct bearing on {r_topic}.",
                f"This reference is key to understanding {ct_auth}'s specific arguments concerning {f_topic} as it relates to {r_topic}.",
                f"Within this work, {ct_auth} unpacks the relationship between {f_topic} and {r_topic} with notable precision.",
                f"A key takeaway from {ct_auth}'s cited text is the intricate connection between {f_topic} and the dynamics of {r_topic}."
            ],
            "theoretical_link": [
                f"{ct_auth} theoretically links {f_topic} with {r_topic}, offering a novel framework.",
                f"The work cited establishes a critical theoretical bridge between {f_topic} and {r_topic}, a contribution of {ct_auth}.",
                f"In this text, {ct_auth} posits a significant, if overlooked, theoretical connection between {f_topic} and {r_topic}.",
                f"One of {ct_auth}'s contributions here is the clear articulation of how {f_topic} and {r_topic} are theoretically intertwined.",
                f"The theoretical architecture {ct_auth} builds around {f_topic} necessarily incorporates an understanding of {r_topic}."
            ]
        }

        chosen_template_text = None
        chosen_raw_template = None # To store the pre-formatted template string for recently_used_note_templates
        attempts = 0
        max_attempts = 70 # Increased attempts for broader search
        history_size = 20 # Increased history size for formatted commentaries
        template_history_size = 15 # For raw templates

        # Flatten all templates and shuffle for variety
        all_templates_with_category = []
        for category, templates in master_template_list.items():
            for tpl_str in templates:
                all_templates_with_category.append((tpl_str, category))
        
        random.shuffle(all_templates_with_category)

        for raw_template_fstring, category in all_templates_with_category:
            # The f-string template itself is now the raw_template
            # We format it to get the potential commentary
            
            # Dynamically create the f-string by evaluating it in the current scope
            # This is inherently unsafe if master_template_list could come from untrusted sources,
            # but here it's internally defined.
            # A safer way would be template.format(ct_auth=ct_auth, ...) but f-strings are used.
            
            # To make this work, we ensure all variables used in the f-string templates 
            # (ct_auth, an_phil, f_topic, r_topic) are defined in this local scope.
            potential_commentary = eval(f"f'{raw_template_fstring.replace("'", "\\'")}'")


            # Check against recently *formatted* commentaries
            if potential_commentary not in self.recently_used_formatted_commentaries and \
               raw_template_fstring not in self.recently_used_note_templates:
                chosen_template_text = potential_commentary
                chosen_raw_template = raw_template_fstring # Store the raw f-string
                self.used_template_patterns.add(category) # Track category usage
                # A simple fingerprint: category + first few words of formatted commentary
                fingerprint = category + ":" + "_".join(chosen_template_text.split()[:3])
                self.used_template_fingerprints.add(fingerprint)
                break
            attempts += 1
            if attempts >= max_attempts:
                # Fallback if too many attempts, try to pick one not in recent formatted list
                # even if its raw template was used, or vice-versa.
                # This prioritizes avoiding exact commentary repeats.
                candidate_fallbacks = []
                for rt_fstr, cat in all_templates_with_category:
                    # Corrected eval line:
                    pc = eval(f"f'{rt_fstr.replace("'", "\\'")}'")
                    if pc not in self.recently_used_formatted_commentaries:
                        candidate_fallbacks.append((pc, rt_fstr))
                if candidate_fallbacks:
                    chosen_template_text, chosen_raw_template = random.choice(candidate_fallbacks)
                break # Exit loop after max_attempts

        if not chosen_template_text:
            # Absolute fallback if no unique option found after extensive search
            fallback_options = [
                f"Further context on {f_topic} is available in the cited work by {ct_auth}.",
                f"{ct_auth} discusses {f_topic} in relation to {r_topic} in this text.",
                f"The cited material by {ct_auth} offers insights into {f_topic}.",
                f"This work by {ct_auth} is relevant to the discussion of {f_topic} and {r_topic}."
            ]
            if self.recently_used_formatted_commentaries:
                 chosen_template_text = random.choice([opt for opt in fallback_options if opt not in self.recently_used_formatted_commentaries] or fallback_options)
            else:
                chosen_template_text = random.choice(fallback_options)
            # chosen_raw_template will be None for this absolute fallback.

        # Add chosen raw template to its history
        if chosen_raw_template: # Only if it's not an absolute fallback
            self.recently_used_note_templates.append(chosen_raw_template)
            if len(self.recently_used_note_templates) > template_history_size:
                self.recently_used_note_templates.pop(0)

        # Add chosen *formatted* commentary to its history
        self.recently_used_formatted_commentaries.append(chosen_template_text)
        if len(self.recently_used_formatted_commentaries) > history_size:
            self.recently_used_formatted_commentaries.pop(0)
            
        return chosen_template_text

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
            
            if '\"' in title:
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
               not (title_part.startswith('\"') and title_part.endswith('\"')):
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
        Tries to ensure variety by not repeating template *structures* or *patterns* too often,
        though true uniqueness of generated text is not guaranteed.

        Args:
            templates_by_category (dict): A dictionary where keys are category names (e.g., "historical")
                                          and values are lists of template strings for that category.
            
        Returns:
            str: A selected template string, or a generic fallback if selection fails.
        """
        if not templates_by_category:
            return "This citation provides additional perspective."

        available_categories = list(templates_by_category.keys())
        
        for _ in range(len(available_categories) * 2):
            category_key = random.choice(available_categories)
            template_list = templates_by_category.get(category_key, [])
            
            if template_list:
                template_str = random.choice(template_list)
                fingerprint = (category_key, template_str.count("{")) 
                
                if fingerprint not in self.used_template_fingerprints:
                    self.used_template_fingerprints.add(fingerprint)
                    if len(self.used_template_fingerprints) > 50:
                        self.used_template_fingerprints.pop()
                    return template_str
        
        category_key = random.choice(available_categories)
        template_list = templates_by_category.get(category_key, [])
        if template_list:
            return random.choice(template_list)

        return "This work is relevant to the discussion."