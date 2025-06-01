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
from json_data_provider import philosophers, concepts, terms, philosopher_concepts, rhetorical_devices, discursive_modes
from capitalization import ensure_proper_capitalization
from sentence import ensure_quote_has_citation

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

def generate_paragraph(template_type, num_sentences, forbidden_philosophers=[], 
                      forbidden_concepts=[], forbidden_terms=[], mentioned_philosophers=set(), 
                      used_quotes=set(), cited_references=None, note_system=None, context=None, coherence_manager=None):
    """
    Generate a paragraph by selecting sentences from a pool, ensuring a central theme for coherence.
    Uses MLA 9 citation style for all citations.
    Utilizes CoherenceManager for thematic consistency if provided.

    Args:
        template_type (str): Type of paragraph ('introduction', 'general', or 'conclusion')
        num_sentences (int): Number of sentences desired in the paragraph
        forbidden_philosophers (list): Philosophers to exclude from generation
        forbidden_concepts (list): Concepts to exclude from generation
        forbidden_terms (list): Terms to exclude from generation
        mentioned_philosophers (set): Set of philosophers already mentioned in the text
        used_quotes (set): Quotes already used in the essay
        cited_references (list): References cited so far in the essay (legacy, use note_system instead)
        note_system (NoteSystem): The note system for managing citations and notes
        context (dict): Contextual information about the paragraph being generated
        coherence_manager (EssayCoherence, optional): The coherence manager for thematic guidance.

    Returns:
        tuple: (paragraph_str, used_concepts_in_paragraph, used_terms_in_paragraph)
    """
    forbidden_philosophers_set = set(forbidden_philosophers)
    forbidden_concepts_set = set(forbidden_concepts)
    forbidden_terms_set = set(forbidden_terms)

    # Initialize sets to track what's actually used in the final selected sentences for this paragraph
    final_used_philosophers = set()
    final_used_concepts = set()
    final_used_terms = set()

    # Determine primary thematic elements for this paragraph
    # Priority: context -> coherence_manager active theme -> coherence_manager weighted choices -> random
    paragraph_theme_concept = None
    paragraph_theme_philosopher = None
    paragraph_theme_term = None

    if context:
        paragraph_theme_concept = context.get('theme_concept')
        paragraph_theme_philosopher = context.get('theme_philosopher')
        # If context has primary concepts/terms from title themes, consider them
        if context.get('title_themes'):
            title_primary_concepts = context['title_themes'].get('primary_concepts', [])
            if title_primary_concepts and not paragraph_theme_concept:
                paragraph_theme_concept = random.choice(title_primary_concepts)
            title_primary_terms = context['title_themes'].get('primary_terms', [])
            if title_primary_terms:
                paragraph_theme_term = random.choice(title_primary_terms)


    if coherence_manager:
        if not paragraph_theme_concept:
            paragraph_theme_concept = coherence_manager.get_weighted_concept(exclude=forbidden_concepts_set)
        if not paragraph_theme_philosopher:
            # Try to get a philosopher related to the paragraph_theme_concept or active theme
            if paragraph_theme_concept and paragraph_theme_concept in coherence_manager.philosopher_concepts:
                 candidates = [p for p, c_list in coherence_manager.philosopher_concepts.items() if paragraph_theme_concept in c_list and p not in forbidden_philosophers_set]
                 if candidates: paragraph_theme_philosopher = random.choice(candidates)
            if not paragraph_theme_philosopher: # Fallback to weighted philosopher
                 paragraph_theme_philosopher = coherence_manager.get_weighted_philosopher(exclude=forbidden_philosophers_set)
        if not paragraph_theme_term:
            paragraph_theme_term = coherence_manager.get_weighted_term(exclude=forbidden_terms_set.union({paragraph_theme_concept} if paragraph_theme_concept else set()))
        
        # Record initial thematic elements as used by coherence_manager for weighting
        coherence_manager.record_usage(
            concepts=[paragraph_theme_concept] if paragraph_theme_concept else [],
            terms=[paragraph_theme_term] if paragraph_theme_term else [],
            philosophers=[paragraph_theme_philosopher] if paragraph_theme_philosopher else []
        )
    else: # Fallback if no coherence_manager
        if not paragraph_theme_concept: paragraph_theme_concept = random.choice([c for c in concepts if c not in forbidden_concepts_set] or concepts)
        if not paragraph_theme_philosopher: paragraph_theme_philosopher = random.choice([p for p in philosophers if p not in forbidden_philosophers_set] or philosophers)
        if not paragraph_theme_term: paragraph_theme_term = random.choice([t for t in terms if t not in forbidden_terms_set] or terms)

    # Generate a pool of sentences, now guided by coherence_manager if available
    pool_size = int(num_sentences * 2.0) # Slightly larger pool
    sentence_pool_data = [] # Will store (sentence_text, used_phils, used_concs, used_trms)

    # Create a focused context for sentence generation
    sentence_generation_context = context.copy() if context else {}
    sentence_generation_context['primary_concept'] = paragraph_theme_concept
    sentence_generation_context['primary_philosopher'] = paragraph_theme_philosopher
    sentence_generation_context['primary_term'] = paragraph_theme_term
    
    # Track elements used *during the generation of the sentence pool* to avoid too much repetition within the pool itself
    temp_used_phils_in_pool = set()
    temp_used_concs_in_pool = set()
    temp_used_trms_in_pool = set()

    for _ in range(pool_size):
        # Pass coherence_manager to generate_sentence
        sentence_parts, used_phils, used_concs, used_trms = generate_sentence(
            template_type, 
            set(mentioned_philosophers).union(final_used_philosophers), # Pass already mentioned ones
            forbidden_philosophers_set.union(temp_used_phils_in_pool),
            forbidden_concepts_set.union(temp_used_concs_in_pool).union({paragraph_theme_term} if paragraph_theme_term else set()), # Avoid term as concept here
            forbidden_terms_set.union(temp_used_trms_in_pool).union({paragraph_theme_concept} if paragraph_theme_concept else set()), # Avoid concept as term
            used_quotes, 
            note_system=note_system, 
            context=sentence_generation_context, # Pass focused context
            coherence_manager=coherence_manager # Pass coherence_manager
        )
        sentence_text, _ = sentence_parts[0] # Assuming first part is the main sentence text
        sentence_pool_data.append({'text': sentence_text, 'philosophers': used_phils, 'concepts': used_concs, 'terms': used_trms})
        
        # Add to temporary pool usage sets to encourage variety in the pool
        if random.random() < 0.5: # Probabilistically add to temp pool to avoid over-restriction
            temp_used_phils_in_pool.update(used_phils)
            temp_used_concs_in_pool.update(used_concs)
            temp_used_trms_in_pool.update(used_trms)

    if not sentence_pool_data: # Fallback if pool is empty
        # Try one more time with less restrictions for sentence generation if pool is empty
        for _ in range(num_sentences): # Generate just enough
            sentence_parts, used_phils, used_concs, used_trms = generate_sentence(
                template_type, 
                set(mentioned_philosophers).union(final_used_philosophers),
                forbidden_philosophers_set, forbidden_concepts_set, forbidden_terms_set, # Less restrictive
                used_quotes, 
                note_system=note_system, context=sentence_generation_context, coherence_manager=coherence_manager
            )
            sentence_text, _ = sentence_parts[0]
            sentence_pool_data.append({'text': sentence_text, 'philosophers': used_phils, 'concepts': used_concs, 'terms': used_trms})
            if not sentence_pool_data: # Should not happen, but as a guard
                 return "Error: Could not generate sentences for paragraph.", set(), set()


    # Select sentences for the paragraph, prioritizing thematic relevance
    # and ensuring variety and coherence.
    selected_sentences_data = []
    
    # Score sentences based on relevance to paragraph_theme_concept, _philosopher, _term
    # and general coherence (e.g., avoiding too much repetition of specific low-weight philosophers/concepts)
    
    def score_sentence(sentence_data):
        score = 0
        if paragraph_theme_concept and paragraph_theme_concept in sentence_data['concepts']:
            score += 5
        if paragraph_theme_term and paragraph_theme_term in sentence_data['terms']:
            score += 4 # Term slightly less weight than main concept
        if paragraph_theme_philosopher and paragraph_theme_philosopher in sentence_data['philosophers']:
            score += 3
        # Penalize if it uses elements already heavily used in *this paragraph*
        if any(p in final_used_philosophers for p in sentence_data['philosophers']): score -= 1
        if any(c in final_used_concepts for c in sentence_data['concepts']): score -=1
        # Add small bonus for new concepts/terms to encourage breadth if needed
        if not any(c in final_used_concepts for c in sentence_data['concepts']) and sentence_data['concepts']: score += 0.5
        return score

    # Iteratively build the paragraph
    available_pool = list(sentence_pool_data)
    random.shuffle(available_pool) # Shuffle to break ties in scores somewhat

    for _ in range(num_sentences):
        if not available_pool:
            break # No more sentences to choose from
        
        available_pool.sort(key=score_sentence, reverse=True)
        
        chosen_sentence_data = available_pool.pop(0) # Take the best scored one
        selected_sentences_data.append(chosen_sentence_data)
        
        # Update what's been used in *this paragraph's final selection*
        final_used_philosophers.update(chosen_sentence_data['philosophers'])
        final_used_concepts.update(chosen_sentence_data['concepts'])
        final_used_terms.update(chosen_sentence_data['terms'])

    # Fallback: if not enough sentences selected, fill with remaining from pool (less ideal)
    while len(selected_sentences_data) < num_sentences and available_pool:
        selected_sentences_data.append(available_pool.pop(0))

    selected_sentences_texts = [s_data['text'] for s_data in selected_sentences_data]

    # Construct the paragraph with sophisticated transitions
    paragraph_sentences = []
    
    # Ensure the first sentence is properly capitalized
    if selected_sentences_texts:
        first_sentence = selected_sentences_texts[0]
        first_sentence = ensure_proper_capitalization(first_sentence)
        paragraph_sentences.append(first_sentence)
    
    # Add transitions between sentences
    for i in range(1, len(selected_sentences_texts)):
        # Decide on transition type based on position in paragraph
        if i == 1:  # For the second sentence, often use additive transitions
            transition_pool = [t for t in transitional_expressions if t in 
                              ["moreover", "furthermore", "additionally", "similarly", 
                               "likewise", "in addition", "what is more"]]
        elif i == len(selected_sentences_texts) - 1:  # For the final sentence, use concluding transitions
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
        sentence = selected_sentences_texts[i]
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
        # Pass coherence_manager to _handle_mla_citation if it needs thematic guidance for choosing which work to cite
        paragraph_str = _handle_mla_citation(paragraph_str, cited_references, note_system, context, coherence_manager=coherence_manager)
    
    # Add meta-references or rhetorical devices based on paragraph type
    if template_type == 'introduction' and random.random() < 0.3:
        # Add a meta-reference about the paper's structure
        meta_sentence = f" {random.choice(meta_references)}, {random.choice(concepts)} offers a productive framework for thinking through {random.choice(terms)}."
        paragraph_str += meta_sentence
    
    elif template_type == 'general' and random.random() < 0.25:
        # Add a rhetorical device
        if rhetorical_devices: # Safety check
            device = random.choice(rhetorical_devices)
            device_sentence = f" This {device} points to the way in which {random.choice(concepts)} both enables and constrains our understanding of {random.choice(terms)}."
            paragraph_str += device_sentence
        else:
            # Optional: log a warning or use a fallback if rhetorical_devices is empty
            pass # Or add a default sentence
    
    elif template_type == 'conclusion' and random.random() < 0.4:
        # Add a reference to discursive mode
        if discursive_modes: # Safety check
            mode = random.choice(discursive_modes)
            # Refined sentence template for discursive modes
            mode_sentence = f" Ultimately, the {mode} adopted in this essay highlights the inherent complexity of the relationship between {random.choice(concepts)} and {random.choice(terms)}."
            paragraph_str += mode_sentence
        else:
            # Optional: log a warning or use a fallback if discursive_modes is empty
            pass # Or add a default sentence

    # Ensure paragraph ends with proper punctuation
    if not paragraph_str.endswith('.') and not paragraph_str.endswith('?') and not paragraph_str.endswith('!'):
        paragraph_str += '.'
    
    # Final capitalization check for the entire paragraph
    paragraph_str = ensure_proper_capitalization(paragraph_str)

    # Final check for quotes without citations
    paragraph_str = ensure_quote_has_citation(paragraph_str)

    # The returned concepts/terms should be what's *actually* in the final paragraph
    return paragraph_str, final_used_concepts, final_used_terms

def _handle_mla_citation(paragraph_str, cited_references, note_system, context=None, coherence_manager=None):
    """
    Helper function to handle MLA citations within a paragraph string.
    Uses NoteSystem for creating and managing citations.
    If coherence_manager is provided, it can guide philosopher/work selection for citation.

    Args:
        paragraph_str (str): Original paragraph with [citation] placeholders
        cited_references (list): List of already cited references (legacy)
        note_system (NoteSystem): The note system for managing citations and works cited
        context (dict, optional): Context information about the paragraph
        coherence_manager (EssayCoherence, optional): The coherence manager for thematic guidance

    Returns:
        str: The paragraph with proper MLA citations
    """
    # If no [citation] markers, return as is
    if "[citation]" not in paragraph_str:
        return paragraph_str
    
    # Count how many citations we need
    num_citations = paragraph_str.count("[citation]")
    
    # Attempt to get a thematically relevant philosopher if context or coherence_manager is available
    cite_philosopher_name = None
    work_to_cite = None

    if coherence_manager:
        # Prioritize philosophers related to active theme or paragraph context
        if context and context.get('theme_philosopher'):
            cite_philosopher_name = context.get('theme_philosopher')
        elif coherence_manager.active_theme_key and coherence_manager.active_theme_data.get('core_philosophers'):
            # Choose from core philosophers of the theme, not yet cited too much in this note
            # This requires note_system to track philosopher citation frequency per note, or a simpler approach:
            active_theme_philosophers = coherence_manager.active_theme_data.get('core_philosophers', [])
            potential_cite_philosophers = [p for p in active_theme_philosophers if p not in (note_system.get_authors_in_current_note() if note_system else [])]
            if potential_cite_philosophers:
                cite_philosopher_name = random.choice(potential_cite_philosophers)
            elif active_theme_philosophers: # Fallback if all theme philosophers somehow in current note
                cite_philosopher_name = random.choice(active_theme_philosophers)
        
        if not cite_philosopher_name: # Fallback to a generally weighted philosopher
            cite_philosopher_name = coherence_manager.get_weighted_philosopher(exclude=(note_system.get_authors_in_current_note() if note_system else []))

        # Try to get a key work for this philosopher
        if cite_philosopher_name and cite_philosopher_name in coherence_manager.philosopher_key_works and coherence_manager.philosopher_key_works[cite_philosopher_name]:
             # Prefer a work not yet cited, or less cited overall
             key_works = coherence_manager.philosopher_key_works[cite_philosopher_name]
             # This needs more sophisticated tracking of which works are cited. For now, random:
             work_title, year = random.choice(key_works)
             # Construct a simplified reference dict for add_note; NoteSystem should ideally handle full ref resolution
             # Type is often 'book' in philosopher_key_works, but could be 'article'. Let's assume default book if not specified.
             # We'd need philosopher_key_works to store type for this to be accurate.
             # For now, let's default to 'book' for key works if not specified, or try to infer.
             # This part needs key_works to provide type. Assuming it's a tuple (title, year) for now.
             work_to_cite = {'author': cite_philosopher_name, 'title': work_title, 'year': year, 'type': 'book'} # Defaulting to book for key works

    if not work_to_cite: # Fallback if thematic selection failed or no coherence_manager
        if cited_references: # Use the old way if new way fails
            random_ref = random.choice(cited_references)
            work_to_cite = random_ref # random_ref is already a dict
            cite_philosopher_name = random_ref.get('author', 'Unknown Author') # Ensure we have an author
        else: # Absolute fallback
            cite_philosopher_name = random.choice(philosophers) if philosophers else "An Anonymous Scholar"
            is_article_type = random.choice([True, False])
            work_to_cite = {
                'author': cite_philosopher_name,
                'title': None,  # Force NoteSystem to generate a title
                'year': random.randint(1980, 2023),
                'type': 'article' if is_article_type else 'book'
                # Journal will be handled by get_enhanced_citation if type is article and journal is None from add_note
            }


    if note_system and work_to_cite:
        # Ensure page numbers are plausible
        # page_number = random.randint(1, 300) if work_to_cite.get('type') != 'online' else None
        # The page number for the in-text citation mark will be handled by add_citation's internals.

        author = work_to_cite.get('author', 'Unknown Author')
        title_override = work_to_cite.get('title') # This can be None if we want NoteSystem to generate it
        year = work_to_cite.get('year', random.randint(1980, 2023)) # Fallback year
        work_type = work_to_cite.get('type', 'book') # Default to book if not specified
        is_article_type = (work_type == 'article')

        # publisher, journal, volume, issue, url, doi are not directly used by get_enhanced_citation's primary path
        # get_enhanced_citation will generate these for articles or use publisher for books from data.py

        full_reference_string = note_system.get_enhanced_citation(
            author_name=author,
            is_article=is_article_type,
            year=year,
            title_override=title_override
            # specific_year_override and is_article_override are not needed here as year and is_article cover it
        )
        
        # Construct a context for the note, if needed by _generate_substantive_note via add_citation
        note_context = {
            'theme_concept': context.get('theme_concept') if context else None,
            'current_concepts_in_paragraph': work_to_cite.get('concepts', []), # Assuming work_to_cite might have concepts
            'current_terms_in_paragraph': work_to_cite.get('terms', []) # Assuming work_to_cite might have terms
        }
        # A more generic context phrase if specific concepts/terms aren't available for work_to_cite
        if not note_context['current_concepts_in_paragraph'] and not note_context['current_terms_in_paragraph']:
             note_context['context_phrase'] = f"This citation relates to {context.get('theme_concept', 'the ongoing discussion') if context else 'the ongoing discussion'}."
        else:
             items = note_context['current_concepts_in_paragraph'] + note_context['current_terms_in_paragraph']
             note_context['context_phrase'] = f"This citation, referencing '{title_override or 'this work'}', is relevant to {', '.join(items)}."


        # Call add_citation, which handles creating the note entry and returning the in-text marker.
        # The context for the note (used by _generate_substantive_note) is passed here.
        citation_mark = note_system.add_citation(
            reference=full_reference_string,
            context=note_context # Pass the constructed context dictionary
        )
        
        # Replace the first occurrence of [citation]
        paragraph_str = paragraph_str.replace('[citation]', citation_mark, 1)
    else: # Fallback if no note_system or work_to_cite somehow becomes None
        paragraph_str = paragraph_str.replace('[citation]', f"({cite_philosopher_name or 'Author'}, {random.randint(1980, 2023)})", 1)
    
    return paragraph_str

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
            "general", random.randint(2, 4), 
            note_system=note_system, context=section_context
        )
        
        # Update section context with new concepts and terms
        section_context['concepts'].update(paragraph_concepts)
        section_context['terms'].update(paragraph_terms)
        
        # Add paragraph to section
        section_parts.append((paragraph_text, None))
        section_parts.append(("\n\n", None))
    
    return section_parts