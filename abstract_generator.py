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
from json_data_provider import philosophers, concepts, terms, contexts, philosopher_concepts, thematic_clusters
from coherence import EssayCoherence
from collections import Counter

def find_relevant_philosophers(current_concepts, current_terms, coherence_manager_instance: EssayCoherence):
    """
    Find philosophers most associated with given concepts and terms, 
    leveraging the coherence manager for thematic relevance.
    
    Args:
        current_concepts (list): List of concepts to match
        current_terms (list): List of terms to match
        coherence_manager_instance (EssayCoherence): The coherence manager instance.
        
    Returns:
        list: Philosophers most relevant to the given concepts and terms (max 3)
    """
    relevant_philosophers = set()

    # Prioritize philosophers from the active theme if one is set
    if coherence_manager_instance.active_theme_key:
        relevant_philosophers.update(coherence_manager_instance.active_theme_data.get('core_philosophers', []))

    # Add philosophers strongly associated with the current concepts/terms via philosopher_concepts
    for concept_item in current_concepts + current_terms: # Terms can sometimes map to philosopher specialties
        for philosopher, philo_concepts_list in philosopher_concepts.items():
            if concept_item in philo_concepts_list:
                relevant_philosophers.add(philosopher)
    
    # If still not enough, get weighted philosophers from coherence manager
    attempts = 0
    while len(relevant_philosophers) < 2 and attempts < 5:
        weighted_phil = coherence_manager_instance.get_weighted_philosopher(exclude=relevant_philosophers)
        if weighted_phil:
            relevant_philosophers.add(weighted_phil)
        attempts += 1
        
    # Fallback: if still empty, get some from primary list or random from all philosophers
    if not relevant_philosophers:
        if coherence_manager_instance.primary_philosophers:
             relevant_philosophers.update(random.sample(coherence_manager_instance.primary_philosophers, min(2, len(coherence_manager_instance.primary_philosophers))))
        else:
             relevant_philosophers.update(random.sample(philosophers, min(2, len(philosophers))))

    return list(relevant_philosophers)[:3] # Return up to 3

def generate_enhanced_abstract(coherence_manager: EssayCoherence, title_themes=None, essay_theme_key=None):
    """
    Generate a comprehensive academic abstract with keywords, potentially guided by an essay theme.
    
    Args:
        coherence_manager (EssayCoherence): The EssayCoherence instance to use.
        title_themes (dict, optional): Dictionary of themes from the title.
        essay_theme_key (str, optional): The key for the overall essay theme from thematic_clusters.
        
    Returns:
        str: A formatted abstract section including keywords
    """
    # If an essay_theme_key is provided and coherence_manager doesn't match, re-initialize/set it.
    # This assumes coherence_manager might be a global or pre-configured instance.
    # If it's instantiated per call, it should be `EssayCoherence(theme_key=essay_theme_key)`.
    if essay_theme_key and coherence_manager.active_theme_key != essay_theme_key:
        coherence_manager.set_active_theme(essay_theme_key)
    elif not coherence_manager.active_theme_key and not essay_theme_key and title_themes: # If no theme but title themes exist
        # Attempt to infer a theme from title_themes if no explicit theme is set
        # This is a simplified inference; could be made more robust
        best_match_score = 0
        inferred_theme_key = None
        title_all_concepts = set(title_themes.get('primary_concepts', []) + title_themes.get('related_concepts', []))
        for th_key, th_data in thematic_clusters.items():
            match_score = len(title_all_concepts.intersection(set(th_data.get('key_concepts',[]))))
            if match_score > best_match_score:
                best_match_score = match_score
                inferred_theme_key = th_key
        if inferred_theme_key:
            coherence_manager.set_active_theme(inferred_theme_key)
            essay_theme_key = inferred_theme_key # Update for consistency

    # Use title themes for consistency if provided, otherwise draw from coherence_manager
    if title_themes and title_themes.get('primary_concepts'):
        abstract_concept = random.choice(title_themes['primary_concepts'])
    else:
        abstract_concept = coherence_manager.get_weighted_concept()
        
    if title_themes and title_themes.get('primary_terms'):
        abstract_term = random.choice(title_themes['primary_terms'])
    else:
        abstract_term = coherence_manager.get_weighted_term()

    # Get primary philosophers for the abstract, guided by coherence_manager
    current_abstract_elements = [abstract_concept, abstract_term]
    # Add some more elements from coherence manager for broader philosopher search
    current_abstract_elements.append(coherence_manager.get_weighted_concept(exclude=set(current_abstract_elements)))
    current_abstract_elements.append(coherence_manager.get_weighted_term(exclude=set(current_abstract_elements)))
    
    # Use the updated find_relevant_philosophers
    abstract_philosophers = find_relevant_philosophers(current_abstract_elements, [], coherence_manager)
    if not abstract_philosophers: # Fallback
        abstract_philosophers = random.sample(philosophers, 2)
    
    # Theoretical framing paragraph
    theme_description_intro = ""
    if coherence_manager.active_theme_key and coherence_manager.active_theme_data.get('description'):
        # Use a part of the theme description for framing
        desc_sentences = coherence_manager.active_theme_data['description'].split('. ')
        if desc_sentences:
            theme_description_intro = desc_sentences[0] + ". " 

    philo_mention = ", ".join(abstract_philosophers[:2])
    if len(abstract_philosophers) > 0:
         philo_mention = coherence_manager.get_philosopher_key_work_citation(abstract_philosophers[0])
         if len(abstract_philosophers) > 1:
             philo_mention += f" and {coherence_manager.get_philosopher_key_work_citation(abstract_philosophers[1])}"
    else: # Fallback if no philosophers were found, which shouldn't happen with fallbacks in find_relevant_philosophers
        philo_mention = f"{coherence_manager.get_weighted_philosopher()} and {coherence_manager.get_weighted_philosopher(exclude=set(abstract_philosophers))}"


    theoretical_framing = (
        f"{theme_description_intro}This paper explores the intricate relationship between {abstract_concept} and {abstract_term}, "
        f"arguing that their dialectical interplay reveals deeper structures of contemporary concern. "
        f"Drawing on theoretical frameworks from {philo_mention}, "
        f"it demonstrates how {abstract_concept} functions both as a condition of possibility for, and as a critical limit to, understanding {abstract_term}. "
    )
    
    # Methodology paragraph
    methodologies = ["discourse analysis", "deconstructive reading", "close textual analysis", 
                     "genealogical investigation", "dialectical critique", "rhizomatic mapping", 
                     "affective inquiry", "new materialist analysis", "postcolonial critique"]
    chosen_methodology1 = random.choice(methodologies)
    chosen_methodology2 = random.choice([m for m in methodologies if m != chosen_methodology1])
    
    theme_context_phrase = coherence_manager.get_theme_context_phrase() if coherence_manager.active_theme_key else random.choice(contexts)
    if not theme_context_phrase: theme_context_phrase = random.choice(contexts) # Ensure fallback

    methodology_concept_focus = coherence_manager.get_weighted_concept(exclude={abstract_concept, abstract_term})

    methodology = (
        f"Through a methodology combining {chosen_methodology1} with {chosen_methodology2}, "
        f"this study examines how {abstract_concept} operates within contemporary theoretical discourse, particularly concerning {abstract_term}. "
        f"Particular attention is paid to the ways in which {methodology_concept_focus} "
        f"mediates this relationship {theme_context_phrase}. "
    )
    
    # Significance paragraph
    metafictional_sig = metafiction.generate_metafictional_element(theme_key=essay_theme_key, coherence_manager=coherence_manager)
    significance_term_focus = coherence_manager.get_weighted_term(exclude={abstract_term})

    significance = (
        f"The significance of this investigation lies in its potential to reconfigure conventional approaches to "
        f"{abstract_term}, offering new avenues for thinking through {abstract_concept} "
        f"beyond the constraints of {significance_term_focus}. "
        f"{metafictional_sig}"
    )
    
    # Enhanced keyword selection
    keyword_candidates = set(coherence_manager.primary_concepts + coherence_manager.primary_terms)
    keyword_candidates.add(abstract_concept)
    keyword_candidates.add(abstract_term)
    keyword_candidates.add(methodology_concept_focus)
    keyword_candidates.add(significance_term_focus)

    if coherence_manager.active_theme_key:
        keyword_candidates.update(coherence_manager.active_theme_data.get('key_concepts', []))
        keyword_candidates.update(coherence_manager.active_theme_data.get('relevant_terms', []))

    # Add philosophers' names as keywords too
    keyword_candidates.update(abstract_philosophers)
    
    # Ensure all are strings and filter out None or empty strings
    keyword_candidates = {str(k) for k in keyword_candidates if k}

    # Weight keywords: title themes and active theme elements get higher preference
    weighted_keywords = Counter()
    for kw in keyword_candidates:
        weight = 1
        if title_themes and (kw in title_themes.get('primary_concepts', []) or kw in title_themes.get('primary_terms', [])):
            weight += 5
        if coherence_manager.active_theme_key and \
           (kw in coherence_manager.active_theme_data.get('key_concepts', []) or \
            kw in coherence_manager.active_theme_data.get('relevant_terms', []) or \
            kw in coherence_manager.active_theme_data.get('core_philosophers', [])):
            weight += 3
        if kw in coherence_manager.concept_weights or kw in coherence_manager.term_weights or kw in coherence_manager.philosopher_weights:
             weight += coherence_manager.concept_weights.get(kw,0) + coherence_manager.term_weights.get(kw,0) + coherence_manager.philosopher_weights.get(kw,0)
        weighted_keywords[kw] = weight
    
    # Select top 5 keywords
    num_keywords = 5
    selected_keywords = [kw for kw, count in weighted_keywords.most_common(num_keywords)]
    
    # Ensure we have exactly 5 keywords if possible, otherwise pad with random keywords
    if len(selected_keywords) < num_keywords:
        additional_needed = num_keywords - len(selected_keywords)
        # Fallback: add from concepts, terms, or philosophers not already selected
        fallback_pool = list((set(concepts) | set(terms) | set(philosophers)) - set(selected_keywords))
        if fallback_pool:
             selected_keywords.extend(random.sample(fallback_pool, min(additional_needed, len(fallback_pool))))
    
    # If still not 5 keywords, pad with random keywords from the general pool (even if repeated, though unlikely with sufficient candidates)
    # This step is crucial to guarantee exactly 5 keywords.
    while len(selected_keywords) < num_keywords:
        # Create a combined pool that allows duplicates if necessary to reach 5
        # This is a last resort and ideally, the previous steps should yield enough unique keywords.
        combined_pool = list(concepts) + list(terms) + list(philosophers)
        if not combined_pool: # Should not happen if data.json is populated
            selected_keywords.append("keyword") # Absolute fallback
            continue
        
        # Try to pick a keyword not already selected if possible
        potential_keyword = random.choice(combined_pool)
        # Add if not already present or if we absolutely need to fill spots (allow duplicates as last resort)
        if potential_keyword not in selected_keywords or len(selected_keywords) < num_keywords - (len(set(selected_keywords)) - len(selected_keywords) +1) : # crude duplicate allowance logic
             selected_keywords.append(potential_keyword)
        elif len(combined_pool) <= num_keywords : # if pool is small, allow duplicates
             selected_keywords.append(potential_keyword)


    # Ensure exactly num_keywords are taken, even if padding added more temporarily (though logic above tries to be exact)
    selected_keywords = selected_keywords[:num_keywords]

    keywords_section = "**Keywords:** " + ", ".join(selected_keywords)
    
    # Build the complete abstract
    abstract_output = f"## Abstract\n\n{theoretical_framing}{methodology}{significance}\n\n{keywords_section}\n\n"
    
    # Record usage in coherence_manager
    coherence_manager.record_usage(
        concepts=list(set([abstract_concept, methodology_concept_focus] + [k for k in selected_keywords if k in concepts])),
        terms=list(set([abstract_term, significance_term_focus] + [k for k in selected_keywords if k in terms])),
        philosophers=list(set(abstract_philosophers + [k for k in selected_keywords if k in philosophers]))
    )
    
    return abstract_output