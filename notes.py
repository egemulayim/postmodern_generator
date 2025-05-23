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
from data import philosophers, concepts, terms
from data import philosopher_key_works, academic_journals, bibliography_title_templates, publishers
from capitalization import ensure_proper_capitalization_with_italics, italicize_terms_in_text, apply_title_case

# Dictionary of authors with non-standard name formatting
NON_STANDARD_AUTHOR_FORMATS = {
    "bell hooks": "hooks, bell"
}

class NoteSystem:
    """
    A system for managing notes (footnotes) and bibliography entries in a postmodern essay.
    This ensures coherence between the notes, the main text, and bibliography.
    Now implements MLA 9 style citations.
    """
    
    def __init__(self):
        """Initialize the note system."""
        self.notes = []
        self.works_cited = []  # Changed from bibliography to works_cited
        self.citation_markers = {}  # Maps reference to note number
        self.used_template_patterns = set()  # Track used template pattern types
        self.used_template_fingerprints = set()  # Track specific template structures
        self.page_numbers = {}  # Maps reference to page number(s)
        # Track which authors have multiple works
        self.author_work_count = {}  # Maps author to count of their works
        self.author_works = {}  # Maps author to dict of their works (title -> full reference)
    
    def add_citation(self, reference, context=None):
        """
        Add a citation reference to the notes system.
        
        Args:
            reference (str): The full reference to cite
            context (dict, optional): Context about where this citation is used
                                     (e.g., concepts, terms being discussed)
        
        Returns:
            str: The citation marker to insert in the text in MLA 9 format
        """
        # Extract author, year, and title for in-text citation
        author, year = self._extract_author_year(reference)
        title_key = self._extract_title_sorting_key(reference)
        
        # Check if a similar reference already exists (avoid duplicates)
        if not self._is_duplicate_reference(reference):
            self.works_cited.append(reference)
            
            # Update author work tracking
            if author not in self.author_work_count:
                self.author_work_count[author] = 1
                self.author_works[author] = {}
            else:
                self.author_work_count[author] += 1
            
            # Map this title to the full reference
            self.author_works[author][title_key] = reference
        
        # Generate a page number if not already assigned
        if reference not in self.page_numbers:
            self.page_numbers[reference] = random.randint(1, 300)
        
        page_num = self.page_numbers[reference]
        
        # In MLA 9, if an author has multiple works, include short title in citation
        # Format: (Author, "Title" Page) for articles or (Author, Title Page) for books
        if self.author_work_count.get(author, 0) > 1:
            # Determine if it's a book or article based on whether title is in quotes
            is_article = '"' in reference
            
            # Get a shortened version of the title (first few words)
            short_title = self._get_short_title(title_key, is_article)
            
            if is_article:
                # For articles, the title is in quotes
                mla_citation = f"({author}, \"{short_title}\" {page_num})"
            else:
                # For books, the title is italicized
                mla_citation = f"({author}, {short_title} {page_num})"
        else:
            # If author has only one work, standard format: (Author Page)
            mla_citation = f"({author} {page_num})"
        
        # Create a substantive note that provides commentary beyond just the citation
        # Only create a note if this reference hasn't been used before
        if reference not in self.citation_markers:
            note_number = len(self.notes) + 1
            self.citation_markers[reference] = note_number
            
            # Create a substantive note that provides commentary beyond just the citation
            note_text = self._generate_substantive_note(reference, context, note_number)
            self.notes.append((note_number, note_text))
        
        return mla_citation
    
    def _get_short_title(self, title, is_article=False):
        """
        Create a shortened version of a title for in-text citations.
        
        Args:
            title (str): The full title
            is_article (bool): Whether this is an article (for formatting)
            
        Returns:
            str: A shortened title suitable for in-text citation
        """
        # Clean the title
        clean_title = title.strip()
        
        # Split into words
        words = clean_title.split()
        
        # For very short titles, use the whole thing
        if len(words) <= 3:
            return clean_title
        
        # For longer titles, use first 3-4 significant words
        # Skip initial articles like "The", "A", "An" in the count
        skip_words = ["the", "a", "an", "of", "in", "on", "for", "and", "or"]
        
        # Get the first 3-4 significant words
        significant_words = []
        for word in words:
            # Skip very common words at the beginning
            if not significant_words and word.lower() in skip_words:
                continue
            significant_words.append(word)
            if len(significant_words) >= 3:
                break
        
        # Join them back together
        short_title = " ".join(significant_words)
        
        # If it ends with punctuation like colon, remove it
        short_title = re.sub(r'[:\.,;]$', '', short_title)
        
        return short_title
    
    def add_indirect_citation(self, original_author, secondary_reference, context=None):
        """
        Add an indirect citation using MLA 9 "qtd. in" format
        
        Args:
            original_author (str): The author being quoted
            secondary_reference (str): The full reference where the quote was found
            context (dict, optional): Context about the citation
            
        Returns:
            str: MLA 9 formatted indirect citation
        """
        # Make sure secondary source is in works cited
        if secondary_reference not in self.works_cited and not self._is_duplicate_reference(secondary_reference):
            self.works_cited.append(secondary_reference)
            
            # Update author work tracking
            secondary_author, _ = self._extract_author_year(secondary_reference)
            title_key = self._extract_title_sorting_key(secondary_reference)
            
            if secondary_author not in self.author_work_count:
                self.author_work_count[secondary_author] = 1
                self.author_works[secondary_author] = {}
            else:
                self.author_work_count[secondary_author] += 1
            
            # Map this title to the full reference
            self.author_works[secondary_author][title_key] = secondary_reference
        
        # Extract author and assign page number
        secondary_author, _ = self._extract_author_year(secondary_reference)
        title_key = self._extract_title_sorting_key(secondary_reference)
        
        if secondary_reference not in self.page_numbers:
            self.page_numbers[secondary_reference] = random.randint(1, 300)
        
        page_num = self.page_numbers[secondary_reference]
        
        # Determine if we need to include title for the secondary source
        if self.author_work_count.get(secondary_author, 0) > 1:
            # Get a shortened version of the title
            is_article = '"' in secondary_reference
            short_title = self._get_short_title(title_key, is_article)
            
            # Format citation based on whether it's an article or book
            if is_article:
                mla_citation = f"({original_author}, qtd. in {secondary_author}, \"{short_title}\" {page_num})"
            else:
                mla_citation = f"({original_author}, qtd. in {secondary_author}, {short_title} {page_num})"
        else:
            # Standard format if author has only one work
            mla_citation = f"({original_author}, qtd. in {secondary_author} {page_num})"
        
        # Add substantive note if needed
        if secondary_reference not in self.citation_markers:
            note_number = len(self.notes) + 1
            self.citation_markers[secondary_reference] = note_number
            
            note_text = self._generate_substantive_note(secondary_reference, context, note_number)
            self.notes.append((note_number, note_text))
        
        return mla_citation
    
    def _extract_author_year(self, reference):
        """
        Extract author and year from a reference.
        
        Args:
            reference (str): The reference string
            
        Returns:
            tuple: (author, year)
        """
        # Try extracting from standard MLA 9 journal article format
        # Format: "Last, First. "Title." Journal, vol. Vol, no. No, Year, pp. Pages."
        journal_match = re.match(r'^([^\.]+)\.\s*"[^"]+\."', reference)
        if journal_match:
            author = journal_match.group(1).strip()
            # For MLA style, only use last name
            if ',' in author:
                last_name = author.split(',')[0].strip()
                return last_name, "n.d."  # Year will be extracted from reference text for note
            return author, "n.d."
        
        # Try extracting from MLA 9 book format
        # Format: "Last, First. Title. Publisher, Year."
        book_match = re.match(r'^([^\.]+)\.\s*([^\.]+)\.', reference)
        if book_match:
            author = book_match.group(1).strip()
            if ',' in author:
                last_name = author.split(',')[0].strip()
                return last_name, "n.d."
            return author, "n.d."
            
        # Try other formats (legacy fallback pattern)
        legacy_match = re.match(r'^([^(]+)\(([0-9]{4})\)', reference)
        if legacy_match:
            author = legacy_match.group(1).strip()
            year = legacy_match.group(2).strip()
            # For MLA style, only use last name
            if ',' in author:
                last_name = author.split(',')[0].strip()
                return last_name, year
            return author, year
            
        # Extract just the first word as fallback (likely a last name)
        first_word_match = re.match(r'^(\w+)', reference)
        if first_word_match:
            return first_word_match.group(1), "n.d."
            
        return "Unknown", "n.d."
    
    def _is_duplicate_reference(self, reference):
        """
        Check if a reference is a duplicate of an existing one.
        
        Args:
            reference (str): The reference to check
        
        Returns:
            bool: True if duplicate found, False otherwise
        """
        # Extract the author and title
        author = self._extract_author_for_note(reference)
        title = self._extract_title_sorting_key(reference)
        
        # Check for duplicates with same author and similar title
        for ref in self.works_cited:
            ref_author = self._extract_author_for_note(ref)
            ref_title = self._extract_title_sorting_key(ref)
            
            # If same author and similar title, consider it a duplicate
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
        # Convert to lowercase and strip punctuation
        t1 = re.sub(r'[^\w\s]', '', title1.lower()) if title1 else ""
        t2 = re.sub(r'[^\w\s]', '', title2.lower()) if title2 else ""
        
        # If either title is empty, assume not similar
        if not t1 or not t2:
            return False
            
        # If titles are identical after cleaning, they're similar
        if t1 == t2:
            return True
            
        # If one is a substring of the other, they're similar
        if t1 in t2 or t2 in t1:
            return True
            
        # If the titles share significant words, they're similar
        words1 = set(t1.split())
        words2 = set(t2.split())
        common_words = words1.intersection(words2)
        
        # If they share more than 60% of the words, consider them similar
        if len(words1) == 0 or len(words2) == 0:
            return False
        similarity_ratio = len(common_words) / max(len(words1), len(words2))
        return similarity_ratio > 0.6
    
    def _extract_title_sorting_key(self, reference):
        """
        Extract the title from a reference for sorting.
        
        Args:
            reference (str): The reference string
            
        Returns:
            str: Title for sorting
        """
        # Try to extract the title for articles (in quotes)
        title_match = re.search(r'"\s*([^"]+?)\s*"', reference)
        if title_match:
            return title_match.group(1).lower()
        
        # Try for books (after author and before publisher)
        book_match = re.match(r'^[^\.]+\.\s+([^\.]+)\.', reference)
        if book_match:
            return book_match.group(1).lower()
        
        # Fallback
        return ""
    
    def _generate_substantive_note(self, reference, context, note_number):
        """
        Generate a substantive footnote that includes both a brief citation and additional commentary.
        
        Args:
            reference (str): The reference being cited
            context (dict): Context about the citation
            note_number (int): The note number
        
        Returns:
            str: The formatted note text
        """
        # Extract author name for the note
        author_name = self._extract_author_for_note(reference)
        
        # Generate substantive commentary based on the citation context
        commentary = self._generate_commentary(reference, context)
        
        # Combine for a substantive note that doesn't just repeat the bibliography
        note_text = f"{commentary}"
        
        return note_text
    
    def _extract_author_for_note(self, reference):
        """
        Extract author name from reference for use in note.
        
        Args:
            reference (str): The reference string
            
        Returns:
            str: Author name
        """
        # Try to match MLA 9 journal article format
        journal_match = re.match(r'^([^\.]+)\.\s*"[^"]+\."', reference)
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
        
        return ""
    
    def _get_template_fingerprint(self, template):
        """
        Generate a fingerprint for a template to identify structurally similar templates.
        This looks at the pattern of the template, not the specific content.
        
        Args:
            template (str): Template string to analyze
            
        Returns:
            str: A fingerprint string representing the template's structure
        """
        # Replace specific placeholders with generic markers
        fingerprint = template.lower()
        
        # Replace variable portions with generic markers
        fingerprint = re.sub(r'\{[^}]+\}', '{}', fingerprint)
        
        # Create a pattern signature based on key phrases and structure
        pattern_markers = [
            # Original markers
            "this represents one of", "most", "engagements with", "establishing",
            "what distinguishes this", "methodological framework", "setting it apart",
            "this concept of", "differs significantly from", "framework",
            "contemporary scholarship", "continues to", "framework established",
            "initially received", "before being", "in discussions of",
            "critical responses to", "have been notably", "particularly regarding",
            "when read alongside", "reveals the", "within the field",
            "this work's", "anticipated key developments", "would later conceptualize",
            "this analysis of", "draws upon but extends beyond", "earlier formulation",
            "the development of this idea parallels", "recent research",
            "later revised this", "in light of criticisms",
            "this intervention in debates", "reception", "this work represents",
            "despite its", "maintains relevance for", "engagements with",
            "this examination of", "approaches developed in", "analysis of",
            "can be traced through", "marks a pivotal", "situates the concept",
            "as an historical intervention", "stands as a corrective",
            "established a new paradigm", "methodological innovation", "yields insights", 
            "significant contribution lies", "privileges", "hybrid methodology",
            "theoretical implications", "advances a novel", "by retheorizing",
            "enduring theoretical contribution", "theoretical intervention", "challenges the conventional",
            "reconceptualizes it as", "reception of this work", "critics of this approach",
            "academic reception shifted", "among theorists", "critical reception has varied",
            "scholarly reception has evolved", "contrasted with", "unlike contemporaneous",
            "approaches through", "invites comparison with", "productive comparison",
            "treats as primarily", "formulation has influenced", "concept as developed",
            "lasting influence", "scholars continue to draw", "enduring impact",
            "theoretical model proposed", "has been critiqued by", "key limitation",
            "subsequent scholarship has challenged", "groundbreaking in its treatment",
            "has questioned whether", "recent scholarship has identified",
            "despite subsequent", "current scholarship", "framework for understanding",
            "continuing relevance", "emerged in a different", "contemporary theorists",
            "represents a transition", "intellectual trajectory", "mature position",
            "established conceptual foundations", "captures distinctive", "frameworks developed here",
            "pivotal reassessment", "radical departure", "definitive statement",
            "landmark contribution", "foundational text", "representative example",
            "exemplary case", "characteristic instance", "prototypical model",
            "frequently cited", "widely discussed", "extensively debated",
            "significant impact", "major influence", "central reference point",
            "generative stimulus", "catalytic force", "intellectual precursor",
            "demonstrates how", "illustrates that", "argues persuasively",
            "convincingly establishes", "effectively challenges", "provocatively suggests",
            "insightfully proposes", "astutely observes", "contends that",
            "extends our understanding", "expands conventional", "offers a nuanced",
            "provides a sophisticated", "presents a complex", "articulates a refined",
            "formulates an elegant", "elaborates a comprehensive", "sketches a preliminary",
            "frequently misinterpreted", "often oversimplified", "sometimes misconstrued",
            "commonly misunderstood", "generally underappreciated", "historically overlooked",
            "subsequent reappraisals", "evolving interpretation", "shifting reception",
            "varied responses", "divergent assessments", "competing evaluations"
        ]
        
        # Create a signature based on which patterns are present
        signature = []
        for marker in pattern_markers:
            if marker in fingerprint:
                signature.append(marker)
        
        return "|".join(signature)
    
    def _select_unique_template(self, templates_by_category):
        """
        Select a template that hasn't been used before in this generation,
        ensuring variety by avoiding templates with similar structure.
        
        Args:
            templates_by_category (dict): Dictionary of templates organized by category
            
        Returns:
            str: A template that provides maximum variety from previously used templates
        """
        # First, choose a category of templates that hasn't been fully used
        available_categories = []
        
        for category, templates in templates_by_category.items():
            # Check if this category has any templates with unused patterns
            has_unused_templates = False
            for template in templates:
                fingerprint = self._get_template_fingerprint(template)
                if fingerprint not in self.used_template_fingerprints:
                    has_unused_templates = True
                    break
            
            if has_unused_templates:
                available_categories.append(category)
        
        # If all categories have been used, reset (use all categories)
        if not available_categories:
            available_categories = list(templates_by_category.keys())
        
        # Select a category
        selected_category = random.choice(available_categories)
        
        # Get templates from this category
        category_templates = templates_by_category[selected_category]
        
        # Find templates whose fingerprints haven't been used
        unused_templates = []
        for template in category_templates:
            fingerprint = self._get_template_fingerprint(template)
            if fingerprint not in self.used_template_fingerprints:
                unused_templates.append((template, fingerprint))
        
        # If no unused templates in this category, select any template
        if not unused_templates:
            template = random.choice(category_templates)
            fingerprint = self._get_template_fingerprint(template)
        else:
            template, fingerprint = random.choice(unused_templates)
        
        # Record this template's fingerprint as used
        self.used_template_fingerprints.add(fingerprint)
        
        return template
    
    def _generate_commentary(self, reference, context):
        """Generate substantive commentary for a note based on context."""
        # Extract author from reference for use in commentary
        author_match = self._extract_author_for_note(reference)
        
        # Generate commentary based on available context
        if context and (context.get('concepts') or context.get('terms')):
            # Select relevant concepts and terms from context
            relevant_concepts = context.get('concepts', [])
            relevant_terms = context.get('terms', [])
            
            # Choose a concept or term to focus on
            focus_topic = (random.choice(list(relevant_concepts)) if relevant_concepts else 
                           random.choice(list(relevant_terms)) if relevant_terms else 
                           random.choice(concepts + terms))
            
            # Find related topics
            related_topics = self._find_related_topics(focus_topic)
            
            # Organize templates by category for better variety
            context_templates_by_category = {
                # Historical context templates
                "historical": [
                    f"Contextually situated within debates on {focus_topic}, this work emerged as {random.choice(['a response to', 'an intervention in', 'a reconsideration of', 'a challenge to'])} prevailing scholarship on {random.choice(related_topics)}.",
                    f"The historical significance of this contribution lies in how it {random.choice(['reframes', 'repositions', 'recalibrates', 'reconfigures'])} discussions of {focus_topic} within broader theoretical conversations about {random.choice(related_topics)}.",
                    f"The intellectual genealogy of this approach to {focus_topic} can be traced through {random.choice(philosophers)}'s earlier work, though with notable divergences in methodology.",
                    f"This text marks a pivotal moment in scholarship on {focus_topic}, preceding later developments in {random.choice(related_topics)} by nearly a decade.",
                    f"Approaching {focus_topic} from a historicist perspective, this work situates the concept within larger intellectual traditions that shaped {random.choice(related_topics)}.",
                    f"When viewed as an historical intervention, this work on {focus_topic} stands as a corrective to earlier conceptualizations of {random.choice(related_topics)}.",
                    f"This publication arrived at a crucial moment in debates about {focus_topic}, offering a timely intervention in discussions that had previously neglected {random.choice(related_topics)}.",
                    f"Chronologically positioned between early formulations of {focus_topic} and more recent theorizations, this work serves as an important bridge in conceptual development.",
                    f"The historical context of the early {random.choice(['1970s', '1980s', '1990s', '2000s'])} shaped this investigation of {focus_topic}, particularly in relation to contemporaneous developments in {random.choice(related_topics)}.",
                    f"As a foundational text in the study of {focus_topic}, this work established parameters that would influence subsequent generations of scholarship on {random.choice(related_topics)}.",
                    f"This landmark contribution to the study of {focus_topic} emerged during a paradigm shift in how scholars approached {random.choice(related_topics)}.",
                    f"The significance of this work becomes clearer when situated within the intellectual currents of its time, particularly debates surrounding {focus_topic} and {random.choice(related_topics)}.",
                ],
                
                # Methodological templates
                "methodological": [
                    f"Methodologically, this examination of {focus_topic} {random.choice(['draws from', 'combines', 'synthesizes', 'integrates'])} approaches developed in {random.choice(philosophers)}'s analysis of {random.choice(related_topics)}.",
                    f"The analytical approach to {focus_topic} deployed here established a new paradigm that distinguishes itself from the conventional study of {random.choice(related_topics)}.",
                    f"The methodological innovation of applying {random.choice(['dialectical analysis', 'deconstructive reading', 'genealogical critique', 'semiotic analysis'])} to {focus_topic} yields insights unavailable through standard approaches to {random.choice(related_topics)}.",
                    f"A significant contribution lies in this work's methodological framework, which approaches {focus_topic} through the lens of {random.choice(['historicity', 'materiality', 'temporality', 'spatiality'])} rather than through {random.choice(related_topics)}.",
                    f"Unlike previous studies of {focus_topic}, the methodology employed here privileges {random.choice(['empirical evidence', 'textual analysis', 'structural relations', 'conceptual genealogy'])} over theoretical abstraction.",
                    f"In its approach to {focus_topic}, this work employs a hybrid methodology that combines {random.choice(['empirical research', 'theoretical speculation', 'historical contextualization', 'conceptual analysis'])} with attention to {random.choice(related_topics)}.",
                    f"Methodologically innovative, this study introduces a {random.choice(['multi-modal', 'cross-disciplinary', 'meta-theoretical', 'trans-historical'])} approach to {focus_topic} that reconfigures its relationship to {random.choice(related_topics)}.",
                    f"The methodological apparatus developed here allows for a more sophisticated analysis of the interplay between {focus_topic} and {random.choice(related_topics)} than previous frameworks permitted.",
                    f"This approach to {focus_topic} demonstrates methodological rigor through its {random.choice(['systematic consideration', 'meticulous examination', 'careful analysis', 'thorough investigation'])} of factors previously overlooked in studies of {random.choice(related_topics)}.",
                    f"Among the work's most significant contributions is its methodological framework, which offers new analytical tools for examining {focus_topic} without reducing it to aspects of {random.choice(related_topics)}.",
                    f"By establishing methodological parameters for studying {focus_topic}, this work has influenced how researchers approach the empirical dimensions of {random.choice(related_topics)}.",
                    f"The distinctive methodological approach pioneered here has become a model for scholars seeking to navigate the complexities of {focus_topic} and its relation to {random.choice(related_topics)}.",
                ],
                
                # Theoretical templates
                "theoretical": [
                    f"The theoretical implications of this work extend well beyond {focus_topic}, especially in relation to how we conceptualize {random.choice(related_topics)} in contemporary discourse.",
                    f"This work advances a novel theoretical position on {focus_topic} that subsequent scholars have adapted for analyzing {random.choice(related_topics)}.",
                    f"By retheorizing {focus_topic} as a {random.choice(['process', 'structure', 'relation', 'practice'])}, this work transforms our understanding of {random.choice(related_topics)}.",
                    f"The most enduring theoretical contribution lies in how this work positions {focus_topic} in relation to broader questions about {random.choice(related_topics)}.",
                    f"As a theoretical intervention, this work challenges the conventional separation between {focus_topic} and {random.choice(related_topics)}.",
                    f"Rather than treating {focus_topic} as primarily {random.choice(['theoretical', 'practical', 'empirical', 'methodological'])}, this work reconceptualizes it as fundamentally {random.choice(['relational', 'processual', 'structural', 'contingent'])}.",
                    f"The theoretical framework elaborated here recasts {focus_topic} through a lens that illuminates previously obscured connections to {random.choice(related_topics)}.",
                    f"This work's theoretical innovation lies in its {random.choice(['problematization', 'reconceptualization', 'reinterpretation', 'reformulation'])} of {focus_topic} as intrinsically connected to questions of {random.choice(related_topics)}.",
                    f"The conceptual architecture developed in this analysis of {focus_topic} offers theoretical resources for addressing persistent questions about {random.choice(related_topics)}.",
                    f"In theoretical terms, this work locates {focus_topic} within a broader matrix of questions concerning {random.choice(related_topics)} and related phenomena.",
                    f"What makes this theoretical intervention distinctive is its treatment of {focus_topic} as {random.choice(['constitutive of', 'irreducible to', 'inextricable from', 'complementary to'])} rather than separate from {random.choice(related_topics)}.",
                    f"The theoretical paradigm established here reorients scholarly attention to aspects of {focus_topic} previously marginalized in discussions of {random.choice(related_topics)}.",
                    f"This work offers a theoretical vocabulary that articulates the complex relationship between {focus_topic} and {random.choice(related_topics)} with unprecedented precision.",
                ],
                
                # Critical reception templates
                "reception": [
                    f"The reception of this work was shaped by contemporaneous debates about {focus_topic}, particularly among scholars focused on {random.choice(related_topics)}.",
                    f"Critics of this approach to {focus_topic} have questioned its applicability to {random.choice(related_topics)}, while proponents emphasize its conceptual flexibility.",
                    f"The academic reception shifted from initial {random.choice(['skepticism', 'enthusiasm', 'indifference', 'curiosity'])} toward greater {random.choice(['acceptance', 'critique', 'engagement', 'application'])} as scholars recognized its relevance to {random.choice(related_topics)}.",
                    f"Among theorists of {focus_topic}, this work has provoked ongoing debate about its implications for how we understand {random.choice(related_topics)}.",
                    f"The critical reception has varied across disciplines, with scholars in {random.choice(['philosophy', 'cultural studies', 'literary theory', 'social sciences'])} finding it more productive than those working on {random.choice(related_topics)}.",
                    f"The scholarly reception has evolved from focusing on this work's limitations regarding {focus_topic} to exploring its unexpected insights about {random.choice(related_topics)}.",
                    f"Responses to this work's treatment of {focus_topic} have been notably {random.choice(['polarized', 'ambivalent', 'nuanced', 'contextual'])}, especially regarding implications for {random.choice(related_topics)}.",
                    f"The work's reception history reveals shifting theoretical priorities in the field, from initial focus on its approach to {focus_topic} toward greater interest in its contributions to understanding {random.choice(related_topics)}.",
                    f"This analysis of {focus_topic} has been both celebrated and contested, with particular debate surrounding its implications for conventional approaches to {random.choice(related_topics)}.",
                    f"While initially recognized primarily for its contributions to understanding {focus_topic}, subsequent scholarship has increasingly emphasized this work's significance for theorizing {random.choice(related_topics)}.",
                    f"The reception of this work illustrates broader disciplinary tensions, as scholars from different traditions have emphasized distinct aspects of its approach to {focus_topic} and {random.choice(related_topics)}.",
                    f"Over time, critical assessments have shifted from questioning the work's theoretical premises regarding {focus_topic} to exploring its methodological implications for studying {random.choice(related_topics)}.",
                ],
                
                # Comparative templates
                "comparative": [
                    f"Contrasted with {random.choice(philosophers)}'s approach to {focus_topic}, this work emphasizes {random.choice(['continuity', 'rupture', 'contradiction', 'ambivalence'])} rather than {random.choice(['structure', 'agency', 'temporality', 'spatiality'])}.",
                    f"Unlike contemporaneous works on {focus_topic}, this study situates the concept within broader debates about {random.choice(related_topics)}.",
                    f"Where {random.choice(philosophers)} approaches {focus_topic} through {random.choice(['dialectical analysis', 'structural critique', 'historical contextualization', 'textual deconstruction'])}, this work employs {random.choice(['genealogical investigation', 'phenomenological description', 'semiotic analysis', 'discursive mapping'])}.",
                    f"This analysis invites comparison with {self._get_alternative_reference(reference)}, particularly in how both navigate the relationship between {focus_topic} and {random.choice(related_topics)}.",
                    f"A productive comparison can be drawn with {random.choice(philosophers)}'s treatment of {random.choice(related_topics)}, which approaches the topic from a complementary theoretical perspective.",
                    f"Unlike {random.choice(philosophers)}, who treats {focus_topic} as primarily {random.choice(['discursive', 'material', 'symbolic', 'political'])}, this work emphasizes its {random.choice(['practical', 'theoretical', 'historical', 'ethical'])} dimensions.",
                    f"This conception of {focus_topic} differs markedly from {random.choice(philosophers)}'s formulation, particularly regarding implications for understanding {random.choice(related_topics)}.",
                    f"Compared to standard treatments of {focus_topic}, this work offers a more {random.choice(['nuanced', 'comprehensive', 'critical', 'systematic'])} account of its relationship to {random.choice(related_topics)}.",
                    f"The approach developed here diverges from {random.choice(philosophers)}'s influential analysis of {focus_topic}, especially in how it conceptualizes connections to {random.choice(related_topics)}.",
                    f"While sharing certain premises with {random.choice(philosophers)}'s account of {focus_topic}, this work reaches substantively different conclusions about its relationship to {random.choice(related_topics)}.",
                    f"This formulation stands in productive tension with {self._get_alternative_reference(reference)}'s analysis, particularly regarding the conceptual boundaries between {focus_topic} and {random.choice(related_topics)}.",
                    f"When read against {random.choice(philosophers)}'s approach to {focus_topic}, this work reveals alternative theoretical pathways for exploring connections to {random.choice(related_topics)}.",
                    f"This analysis complements rather than contradicts {random.choice(philosophers)}'s work on {focus_topic}, offering additional perspectives on its relation to {random.choice(related_topics)}.",
                ],
                
                # Influential impact templates
                "influence": [
                    f"This formulation of {focus_topic} has influenced subsequent work on {random.choice(related_topics)}, particularly in the research of {random.choice(philosophers)}.",
                    f"The concept of {focus_topic} as developed here has been productively applied to studies of {random.choice(related_topics)} by later theorists.",
                    f"This work's lasting influence can be seen in how contemporary scholars approach the relationship between {focus_topic} and {random.choice(related_topics)}.",
                    f"Scholars continue to draw on this framework when analyzing {focus_topic}, particularly in relation to emerging questions about {random.choice(related_topics)}.",
                    f"The enduring impact of this work lies in how it transformed scholarly discourse about {focus_topic}, introducing terminology and concepts now standard in discussions of {random.choice(related_topics)}.",
                    f"The theoretical model proposed here continues to structure debates about {focus_topic}, even as scholars apply it to questions about {random.choice(related_topics)} unanticipated by the original work.",
                    f"This analysis has exerted considerable influence on subsequent theorizations of {focus_topic}, establishing conceptual parameters that continue to shape work on {random.choice(related_topics)}.",
                    f"The framework established here has become a reference point for scholars working at the intersection of {focus_topic} and {random.choice(related_topics)}.",
                    f"This work's most significant impact lies in how it has enabled new approaches to studying the relationship between {focus_topic} and {random.choice(related_topics)}.",
                    f"Subsequent generations of scholars working on {focus_topic} have built upon this foundation while extending its implications for understanding {random.choice(related_topics)}.",
                    f"The conceptual vocabulary introduced here has become standard in discussions of {focus_topic}, particularly when addressing its connection to {random.choice(related_topics)}.",
                    f"This work's influence extends beyond studies of {focus_topic} proper to shape broader theoretical conversations about {random.choice(related_topics)} and related phenomena.",
                    f"The analytical framework developed here has been applied to diverse contexts beyond those initially considered, demonstrating its flexibility for studying various aspects of {random.choice(related_topics)}.",
                ],
                
                # Critical engagement templates
                "critique": [
                    f"This work has been critiqued by {random.choice(philosophers)} for its approach to {focus_topic}, particularly regarding implications for understanding {random.choice(related_topics)}.",
                    f"A key limitation identified by critics concerns how this conceptualization of {focus_topic} tends to obscure certain aspects of {random.choice(related_topics)}.",
                    f"Subsequent scholarship has challenged this approach to {focus_topic}, arguing for greater attention to its relationship with {random.choice(related_topics)}.",
                    f"While groundbreaking in its treatment of {focus_topic}, this work has been critiqued for insufficient attention to questions of {random.choice(['power', 'agency', 'materiality', 'historicity'])} in relation to {random.choice(related_topics)}.",
                    f"{random.choice(philosophers)} has questioned whether this framework adequately addresses the complexities of {focus_topic}, particularly in contexts where {random.choice(related_topics)} is central.",
                    f"Recent scholarship has identified tensions in how this work conceptualizes {focus_topic}, suggesting modifications that better account for {random.choice(related_topics)}.",
                    f"Critical assessments of this approach to {focus_topic} have highlighted its potential limitations for addressing certain dimensions of {random.choice(related_topics)}.",
                    f"While acknowledging this work's contributions to understanding {focus_topic}, {random.choice(philosophers)} has raised important questions about its implications for theorizing {random.choice(related_topics)}.",
                    f"Some scholars have contested this framework's applicability to contemporary manifestations of {focus_topic}, particularly in relation to evolving understandings of {random.choice(related_topics)}.",
                    f"This conception of {focus_topic} has been productively critiqued for its handling of the relationship between {focus_topic} and {random.choice(related_topics)}.",
                    f"Critics have noted potential blind spots in this approach to {focus_topic}, particularly regarding its treatment of aspects central to current understandings of {random.choice(related_topics)}.",
                    f"{random.choice(philosophers)} has engaged critically with this framework, questioning its adequacy for addressing emerging questions about the relationship between {focus_topic} and {random.choice(related_topics)}.",
                    f"Feminist scholars have challenged aspects of this approach to {focus_topic}, particularly its implications for understanding gendered dimensions of {random.choice(related_topics)}.",
                ],
                
                # Contemporary relevance templates
                "contemporary": [
                    f"Despite subsequent theoretical developments, this approach to {focus_topic} remains valuable for addressing contemporary questions about {random.choice(related_topics)}.",
                    f"Current scholarship on {focus_topic} builds upon this foundation while addressing aspects of {random.choice(related_topics)} that have become more salient.",
                    f"This framework for understanding {focus_topic} has proven adaptable to emerging questions about {random.choice(related_topics)} in contemporary contexts.",
                    f"The continuing relevance of this work stems from how it positioned {focus_topic} in relation to enduring questions about {random.choice(related_topics)}.",
                    f"Though this framework emerged in a different intellectual context, it anticipates current debates about the relationship between {focus_topic} and {random.choice(related_topics)}.",
                    f"Contemporary theorists of {focus_topic} continue to engage with this framework, adapting it to address changing conceptions of {random.choice(related_topics)}.",
                    f"This analysis of {focus_topic} retains relevance for contemporary scholars, particularly those investigating its complex relationship with {random.choice(related_topics)}.",
                    f"Current work on {focus_topic} frequently returns to this framework, finding resources for addressing new questions about {random.choice(related_topics)}.",
                    f"Despite changing theoretical fashions, this approach to {focus_topic} continues to inform scholarly understanding of its relationship to {random.choice(related_topics)}.",
                    f"Contemporary scholarship has found new applications for this framework, particularly in exploring emergent connections between {focus_topic} and {random.choice(related_topics)}.",
                    f"The questions this work raises about {focus_topic} remain central to current theoretical debates, particularly regarding implications for {random.choice(related_topics)}.",
                    f"This analysis anticipated current concerns with the relationship between {focus_topic} and {random.choice(related_topics)}, demonstrating its theoretical foresight.",
                    f"The renewed interest in this work reflects its continuing relevance for scholars navigating contemporary questions about {focus_topic} and its relation to {random.choice(related_topics)}.",
                ],
                
                # Author development templates
                "author_development": [
                    f"This work represents a transition in the author's thinking about {focus_topic}, moving from earlier concerns with {random.choice(related_topics)} toward more developed theoretical positions.",
                    f"In the author's intellectual trajectory, this work marks a significant reorientation in approaching {focus_topic}, with implications for later engagements with {random.choice(related_topics)}.",
                    f"This analysis reflects the author's mature position on {focus_topic}, differing from earlier works that emphasized {random.choice(related_topics)}.",
                    f"Through this study of {focus_topic}, the author established conceptual foundations that would inform subsequent investigations of {random.choice(related_topics)}.",
                    f"This work captures the author's distinctive theoretical voice, particularly in how it negotiates the relationship between {focus_topic} and {random.choice(related_topics)}.",
                    f"The frameworks developed here would become characteristic of the author's approach to both {focus_topic} and questions concerning {random.choice(related_topics)}.",
                    f"Within the author's broader oeuvre, this analysis of {focus_topic} represents a pivotal development in their theoretical approach to {random.choice(related_topics)}.",
                    f"This work demonstrates the author's evolving perspective on {focus_topic}, moving beyond earlier formulations to engage more directly with questions of {random.choice(related_topics)}.",
                    f"The conceptual innovations the author develops here regarding {focus_topic} would become central to their subsequent work on {random.choice(related_topics)}.",
                    f"This contribution marks a decisive shift in the author's approach to {focus_topic}, establishing theoretical commitments that would inform later explorations of {random.choice(related_topics)}.",
                    f"The analytical framework elaborated here reflects a synthesis of earlier approaches to {focus_topic} while anticipating later work on {random.choice(related_topics)}.",
                    f"This text reveals the author's methodological development, particularly in approaches to studying the relationship between {focus_topic} and {random.choice(related_topics)}.",
                    f"Positioned within the author's intellectual development, this work demonstrates an increasing sophistication in addressing the complexities of {focus_topic} and its relation to {random.choice(related_topics)}.",
                ],
                
                # Disciplinary impact templates
                "disciplinary": [
                    f"This work has shaped disciplinary approaches to {focus_topic}, establishing methodological parameters that continue to influence research on {random.choice(related_topics)}.",
                    f"The disciplinary impact of this analysis extends beyond studies of {focus_topic} to influence how scholars conceptualize {random.choice(related_topics)}.",
                    f"In disciplinary terms, this work's significance lies in how it repositioned {focus_topic} within broader theoretical conversations about {random.choice(related_topics)}.",
                    f"This intervention altered disciplinary boundaries, creating new spaces for dialogue between scholars of {focus_topic} and those focused on {random.choice(related_topics)}.",
                    f"The disciplinary reconfiguration initiated by this work continues to shape how researchers approach the intersection of {focus_topic} and {random.choice(related_topics)}.",
                    f"By challenging disciplinary conventions regarding {focus_topic}, this work opened new avenues for interdisciplinary engagement with {random.choice(related_topics)}.",
                    f"This analysis helped establish {focus_topic} as a legitimate object of scholarly inquiry, particularly in relation to established research on {random.choice(related_topics)}.",
                    f"The cross-disciplinary conversations this work stimulated have proven particularly productive for understanding the relationship between {focus_topic} and {random.choice(related_topics)}.",
                ],
                
                # Philosophical implications templates
                "philosophical": [
                    f"The philosophical stakes of this analysis concern how we conceptualize the relationship between {focus_topic} and {random.choice(related_topics)} as categories of thought.",
                    f"This work raises profound philosophical questions about the conceptual boundaries between {focus_topic} and {random.choice(related_topics)}.",
                    f"The ontological implications of this approach to {focus_topic} extend to how we understand the existential dimensions of {random.choice(related_topics)}.",
                    f"By reconsidering the philosophical foundations of {focus_topic}, this work necessarily reframes questions central to {random.choice(related_topics)}.",
                    f"The epistemological framework developed here offers new resources for thinking about both {focus_topic} and its relationship to {random.choice(related_topics)}.",
                    f"This analysis contributes to philosophical debates about the nature of {focus_topic} and its conceptual relationship to {random.choice(related_topics)}.",
                ],
                
                # Political implications templates
                "political": [
                    f"The political implications of this approach to {focus_topic} become evident when considering its relationship to questions of {random.choice(related_topics)}.",
                    f"This work's political significance lies in how it reframes the relationship between {focus_topic} and {random.choice(related_topics)} as sites of contestation.",
                    f"By positioning {focus_topic} as a political category, this analysis necessarily reconfigures conventional understandings of {random.choice(related_topics)}.",
                    f"The political stakes of this framework become apparent through its treatment of the relationship between {focus_topic} and structures of {random.choice(related_topics)}.",
                    f"This approach to {focus_topic} has significant political implications, particularly regarding questions of agency in relation to {random.choice(related_topics)}.",
                    f"The framework developed here enables a more nuanced political analysis of the relationship between {focus_topic} and systemic dimensions of {random.choice(related_topics)}.",
                ],
                
                # Original contribution templates
                "original": [
                    f"This work provides an important critique of {focus_topic} that challenges conventional understandings of {random.choice(related_topics)}.",
                    f"The concept of {focus_topic} differs significantly from its usage in {random.choice(philosophers)}'s framework.",
                    f"While focusing on {focus_topic}, the work also offers insights into the related question of {random.choice(related_topics)}.",
                    f"For a contrasting perspective that critiques this position on {focus_topic}, see {self._get_alternative_reference(reference)}.",
                    f"This analysis of {focus_topic} represents a landmark contribution that redefined scholarly approaches to {random.choice(related_topics)}.",
                    f"The approach to {focus_topic} developed here establishes conceptual distinctions that continue to structure debates about {random.choice(related_topics)}.",
                ],
                
                # Terminological innovation templates
                "terminological": [
                    f"The terminological precision this work brings to discussions of {focus_topic} has clarified its conceptual relationship to {random.choice(related_topics)}.",
                    f"By introducing new terminology for analyzing {focus_topic}, this work enables more nuanced engagement with questions of {random.choice(related_topics)}.",
                    f"The conceptual vocabulary developed here has become standard in discussions of the relationship between {focus_topic} and {random.choice(related_topics)}.",
                    f"This work's terminological innovations have shaped how subsequent scholars articulate the connection between {focus_topic} and {random.choice(related_topics)}.",
                    f"The analytical lexicon introduced here provides tools for navigating the complex relationship between {focus_topic} and various dimensions of {random.choice(related_topics)}.",
                    f"This analysis establishes terminological distinctions that have proven productive for theorizing the relationship between {focus_topic} and {random.choice(related_topics)}.",
                ]
            }
            
            # Select a template that maximizes variety
            return self._select_unique_template(context_templates_by_category)
        else:
            # Fallback if no specific context is provided - varied general templates
            general_templates_by_category = {
                # Historical significance
                "historical": [
                    f"This work emerged at a critical juncture in theoretical debates, challenging prevailing paradigms in significant ways.",
                    f"The historical context of this publication coincided with broader intellectual shifts in methodological approaches.",
                    f"This contribution should be understood within the intellectual climate of its period, which was characterized by substantial disciplinary realignments.",
                    f"The publication of this work marked a significant moment in the evolving discourse on theoretical methodology.",
                    f"Emerging during a period of paradigmatic uncertainty, this work both reflects and reshapes the intellectual currents of its time.",
                    f"As a product of its historical moment, this work captures the tension between established theoretical traditions and emerging critical frameworks.",
                    f"Historically situated at the intersection of competing theoretical traditions, this work synthesizes diverse intellectual currents.",
                    f"The timing of this publication gave it particular resonance, appearing during a period of substantial methodological reassessment.",
                    f"As part of a broader intellectual movement of the period, this work participated in redefining disciplinary boundaries.",
                    f"This text emerged from a specific historical context that shaped both its concerns and its reception.",
                    f"Produced during a transitional period in theoretical discourse, this work bridges earlier paradigms with emerging approaches.",
                    f"The historical significance of this work becomes clearer when situated within broader intellectual developments of its era.",
                ],
                
                # Methodological contributions
                "methodological": [
                    f"The methodological innovations introduced here offered alternatives to established approaches in the field.",
                    f"What distinguishes this work is its integration of previously disparate analytical frameworks.",
                    f"The approach combines theoretical precision with contextual sensitivity in ways that merit methodological attention.",
                    f"By introducing novel methodological tools, this work enabled investigations previously considered beyond disciplinary boundaries.",
                    f"The methodological framework developed here demonstrates how theoretical questions can be approached through multiple analytical lenses.",
                    f"This work exemplifies rigorous methodological pluralism, drawing from diverse theoretical traditions without reducing one to another.",
                    f"Methodologically innovative, this study established new parameters for analyzing complex theoretical questions.",
                    f"The analytical method developed here offers resources for navigating persistent conceptual problems.",
                    f"This work's methodological sophistication is evident in how it navigates competing theoretical frameworks.",
                    f"By establishing methodological criteria for addressing theoretical questions, this work has influenced subsequent approaches.",
                    f"The research method elaborated here offers a model of conceptual clarity in addressing complex theoretical questions.",
                    f"This contribution's methodological significance lies in how it explicitly addresses questions often left implicit in theoretical discourse.",
                ],
                
                # Theoretical contributions
                "theoretical": [
                    f"The theoretical architecture of this work reveals a sophisticated engagement with fundamental conceptual problems.",
                    f"By reconceptualizing key analytical categories, this analysis makes substantial contributions to theoretical debates.",
                    f"The conceptual innovations introduced in this study have generated productive theoretical reconsiderations.",
                    f"This work establishes conceptual distinctions that would become foundational for subsequent theoretical developments.",
                    f"Rather than merely applying existing frameworks, this study develops an original theoretical vocabulary.",
                    f"The theoretical perspective advanced here challenges conventional distinctions between previously separated conceptual domains.",
                    f"This analysis offers a theoretical framework that productively reframes persistent questions in the field.",
                    f"By articulating a coherent theoretical position, this work provides conceptual resources for addressing diverse questions.",
                    f"The theoretical model elaborated here has demonstrated remarkable flexibility in application to varied contexts.",
                    f"This contribution's theoretical significance lies in how it integrates previously disconnected conceptual frameworks.",
                    f"As a theoretical intervention, this work establishes parameters that continue to structure disciplinary conversations.",
                    f"The conceptual framework developed here offers new ways of navigating established theoretical problems.",
                ],
                
                # Critical reception 
                "reception": [
                    f"Critical responses to this work have evolved significantly over time, reflecting changing theoretical priorities.",
                    f"The initial reception was marked by methodological skepticism that has since given way to broader acceptance.",
                    f"Scholarly engagement with this work has been characterized by productive tensions between competing interpretations.",
                    f"This contribution continues to generate critical debate, particularly regarding its analytical presuppositions.",
                    f"The reception history of this work reveals shifting disciplinary concerns rather than inherent theoretical limitations.",
                    f"Academic responses have varied across national and linguistic traditions, with particularly significant engagement in {random.choice(['European', 'North American', 'Latin American', 'Asian'])} scholarship.",
                    f"The critical reception has moved from early debate about methodological questions to later engagement with theoretical implications.",
                    f"This work's reception illustrates broader disciplinary tensions regarding appropriate analytical approaches.",
                    f"Critical assessments have shifted markedly over time, from initial skepticism to recognition of lasting contributions.",
                    f"The scholarly conversation surrounding this work demonstrates how reception often reflects changing theoretical priorities.",
                    f"This contribution has been both celebrated and contested, generating productive disagreement about fundamental questions.",
                    f"The reception history offers insight into evolving disciplinary standards and theoretical concerns.",
                ],
                
                # Legacy and influence
                "influence": [
                    f"The enduring influence of this work can be seen in its continued citation across diverse theoretical contexts.",
                    f"Subsequent scholarship has both built upon and critically reassessed the foundations established in this analysis.",
                    f"The intellectual legacy of this contribution extends beyond its immediate theoretical context to inform broader methodological approaches.",
                    f"This work's influence can be traced through multiple scholarly genealogies, often in surprising theoretical domains.",
                    f"By establishing a new conceptual vocabulary, this work has shaped how subsequent scholars frame their research questions.",
                    f"The analytical framework introduced here continues to structure debates across multiple fields, though often in modified form.",
                    f"This contribution has exerted substantial influence on how scholars approach fundamental questions in the field.",
                    f"The impact of this work extends well beyond its original context, informing developments in adjacent fields.",
                    f"As a foundational text, this analysis has shaped subsequent generations of scholarship in both direct and indirect ways.",
                    f"The theoretical model developed here has proven remarkably adaptable to questions beyond those initially addressed.",
                    f"This work's lasting significance lies in how it established parameters for subsequent theoretical developments.",
                    f"The conceptual framework introduced here has become standard reference in discussions of fundamental theoretical questions.",
                ],
                
                # Comparative perspectives
                "comparative": [
                    f"When considered alongside {random.choice(philosophers)}'s contributions, this work reveals significant conceptual parallels despite different theoretical orientations.",
                    f"Comparative analysis with contemporary scholarship highlights both the prescience and limitations of this theoretical approach.",
                    f"The analytical framework developed here bears important comparison with {self._get_alternative_reference(reference)}, particularly regarding methodological assumptions.",
                    f"This work's theoretical position becomes clearer when juxtaposed with competing frameworks developed by {random.choice(philosophers)} and others.",
                    f"A productive comparison can be drawn with {random.choice(philosophers)}'s contemporaneous work, which approaches similar questions through a different theoretical lens.",
                    f"Unlike many contemporaries, this work anticipates theoretical developments that would only later become central to the field.",
                    f"When read alongside similar contributions, this work's distinctive approach to theoretical questions becomes more apparent.",
                    f"Compared with contemporaneous scholarship, this analysis offers a more systematic treatment of fundamental conceptual issues.",
                    f"Viewed in relation to subsequent theoretical developments, this work's innovative qualities become more evident.",
                    f"This contribution can be productively compared with parallel developments in adjacent fields during the same period.",
                    f"The distinctiveness of this approach becomes clearer through comparison with conventional methodologies of its time.",
                    f"Juxtaposed with related work by {random.choice(philosophers)}, this analysis reveals alternative theoretical pathways.",
                ],
                
                # Hermeneutical significance
                "hermeneutical": [
                    f"This work offers hermeneutical resources for interpreting complex theoretical phenomena beyond those directly addressed.",
                    f"The interpretive framework developed here has proven productive for approaching diverse textual and conceptual problems.",
                    f"As a contribution to hermeneutical theory, this work establishes principles for navigating difficult interpretive questions.",
                    f"This analysis demonstrates interpretive sophistication through its engagement with ambiguous theoretical material.",
                    f"The hermeneutical approach developed here has influenced how scholars interpret complex theoretical texts.",
                    f"This work's significance lies partly in its articulation of interpretive principles applicable across diverse contexts.",
                ],
                
                # Conceptual impact
                "conceptual": [
                    f"The conceptual framework established here has demonstrated remarkable durability despite shifting theoretical fashions.",
                    f"By introducing key conceptual distinctions, this work has enabled more precise analysis of complex phenomena.",
                    f"The conceptual vocabulary developed here continues to structure discussions of fundamental theoretical issues.",
                    f"This analysis offers conceptual tools that have proven adaptable to diverse theoretical contexts.",
                    f"The precision with which this work articulates central concepts has contributed to its lasting influence.",
                    f"This contribution's significance lies in its careful elaboration of conceptual relationships often left implicit.",
                ],
                
                # Stylistic innovations
                "stylistic": [
                    f"Stylistically innovative, this work demonstrates how form and content mutually inform theoretical exposition.",
                    f"The rhetorical strategies employed here complement the theoretical positions advanced.",
                    f"This analysis exemplifies how stylistic choices can enhance rather than obscure theoretical clarity.",
                    f"The writing style developed here balances technical precision with accessibility.",
                    f"This work's rhetorical sophistication enhances rather than detracts from its theoretical contributions.",
                    f"By developing a distinctive writing style, this contribution demonstrates the importance of rhetoric in theoretical discourse.",
                ],
                
                # Interdisciplinary significance
                "interdisciplinary": [
                    f"This work's interdisciplinary approach has influenced scholarship across traditional disciplinary boundaries.",
                    f"By bridging previously separated fields, this analysis has stimulated cross-disciplinary conversations.",
                    f"The interdisciplinary framework developed here offers resources for scholars working across conventional divisions.",
                    f"This contribution demonstrates how theoretical questions can be productively addressed through interdisciplinary methods.",
                    f"The significance of this work extends across disciplinary boundaries, informing diverse fields of inquiry.",
                    f"This analysis exemplifies productive interdisciplinary engagement with complex theoretical questions.",
                ],
                
                # Philosophical foundations
                "philosophical": [
                    f"The philosophical foundations of this work support its more specific theoretical claims about disciplinary questions.",
                    f"By engaging explicitly with philosophical traditions, this analysis situates specific questions within broader theoretical contexts.",
                    f"This work's philosophical sophistication is evident in how it addresses fundamental questions underlying disciplinary debates.",
                    f"The philosophical framework developed here provides resources for addressing persistent conceptual problems.",
                    f"This analysis demonstrates philosophical rigor through its careful treatment of foundational theoretical questions.",
                    f"By addressing philosophical assumptions often left implicit, this work clarifies the conceptual terrain of its field.",
                ],
                
                # Empirical contributions
                "empirical": [
                    f"This work's empirical contributions complement its theoretical framework, demonstrating practical applications.",
                    f"By grounding theoretical claims in empirical investigation, this analysis avoids abstraction disconnected from concrete phenomena.",
                    f"The balance of theoretical and empirical components distinguishes this work from purely speculative approaches.",
                    f"This study employs empirical evidence strategically to support broader theoretical arguments.",
                    f"The empirical dimensions of this work demonstrate how theoretical frameworks can illuminate concrete phenomena.",
                    f"By incorporating substantive empirical material, this analysis bridges theoretical abstraction and practical application.",
                ],
                
                # Political dimensions
                "political": [
                    f"The political implications of this work extend beyond its explicit theoretical concerns.",
                    f"This analysis engages with political questions through a theoretical framework that illuminates practical concerns.",
                    f"Without reducing theoretical questions to political positions, this work acknowledges their interconnection.",
                    f"The political dimensions of this analysis emerge through its treatment of fundamental theoretical problems.",
                    f"This work demonstrates how theoretical questions intersect with political concerns without being reducible to them.",
                    f"By addressing political implications of theoretical positions, this analysis avoids false neutrality.",
                ],
                
                # Original templates
                "original": [
                    f"This work represents an important intervention in the field.",
                    f"The methodological approach merits further consideration.",
                    f"For related perspectives, see also {self._get_alternative_reference(reference)}.",
                    f"This theoretical framework has been influential in subsequent scholarship.",
                    f"This argument has been contested by several scholars, most notably {random.choice(philosophers)}.",
                    f"This represents a landmark contribution to theoretical discourse.",
                    f"The significance of this work transcends its immediate context.",
                    f"As a foundational text, this work continues to reward careful study.",
                    f"This contribution exemplifies rigorous engagement with complex theoretical questions.",
                    f"The lasting importance of this analysis stems from its methodological innovations.",
                    f"This work has generated productive debate across multiple scholarly generations.",
                    f"As an exemplary case of theoretical precision, this analysis warrants continued attention.",
                ]
            }
            
            # Select a template that maximizes variety
            return self._select_unique_template(general_templates_by_category)
    
    def _find_related_topics(self, topic):
        """Find topics (concepts or terms) related to the given topic."""
        try:
            # Try to use concept clusters if available
            from data import concept_clusters
            
            # Check if topic is in any cluster
            for cluster, topics_in_cluster in concept_clusters.items():
                if topic in topics_in_cluster:
                    return [t for t in topics_in_cluster if t != topic]
            
            # If no match in clusters, try related terms
            all_topics = concepts + terms
            return random.sample([t for t in all_topics if t != topic], min(3, len(all_topics) - 1))
            
        except ImportError:
            # Fallback if concept_clusters isn't available
            all_topics = concepts + terms
            return random.sample([t for t in all_topics if t != topic], min(3, len(all_topics) - 1))
    
    def _get_alternative_reference(self, reference):
        """Generate an alternative reference as a suggestion in a note."""
        from reference import generate_reference
        
        # Extract author from current reference
        author_match = re.match(r'^([^(]+)', reference)
        current_author = author_match.group(1).strip() if author_match else ""
        
        # Generate alternatives until we find one with a different author
        for _ in range(5):  # Try up to 5 times
            alt_ref = generate_reference()
            alt_author_match = re.match(r'^([^(]+)', alt_ref)
            alt_author = alt_author_match.group(1).strip() if alt_author_match else ""
            
            if alt_author and alt_author != current_author:
                # Extract and return just the citation information
                return self._extract_author_year(alt_ref)[0]
        
        # Fallback to a random philosopher if we couldn't generate a unique reference
        return f"{random.choice(philosophers)}"
    
    def get_authentic_work(self, philosopher_name, is_article=False, fallback_year=None):
        """
        Retrieves an authentic work for a given philosopher from the data.py resources.
        
        Args:
            philosopher_name (str): Full name of the philosopher
            is_article (bool): Whether to generate an article or book
            fallback_year (int, optional): Year to use if no authentic work is found
            
        Returns:
            tuple: (title, year, co-author or None)
        """
        # Try to match philosopher to our database of authentic works
        clean_name = philosopher_name.strip()
        
        # Check for philosopher in our authentic works database
        if clean_name in philosopher_key_works:
            # Select a random authentic work
            work_info = random.choice(philosopher_key_works[clean_name])
            title = work_info[0]
            year = work_info[1]
            co_author = work_info[2] if len(work_info) > 2 else None
            return (title, year, co_author)
        
        # Check for philosopher as co-author
        for key in philosopher_key_works:
            if " & " in key and clean_name in key:
                work_info = random.choice(philosopher_key_works[key])
                title = work_info[0]
                year = work_info[1]
                co_author = key.replace(clean_name, "").replace(" & ", "").strip()
                return (title, year, co_author)
        
        # For Deleuze, check if we should use a co-authored work with Guattari
        if clean_name == "Gilles Deleuze" and random.random() < 0.4:  # 40% chance for co-authored work
            work_info = random.choice(philosopher_key_works["Gilles Deleuze & Félix Guattari"])
            return (work_info[0], work_info[1], "Félix Guattari")
        
        # No authentic work found, generate a plausible title
        year = fallback_year or random.randint(max(1950, 2023 - random.randint(20, 70)), min(2020, 2023 - 3))
        
        # Get concepts for the title
        concept = random.choice(concepts)
        concept2 = random.choice([c for c in concepts if c != concept])
        
        # Get a random adjective for title templates that need it
        from data import adjectives
        adj = random.choice(adjectives)
        
        # Choose a title template and fill it
        template = random.choice(bibliography_title_templates)
        title = template.format(concept=concept.capitalize(), concept2=concept2.capitalize(), adj=adj)
        
        return (title, year, None)

    def get_varied_journal(self):
        """Returns a varied academic journal from data.py resources."""
        return random.choice(academic_journals)

    def get_varied_publisher(self):
        """Returns a varied academic publisher from data.py resources."""
        return random.choice(publishers)

    def get_realistic_page_range(self):
        """Returns a realistic page range for a journal article."""
        start_page = random.randint(1, 100)
        page_length = random.randint(15, 45)  # Most academic articles are 15-45 pages
        end_page = start_page + page_length
        return f"{start_page}-{end_page}"

    def get_enhanced_citation(self, philosopher_name, is_article=False, fallback_year=None):
        """
        Creates a more authentic citation for a philosopher's work using data from data.py.
        
        Args:
            philosopher_name (str): Full name of the philosopher
            is_article (bool): Whether this is a journal article
            fallback_year (int, optional): Year to use if no authentic work is found
            
        Returns:
            str: A properly formatted citation
        """
        # Get authentic work if available, or generate a plausible one
        title_info = self.get_authentic_work(philosopher_name, is_article, fallback_year)
        title, year, co_author = title_info
        
        # Format author name for MLA style (Last, First)
        name_parts = philosopher_name.split()
        
        # Check for authors with non-standard name formatting
        if philosopher_name.lower() in NON_STANDARD_AUTHOR_FORMATS:
            author = NON_STANDARD_AUTHOR_FORMATS[philosopher_name.lower()]
        elif len(name_parts) > 1:
            author = f"{name_parts[-1]}, {' '.join(name_parts[:-1])}"
        else:
            author = name_parts[0]
        
        # Apply title case to title
        title = apply_title_case(title)
        
        # Handle co-author if present
        if co_author:
            co_name_parts = co_author.split()
            if len(co_name_parts) > 1:
                co_author_fmt = f"{co_name_parts[-1]}, {' '.join(co_name_parts[:-1])}"
            else:
                co_author_fmt = co_name_parts[0]
            author_text = f"{author} and {co_author_fmt}"
        else:
            author_text = author
        
        # Build the citation in MLA format
        if is_article:
            journal = self.get_varied_journal()
            volume = random.randint(1, 40)
            issue = random.randint(1, 4)
            pages = self.get_realistic_page_range()
                
            # MLA 9 journal article format
            return f"{author_text}. \"{title}.\" {journal}, vol. {volume}, no. {issue}, {year}, pp. {pages}."
        else:
            # MLA 9 book format
            publisher = self.get_varied_publisher()    
            return f"{author_text}. {title}. {publisher}, {year}."
    
    def add_to_works_cited(self, reference):
        """
        Add a reference to the works cited without creating a note.
        
        Args:
            reference (str): The full reference to add to the works cited
            
        Returns:
            None
        """
        if reference not in self.works_cited and not self._is_duplicate_reference(reference):
            self.works_cited.append(reference)
            
            # Update author work tracking
            author = self._extract_author_for_note(reference)
            title_key = self._extract_title_sorting_key(reference)
            
            if author not in self.author_work_count:
                self.author_work_count[author] = 1
                self.author_works[author] = {}
            else:
                self.author_work_count[author] += 1
            
            # Map this title to the full reference
            self.author_works[author][title_key] = reference
    
    def generate_notes_section(self):
        """
        Generate the complete notes section for the essay.
        
        Returns:
            str: Formatted notes section
        """
        if not self.notes:
            return ""
        
        notes_text = "## Notes\n\n"
        for number, text in self.notes:
            # Format the note text with proper capitalization and italicization
            formatted_text = self._format_note_text(text)
            # Remove the extra blank line between notes - just use a single newline
            notes_text += f"[^{number}]: {formatted_text}\n"
        
        # Add an extra newline at the end to ensure proper spacing between sections
        notes_text += "\n"
        
        return notes_text
    
    def generate_works_cited_section(self):
        """
        Generate the complete Works Cited section for the essay.
        
        Returns:
            str: Formatted Works Cited section
        """
        if not self.works_cited:
            return ""
        
        works_cited_text = "## Works Cited\n\n"
        
        # Group references by author
        author_groups = {}
        for reference in self.works_cited:
            author_key = self._extract_author_sorting_key(reference)
            if author_key not in author_groups:
                author_groups[author_key] = []
            author_groups[author_key].append(reference)
        
        # Sort author keys alphabetically
        sorted_authors = sorted(author_groups.keys())
        
        # Process each author's works
        for author_key in sorted_authors:
            references = author_groups[author_key]
            
            # Sort this author's references by title
            references.sort(key=lambda ref: self._extract_title_sorting_key(ref))
            
            # Format and add each reference
            for i, reference in enumerate(references):
                # Format the reference with proper MLA 9 style
                formatted_ref = self._format_works_cited_entry(reference)
                
                # Apply three hyphens rule for subsequent works by the same author
                if i > 0:
                    # Replace the author part with three hyphens, preserving proper punctuation
                    if "." in formatted_ref:
                        author_end_index = formatted_ref.find(".")
                        # Check if there's a period right at the author name boundary
                        if author_end_index > 0:
                            # Keep any periods that are part of initials
                            has_period_already = formatted_ref[:author_end_index].strip().endswith(".")
                            if has_period_already:
                                # If author already ends with period (like an initial), replace differently
                                formatted_ref = "---. " + formatted_ref[author_end_index+1:].strip()
                            else:
                                # Normal case - author doesn't end with period
                                formatted_ref = "---. " + formatted_ref[author_end_index+1:].strip()
                
                # Add hanging indentation
                lines = formatted_ref.split('\n')
                if len(lines) > 1:
                    for j in range(1, len(lines)):
                        lines[j] = "    " + lines[j]  # Add 4 spaces for hanging indent
                    formatted_ref = '\n'.join(lines)
                
                works_cited_text += f"{formatted_ref}\n\n"
        
        return works_cited_text

    def _extract_author_sorting_key(self, reference):
        """
        Extract a key for sorting references alphabetically by author.
        
        Args:
            reference (str): The reference string
            
        Returns:
            str: A key for sorting
        """
        # Try to extract the author name
        author_match = re.match(r'^([^\.]+)\.', reference)
        if author_match:
            author = author_match.group(1).strip().lower()
            
            # Handle special cases like "hooks, bell"
            if author == "hooks, bell":
                return "hooks"
                
            return author
        
        # Fallback to the beginning of the reference
        return reference.split(' ')[0].lower()
    
    def _format_note_text(self, note_text):
        """Format a note text with proper capitalization and italicization."""
        # Special handling for notes with initials
        # First, identify patterns like "Smith, J.'s analysis"
        initial_pattern = r'([A-Z][a-z]+),\s+([A-Z]\.)\s*\'s\s+([a-z])'
        
        # Replace with correctly capitalized version (don't auto-capitalize after the possessive)
        note_text = re.sub(initial_pattern, lambda m: f"{m.group(1)}, {m.group(2)}'s {m.group(3)}", note_text)
        
        # Apply proper capitalization
        formatted_text = ensure_proper_capitalization_with_italics(note_text)
        
        # Apply italicization to terms
        formatted_text = italicize_terms_in_text(formatted_text)
        
        return formatted_text
    
    def _format_works_cited_entry(self, entry):
        """Format a Works Cited entry with proper MLA 9 style."""
        # Fix extra spaces and periods in author names
        author_pattern = r'^([^\.]+)\.'
        author_match = re.search(author_pattern, entry)
        if author_match:
            author_part = author_match.group(1)
            # Fix extra spaces and periods
            fixed_author_part = re.sub(r'\s+\.\s+', ' ', author_part)
            # Replace in the original entry
            entry = entry.replace(author_part, fixed_author_part)
        
        # Process author names for consistency (use full names instead of initials)
        # Let's first parse to identify the type of entry
        
        # Check if it's an MLA formatted book or journal article
        mla_pattern = r'^([^\.]+)\.\s*(.*?)\.'
        mla_match = re.match(mla_pattern, entry)
        
        if mla_match:
            author_part = mla_match.group(1).strip()
            rest_of_entry = entry[len(author_part)+1:].strip()
            
            # Fix extra spaces and periods in author name
            # Special fix for middle initials: Correct patterns like "Lastname, Firstname M. . "
            author_part = re.sub(r'([A-Z]\.)\s+\.', r'\1', author_part)
            
            # Fix any other spacing issues with periods
            author_part = re.sub(r'(\s*\.\s*)+', '. ', author_part.strip()).strip()
            if author_part.endswith('.'):
                author_part = author_part[:-1]  # Remove trailing period
            
            # Convert authors with initials to full names (when not a special case like "hooks, bell")
            if re.search(r',\s+[A-Z]\.', author_part) and not author_part.lower() == "hooks, bell":
                # Only apply author name expansion for entries with initials
                author_part = self._expand_author_initials(author_part)

            # Check if the entry contains a title in quotes (article) or not (book)
            if '"' in rest_of_entry:  # It's an article
                # Extract the title from quotes
                title_match = re.search(r'"([^"]+)"', rest_of_entry)
                if title_match:
                    title = title_match.group(1).strip()
                    # Apply title case properly
                    title = apply_title_case(title)
                    
                    # Remove any period at the end of the title to avoid double periods
                    if title.endswith('.'):
                        title = title[:-1]  # Remove trailing period
                    
                    # Find everything after the title
                    after_title_index = rest_of_entry.find('"', rest_of_entry.find('"') + 1) + 1  # Find the closing quote and move past it
                    if after_title_index > 0:
                        after_title = rest_of_entry[after_title_index:].strip()
                        
                        # Check for duplicate title pattern
                        duplicate_title_pattern = rf'^\.\s*"{re.escape(title)}\.?"'
                        if re.match(duplicate_title_pattern, after_title):
                            # Skip the duplicated title
                            after_title = re.sub(duplicate_title_pattern, '', after_title).strip()
                            
                        # Remove leading period if present
                        if after_title.startswith('.'):
                            after_title = after_title[1:].strip()
                        
                        # Add correct period after author name
                        author_period = "" if author_part.endswith(".") else "."
                        return f"{author_part}{author_period} \"{title}.\" {after_title}"
                    else:
                        # Fallback if we can't find the end of the title
                        author_period = "" if author_part.endswith(".") else "."
                        return f"{author_part}{author_period} \"{title}.\" {rest_of_entry.split('\"', 2)[-1].strip()}"
            else:  # It's a book
                # For books, titles are not in quotes
                title_end = rest_of_entry.find('.')
                if title_end != -1:
                    title = rest_of_entry[:title_end].strip()
                    # Apply title case properly
                    title = apply_title_case(title)
                    
                    # Get everything after the title
                    after_title = rest_of_entry[title_end+1:].strip()
                    
                    # Check for duplicate title pattern
                    duplicate_title_pattern = rf'^{re.escape(title)}\.?'
                    if re.match(duplicate_title_pattern, after_title):
                        # Skip the duplicated title
                        after_title = re.sub(duplicate_title_pattern, '', after_title).strip()
                    
                    # Remove leading period if present
                    if after_title.startswith('.'):
                        after_title = after_title[1:].strip()
                    
                    # Add correct period after author name
                    author_period = "" if author_part.endswith(".") else "."
                    return f"{author_part}{author_period} {title}. {after_title}"
                else:
                    # If no period found, just use the rest as title
                    title = rest_of_entry.strip()
                    title = apply_title_case(title)
                    author_period = "" if author_part.endswith(".") else "."
                    return f"{author_part}{author_period} {title}."
        
        # If we couldn't parse the entry properly, return it as is
        return entry
    
    def _expand_author_initials(self, author_part):
        """
        Convert author with initials to full names for consistency.
        
        Args:
            author_part (str): The author part of the reference (e.g., "Smith, J.")
            
        Returns:
            str: Author with expanded initials (e.g., "Smith, John")
        """
        # Special cases - don't process these
        if author_part.lower() == "hooks, bell":
            return author_part
            
        # Common first names for initials
        first_name_map = {
            'A': 'Albert', 'B': 'Benjamin', 'C': 'Catherine', 'D': 'David', 
            'E': 'Elizabeth', 'F': 'Frederick', 'G': 'George', 'H': 'Hannah',
            'I': 'Isaac', 'J': 'John', 'K': 'Katherine', 'L': 'Laura',
            'M': 'Michael', 'N': 'Nicole', 'O': 'Oliver', 'P': 'Patricia',
            'Q': 'Quincy', 'R': 'Robert', 'S': 'Sarah', 'T': 'Thomas',
            'U': 'Ursula', 'V': 'Victoria', 'W': 'William', 'X': 'Xavier',
            'Y': 'Yvonne', 'Z': 'Zachary'
        }
        
        # Pattern for Last, Initial. format
        pattern = r'([^,]+),\s+([A-Z])\.(\s+.*)?'
        
        match = re.match(pattern, author_part)
        if match:
            last_name = match.group(1)
            initial = match.group(2)
            rest = match.group(3) if match.group(3) else ""
            
            # Replace with full name
            full_name = first_name_map.get(initial, initial + "name")
            return f"{last_name}, {full_name}{rest}"
            
        return author_part