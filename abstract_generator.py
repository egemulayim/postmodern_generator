"""
A module for generating sophisticated academic abstracts with keywords.
This module creates an abstract for the generated essay,
including a theoretical framing, methodology, and significance details.
It also generates a list of keywords relevant to the essay's themes.
The abstract is designed to be coherent and thematically consistent,
while also incorporating a metafictional element.
"""

import random
import metafiction
from data import philosophers, concepts, terms, contexts, philosopher_concepts

def find_relevant_philosophers(concepts, terms, philosopher_concepts):
    """
    Find philosophers most associated with given concepts and terms.
    
    Args:
        concepts (list): List of concepts to match
        terms (list): List of terms to match
        philosopher_concepts (dict): Dictionary mapping philosophers to their concepts
        
    Returns:
        list: Philosophers most relevant to the given concepts and terms
    """
    relevant_philosophers = []
    
    # Find philosophers associated with concepts
    for concept in concepts:
        for philosopher, philo_concepts in philosopher_concepts.items():
            if concept in philo_concepts:
                relevant_philosophers.append(philosopher)
    
    # If we found relevant philosophers, return them, otherwise return empty list
    if relevant_philosophers:
        return list(set(relevant_philosophers))  # Deduplicate
    else:
        return []

def generate_enhanced_abstract(coherence_manager, title_themes=None):
    """
    Generate a comprehensive academic abstract with keywords.
    
    Args:
        coherence_manager: The EssayCoherence instance to use for theme management
        title_themes (dict, optional): Dictionary of themes from the title
        
    Returns:
        str: A formatted abstract section including keywords
    """
    # Use title themes for consistency if provided
    if title_themes and title_themes['primary_concepts']:
        abstract_concept = title_themes['primary_concepts'][0]
    else:
        abstract_concept = coherence_manager.get_weighted_concept()
        
    if title_themes and title_themes['primary_terms']:
        abstract_term = title_themes['primary_terms'][0]
    else:
        abstract_term = coherence_manager.get_weighted_term()
    
    # Get primary philosophers for consistency
    primary_philosophers = [p for p in coherence_manager.primary_philosophers if p]
    if not primary_philosophers:  # Fallback if empty
        primary_philosophers = random.sample(philosophers, 2)
    
    # Find philosophers most associated with title themes
    if title_themes:
        relevant_philosophers = find_relevant_philosophers(
            title_themes['primary_concepts'] + title_themes['related_concepts'],
            title_themes['primary_terms'],
            philosopher_concepts
        )
        
        # If we found relevant philosophers, prioritize them
        if relevant_philosophers:
            primary_philosophers = relevant_philosophers[:2] if len(relevant_philosophers) >= 2 else relevant_philosophers
    
    # Theoretical framing paragraph explicitly mentioning title themes
    theoretical_framing = (
        f"This paper explores the relationship between {abstract_concept} and {abstract_term}, "
        f"arguing that their dialectical interplay reveals deeper structures of meaning. "
        f"Drawing on theoretical frameworks from {', '.join(primary_philosophers[:2])}, "
        f"I demonstrate how {abstract_concept} functions both as a condition of possibility for {abstract_term} "
        f"and as its limit. "
    )
    
    # Methodology paragraph
    methodologies = ["discourse analysis", "deconstructive reading", "close textual analysis", 
                     "genealogical investigation", "dialectical critique", "rhizomatic mapping"]
    methodology = (
        f"Through a methodology combining {random.choice(methodologies)} and {random.choice(methodologies)}, "
        f"this study examines how {abstract_concept} operates within contemporary theoretical discourse "
        f"on {abstract_term}. "
        f"Particular attention is paid to the ways in which {random.choice(coherence_manager.primary_concepts) if coherence_manager.primary_concepts else random.choice(concepts)} "
        f"mediates between {abstract_concept} and {abstract_term} "
        f"{random.choice(contexts)}. "
    )
    
    # Significance paragraph
    significance = (
        f"The significance of this investigation lies in its reconfiguration of conventional approaches to "
        f"{abstract_term}, offering new possibilities for thinking through {abstract_concept} "
        f"beyond the constraints of {random.choice(coherence_manager.primary_terms) if coherence_manager.primary_terms else random.choice(terms)}. "
        f"{metafiction.generate_metafictional_element()}"
    )
    
    # Enhanced keyword selection with contextual relevance
    # Create a dictionary to count occurrences of concepts and terms in the abstract
    keyword_occurrences = {}
    
    # Count occurrences of concepts in the abstract text
    abstract_text = theoretical_framing + methodology + significance
    for concept in concepts:
        occurrences = abstract_text.lower().count(concept.lower())
        if occurrences > 0:
            keyword_occurrences[concept] = occurrences
    
    # Count occurrences of terms in the abstract text
    for term in terms:
        occurrences = abstract_text.lower().count(term.lower())
        if occurrences > 0:
            keyword_occurrences[term] = occurrences
    
    # Ensure primary concepts and terms are included
    for concept in coherence_manager.primary_concepts:
        if concept not in keyword_occurrences:
            keyword_occurrences[concept] = 1
    
    for term in coherence_manager.primary_terms:
        if term not in keyword_occurrences:
            keyword_occurrences[term] = 1
    
    # Add the main abstract concept and term with high weight
    keyword_occurrences[abstract_concept] = keyword_occurrences.get(abstract_concept, 0) + 3
    keyword_occurrences[abstract_term] = keyword_occurrences.get(abstract_term, 0) + 3
    
    # Prioritize title themes if provided
    if title_themes:
        for concept in title_themes['primary_concepts']:
            if concept in keyword_occurrences:
                keyword_occurrences[concept] += 2
            else:
                keyword_occurrences[concept] = 2
                
        for term in title_themes['primary_terms']:
            if term in keyword_occurrences:
                keyword_occurrences[term] += 2
            else:
                keyword_occurrences[term] = 2
                
        for concept in title_themes.get('related_concepts', []):
            if concept in keyword_occurrences:
                keyword_occurrences[concept] += 1
            else:
                keyword_occurrences[concept] = 1
    
    # Sort keywords by occurrence count (higher is more relevant)
    sorted_keywords = sorted(keyword_occurrences.items(), key=lambda x: x[1], reverse=True)
    
    # Take top 5 keywords
    selected_keywords = [keyword for keyword, _ in sorted_keywords[:5]]
    
    # Ensure we have at least 5 keywords (add random ones if needed)
    if len(selected_keywords) < 5:
        available_keywords = [k for k in concepts + terms if k not in selected_keywords]
        additional_keywords = random.sample(available_keywords, min(5 - len(selected_keywords), len(available_keywords)))
        selected_keywords.extend(additional_keywords)
    
    # Format keywords section
    keywords_section = "**Keywords:** " + ", ".join(selected_keywords)
    
    # Build the complete abstract
    abstract_text = f"## Abstract\n\n{theoretical_framing}{methodology}{significance}\n\n{keywords_section}\n\n"
    
    # Record usage of concepts and terms in the abstract
    coherence_manager.record_usage(
        concepts=[abstract_concept] + [k for k in selected_keywords if k in concepts],
        terms=[abstract_term] + [k for k in selected_keywords if k in terms],
        philosophers=primary_philosophers
    )
    
    return abstract_text