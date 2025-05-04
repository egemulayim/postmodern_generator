"""
A module for generating coherent paragraphs in generated essays.
This module provides functions to create paragraphs with a focus on
thematic coherence, using a variety of transitional expressions and rhetorical devices.
It includes functions to generate paragraphs for different sections of an essay,
such as introductions, general discussions, and conclusions.
The paragraphs are designed to be thematically consistent, incorporating
philosophical concepts, terms, and references to philosophers.
The module also includes a function to ensure proper capitalization
of sentences and proper nouns, as well as a function to generate
metafictional elements for self-referential commentary.
The generated paragraphs are intended to reflect the complexity and depth
of postmodern academic writing, while also adhering to conventional
academic standards and MLA 9 citation formatting.
"""

import random
import re
from collections import Counter
from sentence import generate_sentence
from data import philosophers, concepts, terms, philosopher_concepts, rhetorical_devices, discursive_modes
from capitalization import ensure_proper_capitalization

# Enhanced list of transitional expressions for academic writing
transitional_expressions = [
    # Additive transitions
    "moreover", "furthermore", "additionally", "in addition", "what is more",
    "similarly", "likewise", "in the same vein", "by the same token", "correspondingly",
    
    # Contrastive transitions
    "however", "nonetheless", "nevertheless", "conversely", "on the contrary",
    "on the other hand", "paradoxically", "ironically", "in contrast", "rather",
    "despite this", "notwithstanding", "that said", "even so", "and yet",
    
    # Causal transitions
    "therefore", "consequently", "as a result", "thus", "hence", 
    "accordingly", "it follows that", "for this reason", "in this sense", "in effect",
    
    # Concessive transitions
    "although", "while", "to be sure", "granted", "admittedly",
    "of course", "to be fair", "indeed", "certainly", "undoubtedly",
    
    # Illustrative transitions
    "for instance", "for example", "specifically", "to illustrate", "namely",
    "in particular", "as an example", "to take a case in point", "in other words", "that is",
    
    # Temporal transitions
    "subsequently", "meanwhile", "simultaneously", "eventually", "initially",
    "hitherto", "formerly", "later", "thereafter", "in the interim",
    
    # Restrictive transitions
    "in terms of", "regarding", "with respect to", "concerning", "as for",
    "insofar as", "to the extent that", "in relation to", "vis-à-vis", "relative to",
    
    # Meta-discursive transitions
    "to return to", "to digress briefly", "parenthetically", "in passing", "to resume",
    "to recapitulate", "to reiterate", "to be more precise", "in a broader sense", "strictly speaking",
    
    # Philosophical transitions
    "dialectically speaking", "in a Deleuzian sense", "following Derrida", "in Foucauldian terms",
    "to invoke Baudrillard", "through a Butlerian lens", "within a Lacanian framework",
    "as Spivak might suggest", "in the spirit of Haraway", "echoing Jameson"
]

# References to academic writing conventions
meta_references = [
    "as I have argued elsewhere", "as noted above", "as will become clear",
    "to anticipate a later point", "to foreshadow what follows", "at the risk of repetition",
    "to put it more precisely", "to state the obvious", "to reframe the question",
    "at this juncture", "herein lies the paradox", "the crucial point here is",
    "what remains unexamined", "what requires further elaboration", "what we must interrogate"
]

def generate_paragraph(template_type, num_sentences, references, forbidden_philosophers=[], 
                      forbidden_concepts=[], forbidden_terms=[], mentioned_philosophers=set(), 
                      used_quotes=set(), all_references=None, cited_references=None, 
                      note_system=None, context=None):
    """
    Generate a paragraph by selecting sentences from a pool, ensuring a central theme for coherence.
    Uses MLA 9 citation style for all citations.

    Args:
        template_type (str): Type of paragraph ('introduction', 'general', or 'conclusion')
        num_sentences (int): Number of sentences desired in the paragraph
        references (list): List of references for citations (not used directly)
        forbidden_philosophers (list): Philosophers to exclude from generation
        forbidden_concepts (list): Concepts to exclude from generation
        forbidden_terms (list): Terms to exclude from generation
        mentioned_philosophers (set): Set of philosophers already mentioned in the text
        used_quotes (set): Quotes already used in the essay
        all_references (list): List of all possible references for citation
        cited_references (list): References cited so far in the essay (legacy, use note_system instead)
        note_system (NoteSystem): The note system for managing citations and notes
        context (dict): Contextual information about the paragraph being generated

    Returns:
        tuple: (paragraph_str, used_concepts_in_paragraph, used_terms_in_paragraph)
    """
    # Convert forbidden lists to sets
    forbidden_philosophers_set = set(forbidden_philosophers)
    forbidden_concepts_set = set(forbidden_concepts)
    forbidden_terms_set = set(forbidden_terms)

    used_phils_in_paragraph = set()
    used_concs_in_paragraph = set()
    used_trms_in_paragraph = set()

    # Generate a larger pool of sentences to select from
    pool_size = int(num_sentences * 1.8)  # Increased pool size for better selection
    sentence_pool = []
    used_data = []
    
    for _ in range(pool_size):
        sentence_parts, used_phils, used_concs, used_trms = generate_sentence(
            template_type, references, mentioned_philosophers,
            forbidden_philosophers_set | used_phils_in_paragraph,
            forbidden_concepts_set | used_concs_in_paragraph,
            forbidden_terms_set | used_trms_in_paragraph,
            used_quotes, all_references, cited_references,
            note_system=note_system, context=context
        )
        sentence_text, _ = sentence_parts[0]
        sentence_pool.append(sentence_text)
        used_data.append((used_phils, used_concs, used_trms))
        used_phils_in_paragraph.update(used_phils)
        used_concs_in_paragraph.update(used_concs)
        used_trms_in_paragraph.update(used_trms)

    # Find the most common concept or term for thematic focus
    all_concs = [c for _, concs, _ in used_data for c in concs]
    all_trms = [t for _, _, trms in used_data for t in trms]
    concept_counter = Counter(all_concs)
    term_counter = Counter(all_trms)
    
    most_common_concepts = concept_counter.most_common(2)
    most_common_terms = term_counter.most_common(2)
    
    central_themes = []
    if most_common_concepts and most_common_concepts[0][1] > 1:
        central_themes.append(most_common_concepts[0][0])
    if most_common_terms and most_common_terms[0][1] > 1:
        central_themes.append(most_common_terms[0][0])
        
    central_theme = random.choice(central_themes) if central_themes else (
        most_common_concepts[0][0] if most_common_concepts else 
        most_common_terms[0][0] if most_common_terms else 
        random.choice(concepts + terms)
    )

    # Select sentences with the central theme and ensure thematic coherence
    themed_sentences = []
    for i, (_, concs, trms) in enumerate(used_data):
        if central_theme in concs or central_theme in trms:
            themed_sentences.append(i)
    
    other_sentences = [i for i in range(len(sentence_pool)) if i not in themed_sentences]
    
    # Select a mix of themed and other sentences
    num_themed = max(1, min(num_sentences - 1, len(themed_sentences)))
    selected_indices = random.sample(themed_sentences, num_themed) if len(themed_sentences) >= num_themed else themed_sentences[:]
    
    remaining = num_sentences - len(selected_indices)
    if remaining > 0 and other_sentences:
        additional = random.sample(other_sentences, min(remaining, len(other_sentences)))
        selected_indices.extend(additional)
    
    # Ensure we have exactly the requested number of sentences
    while len(selected_indices) < num_sentences and sentence_pool:
        remaining_indices = [i for i in range(len(sentence_pool)) if i not in selected_indices]
        if not remaining_indices:
            break
        selected_indices.append(random.choice(remaining_indices))
    
    # Order the sentences for logical flow
    selected_indices.sort()  # Simple approach: maintain original order
    selected_sentences = [sentence_pool[i] for i in selected_indices]

    # Track concepts and terms used in the final paragraph
    used_concepts_in_paragraph = set()
    used_terms_in_paragraph = set()
    
    for idx in selected_indices:
        _, used_concs, used_trms = used_data[idx]
        used_concepts_in_paragraph.update(used_concs)
        used_terms_in_paragraph.update(used_trms)

    # Construct the paragraph with sophisticated transitions
    paragraph_sentences = []
    
    # Ensure the first sentence is properly capitalized
    if selected_sentences:
        first_sentence = selected_sentences[0]
        first_sentence = ensure_proper_capitalization(first_sentence)
        paragraph_sentences.append(first_sentence)
    
    # Add transitions between sentences
    for i in range(1, len(selected_sentences)):
        # Decide on transition type based on position in paragraph
        if i == 1:  # For the second sentence, often use additive transitions
            transition_pool = [t for t in transitional_expressions if t in 
                              ["moreover", "furthermore", "additionally", "similarly", 
                               "likewise", "in addition", "what is more"]]
        elif i == len(selected_sentences) - 1:  # For the final sentence, use concluding transitions
            transition_pool = [t for t in transitional_expressions if t in 
                              ["therefore", "consequently", "thus", "hence", 
                               "in conclusion", "ultimately", "in sum"]]
        else:  # For middle sentences, use a mix of transitions with emphasis on contrastive
            if random.random() < 0.4:  # 40% chance of contrastive
                transition_pool = [t for t in transitional_expressions if "however" in t 
                                 or "contrast" in t or "yet" in t or "though" in t
                                 or "conversely" in t or "on the other hand" in t]
            else:  # Otherwise use the full pool
                transition_pool = transitional_expressions
        
        if not transition_pool:  # Fallback if our filtered list is empty
            transition_pool = transitional_expressions
            
        transition = random.choice(transition_pool)
        
        # Format the transition properly
        transition = transition.capitalize() + ","
        
        # Format the sentence after transition
        sentence = selected_sentences[i]
        words = sentence.split()
        
        # Don't decapitalize proper nouns or the beginnings of quotes
        if words and words[0].lower() not in terms and words[0].lower() not in concepts and words[0] not in philosophers:
            # Don't lowercase if it's a quoted passage
            if not (words[0].startswith('"') or words[0].startswith("'")):
                sentence = words[0].lower() + ' ' + ' '.join(words[1:]) if len(words) > 1 else words[0].lower()
        
        # Apply capitalization to ensure proper nouns are capitalized, but DON'T capitalize the first letter
        sentence = ensure_proper_capitalization(sentence, capitalize_first=False)
        
        paragraph_sentences.append(f"{transition} {sentence}")

    # Combine sentences into paragraph
    paragraph_str = ' '.join(paragraph_sentences)
    
    # Handle [citation] placeholders with MLA 9 style citations
    if '[citation]' in paragraph_str:
        paragraph_str = _handle_mla_citation(paragraph_str, cited_references, note_system, all_references, context)
    
    # Add meta-references or rhetorical devices based on paragraph type
    if template_type == 'introduction' and random.random() < 0.3:
        # Add a meta-reference about the paper's structure
        meta_sentence = f" {random.choice(meta_references)}, {random.choice(concepts)} offers a productive framework for thinking through {random.choice(terms)}."
        paragraph_str += meta_sentence
    
    elif template_type == 'general' and random.random() < 0.25:
        # Add a rhetorical device
        device = random.choice(rhetorical_devices)
        device_sentence = f" This {device} points to the way in which {random.choice(concepts)} both enables and constrains our understanding of {random.choice(terms)}."
        paragraph_str += device_sentence
    
    elif template_type == 'conclusion' and random.random() < 0.4:
        # Add a reference to discursive mode
        mode = random.choice(discursive_modes)
        mode_sentence = f" The {mode} of this analysis reflects the inherent complexity of the relationship between {random.choice(concepts)} and {random.choice(terms)}."
        paragraph_str += mode_sentence

    # Ensure paragraph ends with proper punctuation
    if not paragraph_str.endswith('.') and not paragraph_str.endswith('?') and not paragraph_str.endswith('!'):
        paragraph_str += '.'
    
    # Final capitalization check for the entire paragraph
    paragraph_str = ensure_proper_capitalization(paragraph_str)

    return paragraph_str, used_concepts_in_paragraph, used_terms_in_paragraph

def _handle_mla_citation(paragraph_str, cited_references, note_system, all_references, context=None):
    """
    Handle [citation] placeholders in paragraph text with MLA 9 style citations.
    
    Args:
        paragraph_str (str): Original paragraph with [citation] placeholders
        cited_references (list): List of already cited references (legacy)
        note_system (NoteSystem): The note system for managing citations and works cited
        all_references (list): List of all available references
        context (dict, optional): Context information about the paragraph
        
    Returns:
        str: The paragraph with proper MLA citations
    """
    # If no [citation] markers, return as is
    if "[citation]" not in paragraph_str:
        return paragraph_str
    
    # Count how many citations we need
    num_citations = paragraph_str.count("[citation]")
    
    # For each [citation] placeholder, replace with MLA style citation
    for _ in range(num_citations):
        if note_system:
            # If we have a note system, use it
            reference = random.choice(all_references)
            
            # Use add_citation instead of add_to_works_cited to create notes
            citation = note_system.add_citation(reference, context)
            
            # Replace with MLA style citation
            paragraph_str = paragraph_str.replace("[citation]", citation, 1)
        else:
            # Legacy handling
            reference = random.choice(all_references)
            if reference not in cited_references:
                cited_references.append(reference)
            
            # Generate a footnote number
            number = cited_references.index(reference) + 1
            footnote = f"[^{number}]"
            paragraph_str = paragraph_str.replace("[citation]", footnote, 1)
    
    return paragraph_str

def _generate_mla_citation(reference, note_system):
    """
    Generate an MLA 9 style citation for a reference.
    
    Args:
        reference (str): The reference string
        note_system (NoteSystem): System for managing citations
        
    Returns:
        tuple: (MLA citation string, page number)
    """
    # Extract author information
    author_match = re.match(r'^([^(]+)', reference)
    if author_match:
        author = author_match.group(1).strip()
        # Get the last name for MLA style
        if ',' in author:
            last_name = author.split(',')[0].strip()
        else:
            name_parts = author.split()
            last_name = name_parts[-1] if name_parts else "Smith"
    else:
        last_name = "Smith"
    
    # Use add_citation to create notes
    citation = note_system.add_citation(reference, None)
    
    # Get the page number from the citation
    page_num = note_system.page_numbers.get(reference, random.randint(1, 300))
    
    return citation, page_num

def generate_section(heading, num_paragraphs, references, note_system=None):
    """
    Generate a complete section with heading and paragraphs.
    
    Args:
        heading (str): The section heading
        num_paragraphs (int): Number of paragraphs to generate
        references (list): References for citations
        note_system (NoteSystem, optional): System for managing citations
        
    Returns:
        list: List of section parts (heading and paragraphs)
    """
    section_parts = [(f"## {heading}\n\n", None)]
    
    # Create context for this section
    section_context = {
        'section': heading.lower(),
        'concepts': set(),
        'terms': set()
    }
    
    # Generate paragraphs for this section
    for i in range(num_paragraphs):
        # Update context with concepts and terms from previous paragraphs
        paragraph_text, paragraph_concepts, paragraph_terms = generate_paragraph(
            "general", random.randint(2, 4), references, 
            note_system=note_system, context=section_context
        )
        
        # Update section context with new concepts and terms
        section_context['concepts'].update(paragraph_concepts)
        section_context['terms'].update(paragraph_terms)
        
        # Add paragraph to section
        section_parts.append((paragraph_text, None))
        section_parts.append(("\n\n", None))
    
    return section_parts