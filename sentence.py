"""
A module for sentence generation that incorporates
dynamic philosopher names, quotes, and citation systems.

This module generates sophisticated sentences for postmodern academic writing,
with proper references, quotes, and thematic consistency.
It supports different sentence types (introduction, general, conclusion)
and handles philosopher citations, concept relationships, and term usage.
The module integrates with the note system for coherent citations
and maintains thematic consistency throughout the generated text.
All citations follow MLA 9 style guidelines.
"""

import random
import string
import re
from data import (philosophers, concepts, terms, philosopher_concepts, contexts,
                 citation_relationships,
                 philosophical_movements, first_names, last_names)
from postmodern_sentence import (enhanced_introduction_templates, enhanced_general_templates, 
                               enhanced_conclusion_templates, metafictional_templates,
                               rhetorical_question_templates, citation_with_framing_templates,
                               philosophical_dialogue_templates)
from quotes import quotes

# Quote-focused templates for enhanced sentence generation 
quote_enhanced_templates = [
    "As {philosopher} writes, \"{quote},\" {citation} which fundamentally reconfigures our understanding of {concept} in relation to {term}.",
    "In a characteristic formulation, {philosopher} argues that \"{quote},\" {citation} thus reframing debates about {concept} and {term}.",
    "The significance of {philosopher}'s claim that \"{quote}\" {citation} lies in how it illuminates the relationship between {concept} and {term}.",
    "{philosopher}'s provocative assertion that \"{quote}\" {citation} offers a productive lens through which to reconsider {term} beyond conventional frameworks.",
    "One might read {philosopher}'s observation that \"{quote}\" {citation} as a direct challenge to standard accounts of the relationship between {concept} and {term}.",
    "When {philosopher} famously claimed that \"{quote},\" {citation} what was at stake was nothing less than the reconceptualization of {term} through the lens of {concept}.",
    "Consider {philosopher}'s influential formulation: \"{quote}\" {citation} - a statement that resituates {concept} within the broader discourse on {term}.",
    "{philosopher}'s insight that \"{quote}\" {citation} reveals the underlying tension between {concept} and {term} that structures much contemporary theory.",
    "The force of {philosopher}'s claim that \"{quote}\" {citation} derives from its radical rethinking of the relationship between {concept} and {term}.",
    "For {philosopher}, the realization that \"{quote}\" {citation} marks a decisive shift in how we conceptualize the interplay of {concept} and {term}."
]

# Quote-focused templates for philosophical dialogues
quote_dialogue_templates = [
    "Where {philosopher1} contends that \"{quote},\" {citation} {philosopher2} emphasizes the ways in which {concept} reconfigures our understanding of {term}.",
    "Although {philosopher1} famously argued that \"{quote},\" {citation} {philosopher2} offers a contrasting approach to {concept} that transforms how we engage with {term}.",
    "Reading {philosopher1}'s claim that \"{quote}\" {citation} against {philosopher2}'s work reveals the complex dialectic between {concept} and {term}.",
    "{philosopher1}'s assertion that \"{quote}\" {citation} can be productively contrasted with {philosopher2}'s approach to {concept} vis-à-vis {term}.",
    "While {philosopher1} maintained that \"{quote},\" {citation} {philosopher2} developed an account of {concept} that fundamentally reimagines its relationship to {term}."
]

# Quote-focused templates for citations
quote_citation_templates = [
    "Echoing {philosopher}'s notable claim that \"{quote}\" {citation}, {author} develops an analysis of {concept} that extends beyond conventional understandings of {term}.",
    "Building on {philosopher}'s insight that \"{quote}\" {citation}, {author} reconsiders the relationship between {concept} and {term}.",
    "{author} draws on {philosopher}'s formulation that \"{quote}\" {citation} to elaborate a more nuanced account of how {concept} shapes our understanding of {term}.",
    "Taking up {philosopher}'s provocative assertion that \"{quote}\" {citation}, {author} offers a compelling reframing of {concept} in relation to {term}.",
    "In conversation with {philosopher}'s argument that \"{quote}\" {citation}, {author} examines how {concept} operates within contemporary discourses on {term}."
]

# Original templates from the previous version
introduction_templates = [
    "this paper examines {term} in relation to {concept} within {context}.",
    "the interplay between {concept} and {term} shapes our understanding of {context}.",
    "this paper explores the intricate relationship between {term} and {concept} within the discursive field of {context}.",
    "in recent scholarly endeavors, {term} has emerged as a focal point, particularly within the ambit of {context}.",
    "this study seeks to interrogate the modalities through which {concept} shapes {term} in {context}.",
    "the ensuing analysis situates {concept} within the broader epistemic terrain of {term} in {context}.",
    "it merits consideration that {concept} has assumed a pivotal role in elucidating {term} within {context}.",
    "contemporary discourse increasingly gravitates toward {term}, especially when viewed through {context}.",
    "the confluence of {concept} and {term} yields novel insights into the fabric of {context}.",
    "by refracting {concept} through the prism of {term}, this paper enriches the discourse of {context}.",
    "to apprehend {term} fully, one must adopt a nuanced engagement with {concept} in {context}.",
    "this inquiry probes {concept}'s constitutive role in the reconfiguration of {term} within {context}.",
    "this essay, in its initial foray, navigates the contested terrain of {term} through {concept} in {context}, resisting closure.",
    "the opening salvo of this analysis foregrounds {concept}'s entanglement with {term} within {context}, a terrain of perpetual deferral.",
    "here, we embark on an exploration of {term}, its nexus with {concept} unfolding within the fractured landscape of {context}.",
    "this essay, in its attempt to grapple with {term}, inadvertently becomes a testament to {concept} within {context}.",
    "the following analysis, while centered on {term}, is invariably shaped by the specter of {concept} in {context}.",
    "to commence, {term} emerges not as a stable entity but as a diffraction of {concept} within {context}, eluding fixity.",
    "this text initiates its journey by tracing the unstable contours of {term} through {concept}, situated precariously in {context}.",
    "in a gesture both preliminary and provisional, this study probes {term} as it intersects with {concept} amidst {context}."
]

general_templates = [
    "{philosopher} argues that {concept} redefines {term} in significant ways.",
    "according to {philosopher}, {term} is deeply tied to {concept}.",
    "as {philosopher} stated, \"{quote}\", highlighting {concept} in {context}.",
    "{philosopher1} and {philosopher2} offer contrasting views on {term} through {concept}.",
    "{philosopher} posits that {concept} serves as a linchpin in reimagining {term}.",
    "for {philosopher}, {concept} destabilizes the sedimented meanings of {term}.",
    "within the ambit of {term}, {concept} emerges as a site of epistemic rupture. [citation]",
    "{concept}, as {philosopher} delineates, reorients our engagement with {term}.",
    "{philosopher1} and {philosopher2} proffer divergent readings of {concept} vis-à-vis {term}.",
    "certain critics aver that {philosopher}'s {concept} elides critical dimensions of {term}. [citation]",
    "can {concept}, as {philosopher} contemplates, fully encapsulate the complexities of {term}?",
    "in {philosopher}'s corpus, {concept} casts a revelatory light upon {term}.",
    "{term} functions as the ground against which {philosopher} articulates {concept}.",
    "through the lens of {concept}, {philosopher} interrogates the foundational axioms of {term}. [citation]",
    "{philosopher} embeds {concept} within the expansive discourse of {term}.",
    "the dialectical interplay of {concept} and {term} recurs throughout {philosopher}'s oeuvre.",
    "this analysis probes the différance inherent in {concept}, per {philosopher}, relative to {term}.",
    "in {philosopher}'s schema, {concept} constitutes a contested terrain for {term}.",
    "the trace of {concept} within {philosopher}'s texts unveils its imbrication with {term}.",
    "{philosopher} often cites {other_philosopher}'s work, particularly the idea of {other_concept}, saying, \"{quote}\", to support their argument on {term}.",
    "{philosopher}'s engagement with {concept} resonates with {other_philosopher}'s exploration of {other_concept}, illuminating {term}.",
    "echoing {other_philosopher}'s insights, {philosopher} frames {concept} as a {term} within {context}.",
    "{philosopher1}'s notion of {concept} can be juxtaposed with {philosopher2}'s {other_concept}, revealing the multifaceted nature of {term}.",
    "this essay, in its exploration of {term}, finds itself entangled in the very {concept} it seeks to unpack.",
    "the act of writing about {concept} inevitably entangles the author in the same discursive practices that {term} critiques.",
    "this paragraph, in its attempt to elucidate {term}, inevitably falls into the trap of {concept}.",
    "as we proceed, it becomes clear that the very act of writing about {term} implicates us in {concept}.",
    "in writing this essay, the author becomes complicit in the {concept} they analyze, a {term} without resolution.",
    "this text, in its interrogation of {term}, mirrors the very {concept} it seeks to deconstruct.",
    "it is ironic that, in an age obsessed with {term}, {concept} remains elusive.",
    "any definitive statement about {concept} is inherently problematic, given its fluid and contested nature.",
    "the pursuit of {concept} as a {term} reveals its own impossibility, a paradox {philosopher} might appreciate.",
    "in the shadow of {concept}, {term} becomes a site of perpetual deferral, as {philosopher} might suggest.",
    "{philosopher} argues that {concept} is central to understanding {term} (though some, like {other_philosopher}, disagree).",
    "the concept of {concept}, as {philosopher} suggests, is fraught with contradictions—yet it remains indispensable for analyzing {term}.",
    "while {philosopher} celebrates {concept}, it is crucial to recognize its limitations in addressing {term}.",
    "{philosopher}'s {concept} offers a powerful lens for viewing {term}, yet it risks oversimplifying the complexities involved.",
    "in a {context}, {term} becomes a battleground where {concept} and its counterpoints collide."
]

conclusion_templates = [
    "in summation, this inquiry has elucidated the indelible role of {concept} in apprehension {term}.",
    "these findings bear profound implications for {context}, particularly through the prism of {concept}.",
    "to conclude, this analysis underscores the salience of {term} vis-à-vis {concept}.",
    "this study has demonstrated that {concept} fundamentally reconfigures our approach to {term} in {context}.",
    "future scholarship might fruitfully explore {concept}'s ramification for {term} within {context}.",
    "the symbiosis of {concept} and {term} proves essential to grasping {context}, as evidenced herein.",
    "by traversing {term} through {concept}, this paper augments our understanding of {context}.",
    "the results intimate that {concept} is a decisive vector in the constitution of {term} within {context}.",
    "this examination reveals {term}'s profound entanglement with {concept}, upending orthodoxies in {context}.",
    "ultimately, these insights affirm that {concept} is indispensable to any rigorous study of {term} in {context}.",
    "this essay, in its attempt to {term}, has perhaps only succeeded in demonstrating the complexity and elusiveness of {concept}.",
    "the very act of concluding this discussion underscores {concept}'s pervasive influence, as even in summarizing, we are entangled in its discursive web.",
    "in closing, the interplay of {concept} and {term} within {context} remains a site of unending contestation.",
    "this analysis, in its final gesture, affirms {concept}'s centrality to {term}, yet leaves its resolution open.",
    "the conclusion, like {concept} itself, resists closure, echoing {term}'s fluidity in {context}.",
    "ultimately, this exploration of {term} through {concept} leaves us with more questions than answers, a fitting end for a postmodern inquiry.",
    "as we conclude, it becomes apparent that {concept} is not merely a lens for viewing {term}, but an inescapable condition of our {context}.",
    "in attempting to conclude this essay, we find ourselves caught in the very {concept} we sought to analyze, a testament to its pervasive influence."
]

def match_philosopher_to_quotes(philosopher_name):
    """
    Match a philosopher name (which might be just a last name) to a full name in the quotes dictionary.
    
    Args:
        philosopher_name (str): The philosopher name to match (could be full name or last name)
        
    Returns:
        str: The matching full name from the quotes dictionary, or None if no match is found
    """
    # If the full name is in the quotes dictionary, return it
    if philosopher_name in quotes:
        return philosopher_name
    
    # Check if it's a last name that matches a full name in the quotes dictionary
    for full_name in quotes.keys():
        if full_name.split()[-1] == philosopher_name:
            return full_name
    
    # No match found
    return None


def get_introduction_templates():
    """Get the pool of introduction templates, prioritizing enhanced ones."""
    # Use 80% enhanced templates, 20% original templates for variety
    templates = enhanced_introduction_templates + introduction_templates[:5]
    return templates


def get_general_templates():
    """Get the pool of general templates, prioritizing enhanced ones and including quote templates."""
    # Use enhanced templates, original templates, and our new quote templates
    templates = enhanced_general_templates + general_templates[:10] + quote_enhanced_templates
    return templates


def get_conclusion_templates():
    """Get the pool of conclusion templates, prioritizing enhanced ones."""
    # Use 80% enhanced templates, 20% original templates for variety
    templates = enhanced_conclusion_templates + conclusion_templates[:5]
    return templates


def get_dialogue_templates():
    """Get dialogue templates, including quote-focused ones."""
    # Add our new quote dialogue templates to the existing ones
    templates = philosophical_dialogue_templates + quote_dialogue_templates
    return templates


def get_citation_templates():
    """Get citation templates, including quote-focused ones."""
    # Add our new quote citation templates to the existing ones
    templates = citation_with_framing_templates + quote_citation_templates
    return templates


def generate_sentence(template_type, references, mentioned_philosophers, forbidden_philosophers=[], 
                     forbidden_concepts=[], forbidden_terms=[], used_quotes=set(), 
                     all_references=None, cited_references=None, note_system=None, context=None):
    """
    Generate a sentence based on template type, handling philosopher names and quotes dynamically
    with enhanced sophistication and academic authenticity.
    
    Args:
        template_type (str): Type of sentence ('introduction', 'conclusion', or 'general').
        references: Legacy parameter (retained for compatibility)
        mentioned_philosophers (set): Philosophers already mentioned in the essay.
        forbidden_philosophers (list): Philosophers to exclude.
        forbidden_concepts (list): Concepts to exclude.
        forbidden_terms (list): Terms to exclude.
        used_quotes (set): Quotes already used.
        all_references (list): Legacy parameter, use note_system instead
        cited_references (list): Legacy parameter, use note_system instead
        note_system (NoteSystem): System for managing notes and citations
        context (dict): Contextual information about the sentence being generated
    
    Returns:
        tuple: (sentence_list, used_philosophers, used_concepts, used_terms)
    """
    # Initialize or create context dict if not provided
    if context is None:
        context = {'type': template_type}
    else:
        context['type'] = template_type
    
    # Select appropriate template pool based on type
    if template_type == "introduction":
        return _generate_introduction_sentence(mentioned_philosophers, forbidden_philosophers,
                                             forbidden_concepts, forbidden_terms, context)
    
    elif template_type == "conclusion":
        return _generate_conclusion_sentence(mentioned_philosophers, forbidden_philosophers,
                                           forbidden_concepts, forbidden_terms, context)
    
    else:  # general sentences
        return _generate_general_sentence(mentioned_philosophers, forbidden_philosophers, 
                                        forbidden_concepts, forbidden_terms, used_quotes,
                                        all_references, cited_references, note_system, context)


def _generate_introduction_sentence(mentioned_philosophers, forbidden_philosophers,
                                  forbidden_concepts, forbidden_terms, context):
    """Generate an introduction-type sentence."""
    templates = get_introduction_templates()
    
    # Occasionally use metafictional templates in introduction
    if random.random() < 0.2:
        templates.extend(metafictional_templates[:3])
        
    template = random.choice(templates)
    
    # Prioritize terms and concepts from title themes if available in context
    title_themes = context.get('title_themes', {})
    
    if title_themes and title_themes.get('primary_concepts') and random.random() < 0.8:
        # 80% chance to use a concept from title themes
        available_concepts = [c for c in title_themes['primary_concepts'] 
                            if c not in forbidden_concepts]
        if not available_concepts and title_themes.get('related_concepts'):
            available_concepts = [c for c in title_themes['related_concepts'] 
                                if c not in forbidden_concepts]
        if available_concepts:
            concept = random.choice(available_concepts)
        else:
            concept = random.choice([c for c in concepts if c not in forbidden_concepts])
    else:
        concept = random.choice([c for c in concepts if c not in forbidden_concepts])
    
    if title_themes and title_themes.get('primary_terms') and random.random() < 0.8:
        # 80% chance to use a term from title themes
        available_terms = [t for t in title_themes['primary_terms'] 
                         if t not in forbidden_terms]
        if available_terms:
            term = random.choice(available_terms)
        else:
            term = random.choice([t for t in terms if t not in forbidden_terms])
    else:
        term = random.choice([t for t in terms if t not in forbidden_terms])
    
    adj = random.choice(["critical", "radical", "postmodern", "deconstructive", "theoretical", 
                       "discursive", "dialectical", "phenomenological", "ontological", "epistemological"])
    context_text = random.choice(contexts)
    
    # Format the template with selected terms
    sentence = template.format(term=term, concept=concept, context=context_text, adj=adj)
    
    used_philosophers = []
    used_concepts = [concept]
    used_terms = [term]
    
    return [(sentence, None)], used_philosophers, used_concepts, used_terms


def _generate_conclusion_sentence(mentioned_philosophers, forbidden_philosophers,
                                forbidden_concepts, forbidden_terms, context):
    """Generate a conclusion-type sentence."""
    templates = get_conclusion_templates()
    
    # Higher chance of metafictional elements in conclusions
    if random.random() < 0.3:
        templates.extend(metafictional_templates[:5])
        
    template = random.choice(templates)
    
    # For conclusions, we want to refer back to core concepts
    term = random.choice([t for t in terms if t not in forbidden_terms])
    concept = random.choice([c for c in concepts if c not in forbidden_concepts])
    context_text = random.choice(contexts)
    
    # Format the template with selected terms
    sentence = template.format(term=term, concept=concept, context=context_text)
    
    used_philosophers = []
    used_concepts = [concept]
    used_terms = [term]
    
    return [(sentence, None)], used_philosophers, used_concepts, used_terms

def _generate_general_sentence(mentioned_philosophers, forbidden_philosophers, 
                             forbidden_concepts, forbidden_terms, used_quotes,
                             all_references, cited_references, note_system, context):
    """Generate a general-type sentence with various sub-types."""
    # Determine what type of general sentence to generate
    sentence_type = random.choice([
        "standard",       # 50% standard templates
        "standard", 
        "standard",
        "standard",
        "standard",
        "standard",
        "dialogue",       # 20% philosophical dialogue
        "dialogue",
        "quote",          # 8% quote-focused templates
        "rhetorical",     # 10% rhetorical questions
        "citation",       # 10% citation with framing
        "metafictional",  # 2% metafictional
    ])
    
    # Get available philosophers - prioritize from context if available
    available_philosophers = [p for p in philosophers if p not in forbidden_philosophers]
    
    # Prioritize relevant philosophers from title themes if available
    relevant_philosophers = context.get('relevant_philosophers', []) if context else []
    if relevant_philosophers and random.random() < 0.7:  # 70% chance to use title-relevant philosophers
        prioritized_philosophers = [p for p in relevant_philosophers if p not in forbidden_philosophers]
        if prioritized_philosophers:
            available_philosophers = prioritized_philosophers + available_philosophers
    
    # Find philosophers who have quotes (either full name or last name)
    philosophers_with_quotes = []
    for philosopher in available_philosophers:
        if match_philosopher_to_quotes(philosopher) is not None:
            philosophers_with_quotes.append(philosopher)
    
    # If we need a quote-based template, prioritize philosophers with quotes
    if sentence_type == "quote" and philosophers_with_quotes:
        available_philosophers = philosophers_with_quotes
    
    if not available_philosophers:
        # Fallback if no philosophers are available
        available_philosophers = philosophers[:5]
    
    # Choose template based on sentence type
    if sentence_type == "standard":
        template_pool = get_general_templates()
    elif sentence_type == "dialogue":
        template_pool = get_dialogue_templates()
    elif sentence_type == "quote":
        template_pool = quote_enhanced_templates  # Our new quote templates
    elif sentence_type == "rhetorical":
        template_pool = rhetorical_question_templates
    elif sentence_type == "citation":
        template_pool = get_citation_templates()
    else:  # metafictional
        template_pool = metafictional_templates
        
    # Try to select a template that can be filled with available philosophers
    valid_templates = []
    for t in template_pool:
        # Count required philosopher fields
        required_philosophers = sum(1 for _, field, _, _ in string.Formatter().parse(t) 
                                  if field and (field.startswith('philosopher') or field == 'other_philosopher'))
        if required_philosophers <= len(available_philosophers):
            valid_templates.append(t)
    
    # If no valid templates, use simpler templates
    if not valid_templates:
        template = "The work of {philosopher} on {concept} has significant implications for {term}."
    else:
        template = random.choice(valid_templates)
    
    # Parse all fields in the template
    fields = [field for _, field, _, _ in string.Formatter().parse(template) if field]
    
    # Determine quote source if needed
    quote_source_field = 'other_philosopher' if 'other_philosopher' in fields else ('philosopher' if 'philosopher' in fields else 'philosopher1')
    
    # Initialize data and tracking lists
    data = {}
    used_philosophers = []
    used_concepts = []
    used_terms = []
    
    # Get title themes if available
    title_themes = context.get('title_themes', {}) if context else {}
    title_concepts = title_themes.get('primary_concepts', []) + title_themes.get('related_concepts', []) if title_themes else []
    title_terms = title_themes.get('primary_terms', []) if title_themes else []
    
    # Populate fields in template
    _populate_philosopher_fields(fields, data, available_philosophers, used_philosophers, mentioned_philosophers)
    
    # Prioritize title concepts if available (70% chance)
    if 'concept' in fields and title_concepts and random.random() < 0.7:
        available_title_concepts = [c for c in title_concepts if c not in forbidden_concepts and c not in used_concepts]
        if available_title_concepts:
            data['concept'] = random.choice(available_title_concepts)
            used_concepts.append(data['concept'])
        else:
            _populate_concept_fields(fields, data, used_philosophers, forbidden_concepts, used_concepts)
    else:
        _populate_concept_fields(fields, data, used_philosophers, forbidden_concepts, used_concepts)
    
    # Prioritize title terms if available (70% chance)
    if 'term' in fields and title_terms and random.random() < 0.7:
        available_title_terms = [t for t in title_terms if t not in forbidden_terms and t not in used_terms]
        if available_title_terms:
            data['term'] = random.choice(available_title_terms)
            used_terms.append(data['term'])
        else:
            _populate_term_fields(fields, data, forbidden_terms, used_terms)
    else:
        _populate_term_fields(fields, data, forbidden_terms, used_terms)
    
    _populate_context_fields(fields, data)
    
    # Handle quotes if needed
    if 'quote' in fields:
        template = _handle_quote_in_template(template, data, quote_source_field, used_quotes, 
                                          used_concepts, used_terms, used_philosophers, note_system, context)
    
    # Handle citation fields for citation_with_framing_templates
    if 'author' in fields and 'year' in fields:
        template = _handle_author_citation(template, data, context, used_concepts, 
                                        used_terms, used_philosophers, note_system)
    
    # Format the sentence with all the collected data
    sentence = _format_sentence_from_template(template, data, used_concepts, used_terms, 
                                            note_system, context)
    
    # Handle citations with the note system
    if '[citation]' in sentence and note_system:
        sentence = _handle_citation_marker(sentence, context, used_concepts, 
                                        used_terms, used_philosophers, note_system)
    # Legacy citation handling for backward compatibility    
    elif '[citation]' in sentence and all_references and cited_references is not None:
        sentence = _handle_legacy_citation(sentence, all_references, cited_references)
    
    # Finalize sentence
    sentence = _finalize_sentence(sentence)
    
    return [(sentence, None)], used_philosophers, used_concepts, used_terms


def _populate_philosopher_fields(fields, data, available_philosophers, used_philosophers, mentioned_philosophers):
    """Populate philosopher-related fields in the template data dictionary."""
    for field in fields:
        if field.startswith('philosopher') or field == 'other_philosopher':
            available_pool = [p for p in available_philosophers if p not in used_philosophers]
            
            # If second philosopher, try to select a related one
            if field in ['philosopher2', 'other_philosopher'] and used_philosophers:
                phil = _select_related_philosopher(used_philosophers[0], available_pool, available_philosophers)
            else:
                # For first philosopher, prioritize those not yet mentioned
                phil = _select_first_philosopher(available_pool, mentioned_philosophers, available_philosophers)
            
            # Format philosopher name appropriately
            phil_name = phil if phil not in mentioned_philosophers else phil.split()[-1]
            if phil not in mentioned_philosophers:
                mentioned_philosophers.add(phil)
                
            data[field] = phil_name
            used_philosophers.append(phil)


def _select_related_philosopher(first_phil, available_pool, all_philosophers):
    """Select a philosopher related to the first philosopher in the sentence."""
    # Check citation relationships for possible related philosophers
    if first_phil in citation_relationships and citation_relationships[first_phil]:
        related_phils = [p for p in citation_relationships[first_phil] 
                        if p in available_pool]
        if related_phils:
            return random.choice(related_phils)
        else:
            # If no related philosophers, use movement relationships
            movement_match = False
            for movement, movement_phils in philosophical_movements.items():
                if first_phil in movement_phils:
                    movement_options = [p for p in movement_phils 
                                     if p in available_pool]
                    if movement_options:
                        return random.choice(movement_options)
                        movement_match = True
                        break
            
            if not movement_match:
                # Fallback to random selection
                return random.choice(available_pool) if available_pool else random.choice(all_philosophers)
    else:
        # Fallback to random selection
        return random.choice(available_pool) if available_pool else random.choice(all_philosophers)


def _select_first_philosopher(available_pool, mentioned_philosophers, all_philosophers):
    """Select the first philosopher for a sentence, favoring new philosophers."""
    unmention_phils = [p for p in available_pool if p not in mentioned_philosophers]
    if unmention_phils and random.random() < 0.7:  # 70% chance to use new philosopher
        return random.choice(unmention_phils)
    else:
        return random.choice(available_pool) if available_pool else random.choice(all_philosophers)


def _populate_concept_fields(fields, data, used_philosophers, forbidden_concepts, used_concepts):
    """Populate concept-related fields in the template data dictionary."""
    for field in fields:
        if field == 'concept':
            # Try to use a concept related to the philosopher
            main_phil = data.get('philosopher', data.get('philosopher1'))
            if main_phil and main_phil in philosopher_concepts:
                related_concepts = [c for c in philosopher_concepts[main_phil] 
                                  if c not in forbidden_concepts and c not in used_concepts]
                if related_concepts:
                    concept = random.choice(related_concepts)
                else:
                    concept = random.choice([c for c in concepts 
                                         if c not in forbidden_concepts and c not in used_concepts])
            else:
                concept = random.choice([c for c in concepts 
                                     if c not in forbidden_concepts and c not in used_concepts])
            data[field] = concept
            used_concepts.append(concept)
        elif field == 'other_concept':
            # For other_concept, prefer to use a related concept
            if used_concepts:
                concept = _select_related_concept(used_concepts[0], used_philosophers, 
                                               data, forbidden_concepts, used_concepts)
            else:
                concept = random.choice([c for c in concepts 
                                     if c not in forbidden_concepts 
                                     and c not in used_concepts])
            
            data[field] = concept
            used_concepts.append(concept)


def _select_related_concept(primary_concept, used_philosophers, data, forbidden_concepts, used_concepts):
    """Select a concept related to the primary concept in the sentence."""
    # Try to find a related concept through clusters
    try:
        from data import concept_clusters
        related_cluster_concepts = []
        for cluster, cluster_concepts in concept_clusters.items():
            if primary_concept in cluster_concepts:
                related_cluster_concepts = [c for c in cluster_concepts 
                                         if c != primary_concept and c not in forbidden_concepts
                                         and c not in used_concepts]
        
        if related_cluster_concepts:
            return random.choice(related_cluster_concepts)
        else:
            # If no cluster relationship, use philosopher relationship
            other_phil = data.get('other_philosopher', data.get('philosopher2'))
            if other_phil and other_phil in philosopher_concepts:
                phil_concepts = [c for c in philosopher_concepts[other_phil] 
                              if c not in forbidden_concepts and c not in used_concepts]
                if phil_concepts:
                    return random.choice(phil_concepts)
                else:
                    return random.choice([c for c in concepts 
                                       if c not in forbidden_concepts 
                                       and c not in used_concepts])
            else:
                return random.choice([c for c in concepts 
                                   if c not in forbidden_concepts 
                                   and c not in used_concepts])
    except ImportError:
        # Fallback if concept_clusters isn't available
        return random.choice([c for c in concepts 
                           if c not in forbidden_concepts 
                           and c not in used_concepts and c != primary_concept])


def _populate_term_fields(fields, data, forbidden_terms, used_terms):
    """Populate term-related fields in the template data dictionary."""
    if 'term' in fields:
        term = random.choice([t for t in terms if t not in forbidden_terms and t not in used_terms])
        data['term'] = term
        used_terms.append(term)


def _populate_context_fields(fields, data):
    """Populate context and adjective fields in the template data dictionary."""
    if 'context' in fields:
        data['context'] = random.choice(contexts)
        
    if 'adj' in fields:
        data['adj'] = random.choice(["critical", "radical", "postmodern", "deconstructive", "theoretical", 
                                  "discursive", "dialectical", "phenomenological", "ontological", "epistemological"])


def _format_quote_for_academic_style(quote, template):
    """
    Format a quote according to academic guidelines based on context.
    
    Args:
        quote (str): The quote to format
        template (str): The template containing the quote
        
    Returns:
        str: Properly formatted quote
    """
    # Check if the quote is mid-sentence (not at the end of the template)
    is_mid_sentence = False
    
    # Look for patterns that indicate the quote is mid-sentence
    mid_sentence_indicators = [
        '"{quote}," ', '"{quote}" ', '"{quote}—', '"{quote}" which',
        '"{quote}" in', '"{quote}" that', '"{quote}" thus', '"{quote}" offering'
    ]
    for indicator in mid_sentence_indicators:
        if indicator in template:
            is_mid_sentence = True
            break
    
    # If the quote ends with a period and is in the middle of a sentence, remove the period
    if is_mid_sentence and quote and quote.endswith('.'):
        quote = quote[:-1]
    
    # For other punctuation (comma, semicolon, etc.), only remove if template adds identical punctuation
    elif quote and quote[-1] in ',;:!?':
        # Check if the template adds punctuation after the quote
        if '"{quote},' in template or '"{quote};"' in template or '"{quote}:"' in template or '"{quote}!"' in template or '"{quote}?"' in template:
            quote = quote[:-1]
    
    # Handle lowercase bracketed first letter for quotes after "that", "which", etc.
    lowercase_indicators = ['that "{quote}', 'which "{quote}', 'in which "{quote}', 'through which "{quote}']
    needs_lowercase = any(indicator in template for indicator in lowercase_indicators)
    
    if needs_lowercase and quote and len(quote) > 0 and quote[0].isupper():
        # Add brackets around first letter and make it lowercase for academic style
        quote = '[' + quote[0].lower() + ']' + quote[1:]
    
    return quote


def _handle_quote_in_template(template, data, quote_source_field, used_quotes, 
                           used_concepts, used_terms, used_philosophers, note_system, context):
    """
    Handle quotes in templates, including formatting and MLA citations.
    Prioritize quotes from philosophers associated with title themes.
    
    Args:
        template (str): Template string containing {quote} placeholder
        data (dict): Data dictionary with populated fields
        quote_source_field (str): Field name for the quote source philosopher
        used_quotes (set): Set of quotes already used
        used_concepts (list): Concepts used in this sentence
        used_terms (list): Terms used in this sentence
        used_philosophers (list): Philosophers referenced in this sentence
        note_system (NoteSystem): System for managing citations
        context (dict): Context information for this sentence
        
    Returns:
        str: Template with quote filled in and properly cited
    """
    quote_source_name = data.get(quote_source_field)
    
    # Get title themes if available
    title_themes = context.get('title_themes', {})
    title_concepts = title_themes.get('primary_concepts', []) if title_themes else []
    title_terms = title_themes.get('primary_terms', []) if title_themes else []
    
    # Get list of relevant philosophers if available
    relevant_philosophers = context.get('relevant_philosophers', [])
    
    # If there are title themes and relevant philosophers, try to use them with high probability
    if (title_concepts or title_terms) and relevant_philosophers and random.random() < 0.7:
        # Replace current philosopher with a more relevant one
        if quote_source_name not in relevant_philosophers:
            quote_source_name = random.choice(relevant_philosophers)
            data[quote_source_field] = quote_source_name
    
    if quote_source_name:
        # Match the philosopher name to a full name in the quotes dictionary
        full_name = match_philosopher_to_quotes(quote_source_name)
        
        if full_name and full_name in quotes:
            available_quotes = [q for q in quotes[full_name] if q not in used_quotes]
            if available_quotes:
                selected_quote = random.choice(available_quotes)
                
                # Format the quote according to academic guidelines
                formatted_quote = _format_quote_for_academic_style(selected_quote, template)
                
                # Replace the quote placeholder
                template = template.replace('{quote}', formatted_quote)
                used_quotes.add(selected_quote)
                
                # Create a citation for this quote
                if note_system:
                    # Create a plausible source
                    year = random.randint(1950, 2010)  
                    
                    # Use enhanced citation method
                    is_article = random.random() < 0.3  # 30% chance to be an article
                    reference = note_system.get_enhanced_citation(full_name, is_article, year)
                    
                    # Get last name for citation
                    last_name = full_name.split()[-1]
                    
                    # Use add_citation to add the reference to works cited
                    citation = note_system.add_citation(reference, context)
                    
                    # Make sure every quote has a citation immediately following it
                    # First, find where the quote ends in the template
                    quote_end_positions = []
                    for i in range(len(template)):
                        if template[i:i+1] == '"' and i > template.find(formatted_quote):
                            quote_end_positions.append(i)
                    
                    if quote_end_positions:
                        quote_end_pos = quote_end_positions[0]
                        
                        # Check if the quote is at the end of a sentence
                        is_end_of_sentence = False
                        for pos in range(quote_end_pos+1, min(quote_end_pos+5, len(template))):
                            if pos < len(template) and template[pos] in '.?!':
                                is_end_of_sentence = True
                                break
                        
                        # Insert citation after the closing quote, preserving punctuation properly
                        if is_end_of_sentence:
                            # Move punctuation to after citation
                            before_quote = template[:quote_end_pos+1]
                            after_quote = template[quote_end_pos+1:]
                            punctuation_match = re.search(r'^[.!?,;:]', after_quote.lstrip())
                            
                            if punctuation_match:
                                punctuation = punctuation_match.group(0)
                                template = before_quote + " " + citation + punctuation + after_quote.lstrip()[1:]
                            else:
                                template = before_quote + " " + citation + after_quote
                        else:
                            # Insert citation after quote with no punctuation changes
                            template = template[:quote_end_pos+1] + " " + citation + template[quote_end_pos+1:]
                    else:
                        # Fallback if we can't find quote end - add citation to end of template
                        if template.endswith('.'):
                            template = template[:-1] + " " + citation + "."
                        else:
                            template = template + " " + citation
            else:
                # If no unused quotes, create a generic quote with citation
                generic_quote = f"the relationship between {data.get('concept', 'theory')} and {data.get('term', 'practice')} is always already mediated by power"
                template = template.replace('{quote}', generic_quote)
                
                if note_system:
                    # Create a generic reference
                    reference = note_system.get_enhanced_citation(quote_source_name, False, random.randint(1950, 2010))
                    citation = note_system.add_citation(reference, context)
                    
                    # Add citation after the generic quote
                    quote_pos = template.find(generic_quote) + len(generic_quote)
                    before = template[:quote_pos]
                    after = template[quote_pos:]
                    
                    # Add citation after quote
                    quote_end_match = re.search(r'"\s*[,.;:]?', after)
                    if quote_end_match:
                        quote_end = quote_end_match.end()
                        template = before + after[:quote_end].rstrip() + " " + citation + after[quote_end:]
                    else:
                        template = before + "\" " + citation + after
        else:
            # If no quotes for the philosopher, create a generic quote with citation
            generic_quote = f"the relationship between {data.get('concept', 'theory')} and {data.get('term', 'practice')} is always already mediated by power"
            template = template.replace('{quote}', generic_quote)
            
            if note_system:
                # Create a generic reference
                reference = note_system.get_enhanced_citation(quote_source_name, False, random.randint(1950, 2010))
                citation = note_system.add_citation(reference, context)
                
                # Add citation after the generic quote
                quote_pos = template.find(generic_quote) + len(generic_quote)
                template = template[:quote_pos] + "\" " + citation + template[quote_pos:]
    else:
        # If no philosopher specified, use a generic quote with generic citation
        generic_quote = f"the analysis of {data.get('concept', 'theory')} requires a reconsideration of {data.get('term', 'practice')}"
        template = template.replace('{quote}', generic_quote)
        
        if note_system:
            # Create a generic reference to "Smith"
            reference = note_system.get_enhanced_citation("Smith, John", False, random.randint(1950, 2010))
            citation = note_system.add_citation(reference, context)
            
            # Add citation after the generic quote
            quote_pos = template.find(generic_quote) + len(generic_quote)
            template = template[:quote_pos] + "\" " + citation + template[quote_pos:]
    
    # Final check for periods before citations
    template = re.sub(r'\.\s+\(([^)]+)\)', r' (\1).', template)
    template = re.sub(r',\s+\(([^)]+)\)', r' (\1),', template)
    
    return template

def _process_citation_placeholders(sentence, note_system, context, philosopher_name=None):
    """
    Process citation placeholders in a sentence.
    
    Args:
        sentence (str): The sentence with {citation} placeholders
        note_system (NoteSystem): System for managing citations
        context (dict): Context information for the sentence
        philosopher_name (str, optional): Name of the philosopher to cite
        
    Returns:
        str: The sentence with proper citations
    """
    if '{citation}' not in sentence:
        return sentence
    
    # Generate a citation if we have a note system
    if note_system and philosopher_name:
        # Create a reference for the citation
        year = random.randint(1950, 2010)
        is_article = random.random() < 0.3
        reference = note_system.get_enhanced_citation(philosopher_name, is_article, year)
        citation = note_system.add_citation(reference, context)
        
        # Replace the {citation} placeholder
        sentence = sentence.replace('{citation}', citation)
    else:
        # Remove the placeholder if we can't create a citation
        sentence = sentence.replace('{citation}', '')
    
    return sentence

def _handle_author_citation(template, data, context, used_concepts, used_terms, used_philosophers, note_system):
    """
    Handle author citations in templates, including formatting and bibliography entries in MLA 9 style.
    
    Args:
        template (str): Template string containing author citation placeholders
        data (dict): Data dictionary with populated fields
        context (dict): Context information for this sentence
        used_concepts (list): Concepts used in this sentence
        used_terms (list): Terms used in this sentence
        used_philosophers (list): Philosophers referenced in this sentence
        note_system (NoteSystem): System for managing citations
        
    Returns:
        str: Template with author citations formatted in MLA style
    """
    # Create a relevant reference based on context
    reference = _generate_contextual_reference(context, used_concepts, used_terms)
    
    # Simple parsing to extract author and year from reference
    author_match = re.match(r'^([^(]+)\(([0-9]{4})\)', reference)
    if author_match:
        author, year = author_match.groups()
        data['author'] = author.strip()
        data['year'] = year.strip()
    else:
        # Fallback
        data['author'] = "Smith"
        data['year'] = str(random.randint(1950, 2023))
    
    # Extract just the last name for MLA style
    if ',' in data['author']:
        last_name = data['author'].split(',')[0]
    else:
        name_parts = data['author'].split()
        last_name = name_parts[-1] if name_parts else "Smith"
    
    # Add citation to note system if available
    if note_system:
        # Use add_citation instead of add_to_works_cited to create notes
        citation = note_system.add_citation(reference, context)
        
        # Make sure the template includes the citation
        if not template.endswith('.'):
            template += f" {citation}."
        elif template.endswith('. '):
            template = template[:-2] + f" {citation}. "
        else:
            template = template[:-1] + f" {citation}."
    
    return template

def ensure_quote_has_citation(text):
    """
    Ensure that every direct quote in the text has a citation.
    
    Args:
        text (str): The text to check
        
    Returns:
        str: The text with properly cited quotes
    """
    # Find all quotes in the text
    quote_pattern = r'"([^"]+)"'
    matches = re.finditer(quote_pattern, text)
    
    result = text
    for match in matches:
        quote = match.group(1)
        quote_end_pos = match.end()
        
        # Check if there's a citation after the quote
        citation_pattern = r'"\s*\([^)]+\)'
        has_citation = re.search(citation_pattern, text[match.start():match.start()+len(quote)+50])
        
        if not has_citation:
            # Add a generic citation for any uncited quote
            # This is a fallback for any quotes that slipped through
            generic_citation = " (Author 25)"
            
            # Insert the citation after the closing quote
            result = result[:quote_end_pos] + generic_citation + result[quote_end_pos:]
    
    return result

def _format_sentence_from_template(template, data, used_concepts, used_terms, note_system=None, context=None):
    """
    Format a sentence from a template and data dictionary, handling any missing keys.
    
    Args:
        template (str): Template string with placeholders
        data (dict): Data dictionary with values for placeholders
        used_concepts (list): List to track concepts used
        used_terms (list): List to track terms used
        note_system (NoteSystem): System for managing citations
        context (dict): Context information for this sentence
        
    Returns:
        str: Formatted sentence
    """
    try:
        sentence = template.format(**data)
        
        # Process citation placeholders if present
        if '{citation}' in sentence and note_system:
            philosopher_name = data.get('philosopher', data.get('philosopher1'))
            sentence = _process_citation_placeholders(sentence, note_system, context, philosopher_name)
        
    except KeyError as e:
        # Fallback if template has missing fields
        missing_key = str(e).strip("'")
        if missing_key.startswith('philosopher'):
            data[missing_key] = random.choice(philosophers)
        elif missing_key == 'concept' or missing_key == 'other_concept':
            data[missing_key] = random.choice(concepts)
        elif missing_key == 'term':
            data[missing_key] = random.choice(terms)
        elif missing_key == 'context':
            data[missing_key] = random.choice(contexts)
        elif missing_key == 'adj':
            data[missing_key] = random.choice(["critical", "radical", "postmodern"])
        elif missing_key == 'author':
            data[missing_key] = "Smith"
        elif missing_key == 'year':
            data[missing_key] = str(random.randint(1950, 2023))
        elif missing_key == 'citation':
            data[missing_key] = ''  # Empty string for citation placeholder if we can't resolve it
        
        # Try again with added data
        try:
            sentence = template.format(**data)
            
            # Process citation placeholders if present
            if '{citation}' in sentence and note_system:
                philosopher_name = data.get('philosopher', data.get('philosopher1'))
                sentence = _process_citation_placeholders(sentence, note_system, context, philosopher_name)
                
        except KeyError:
            # Ultimate fallback
            sentence = f"The work of {data.get('philosopher', random.choice(philosophers))} on {data.get('concept', random.choice(concepts))} has significant implications for {data.get('term', random.choice(terms))}."
    
    return sentence


def _handle_citation_marker(sentence, context, used_concepts, used_terms, used_philosophers, note_system):
    """
    Replace [citation] placeholders with actual MLA 9 style citation markers.
    """
    # If no [citation] markers, return as is
    if "[citation]" not in sentence:
        return sentence
    
    # Count how many citations we need
    num_citations = sentence.count("[citation]")
    
    # Create enhanced context with title information
    enhanced_context = context.copy() if context else {}
    # [existing context enhancement code]
    
    # For each [citation] placeholder, replace with MLA style citation
    for _ in range(num_citations):
        # Generate a contextually appropriate reference
        reference = _generate_contextual_reference(enhanced_context, used_concepts, used_terms)
        
        # Use add_citation instead of add_to_works_cited to create notes
        citation = note_system.add_citation(reference, enhanced_context)
        
        # Check if [citation] is preceded by a period and fix format if needed
        if ". [citation]" in sentence:
            # Move period after citation: ". [citation]" -> " [citation]."
            sentence = sentence.replace(". [citation]", " [citation].", 1)
        
        # Replace the [citation] placeholder with the actual marker
        sentence = sentence.replace("[citation]", citation, 1)
    
    # Final check for periods before citations: ". (Author)" -> " (Author)."
    sentence = re.sub(r'\.\s+\(([^)]+)\)', r' (\1).', sentence)
    
    return sentence


def _handle_legacy_citation(sentence, all_references, cited_references):
    """
    Handle legacy citation format for backward compatibility.
    
    Args:
        sentence (str): Sentence with [citation] placeholders
        all_references (list): List of all available references
        cited_references (list): List of already cited references
        
    Returns:
        str: Sentence with citation markers
    """
    reference = random.choice(all_references)
    if reference not in cited_references:
        cited_references.append(reference)
    number = cited_references.index(reference) + 1
    citation_text = f"[^{number}]"
    return sentence.replace('[citation]', citation_text)


def _finalize_sentence(sentence):
    """
    Finalize a sentence by cleaning whitespace and ensuring proper punctuation.
    
    Args:
        sentence (str): Raw sentence
        
    Returns:
        str: Cleaned and properly punctuated sentence
    """
    # Remove extra whitespace
    sentence = ' '.join(sentence.split())
    
    # Ensure sentence ends with proper punctuation
    if not sentence.endswith('.') and not sentence.endswith('?') and not sentence.endswith('!'):
        sentence += '.'
    
    return sentence

def _generate_contextual_reference(context, concepts=None, terms=None):
    """
    Generate a reference that is contextually relevant to the concepts and terms being discussed.
    
    Args:
        context (dict): Context information about the current section/paragraph
        concepts (list): Concepts being discussed
        terms (list): Terms being discussed
        
    Returns:
        str: A contextually appropriate reference
    """
    # First, try to use any concepts or terms to create a contextualized reference
    relevant_topics = []
    if concepts:
        relevant_topics.extend(concepts)
    if terms:
        relevant_topics.extend(terms)
    if context and 'concepts' in context:
        relevant_topics.extend(context['concepts'])
    if context and 'terms' in context:
        relevant_topics.extend(context['terms'])
    
    # Pick some topics if available, otherwise use random ones
    topics = random.sample(relevant_topics, min(2, len(relevant_topics))) if relevant_topics else [
        random.choice(concepts) if concepts else random.choice(terms) if terms else "theory"
    ]
    
    # Generate verbs and adjectives for title construction
    verbs = ["Analyzing", "Examining", "Exploring", "Theorizing", "Rethinking", 
            "Deconstructing", "Mapping", "Interrogating", "Situating", "Questioning"]
    
    adjectives = ["Critical", "Radical", "Postmodern", "Deconstructive", "Theoretical",
                "Discursive", "Dialectical", "Phenomenological", "Ontological", "Epistemological"]
    
    # Construct a contextually relevant title
    title_templates = [
        f"{random.choice(verbs)} {topics[0]}: {random.choice(adjectives)} Perspectives",
        f"The {random.choice(adjectives)} Dimensions of {topics[0]}",
        f"{topics[0]} and {topics[1] if len(topics) > 1 else random.choice(concepts+terms)}: Toward a Theory",
        f"Beyond {topics[0]}: Reconsidering {topics[1] if len(topics) > 1 else random.choice(concepts+terms)}",
        f"{random.choice(verbs)} the {random.choice(adjectives)} Implications of {topics[0]}"
    ]
    
    title = random.choice(title_templates)
    
    # Generate author - USING FULL NAMES INSTEAD OF INITIALS
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    
    # MLA 9 style requires full author names, not initials
    author = f"{last_name}, {first_name}"  # Use full first name instead of just an initial
    
    year = random.randint(1950, 2022)
    
    # Generate a synthetic reference based on the context
    sources = ["Journal of Theoretical Studies", "Critical Inquiry", "Theory, Culture & Society",
              "New Literary History", "Cultural Critique", "Diacritics", "boundary 2",
              "Harvard University Press", "MIT Press", "Duke University Press", 
              "Routledge", "Verso Books", "University of Minnesota Press"]
    
    source = random.choice(sources)
    
    # Create MLA 9 style reference
    if "Press" in source:
        # Book format
        # MLA 9: Last, First. Title. Publisher, Year.
        reference = f"{author}. {title}. {source}, {year}."
    else:
        # Journal format
        volume = random.randint(1, 40)
        issue = random.randint(1, 4)
        start_page = random.randint(1, 100)
        end_page = start_page + random.randint(10, 45)
        # MLA 9: Last, First. "Title." Journal Name, vol. Volume, no. Issue, Year, pp. Pages.
        reference = f"{author}. \"{title}.\" {source}, vol. {volume}, no. {issue}, {year}, pp. {start_page}-{end_page}."
    
    return reference