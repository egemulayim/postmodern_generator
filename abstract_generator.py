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

def generate_enhanced_abstract(coherence_manager):
    """
    Generate a comprehensive academic abstract with keywords.
    
    Args:
        coherence_manager: The EssayCoherence instance to use for theme management
    
    Returns:
        str: A formatted abstract section including keywords
    """
    # Get primary themes for consistency
    abstract_concept = coherence_manager.get_weighted_concept()
    abstract_term = coherence_manager.get_weighted_term()
    primary_philosophers = [p for p in coherence_manager.primary_philosophers if p]
    if not primary_philosophers:  # Fallback if empty
        primary_philosophers = random.sample(philosophers, 2)
    
    # Theoretical framing paragraph
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
    
    # Collect potential keywords (prefer primary concepts and terms, then used ones, then random)
    potential_keywords = []
    potential_keywords.extend(coherence_manager.primary_concepts)
    potential_keywords.extend(coherence_manager.primary_terms)
    potential_keywords.extend([abstract_concept, abstract_term])
    
    # Ensure we have enough keywords
    while len(potential_keywords) < 7:  # Get more than we need for variety
        random_term = random.choice(concepts + terms)
        if random_term not in potential_keywords:
            potential_keywords.append(random_term)
    
    # Shuffle and select 5 unique keywords
    random.shuffle(potential_keywords)
    selected_keywords = []
    for keyword in potential_keywords:
        if keyword not in selected_keywords and len(selected_keywords) < 5:
            selected_keywords.append(keyword)
    
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