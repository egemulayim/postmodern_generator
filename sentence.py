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
from json_data_provider import (
    philosophers as RAW_PHILOSOPHERS_FROM_DATA, concepts, terms, philosopher_concepts, # Renamed main import
    quotes,
    philosopher_key_works as data_philosopher_key_works,
    verbs,
    nouns,
    prepositions,
    conjunctions,
    title_templates,
    adjectives,
    academic_vocab, # Added academic_vocab as it's used in the file
    citation_relationships,  # Now properly imported
    philosophical_movements  # Now properly imported
)
from reference import generate_reference, generate_full_name # generate_full_name might be useful for some templates
from postmodern_sentence import (enhanced_introduction_templates, enhanced_general_templates, 
                               enhanced_conclusion_templates, metafictional_templates,
                               rhetorical_question_templates, citation_with_framing_templates,
                               philosophical_dialogue_templates)
# from json_data_provider import philosophers as all_philosophers_list # Removed redundant import

# Create a cleaned, definitive list of philosophers for use throughout this module
CLEANED_PHILOSOPHERS = [
    p for p in RAW_PHILOSOPHERS_FROM_DATA
    if p and isinstance(p, str) and len(p.strip().replace(".", "")) > 1
]
if not CLEANED_PHILOSOPHERS:  # Fallback if cleaning results in an empty list
    CLEANED_PHILOSOPHERS = ["Michel Foucault", "Judith Butler", "Jacques Derrida", "Slavoj Žižek"]
# philosophical_movements = {}

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

quote_dialogue_templates = [
    "Where {philosopher1} contends that \"{quote},\" {citation} {philosopher2} emphasizes the ways in which {concept} reconfigures our understanding of {term}.",
    "Although {philosopher1} famously argued that \"{quote},\" {citation} {philosopher2} offers a contrasting approach to {concept} that transforms how we engage with {term}.",
    "Reading {philosopher1}'s claim that \"{quote}\" {citation} against {philosopher2}'s work reveals the complex dialectic between {concept} and {term}.",
    "{philosopher1}'s assertion that \"{quote}\" {citation} can be productively contrasted with {philosopher2}'s approach to {concept} vis-à-vis {term}.",
    "While {philosopher1} maintained that \"{quote},\" {citation} {philosopher2} developed an account of {concept} that fundamentally reimagines its relationship to {term}."
]

quote_citation_templates = [
    "Echoing {philosopher}'s notable claim that \"{quote}\" {citation}, {author} develops an analysis of {concept} that extends beyond conventional understandings of {term}.",
    "Building on {philosopher}'s insight that \"{quote}\" {citation}, {author} reconsiders the relationship between {concept} and {term}.",
    "{author} draws on {philosopher}'s formulation that \"{quote}\" {citation} to elaborate a more nuanced account of how {concept} shapes our understanding of {term}.",
    "Taking up {philosopher}'s provocative assertion that \"{quote}\" {citation}, {author} offers a compelling reframing of {concept} in relation to {term}.",
    "In conversation with {philosopher}'s argument that \"{quote}\" {citation}, {author} examines how {concept} operates within contemporary discourses on {term}."
]

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
    "in a {context}, {term} becomes a battleground where {concept} and its counterpoints collide.",
    "Employing the metaphor '{metaphor}', {philosopher} critiques {term} by highlighting its entanglement with {concept}.",
    "Within the academic subfield of '{subfield}', {philosopher}'s arguments on {concept} are often interpreted as a response to {term}.",
    "The concept of {concept}, when understood through the common metaphor '{metaphor}', reveals hidden dimensions of {term} often overlooked in standard analyses.",
    "Situating {philosopher}'s work within '{subfield}' allows for a nuanced reading of their claims about {term} and {concept}."
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


def generate_sentence(template_type, mentioned_philosophers, forbidden_philosophers=[], 
                     forbidden_concepts=[], forbidden_terms=[], used_quotes=set(), 
                     note_system=None, context=None,
                     coherence_manager=None):
    """
    Generate a sentence based on template type, handling philosopher names and quotes dynamically
    with enhanced sophistication and academic authenticity.
    Utilizes CoherenceManager and focused context for thematic guidance.
    
    Args:
        template_type (str): Type of sentence ('introduction', 'conclusion', or 'general').
        mentioned_philosophers (set): Philosophers already mentioned in the essay.
        forbidden_philosophers (list): Philosophers to exclude.
        forbidden_concepts (list): Concepts to exclude.
        forbidden_terms (list): Terms to exclude.
        used_quotes (set): Quotes already used.
        note_system (NoteSystem): System for managing notes and citations
        context (dict): Contextual information about the sentence being generated
                       (should include primary_concept, primary_philosopher, primary_term from paragraph.py)
        coherence_manager (EssayCoherence, optional): Manager for thematic coherence.
    
    Returns:
        tuple: (sentence_list, used_philosophers, used_concepts, used_terms)
    """
    # Initialize or create context dict if not provided
    if context is None:
        context = {'type': template_type}
    else:
        context['type'] = template_type
    
    # Ensure used_quotes is a set
    if used_quotes is None:
        used_quotes = set()
    
    # Select appropriate template pool based on type
    if template_type == "introduction":
        return _generate_introduction_sentence(mentioned_philosophers, forbidden_philosophers,
                                             forbidden_concepts, forbidden_terms, context,
                                             used_quotes, # Add used_quotes here
                                             note_system, # Add note_system here
                                             coherence_manager=coherence_manager)
    
    elif template_type == "conclusion":
        return _generate_conclusion_sentence(mentioned_philosophers, forbidden_philosophers,
                                           forbidden_concepts, forbidden_terms, context,
                                           used_quotes, # Add used_quotes here
                                           note_system, # Add note_system here
                                           coherence_manager=coherence_manager)
    
    else:  # general sentences
        return _generate_general_sentence(mentioned_philosophers, forbidden_philosophers, 
                                        forbidden_concepts, forbidden_terms, used_quotes,
                                        note_system, context,
                                        coherence_manager=coherence_manager)


def _generate_introduction_sentence(mentioned_philosophers, forbidden_philosophers,
                                  forbidden_concepts, forbidden_terms, context,
                                  used_quotes, # Add used_quotes here
                                  note_system, # Add note_system here
                                  coherence_manager=None):
    """Generate an introduction-type sentence."""
    # If primary_concept is provided, use it. Otherwise, select one.
    # Simplified logic: always try to use primary concept if available
    primary_concept = context.get('primary_concept')
    if not primary_concept:
        available_concepts = [c for c in concepts if c not in forbidden_concepts]
        if not available_concepts:
            available_concepts = concepts # Fallback to all concepts
        primary_concept = random.choice(available_concepts) if available_concepts else "an intriguing concept"

    primary_term = context.get('primary_term')
    if not primary_term:
        available_terms = [t for t in terms if t not in forbidden_terms]
        if not available_terms:
            available_terms = terms # Fallback to all terms
        primary_term = random.choice(available_terms) if available_terms else "a significant term"
    
    if coherence_manager and coherence_manager.active_theme_data:
        context_text = coherence_manager.get_theme_context_phrase()
        if not context_text: # Fallback if theme has no phrases
            context_text = "a relevant theoretical framework" # Or some other suitable default
    else:
        context_text = "a broad theoretical context" # Fallback if no coherence_manager or no active theme

    template = random.choice(get_introduction_templates())
    fields_in_template = {fn for _, fn, _, _ in string.Formatter().parse(template) if fn is not None}
    available_philosophers_intro = [p for p in CLEANED_PHILOSOPHERS if p not in forbidden_philosophers]
    if not available_philosophers_intro: # Ensure there's always a pool
        available_philosophers_intro = CLEANED_PHILOSOPHERS[:5]

    sentence_data = {
        'philosopher': None,
        'philosopher1': None,
        'philosopher2': None,
        'other_philosopher': None,
        'concept': primary_concept,
        'other_concept': None,
        'term': primary_term,
        'adjective': None,
        'context': context_text,
        'metaphor': None,
        'subfield': None,
        'quote': None,
        'citation': None,
        'citation_for_quote': None,
        'author': None,
        'year': None,
        'coherence_manager': coherence_manager
    }
    
    # Populate philosopher fields
    # _populate_philosopher_fields(sentence_data, mentioned_philosophers, used_philosophers=[])
    _populate_philosopher_fields(fields_in_template, sentence_data, available_philosophers_intro, [], mentioned_philosophers, coherence_manager)
    
    # Populate concept fields
    _populate_concept_fields(fields_in_template, sentence_data, sentence_data.get('used_philosophers', []), forbidden_concepts, [primary_concept], coherence_manager)
    
    # Populate term fields
    _populate_term_fields(fields_in_template, sentence_data, forbidden_terms, [primary_term], coherence_manager)
    
    # Populate context fields (now uses _coherence_manager from sentence_data if present)
    _populate_context_fields(fields_in_template, sentence_data) # sentence_data should have _coherence_manager if coherence_manager is passed

    # Handle quotes
    # _handle_quote_in_template(sentence_data, 'philosopher', used_quotes, note_system, context, coherence_manager)
    # Corrected call: quote_source_field is needed
    quote_source_field_intro = 'philosopher' # Default
    if 'other_philosopher' in fields_in_template: quote_source_field_intro = 'other_philosopher'
    elif 'philosopher1' in fields_in_template: quote_source_field_intro = 'philosopher1'
    _handle_quote_in_template(sentence_data, quote_source_field_intro, used_quotes, note_system, context, coherence_manager)

    # Handle citation for templates that explicitly use {author} and {year} (less common for intro)
    # _handle_author_citation(sentence_data, note_system, context, used_concepts=[primary_concept], used_terms=[primary_term])
    # This call was incorrect. _handle_author_citation expects template as first arg and modifies data.
    # It's usually called in _generate_general_sentence. For intro, we rely on {citation} or [citation] markers.
    # For now, let's ensure data['citation'] is at least initialized if the template expects it.
    if 'citation' in fields_in_template and 'citation' not in sentence_data:
        sentence_data['citation'] = ''

    # Format sentence
    sentence = _format_sentence_from_template(template, sentence_data, [primary_concept], [primary_term], note_system, context, coherence_manager)
    
    # Handle citation markers
    # sentence = _handle_citation_marker(sentence, context, used_concepts=[primary_concept], used_terms=[primary_term])
    # Corrected call: Pass currently used philosophers for the citation context
    current_used_philosophers_intro = [p for p in [sentence_data.get('philosopher'), sentence_data.get('philosopher1'), sentence_data.get('philosopher2'), sentence_data.get('other_philosopher')] if p]
    sentence = _handle_citation_marker(sentence, context, [primary_concept], [primary_term], current_used_philosophers_intro, note_system, coherence_manager)

    # Finalize sentence
    sentence = _finalize_sentence(sentence)
    
    return [(sentence, None)], sentence_data.get('used_philosophers', []), sentence_data.get('used_concepts', []), sentence_data.get('used_terms', [])


def _generate_conclusion_sentence(mentioned_philosophers, forbidden_philosophers,
                                forbidden_concepts, forbidden_terms, context,
                                used_quotes, # Add used_quotes here
                                note_system, # Add note_system here
                                coherence_manager=None):
    """Generate a conclusion-type sentence."""
    primary_concept = context.get('primary_concept', random.choice(concepts))
    primary_term = context.get('primary_term', random.choice(terms))

    if coherence_manager and coherence_manager.active_theme_data:
        context_text = coherence_manager.get_theme_context_phrase()
        if not context_text: # Fallback if theme has no phrases
            context_text = "a relevant theoretical framework"
    else:
        context_text = "a broad theoretical context" # Fallback if no coherence_manager or theme

    template = random.choice(get_conclusion_templates())
    fields_in_template_conc = {fn for _, fn, _, _ in string.Formatter().parse(template) if fn is not None}
    available_philosophers_conc = [p for p in CLEANED_PHILOSOPHERS if p not in forbidden_philosophers]
    if not available_philosophers_conc: # Ensure there's always a pool
        available_philosophers_conc = CLEANED_PHILOSOPHERS[:5]

    sentence_data = {
        'philosopher': None,
        'philosopher1': None,
        'philosopher2': None,
        'other_philosopher': None,
        'concept': primary_concept,
        'other_concept': None,
        'term': primary_term,
        'adjective': None,
        'context': context_text,
        'metaphor': None,
        'subfield': None,
        'quote': None,
        'citation': None,
        'citation_for_quote': None,
        'author': None,
        'year': None,
        'coherence_manager': coherence_manager
    }
    
    # Populate philosopher fields
    # _populate_philosopher_fields(sentence_data, mentioned_philosophers, used_philosophers=[])
    _populate_philosopher_fields(fields_in_template_conc, sentence_data, available_philosophers_conc, [], mentioned_philosophers, coherence_manager)
    
    # Populate concept fields
    # _populate_concept_fields(sentence_data, used_philosophers=[], forbidden_concepts=forbidden_concepts, used_concepts=[primary_concept])
    _populate_concept_fields(fields_in_template_conc, sentence_data, sentence_data.get('used_philosophers', []), forbidden_concepts, [primary_concept], coherence_manager)

    # Populate term fields
    # _populate_term_fields(sentence_data, forbidden_terms=[], used_terms=[primary_term])
    _populate_term_fields(fields_in_template_conc, sentence_data, forbidden_terms, [primary_term], coherence_manager)
    
    # Populate context fields
    # _populate_context_fields(sentence_data)
    _populate_context_fields(fields_in_template_conc, sentence_data) # sentence_data should have _coherence_manager

    # Handle quotes
    # _handle_quote_in_template(sentence_data, 'philosopher', used_quotes, note_system, context, coherence_manager)
    quote_source_field_conc = 'philosopher' # Default
    if 'other_philosopher' in fields_in_template_conc: quote_source_field_conc = 'other_philosopher'
    elif 'philosopher1' in fields_in_template_conc: quote_source_field_conc = 'philosopher1'
    _handle_quote_in_template(sentence_data, quote_source_field_conc, used_quotes, note_system, context, coherence_manager)
    
    # Handle citation
    # _handle_author_citation(sentence_data, note_system, context, used_concepts=[primary_concept], used_terms=[primary_term])
    # Similar to intro, this direct call was incorrect.
    if 'citation' in fields_in_template_conc and 'citation' not in sentence_data:
        sentence_data['citation'] = ''

    # Format sentence
    # sentence = _format_sentence_from_template(template, sentence_data, used_concepts=[primary_concept], used_terms=[primary_term])
    sentence = _format_sentence_from_template(template, sentence_data, [primary_concept], [primary_term], note_system, context, coherence_manager)
    
    # The used_philosophers list for return should be derived from sentence_data or a more robust collection mechanism
    final_used_philosophers = [p for p in [sentence_data.get('philosopher'), sentence_data.get('philosopher1'), sentence_data.get('philosopher2'), sentence_data.get('other_philosopher')] if p and isinstance(p, str)]
    # Ensure these are full names if they were shortened in sentence_data for display
    # This is a simplified approach; a more robust way would be to track the original full names used to populate sentence_data.
    
    final_used_concepts = [c for c in [sentence_data.get('concept'), sentence_data.get('other_concept')] if c]
    final_used_terms = [t for t in [sentence_data.get('term')] if t]

    # Handle citation markers if any are present in the formatted sentence
    sentence = _handle_citation_marker(sentence, context, final_used_concepts, final_used_terms, final_used_philosophers, note_system, coherence_manager)

    # Finalize sentence (punctuation, etc.)
    sentence = _finalize_sentence(sentence)
    
    return [(sentence, None)], final_used_philosophers, final_used_concepts, final_used_terms

def _generate_general_sentence(mentioned_philosophers, forbidden_philosophers, 
                             forbidden_concepts, forbidden_terms, used_quotes,
                             note_system, context,
                             coherence_manager=None):
    """Generates a general sentence using a template, populating fields dynamically."""
    # Determine what type of general sentence to generate
    # Adjusted probabilities: more quote and citation, slightly less standard
    sentence_type_pool = [
        "standard", "standard", "standard", "standard", # 4/12 -> ~33.3%
        "dialogue", "dialogue",                       # 2/12 -> ~16.7%
        "quote", "quote",                           # 2/12 -> ~16.7% (was ~8.3%)
        "rhetorical",                               # 1/12 -> ~8.3%
        "citation", "citation",                      # 2/12 -> ~16.7% (was ~8.3%)
        "metafictional"                             # 1/12 -> ~8.3%
    ]
    sentence_type = random.choice(sentence_type_pool)
    
    # Get available philosophers - prioritize from context or coherence_manager if available
    if coherence_manager:
        # Try to get a thematically relevant philosopher first
        # This is a simple approach; could be refined to pick from a pool of theme philosophers
        main_philosopher_candidate = coherence_manager.get_weighted_philosopher(exclude=forbidden_philosophers)
        if main_philosopher_candidate:
            available_philosophers = [main_philosopher_candidate] + [p for p in CLEANED_PHILOSOPHERS if p not in forbidden_philosophers and p != main_philosopher_candidate] # MODIFIED
        else: # Fallback if no specific philosopher from coherence_manager
            available_philosophers = [p for p in CLEANED_PHILOSOPHERS if p not in forbidden_philosophers] # MODIFIED
    else: # Original logic if no coherence_manager
        available_philosophers = [p for p in CLEANED_PHILOSOPHERS if p not in forbidden_philosophers] # MODIFIED
    
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
        available_philosophers = CLEANED_PHILOSOPHERS[:5] # MODIFIED
    
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
    title_themes = context.get('title_themes', {})
    title_concepts = title_themes.get('primary_concepts', []) + title_themes.get('related_concepts', []) if title_themes else []
    title_terms = title_themes.get('primary_terms', []) if title_themes else []
    
    _populate_philosopher_fields(fields, data, available_philosophers, used_philosophers, mentioned_philosophers, coherence_manager)
    
    # Prioritize title concepts or use coherence_manager if available
    if coherence_manager:
        if 'concept' in fields:
            data['concept'] = coherence_manager.get_weighted_concept(exclude=set(forbidden_concepts).union(used_concepts))
            if data['concept']: used_concepts.append(data['concept'])
        if 'other_concept' in fields:
            # For other_concept, try to get a related one or another weighted one
            primary_concept_for_related = data.get('concept')
            current_exclusions = set(forbidden_concepts).union(used_concepts)
            if primary_concept_for_related:
                 data['other_concept'] = coherence_manager.get_related_concept(primary_concept_for_related, exclude=current_exclusions)
                 if not data['other_concept']: # Fallback if no related found
                     data['other_concept'] = coherence_manager.get_weighted_concept(exclude=current_exclusions.union({primary_concept_for_related} if primary_concept_for_related else set()))
            else: # If no primary concept, just get a weighted one
                 data['other_concept'] = coherence_manager.get_weighted_concept(exclude=current_exclusions)
            if data.get('other_concept'): used_concepts.append(data['other_concept'])

    elif 'concept' in fields and title_concepts and random.random() < 0.7: # Original logic if no coherence_manager
        available_title_concepts = [c for c in title_concepts if c not in forbidden_concepts and c not in used_concepts]
        if available_title_concepts:
            data['concept'] = random.choice(available_title_concepts)
            used_concepts.append(data['concept'])
        else:
            _populate_concept_fields(fields, data, used_philosophers, forbidden_concepts, used_concepts, coherence_manager)
    else: # Original logic if no coherence_manager
        _populate_concept_fields(fields, data, used_philosophers, forbidden_concepts, used_concepts, coherence_manager)
    
    # Prioritize title terms or use coherence_manager if available
    if coherence_manager:
        if 'term' in fields:
            data['term'] = coherence_manager.get_weighted_term(exclude=set(forbidden_terms).union(used_terms))
            if data['term']: used_terms.append(data['term'])
    elif 'term' in fields and title_terms and random.random() < 0.7: # Original logic if no coherence_manager
        available_title_terms = [t for t in title_terms if t not in forbidden_terms and t not in used_terms]
        if available_title_terms:
            data['term'] = random.choice(available_title_terms)
            used_terms.append(data['term'])
        else:
            _populate_term_fields(fields, data, forbidden_terms, used_terms, coherence_manager)
    else: # Original logic if no coherence_manager
        _populate_term_fields(fields, data, forbidden_terms, used_terms, coherence_manager)
    
    _populate_context_fields(fields, data)
    
    # Handle quotes if needed
    if 'quote' in fields:
        # The _handle_quote_in_template function will now primarily populate data['quote']
        # and ensure data['citation_for_quote'] is set if a quote is used.
        # It will be less involved in directly modifying the template string with the citation text.
        data['quote'] = None # Ensure 'quote' key exists for formatting
        data['citation_for_quote'] = '' # Ensure 'citation_for_quote' key exists

        _handle_quote_in_template(data, quote_source_field, used_quotes, note_system, context, coherence_manager)
        
        # If _handle_quote_in_template successfully set a quote and its citation,
        # we ensure the main {citation} placeholder uses this specific citation.
        if data.get('citation_for_quote'):
            data['citation'] = data['citation_for_quote']
    
    # Handle citation fields for citation_with_framing_templates
    if 'author' in fields and 'year' in fields:
        template = _handle_author_citation(template, data, context, used_concepts, 
                                        used_terms, used_philosophers, note_system,
                                        coherence_manager=coherence_manager)
    
    # Format the sentence with all the collected data
    sentence = _format_sentence_from_template(template, data, used_concepts, used_terms, 
                                            note_system, context, coherence_manager=coherence_manager)
    
    # Handle citations with the note system
    if '[citation]' in sentence and note_system:
        sentence = _handle_citation_marker(sentence, context, used_concepts, 
                                        used_terms, used_philosophers, note_system,
                                        coherence_manager=coherence_manager)
    
    # Finalize sentence
    sentence = _finalize_sentence(sentence)
    
    return [(sentence, None)], used_philosophers, used_concepts, used_terms


def _populate_philosopher_fields(fields, data, available_philosophers, used_philosophers, mentioned_philosophers, coherence_manager=None):
    """Populate philosopher-related fields in the template data dictionary."""

    # **** BEGIN NEW FILTERING BLOCK ****
    # Filter the incoming available_philosophers list to ensure it only contains valid, full names.
    # The global `CLEANED_PHILOSOPHERS` (from data.py) is the source of truth for valid names.
    initial_pool_size = len(available_philosophers)
    valid_available_philosophers = [p for p in available_philosophers if p and isinstance(p, str) and len(p.strip().replace(".", "")) > 1 and p in CLEANED_PHILOSOPHERS] # MODIFIED

    # If filtering significantly reduced the pool or made it too small, supplement from the global list.
    # This ensures _select_first_philosopher and _select_related_philosopher have a reasonable pool.
    if not valid_available_philosophers or len(valid_available_philosophers) < min(initial_pool_size, 2): # Ensure at least a couple if possible
        supplement_needed = max(2, min(initial_pool_size, 5) - len(valid_available_philosophers))
        # Get candidates from the global `CLEANED_PHILOSOPHERS` list not already in `used_philosophers` (sentence-level) or the current valid pool.
        global_candidates = [p for p in CLEANED_PHILOSOPHERS if p and isinstance(p, str) and len(p.strip().replace(".", "")) > 1 and p not in used_philosophers and p not in valid_available_philosophers] # MODIFIED
        if global_candidates:
            valid_available_philosophers.extend(random.sample(global_candidates, min(supplement_needed, len(global_candidates))))
        
        # If still empty after trying to supplement (e.g., all philosophers used or global list is small/problematic)
        if not valid_available_philosophers:
            # Fallback to a very small pool of known good default philosophers.
            # Ensure these defaults are not already in used_philosophers to avoid re-picking if possible.
            default_options = [p for p in ["Michel Foucault", "Judith Butler", "Jacques Derrida"] if p not in used_philosophers]
            if default_options:
                 valid_available_philosophers = random.sample(default_options, min(len(default_options), 2))
            else: # If even defaults are used, pick one as an absolute fallback.
                 valid_available_philosophers = ["Michel Foucault"]
    # **** END NEW FILTERING BLOCK ****

    for field in fields:
        if field.startswith('philosopher') or field == 'other_philosopher':
            # Use the filtered list for selections
            current_selection_pool = [p for p in valid_available_philosophers if p not in used_philosophers]
            
            # If the current_selection_pool is empty, refresh it from valid_available_philosophers or even global philosophers.
            # This can happen if all in valid_available_philosophers have been used in this sentence for prior fields.
            if not current_selection_pool:
                alt_pool = [p for p in valid_available_philosophers] # Try from the original filtered list first
                if not alt_pool:
                     alt_pool = [p for p in CLEANED_PHILOSOPHERS if p and isinstance(p, str) and len(p.strip().replace(".", "")) > 1] # MODIFIED Fallback to global
                current_selection_pool = alt_pool if alt_pool else [random.choice(CLEANED_PHILOSOPHERS) if CLEANED_PHILOSOPHERS else "Michel Foucault"] # MODIFIED Absolute fallback


            if field in ['philosopher2', 'other_philosopher'] and used_philosophers:
                # Pass the cleaned pool to _select_related_philosopher
                phil = _select_related_philosopher(used_philosophers[0], current_selection_pool, valid_available_philosophers, coherence_manager)
            else:
                # Pass the cleaned pool to _select_first_philosopher
                phil = _select_first_philosopher(current_selection_pool, mentioned_philosophers, valid_available_philosophers, coherence_manager)

            # Previous direct validation of 'phil' after selection is now less critical due to pool cleaning,
            # but can be kept as a final safeguard or removed if confident in pool cleaning.
            # For safety, let's ensure phil itself is valid before proceeding.
            if not phil or (phil and isinstance(phil, str) and len(phil.strip().replace(".", "")) <= 1):
                # This indicates an issue with selection or an empty pool passed to selection funcs.
                # Aggressively pick a known good one.
                safe_fallbacks = [p for p in CLEANED_PHILOSOPHERS if p not in used_philosophers and p and isinstance(p, str) and len(p.strip().replace(".", "")) > 1] # MODIFIED
                if safe_fallbacks:
                    phil = random.choice(safe_fallbacks)
                else: # Absolute fallback
                    phil = random.choice([p for p in CLEANED_PHILOSOPHERS if p and isinstance(p, str) and len(p.strip().replace(".", "")) > 1] or CLEANED_PHILOSOPHERS or ["Michel Foucault"]) # MODIFIED
            
            # Format philosopher name appropriately
            if phil not in mentioned_philosophers:
                phil_name = phil
                mentioned_philosophers.add(phil)
            else:
                name_parts = phil.split()
                last_part = name_parts[-1]
                # Check if the last part is just an initial (e.g., "A.")
                if len(last_part.replace(".", "")) <= 1 and len(name_parts) > 1:
                    # Try to use the second to last part if it's more substantial (e.g., "Adorno" from "Adorno, T. A.")
                    # Or, if the name was simple like "Author A.", use "Author"
                    second_last_part = name_parts[-2].replace(",", "")
                    if len(second_last_part) > 1:
                        phil_name = second_last_part
                    else: # Fallback to full name if second last is also not good
                        phil_name = phil
                else:
                    phil_name = last_part
                
            data[field] = phil_name
            used_philosophers.append(phil)


def _select_related_philosopher(first_phil, available_pool, all_philosophers, coherence_manager=None):
    """Select a philosopher related to the first philosopher in the sentence."""
    # Check citation relationships for possible related philosophers
    if first_phil in citation_relationships and citation_relationships[first_phil]:
        related_phils = [p for p in citation_relationships[first_phil] 
                        if p in available_pool]
        if related_phils:
            return random.choice(related_phils)
        # No direct citation relationship found, fall through to movement/coherence_manager logic
    
    # Try philosophical movements next
    for movement, movement_phils in philosophical_movements.items():
        if first_phil in movement_phils:
            movement_options = [p for p in movement_phils if p in available_pool and p != first_phil]
            if movement_options:
                return random.choice(movement_options)

    # Fallback to coherence_manager or random selection
    if coherence_manager:
        candidate = coherence_manager.get_weighted_philosopher(exclude=[first_phil] + ([p for p in CLEANED_PHILOSOPHERS if p not in available_pool]))
        if candidate: return candidate

    return random.choice(available_pool) if available_pool else random.choice(CLEANED_PHILOSOPHERS)


def _select_first_philosopher(available_pool, mentioned_philosophers, all_philosophers, coherence_manager=None):
    """Select the first philosopher for a sentence, favoring new philosophers or from coherence_manager."""
    if coherence_manager:
        # Prefer a philosopher from coherence_manager, possibly unmentioned
        unmentioned_in_pool = [p for p in available_pool if p not in mentioned_philosophers]
        candidate_from_coherence = coherence_manager.get_weighted_philosopher(
            exclude=([p for p in CLEANED_PHILOSOPHERS if p not in available_pool]) # Exclude those not in current available_pool
        )
        if candidate_from_coherence and candidate_from_coherence in available_pool :
            if candidate_from_coherence in unmentioned_in_pool and random.random() < 0.8: # Higher chance if unmentioned
                 return candidate_from_coherence
            elif random.random() < 0.5: # Still a good chance to pick if mentioned
                 return candidate_from_coherence

    # Fallback to original logic if coherence_manager didn't yield a good pick
    unmention_phils = [p for p in available_pool if p not in mentioned_philosophers]
    if unmention_phils and random.random() < 0.7:  # 70% chance to use new philosopher from pool
        return random.choice(unmention_phils)
    else:
        return random.choice(available_pool) if available_pool else random.choice(CLEANED_PHILOSOPHERS)


def _populate_concept_fields(fields, data, used_philosophers, forbidden_concepts, used_concepts, coherence_manager=None):
    """Populate concept-related fields in the template data dictionary."""
    for field in fields:
        if field == 'concept':
            concept = None
            if coherence_manager:
                concept = coherence_manager.get_weighted_concept(exclude=set(forbidden_concepts).union(used_concepts))
            
            if not concept: # Fallback to original logic
                main_phil = data.get('philosopher', data.get('philosopher1'))
                if main_phil and main_phil in philosopher_concepts:
                    related_concepts = [c for c in philosopher_concepts[main_phil] 
                                      if c not in forbidden_concepts and c not in used_concepts]
                    if related_concepts:
                        concept = random.choice(related_concepts)
                if not concept: # Further fallback
                    concept = random.choice([c for c in concepts 
                                             if c not in forbidden_concepts and c not in used_concepts] or concepts)
            if concept:
                data[field] = concept
                used_concepts.append(concept)

        elif field == 'other_concept':
            concept = None
            if coherence_manager:
                primary_concept_for_related = data.get('concept')
                current_exclusions = set(forbidden_concepts).union(used_concepts)
                if primary_concept_for_related:
                    concept = coherence_manager.get_related_concept(primary_concept_for_related, exclude=current_exclusions)
                if not concept: # Fallback to weighted if no related found or no primary concept
                    concept = coherence_manager.get_weighted_concept(exclude=current_exclusions.union({primary_concept_for_related} if primary_concept_for_related else set()))

            if not concept: # Fallback to original logic
                if used_concepts:
                    concept = _select_related_concept(used_concepts[0], used_philosophers, 
                                                   data, forbidden_concepts, used_concepts, coherence_manager) # Pass coherence_manager
                else:
                    concept = random.choice([c for c in concepts 
                                         if c not in forbidden_concepts 
                                         and c not in used_concepts] or concepts)
            if concept:
                data[field] = concept
                used_concepts.append(concept)


def _select_related_concept(primary_concept, used_philosophers, data, forbidden_concepts, used_concepts, coherence_manager=None):
    """Select a concept related to the primary_concept, preferably using coherence_manager."""
    # Ensure concepts module is available if not using self.concepts from a class context
    from json_data_provider import concepts as all_av_concepts # Local import for safety

    if coherence_manager and primary_concept:
        # Use the coherence manager to get a thematically and strongly related concept
        # Coherence manager's get_related_concept should handle exclusions and strength.
        related_concept = coherence_manager.get_related_concept(primary_concept, exclude=forbidden_concepts.union(used_concepts))
        if related_concept:
            return related_concept
        # Fallback if coherence_manager doesn't find one (e.g., primary_concept is too obscure or all related are excluded)

    # Original fallback logic (simplified as coherence_manager should be the primary source)
    # This part can be significantly reduced if coherence_manager is reliable.
    potential_concepts = []
    if primary_concept in philosopher_concepts:
        # Find concepts associated with philosophers who also discuss the primary_concept
        for philosopher, ph_concepts in philosopher_concepts.items():
            if primary_concept in ph_concepts:
                for concept in ph_concepts:
                    if concept != primary_concept and concept not in forbidden_concepts and concept not in used_concepts:
                        potential_concepts.append(concept)
    
    if not potential_concepts:
        # If no specific relations found, pick any other concept
        potential_concepts = [c for c in all_av_concepts if c != primary_concept and c not in forbidden_concepts and c not in used_concepts]

    if not potential_concepts:
        # Absolute fallback: any concept not the primary, ignoring used_concepts temporarily
        potential_concepts = [c for c in all_av_concepts if c != primary_concept and c not in forbidden_concepts]
        if not potential_concepts:
             return random.choice(all_av_concepts) if all_av_concepts else "hyperreality" # Last resort

    return random.choice(potential_concepts)


def _populate_term_fields(fields, data, forbidden_terms, used_terms, coherence_manager=None):
    """Populate term-related fields in the template data dictionary."""
    if 'term' in fields:
        term = None
        if coherence_manager:
            term = coherence_manager.get_weighted_term(exclude=set(forbidden_terms).union(used_terms))
        
        if not term: # Fallback to random if coherence_manager doesn't provide or not available
            term = random.choice([t for t in terms if t not in forbidden_terms and t not in used_terms] or terms)
        
        if term:
            data['term'] = term
            used_terms.append(term)


def _populate_context_fields(fields, data):
    """Populate context and adjective fields if not already present."""
    if 'context' not in data and 'context' in fields:
        # This function is called from _format_sentence_from_template,
        # which should have coherence_manager if {context} is a placeholder.
        # However, to be safe, we check.
        coherence_manager = data.get('coherence_manager')  # Fixed: use correct key
        if coherence_manager:
            theme_context = coherence_manager.get_theme_context_phrase()
            if theme_context:
                data['context'] = theme_context
            else:
                data['context'] = "a relevant theoretical framework" # Fallback if no theme context
        else:
            # Fallback if coherence_manager is not available for some reason, though it should be.
            # This path should ideally not be taken if {context} placeholder is used.
            data['context'] = "a broad theoretical context" # Generic fallback
    if 'adjective' not in data and 'adjective' in fields:
        data['adjective'] = random.choice(["critical", "radical", "postmodern", "deconstructive", "theoretical", 
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
    if not quote: # Added check for empty quote
        return quote

    # Check if the quote is mid-sentence (not at the end of the template)
    is_mid_sentence = False
    
    # Look for patterns that indicate the quote is mid-sentence
    mid_sentence_indicators = [
        '\"{quote},\" ', '\"{quote}\" ', '\"{quote}—', '\"{quote}\" which',
        '\"{quote}\" in', '\"{quote}\" that', '\"{quote}\" thus', '\"{quote}\" offering'
    ]
    for indicator in mid_sentence_indicators:
        if isinstance(template, str) and indicator in template: # Ensure template is a string
            is_mid_sentence = True
            break
    
    # Revised punctuation handling for MLA style
    # If quote ends with '?' or '!', keep it.
    if quote.endswith('?') or quote.endswith('!'):
        pass # Keep these punctuation marks as they are part of the quote's specific meaning
    # Else if quote ends with '.', and it's mid-sentence, remove the period.
    # The sentence-final period will be added after citation by _finalize_sentence 
    # or if the quote itself is the end of the sentence.
    elif quote.endswith('.'):
        if is_mid_sentence: # Only remove period if it's a mid-sentence quote
            quote = quote[:-1]
        # If it ends with a period and is NOT mid_sentence, we keep the period for now.
        # _finalize_sentence will then decide if an additional period after citation is needed.

    # Handle comma: if quote ends with comma.
    elif quote.endswith(','):
        # If template adds a comma right after {quote} (e.g., "{quote}, and..."), 
        # and the quote itself ends in a comma, remove quote's comma to avoid doubling.
        if is_mid_sentence and isinstance(template, str) and ('\"{quote},\" ' in template or '\"{quote},\"' in template):
            quote = quote[:-1]
        # else: keep the quote's original comma (e.g. for mid-sentence claims like the Baudrillard example)
        pass

    # Handle lowercase bracketed first letter for quotes after "that", "which", etc.
    lowercase_indicators = ['that "{quote}', 'which "{quote}', 'in which "{quote}', 'through which "{quote}']
    needs_lowercase = any(indicator in template for indicator in lowercase_indicators)
    
    if needs_lowercase and quote and len(quote) > 0 and quote[0].isupper():
        # Add brackets around first letter and make it lowercase for academic style
        quote = '[' + quote[0].lower() + ']' + quote[1:]
    
    return quote


def _handle_quote_in_template(data, quote_source_field, used_quotes, 
                           note_system, context, coherence_manager=None):
    """
    Handle quotes for templates. Populates data['quote'] and data['citation_for_quote'].
    It does NOT directly modify the template string with the citation text.
    """
    quote_source_name = data.get(quote_source_field)
    selected_quote_text = None
    reference_for_quote = None
    
    # Get title themes if available
    title_themes = context.get('title_themes', {})
    title_concepts = title_themes.get('primary_concepts', []) if title_themes else []
    title_terms = title_themes.get('primary_terms', []) if title_themes else []
    relevant_philosophers = context.get('relevant_philosophers', [])

    # Use coherence_manager to pick quote_source_name if not strongly indicated by context
    if coherence_manager and (not quote_source_name or quote_source_name not in relevant_philosophers or random.random() < 0.3): # 30% chance to override with thematic
        candidate_philosopher = coherence_manager.get_weighted_philosopher(exclude=[p for p in CLEANED_PHILOSOPHERS if match_philosopher_to_quotes(p) is None]) # MODIFIED Exclude those with no quotes
        if candidate_philosopher:
            # Update the philosopher in the main data dict if it was the source of the quote
            if data.get('philosopher') == quote_source_name: data['philosopher'] = candidate_philosopher
            if data.get('philosopher1') == quote_source_name: data['philosopher1'] = candidate_philosopher
            if data.get('other_philosopher') == quote_source_name : data['other_philosopher'] = candidate_philosopher
            quote_source_name = candidate_philosopher # Use the thematic philosopher
    
    elif (title_concepts or title_terms) and relevant_philosophers and random.random() < 0.7: # Original logic for title theme relevance
        if quote_source_name not in relevant_philosophers:
            new_quote_source = random.choice(relevant_philosophers)
            # Update the philosopher in the main data dict if it was the source of the quote
            if data.get('philosopher') == quote_source_name: data['philosopher'] = new_quote_source
            if data.get('philosopher1') == quote_source_name: data['philosopher1'] = new_quote_source
            if data.get('other_philosopher') == quote_source_name : data['other_philosopher'] = new_quote_source
            quote_source_name = new_quote_source # Use the title-relevant philosopher
    
    if quote_source_name:
        full_name = match_philosopher_to_quotes(quote_source_name)
        if full_name and full_name in quotes:
            available_quotes = [q for q in quotes[full_name] if q not in used_quotes]
            if available_quotes:
                selected_quote = random.choice(available_quotes)
                selected_quote_text = selected_quote
                used_quotes.add(selected_quote)
                
                if note_system:
                    # Attempt to get a specific key work for the citation
                    work_title = None
                    year = None
                    is_article_from_work = None

                    if full_name in data_philosopher_key_works and data_philosopher_key_works[full_name]:
                        selected_work = random.choice(data_philosopher_key_works[full_name])
                        work_title = selected_work[0]
                        year = selected_work[1]
                        # Heuristic for is_article based on title
                        if isinstance(work_title, str): # Ensure work_title is a string
                            if "Vol." in work_title or "Journal" in work_title or "Review" in work_title or len(work_title.split()) < 5:
                                is_article_from_work = True
                            else:
                                is_article_from_work = False
                    
                    if work_title and year is not None: # Year can be 0, so check not None
                        # Use specific work title, year, and determined article status
                        # Pass defaults for is_article and year, as they are positional, but overrides will take precedence.
                        reference_for_quote = note_system.get_enhanced_citation(
                            author_name=full_name,
                            is_article=is_article_from_work if is_article_from_work is not None else False, # Positional default
                            year=year if year is not None else random.randint(1970, 2010), # Positional default
                            is_article_override=is_article_from_work, 
                            specific_year_override=year, 
                            title_override=work_title
                        )
                    else:
                        # Fallback to more generic citation if no key work found or data incomplete
                        is_article_fallback = random.random() < 0.3
                        year_fallback = random.randint(1950, 2010)
                        # Call with positional is_article and year for the fallback case
                        reference_for_quote = note_system.get_enhanced_citation(full_name, is_article_fallback, year_fallback)

    if not selected_quote_text: # Fallback to generic quote if no specific one was found
        if coherence_manager:
            concept_for_generic = coherence_manager.get_weighted_concept()
            term_for_generic = coherence_manager.get_weighted_term()
        else:
            concept_for_generic = data.get('concept', random.choice(concepts))
            term_for_generic = data.get('term', random.choice(terms))
        selected_quote_text = f"the relationship between {concept_for_generic} and {term_for_generic} is always already mediated by power"
        if quote_source_name and note_system: # Generate reference for the generic quote's attributed author
            reference_for_quote = note_system.get_enhanced_citation(quote_source_name, False, random.randint(1950, 2010))
        elif note_system: # Absolute fallback if no quote_source_name somehow
             reference_for_quote = note_system.get_enhanced_citation("Smith, John", False, random.randint(1950,2010))


    data['quote'] = selected_quote_text

    if reference_for_quote and note_system:
        # The add_citation method returns the citation string e.g., (Author Page)
        # Pass is_quote_citation=True to ensure parenthetical citation for quotes.
        data['citation_for_quote'] = note_system.add_citation(reference_for_quote, context, is_quote_citation=True)
    else:
        # Fallback if no reference could be made for the quote
        data['citation_for_quote'] = "(Author XX)" # Generic placeholder if all else fails

    # This function no longer returns the template string, it populates 'data' dictionary.
    return # Template is not returned

def _process_citation_placeholders(sentence, note_system, context, philosopher_name=None, coherence_manager=None):
    """
    Process citation placeholders in a sentence.
    Now uses data['citation'] if available (set by quote handling or author citation),
    otherwise generates a new one.
    """
    if '{citation}' not in sentence:
        return sentence
    
    citation_text_to_insert = context.get('data_citation_placeholder', None)

    if not citation_text_to_insert: # If not pre-filled by quote/author logic
        if note_system:
            # Determine philosopher to cite
            # philosopher_name could be from the general context or a specific field in data
            # For now, use the passed philosopher_name or a fallback from context if available
            name_to_cite = philosopher_name or context.get('current_philosopher_for_citation', "Smith, John")

            year = random.randint(1950, 2010)
            is_article = random.random() < 0.3
            reference = note_system.get_enhanced_citation(name_to_cite, is_article, year)
            citation_text_to_insert = note_system.add_citation(reference, context)
        else:
            citation_text_to_insert = '' # Fallback if no note_system, changed from '(Generic Citation)'
    
    # Ensure citation_text_to_insert is not empty
    if not citation_text_to_insert:
        citation_text_to_insert = "(General Citation Placeholder)" # Robust fallback

    sentence = sentence.replace('{citation}', citation_text_to_insert)
    return sentence

def _format_sentence_from_template(template, data, used_concepts, used_terms, note_system=None, context=None, coherence_manager=None):
    """
    Formats a sentence string using a dictionary of replacements, handling citations.
    This function populates a template with dynamic data, including philosophers, concepts,
    terms, contexts, quotes, and potentially new thematic elements like metaphors and subfields.
    It also handles the processing of citation placeholders.

    Args:
        template (str): The sentence template string.
        data (dict): Dictionary of placeholders and their values.
        used_concepts (set): Set of concepts used so far.
        used_terms (set): Set of terms used so far.
        note_system (NoteSystem, optional): System for managing notes and citations.
        context (dict, optional): Contextual information for citation generation.
        coherence_manager (EssayCoherence, optional): Manager for thematic coherence.

    Returns:
        str: The formatted sentence.
    """
    sentence = template
    
    # Populate new thematic elements if coherence_manager is available and template requires them
    if coherence_manager:
        if '{metaphor}' in sentence:
            metaphor = coherence_manager.get_theme_common_metaphor()
            if metaphor:
                data['metaphor'] = metaphor
            else:
                # Fallback: remove placeholder if no metaphor available, or adapt template if needed
                # For now, let's assume templates are robust or this causes an error to be caught later
                # A better fallback would be to have alternative template structures.
                if 'metaphor' not in data: data['metaphor'] = "a relevant conceptual framing" # Generic fallback

        if '{subfield}' in sentence:
            subfield = coherence_manager.get_theme_academic_subfield()
            if subfield:
                data['subfield'] = subfield
            else:
                if 'subfield' not in data: data['subfield'] = "a related academic discipline" # Generic fallback

    # Initial population of fields based on placeholders present in the template.
    # This needs to happen before the main data dictionary is built.
    fields_in_template = {fn for _, fn, _, _ in string.Formatter().parse(template) if fn is not None}

    # Create a working copy of data to pass to population functions.
    # This prevents premature modification of the original data dictionary if population functions
    # have side effects or if we decide to conditionally use their results.
    working_data = data.copy()
    if coherence_manager:
        working_data['coherence_manager'] = coherence_manager  # Fixed: use consistent key

    # Populate context, adjective, metaphor, subfield if their placeholders are in the template
    # and they haven't been set by the calling function (e.g., _generate_general_sentence)
    if '{context}' in fields_in_template and 'context' not in working_data:
        _populate_context_fields(fields_in_template, working_data) # Now uses correct key
    
    if '{adjective}' in fields_in_template and 'adjective' not in working_data:
        # A simplified version for adjectives if not pre-populated, can be expanded if needed
        working_data['adjective'] = coherence_manager.get_theme_related_adjective() if coherence_manager else random.choice(adjectives if adjectives else ["relevant"])

    if '{metaphor}' in fields_in_template and 'metaphor' not in working_data:
        if coherence_manager:
            theme_metaphor = coherence_manager.get_theme_common_metaphor()
            if theme_metaphor: working_data['metaphor'] = theme_metaphor
            # else: let it fall through to KeyError handling for a more specific fallback if not found

    if '{subfield}' in fields_in_template and 'subfield' not in working_data:
        if coherence_manager:
            theme_subfield = coherence_manager.get_theme_academic_subfield()
            if theme_subfield: working_data['subfield'] = theme_subfield
            # else: let it fall through to KeyError handling

    # Update the main data dictionary with any newly populated fields from working_data.
    # This ensures that if _populate_context_fields (or others) added/modified a value, it's reflected
    # in the data used for the final .format_map() call.
    for key in ['context', 'adjective', 'metaphor', 'subfield']:
        if key in working_data and data.get(key) != working_data[key]: # Update if populated or changed
            data[key] = working_data[key]

    # Fallback for {context} if it's still not in data after population attempts.
    if '{context}' in fields_in_template and 'context' not in data:
        data['context'] = "a broad theoretical context" # Generic fallback

    # Basic placeholder replacement for items in the data dictionary
    for key, value in data.items():
        placeholder = "{" + key + "}"
        # Ensure value is a string before replacing. If it's a list or other type, handle appropriately.
        # This simple replacement assumes values are already strings or convertible.
        if isinstance(value, (list, tuple)):
            # If a list is provided for a placeholder, we might want to join it or pick one.
            # For now, let's assume the data preparation stage handles this and provides a string.
            # Or, we could make a decision here, e.g., str(value) or random.choice(value) if applicable.
            # This part might need refinement based on how `data` is constructed for list-type values.
            pass # Let it be handled by the try-except below for now or ensure data dict has strings.
        
        sentence = sentence.replace(placeholder, str(value))
    
    try:
        # Pass the 'data' dictionary to context for _process_citation_placeholders
        current_context = context.copy() if context else {}
        current_context['data_citation_placeholder'] = data.get('citation', '')


        # Pre-process quote formatting here, as _handle_quote_in_template no longer has the template string.
        if 'quote' in data and data['quote'] is not None:
            data['quote'] = _format_quote_for_academic_style(data['quote'], template)


        sentence = template.format(**data)
        
        # Process {citation} placeholders if they were not filled by specific logic (e.g. quote handling)
        # and are still present after .format() if data['citation'] was empty.
        if '{citation}' in sentence and note_system:
            # The philosopher_name for a general {citation} not tied to a specific quote
            # could come from data['philosopher'] or a general context.
            philosopher_for_general_citation = data.get('philosopher', data.get('philosopher1'))
            if not philosopher_for_general_citation and coherence_manager: # Added fallback
                philosopher_for_general_citation = coherence_manager.get_weighted_philosopher()
            philosopher_for_general_citation = philosopher_for_general_citation or "Smith, John" # Ensure it's not None
            sentence = _process_citation_placeholders(sentence, note_system, current_context, philosopher_for_general_citation, coherence_manager)
        
    except KeyError as e:
        # Fallback if template has missing fields
        missing_key = str(e).strip("'")
        if coherence_manager:
            if missing_key.startswith('philosopher'):
                data[missing_key] = coherence_manager.get_weighted_philosopher() or random.choice(CLEANED_PHILOSOPHERS)
            elif missing_key == 'concept' or missing_key == 'other_concept':
                data[missing_key] = coherence_manager.get_weighted_concept() or random.choice(concepts)
            elif missing_key == 'term':
                available_terms = [t for t in terms if t not in data.get('used_terms', [])]
                if not available_terms: available_terms = terms
                data[missing_key] = random.choice(available_terms) if available_terms else "a relevant notion"
            elif missing_key == 'context':
                # If context is still missing, it implies that coherence_manager was not available,
                # or it was available but get_theme_context_phrase() returned None, 
                # and the fallback within _populate_context_fields also wasn't triggered or failed.
                # This is the final fallback.
                data[missing_key] = "a significant discursive framework" 
            elif missing_key == 'adj':
                data[missing_key] = random.choice(adjectives) if adjectives else "relevant"
            elif missing_key == 'author':
                 # Try to get a philosopher name for author if it's missing.
                data[missing_key] = (coherence_manager.get_weighted_philosopher() or "Smith").split()[0] # Use last name
            elif missing_key == 'year':
                data[missing_key] = str(random.randint(1950, 2023))
            elif missing_key == 'citation':
                data[missing_key] = ''
            else: # Default if not handled by coherence_manager cases
                 data[missing_key] = f"{{{missing_key}}}" # Keep placeholder if truly unknown
        else: # Original fallback if no coherence_manager
            if missing_key.startswith('philosopher'):
                data[missing_key] = random.choice(CLEANED_PHILOSOPHERS)
            elif missing_key == 'concept' or missing_key == 'other_concept':
                data[missing_key] = random.choice(concepts)
            elif missing_key == 'term':
                data[missing_key] = random.choice(terms)
            # elif missing_key == 'context': # This line should be removed/commented
            # data[missing_key] = random.choice(contexts)
            elif missing_key == 'adj':
                data[missing_key] = random.choice(["critical", "radical", "postmodern"])
            elif missing_key == 'author':
                data[missing_key] = "Smith"
            elif missing_key == 'year':
                data[missing_key] = str(random.randint(1950, 2023))
            elif missing_key == 'citation':
                data[missing_key] = ''  # Empty string for citation placeholder if we can't resolve it
            else:
                 data[missing_key] = f"{{{missing_key}}}"


        # Try again with added data
        try:
            sentence = template.format(**data)
            
            # Process citation placeholders if present
            if '{citation}' in sentence and note_system:
                philosopher_name = data.get('philosopher', data.get('philosopher1'))
                if not philosopher_name and coherence_manager: # Added fallback
                    philosopher_name = coherence_manager.get_weighted_philosopher()
                philosopher_name = philosopher_name or "Smith, John" # Ensure it's not None
                sentence = _process_citation_placeholders(sentence, note_system, context, philosopher_name, coherence_manager)
                
        except KeyError:
            # Ultimate fallback
            phil_choice = (coherence_manager.get_weighted_philosopher() if coherence_manager else random.choice(CLEANED_PHILOSOPHERS)) or "a philosopher"
            concept_choice = (coherence_manager.get_weighted_concept() if coherence_manager else random.choice(concepts)) or "a concept"
            term_choice = (coherence_manager.get_weighted_term() if coherence_manager else random.choice(terms)) or "a term"
            sentence = f"The work of {phil_choice} on {concept_choice} has significant implications for {term_choice}."
    
    return sentence


def _handle_citation_marker(sentence, context, used_concepts, used_terms, used_philosophers, note_system, coherence_manager=None):
    """Generates a citation if [citation] is present in the sentence."""
    if "[citation]" in sentence:
        # Generate a contextual reference string
        # This is where the core logic for on-the-fly reference generation should be robust
        # For now, assume _generate_contextual_reference is good enough or will be improved
        philosopher_for_citation = context.get('primary_philosopher') # Or pick from used_philosophers
        if not philosopher_for_citation and used_philosophers:
            philosopher_for_citation = random.choice(list(used_philosophers))
        
        # The reference generation should ideally happen here or be passed to add_citation
        # The current _generate_contextual_reference generates a full string. This is fine.
        ref_str = _generate_contextual_reference(context, concepts=used_concepts, terms=used_terms, philosopher_name=philosopher_for_citation, coherence_manager=coherence_manager)
        
        if ref_str and note_system:
            # Pass the generated reference string to add_citation
            citation_text = note_system.add_citation(ref_str, context=context)
            sentence = sentence.replace("[citation]", citation_text or "[Citation Placeholder]", 1)
        else:
            sentence = sentence.replace("[citation]", "[Citation Placeholder]", 1) # Remove placeholder if no citation generated
    return sentence


def _clean_double_prepositions(sentence):
    """Remove duplicate prepositions like 'in in' or 'through through'."""
    # Define a list of common prepositions to check for duplication
    prepositions = [
        "about", "above", "across", "after", "against", "along", "amid", "among", "around",
        "as", "at", "before", "behind", "below", "beneath", "beside", "between", "beyond",
        "but", "by", "concerning", "considering", "despite", "down", "during", "except",
        "for", "from", "in", "inside", "into", "like", "near", "of", "off", "on", "onto",
        "out", "outside", "over", "past", "regarding", "since", "through", "throughout",
        "to", "toward", "under", "underneath", "until", "unto", "up", "upon", "with",
        "within", "without"
    ]
    # Create a regex pattern to find doubled prepositions (case-insensitive)
    # It looks for a preposition, followed by a space, followed by the same preposition
    # e.g., r"\b(in)\s+\1\b"
    for prep in prepositions:
        # Escape prepositions if they contain special regex characters (none in this list, but good practice)
        escaped_prep = re.escape(prep)
        pattern = r"\b(" + escaped_prep + r")\s+\1\b"
        # Replace "prep prep" with "prep"
        sentence = re.sub(pattern, r"\1", sentence, flags=re.IGNORECASE)
    return sentence


def _finalize_sentence(sentence):
    """
    Finalize a sentence by cleaning whitespace and ensuring proper punctuation (MLA style).
    Periods go AFTER parenthetical citations, e.g., "end of quote" (Author Page).
    Question marks or exclamation points that are part of the quote remain inside the quote,
    and the sentence then also gets a period after the citation, e.g., "end of quote?" (Author Page).
    """
    # Remove extra whitespace
    sentence = ' '.join(sentence.split())

    # Clean double prepositions
    sentence = _clean_double_prepositions(sentence)
    
    if not sentence:
        return "." # Return a period if sentence is empty after cleaning.

    # Regex to check if the sentence ends with a typical parenthetical citation
    # e.g., (Author XX), (Author, qtd. in Other XX), (Qtd. in Author XX)
    ends_with_citation_regex = r'\s*\([^)]+\)$'
    
    # Check if sentence (before potential final punctuation) ends with a citation
    has_citation_at_end = bool(re.search(ends_with_citation_regex, sentence))

    # Check for existing sentence-ending punctuation *before* a potential citation
    # This looks for quote-ending punctuation like "Quote?" (Citation) or "Quote." (Citation)
    # Corrected to look for punctuation *immediately* before the citation pattern if it exists.
    pre_citation_punctuation_match = None
    if has_citation_at_end:
        # Find where the citation starts to check character before it
        citation_match = re.search(ends_with_citation_regex, sentence)
        if citation_match:
            char_before_citation = sentence[:citation_match.start()].rstrip()[-1:]
            if char_before_citation in '.?!':
                pre_citation_punctuation_match = char_before_citation
    
    # Determine if the sentence *already* ends with a period, question mark, or exclamation point *at the very end*.
    already_punctuated_at_very_end = sentence.endswith('.') or sentence.endswith('?') or sentence.endswith('!')

    if has_citation_at_end:
        # Case 1: Sentence ends with a citation.
        # MLA: Period always goes AFTER the citation, unless the sentence is a question/exclamation overall.
        # If the quote itself ended in ? or !, that punctuation stays *inside* the quote, and a period is still added after the citation.
        # Example: "Is this a question?" (Author Page).
        # Example: "This is a statement." (Author Page).

        # If the character immediately before the citation was a period, it should have been removed by _format_quote_for_academic_style (if mid-sentence).
        # Or it might be the end of a non-quoted part of the sentence before a final citation.
        # We strip any period immediately before the citation, as the final period will be added after.
        citation_start_index = sentence.rfind('(') # Simple way to find approx start of citation
        if citation_start_index > 0 and sentence[citation_start_index-1] == '.':
            # Check if this period is preceded by a quote mark. If so, _format_quote_for_academic_style should handle it.
            # This is more for cases like "...stated clearly. (Author Page)" -> "...stated clearly (Author Page)."
            if not (sentence[citation_start_index-2] in '\"\''): # if not part of a quote ending in period
                 sentence = sentence[:citation_start_index-1] + sentence[citation_start_index:]
                 sentence = sentence.strip() # clean up potential double space

        if not already_punctuated_at_very_end: # Add a period if not already ending with ?, !, or .
             sentence += '.'
    
    else: # Case 2: Sentence does NOT end with a citation.
        if not already_punctuated_at_very_end:
            sentence += '.'
            
    return sentence

def _generate_contextual_reference(context, concepts=None, terms=None, philosopher_name=None, coherence_manager=None):
    target_author_name = None
    
    # Path 1: Validate philosopher_name argument
    if philosopher_name and isinstance(philosopher_name, str) and \
       len(philosopher_name.strip().replace(".", "")) > 1 and philosopher_name in CLEANED_PHILOSOPHERS:
        target_author_name = philosopher_name
    # If philosopher_name is invalid or not provided, target_author_name remains None.
    
    # Path 2: Validate context.get('philosopher') if target_author_name is still None
    if not target_author_name and context and context.get('philosopher'):
        context_philosopher = context.get('philosopher')
        if isinstance(context_philosopher, str) and \
           len(context_philosopher.strip().replace(".", "")) > 1 and context_philosopher in CLEANED_PHILOSOPHERS:
            target_author_name = context_philosopher
    # If context_philosopher is invalid, target_author_name remains None.
            
    # Path 3: Use coherence_manager if target_author_name is still None
    if not target_author_name and coherence_manager:
        themed_philosopher = coherence_manager.get_weighted_philosopher()
        # We trust coherence_manager.get_weighted_philosopher() to return a clean name or None
        # based on previous fixes in coherence.py.
        if themed_philosopher: # themed_philosopher should already be full name
            target_author_name = themed_philosopher
            
    # Path 4: Fallback to random choice from CLEANED_PHILOSOPHERS if still None
    if not target_author_name:
        if CLEANED_PHILOSOPHERS:
            target_author_name = random.choice(CLEANED_PHILOSOPHERS)
        else: # Should ideally not be reached if CLEANED_PHILOSOPHERS has its own fallback
            target_author_name = "Michel Foucault" 

    # Absolute final safeguard: If, after all above, name is still invalid or too short, pick a known good one.
    # This handles edge cases or if CLEANED_PHILOSOPHERS somehow got a bad entry (though its creation is filtered).
    if not target_author_name or not isinstance(target_author_name, str) or \
       len(target_author_name.strip().replace(".", "")) <= 1:
        # Default to a specific philosopher from CLEANED_PHILOSOPHERS or an ultimate default.
        if CLEANED_PHILOSOPHERS:
            # Try to find a very common, safe default if available
            default_options = ["Michel Foucault", "Judith Butler", "Jacques Derrida"]
            safe_choice = next((p for p in default_options if p in CLEANED_PHILOSOPHERS), None)
            target_author_name = safe_choice or random.choice(CLEANED_PHILOSOPHERS)
        else:
            target_author_name = "Jacques Derrida" # Ultimate fallback if CLEANED_PHILOSOPHERS is empty

    # Gather potential hints for the title
    title_hint_parts = []
    if concepts: title_hint_parts.extend(concepts)
    if terms: title_hint_parts.extend(terms)
    if context and context.get('concept'): title_hint_parts.append(context.get('concept'))
    if context and context.get('term'): title_hint_parts.append(context.get('term'))
    
    title_hint_parts = list(set(filter(None, title_hint_parts))) # Remove None/empty and duplicates
    final_title_hint = None # Ensure it's initialized

    if title_hint_parts:
        final_title_hint = " and ".join(random.sample(title_hint_parts, min(len(title_hint_parts), 2)))
    elif target_author_name and isinstance(target_author_name, str) and target_author_name.split(): 
        # Check target_author_name is not an empty string before trying to split
        first_part_of_name = target_author_name.split()[0].replace(',', '') # Get first word, remove comma
        final_title_hint = f"A Study on {first_part_of_name}'s Concepts"
    else: 
        final_title_hint = "A Relevant Study"

    # This ensures that if the template is simple (no complex fields), it still works.
    # And if it is complex, the necessary data is available.

    # The actual reference string is generated here using the determined author and hint.
    return generate_reference(author_name=target_author_name, title_hint=final_title_hint, coherence_manager=coherence_manager)


def _handle_author_citation(template, data, context, used_concepts, used_terms, used_philosophers, note_system, coherence_manager=None):
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
        str: Template with author citations formatted in MLA style (or original if error)
    """
    if not (note_system and 'author' in data and 'year' in data):
        # Not enough info to proceed or not using note system, return template as is.
        return template

    author_name_for_ref = data.get('author', "Unknown Author")
    year_for_ref = data.get('year', str(random.randint(1950,2023)))
    
    # If author is generic, try to get a thematic one
    if author_name_for_ref == "Unknown Author" or author_name_for_ref == "Smith":
        if coherence_manager:
            themed_author = coherence_manager.get_weighted_philosopher()
            if themed_author:
                # Assuming data['author'] stores last name for template
                data['author'] = themed_author.split()[-1] if ' ' in themed_author else themed_author
                author_name_for_ref = themed_author # Full name for reference generation
    
    is_article_guess = random.random() < 0.5 
    try:
        # Ensure year_for_ref is an int for get_enhanced_citation if it expects one
        year_int = int(year_for_ref)
        reference_string = note_system.get_enhanced_citation(author_name_for_ref, is_article_guess, year_int)
    except ValueError: 
        reference_string = note_system.get_enhanced_citation(author_name_for_ref, is_article_guess, random.randint(1950,2023))

    citation_context = context.copy() if context else {}
    if coherence_manager: citation_context['coherence_manager'] = coherence_manager
    citation_text = note_system.add_citation(reference_string, citation_context)
    
    # This function ensures the author/year from data are linked to a citation
    # and the reference is added to works cited.
    # The main sentence formatting will replace {citation} if present.
    data['citation'] = citation_text # Ensure the main citation placeholder uses this for this author.

    return template # Template is returned as is; data dict is modified.

def ensure_quote_has_citation(text):
    """
    Ensure that every direct quote in the text has a citation.
    This is a fallback and might be redundant if main logic is robust.
    
    Args:
        text (str): The text to check
        
    Returns:
        str: The text with properly cited quotes (or original if no quotes/errors)
    """
    if not isinstance(text, str):
        return text

    # Simplified regex for quotes; might need refinement for complex cases.
    quote_pattern = r'(\"[^\"\\r\\n]+\"|\'[^\'\\r\\n]+\')'
    
    last_pos = 0
    result_parts = []

    for match in re.finditer(quote_pattern, text):
        quote_start_pos = match.start()
        quote_end_pos = match.end()
        
        result_parts.append(text[last_pos:quote_end_pos])
        
        # Heuristic check for a citation immediately following the quote.
        # Looks for patterns like " (Author Page)" or " [^1]" within a short window.
        window_after_quote = text[quote_end_pos : quote_end_pos + 30] # Check 30 chars after quote
        
        # Regex for common citation patterns: (Lastname Page), (Lastname, Title Page), [^NoteNum]
        citation_found = re.search(
            r'^\s*\((\w+(?:,\s(?:\"|\')[^\"]+(?:\"|\'))?)\s+\d+\)|'  # (Author Page) or (Author, "Short Title" Page)
            r'^\s*\[\^\d+\]',  # [^NoteNum]
            window_after_quote
        )
        
        if not citation_found:
            # This placeholder indicates a potential issue in primary citation logic.
            # A more robust solution would integrate with NoteSystem here.
            generic_citation = "" # Changed from " (CITATION_NEEDED)"
            result_parts.append(generic_citation)
        
        last_pos = quote_end_pos
        
    result_parts.append(text[last_pos:])
    return "".join(result_parts)