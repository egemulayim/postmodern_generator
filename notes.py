"""
notes.py - A module for generating footnotes and bibliography entries
that maintain coherence with the main text of the essay.
This module provides a system for managing notes (footnotes) and bibliography entries.
It ensures coherence between the notes, the main text, and bibliography.
It includes functions to add citations, generate substantive notes,
and format bibliography entries.
It also provides functions to format notes and bibliography entries
"""

import random
import re
from data import philosophers, concepts, terms
from capitalization import ensure_proper_capitalization_with_italics, italicize_terms_in_text, apply_title_case

class NoteSystem:
    """
    A system for managing notes (footnotes) and bibliography entries in a postmodern essay.
    This ensures coherence between the notes, the main text, and bibliography.
    """
    
    def __init__(self):
        """Initialize the note system."""
        self.notes = []
        self.bibliography = []
        self.citation_markers = {}  # Maps reference to note number
    
    def add_citation(self, reference, context=None):
        """
        Add a citation reference to the notes system.
        
        Args:
            reference (str): The full reference to cite
            context (dict, optional): Context about where this citation is used
                                     (e.g., concepts, terms being discussed)
        
        Returns:
            str: The citation marker to insert in the text
        """
        # Extract author and year for brief in-text citation
        author_year = self._extract_author_year(reference)
        
        # Add to bibliography if not already there
        if reference not in self.bibliography:
            self.bibliography.append(reference)
        
        # Check if this reference already has a citation marker
        if reference in self.citation_markers:
            note_number = self.citation_markers[reference]
            return f"[^{note_number}]"
        
        # Create a new note with substantive commentary
        note_number = len(self.notes) + 1
        self.citation_markers[reference] = note_number
        
        # Create a substantive note that provides commentary beyond just the citation
        note_text = self._generate_substantive_note(reference, context, note_number)
        self.notes.append((note_number, note_text))
        
        return f"[^{note_number}]"
    
    def _extract_author_year(self, reference):
        """Extract author and year from a reference."""
        # Simple regex to extract author and year from typical reference format
        match = re.match(r'^([^(]+)\(([0-9]{4})\)', reference)
        if match:
            author = match.group(1).strip()
            year = match.group(2).strip()
            # Simplify author if it has multiple names
            if ',' in author:
                last_name = author.split(',')[0].strip()
                return f"{last_name} ({year})"
            return f"{author} ({year})"
        return "Unknown author and date"
    
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
        # Extract author and year from reference
        citation_info = self._extract_author_year(reference)
        
        # Generate substantive commentary based on the citation context
        commentary = self._generate_commentary(reference, context)
        
        # Combine for a substantive note that doesn't just repeat the bibliography
        note_text = f"{citation_info}. {commentary}"
        
        return note_text
    
    def _generate_commentary(self, reference, context):
        """Generate substantive commentary for a note based on context."""
        # Extract author from reference for use in commentary
        author_match = re.match(r'^([^(]+)', reference)
        author = author_match.group(1).strip() if author_match else "The author"
        
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
            
            # Generate commentary templates
            commentary_templates = [
                f"This work provides an important critique of {focus_topic} that challenges conventional understandings of {random.choice(related_topics)}.",
                f"{author}'s argument should be considered alongside {random.choice(philosophers)}'s work on {random.choice(related_topics)}.",
                f"While focusing on {focus_topic}, {author} also offers insights into the related question of {random.choice(related_topics)}.",
                f"For a contrasting perspective that critiques this position on {focus_topic}, see {self._get_alternative_reference(reference)}.",
                f"This concept of {focus_topic} differs significantly from its usage in {random.choice(philosophers)}'s framework.",
                f"{author} later revised this theoretical position in light of criticisms from {random.choice(philosophers)}.",
                f"This analysis of {focus_topic} draws upon but extends beyond {random.choice(philosophers)}'s earlier formulation.",
                f"The development of this idea parallels similar work on {random.choice(related_topics)} in {random.choice(philosophers)}'s recent research."
            ]
            
            return random.choice(commentary_templates)
        else:
            # Fallback if no specific context is provided
            general_templates = [
                f"This work represents an important intervention in the field.",
                f"{author}'s methodological approach merits further consideration.",
                f"For related perspectives, see also {self._get_alternative_reference(reference)}.",
                f"This theoretical framework has been influential in subsequent scholarship.",
                f"This argument has been contested by several scholars, most notably {random.choice(philosophers)}."
            ]
            return random.choice(general_templates)
    
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
            # Fallback if concept_clusters not available
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
                return self._extract_author_year(alt_ref)
        
        # Fallback to a random philosopher if we couldn't generate a unique reference
        return f"{random.choice(philosophers)} (recent work)"
    
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
        
        return notes_text
    
    def generate_bibliography_section(self):
        """
        Generate the complete bibliography section for the essay.
        
        Returns:
            str: Formatted bibliography section
        """
        if not self.bibliography:
            return ""
        
        bibliography_text = "## Bibliography\n\n"
        for reference in self.bibliography:
            # Format the reference with proper capitalization
            formatted_ref = self._format_bibliography_entry(reference)
            bibliography_text += f"{formatted_ref}\n\n"
        
        return bibliography_text
    
    def _format_note_text(self, note_text):
        """Format a note text with proper capitalization and italicization."""
        # Apply proper capitalization
        formatted_text = ensure_proper_capitalization_with_italics(note_text)
        
        # Apply italicization to terms
        formatted_text = italicize_terms_in_text(formatted_text)
        
        return formatted_text
    
    def _format_bibliography_entry(self, entry):
        """Format a bibliography entry with proper capitalization and italicization."""
        # Extract components for individual formatting
        author_year_match = re.match(r'^(.*?)(\([0-9]{4}\))\.(.*)$', entry)
        
        if author_year_match:
            author, year, rest = author_year_match.groups()
            
            # Format author (maintain capitalization)
            author = ensure_proper_capitalization_with_italics(author.strip())
            
            # Find and format title (apply title case)
            title_match = re.search(r'\*(.*?)\*', rest)
            if title_match:
                title = title_match.group(1)
                # Apply title case to the title
                capitalized_title = apply_title_case(title)
                # Replace the title in the rest of the text
                rest = rest.replace(f"*{title}*", f"*{capitalized_title}*")
            
            # Format the rest of the reference
            rest = ensure_proper_capitalization_with_italics(rest)
            
            formatted_entry = f"{author} {year}.{rest}"
        else:
            # If the pattern doesn't match, apply general capitalization
            formatted_entry = ensure_proper_capitalization_with_italics(entry)
        
        # Apply italicization to terms
        formatted_entry = italicize_terms_in_text(formatted_entry)
        
        return formatted_entry