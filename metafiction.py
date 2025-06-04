"""
A module for generating metafictional elements in generated essays.
This module provides functions to create metafictional elements
that can be inserted into academic writing, particularly in the context of
postmodern philosophy and theory.
It includes functions to generate metafictional elements for paragraphs,
insert them into existing text, and create metafictional conclusions.
The metafictional elements are designed to reflect the self-referential nature
of postmodern discourse, often questioning the very frameworks and methodologies
they employ.
It also includes a function to generate a metafictional conclusion
that references concepts and terms used in the essay.
This module is intended to enhance the complexity and depth of
academic writing, particularly in the context of postmodern philosophy.
It is designed to be used in conjunction with other modules
for generating essays, abstracts, and citations.
"""

import random
import re
from json_data_provider import (
    concepts, terms, philosophers, 
    METAFICTIONAL_TEMPLATES, METAFICTIONAL_CONCLUSIONS,
    thematic_clusters # Added for theme-specific metafiction
)
# It's generally better to pass coherence_manager as an argument if it's used extensively
# from coherence import EssayCoherence # Avoid direct import if passing as arg

# Metafiction intensity levels that control frequency and type
METAFICTION_LEVELS = {
    'subtle': {
        'paragraph_probability': 0.08,
        'conclusion_probability': 0.25,
        'max_per_section': 1,
        'avoid_short_sections': True,
        'prefer_later_placement': True
    },
    'moderate': {
        'paragraph_probability': 0.15,
        'conclusion_probability': 0.40,
        'max_per_section': 2,
        'avoid_short_sections': True,
        'prefer_later_placement': False
    },
    'highly_self_aware': {
        'paragraph_probability': 0.25,
        'conclusion_probability': 0.60,
        'max_per_section': 3,
        'avoid_short_sections': False,
        'prefer_later_placement': False
    }
}

# Strategic placement indicators - these signal moments that would benefit from metafictional reflection
STRATEGIC_PLACEMENT_INDICATORS = {
    'bold_claims': [
        'fundamentally', 'entirely', 'completely', 'absolutely', 'necessarily',
        'inevitably', 'always already', 'can only', 'must be understood',
        'it is clear that', 'obviously', 'undoubtedly', 'without question'
    ],
    'dense_theoretical': [
        'apparatus', 'assemblage', 'dispositif', 'rhizome', 'différance',
        'aporia', 'supplement', 'trace', 'pharmakon', 'the Real',
        'jouissance', 'episteme', 'genealogy', 'archaeology'
    ],
    'dialectical_transitions': [
        'however', 'nevertheless', 'on the contrary', 'conversely',
        'in contrast', 'alternatively', 'yet', 'nonetheless',
        'paradoxically', 'ironically', 'contradictorily'
    ],
    'oppositional_moments': [
        'opposition', 'tension', 'contradiction', 'antithesis',
        'binary', 'dichotomy', 'synthesis', 'dialectic'
    ]
}

def detect_strategic_moment(paragraph_text, sentence_index=None, total_sentences=None):
    """
    Detect if this is a strategic moment for metafictional insertion.
    Returns a tuple: (is_strategic, moment_type, placement_weight)
    """
    text_lower = paragraph_text.lower()
    
    # Check for bold claims
    bold_claim_count = sum(1 for indicator in STRATEGIC_PLACEMENT_INDICATORS['bold_claims'] 
                          if indicator in text_lower)
    
    # Check for dense theoretical moments
    theoretical_density = sum(1 for indicator in STRATEGIC_PLACEMENT_INDICATORS['dense_theoretical'] 
                             if indicator in text_lower)
    
    # Check for dialectical transitions
    dialectical_signals = sum(1 for indicator in STRATEGIC_PLACEMENT_INDICATORS['dialectical_transitions'] 
                             if indicator in text_lower)
    
    # Check for oppositional moments
    oppositional_signals = sum(1 for indicator in STRATEGIC_PLACEMENT_INDICATORS['oppositional_moments'] 
                              if indicator in text_lower)
    
    # Calculate strategic value
    strategic_score = bold_claim_count * 3 + theoretical_density * 2 + dialectical_signals * 2 + oppositional_signals * 1
    
    if strategic_score >= 3:
        # Determine moment type
        if bold_claim_count >= 1:
            moment_type = 'bold_claim'
        elif theoretical_density >= 2:
            moment_type = 'dense_theoretical'
        elif dialectical_signals >= 1:
            moment_type = 'dialectical_transition'
        else:
            moment_type = 'oppositional_moment'
        
        # Higher scores get higher placement weights
        placement_weight = min(strategic_score / 10.0, 1.0)
        return True, moment_type, placement_weight
    
    return False, None, 0.0

def should_insert_metafiction(paragraph_text, metafiction_level='moderate', section_length=3, 
                            essay_length=5, metafiction_count_this_section=0, 
                            coherence_manager=None, dialectical_context=None):
    """
    Determine whether to insert metafiction based on multiple contextual factors.
    
    Args:
        paragraph_text (str): The paragraph text to analyze
        metafiction_level (str): 'subtle', 'moderate', or 'highly_self_aware'
        section_length (int): Number of paragraphs in current section
        essay_length (int): Total number of sections in essay
        metafiction_count_this_section (int): How many metafictional elements already in this section
        coherence_manager: Coherence manager for dialectical context
        dialectical_context (dict): Information about current dialectical moment
    
    Returns:
        tuple: (should_insert, insertion_probability, strategic_info)
    """
    config = METAFICTION_LEVELS.get(metafiction_level, METAFICTION_LEVELS['moderate'])
    
    # Check if we've exceeded max for this section
    if metafiction_count_this_section >= config['max_per_section']:
        return False, 0.0, {}
    
    # Avoid short sections if configured
    if config['avoid_short_sections'] and section_length <= 2:
        return False, 0.0, {}
    
    # Check for existing metafictional indicators to avoid redundancy
    metafictional_indicators = [
        "this essay", "this text", "this paper", "this analysis", 
        "in writing", "the author", "inevitably", "implicated", 
        "complicit", "paradox", "entangled", "self-reflexive",
        "reproduces existing paradigms", "discourses it critiques", 
        "economy of academic knowledge production", "logic it seeks to critique", 
        "theoretical tools to critique", "systems under examination"
    ]
    
    if any(indicator in paragraph_text.lower() for indicator in metafictional_indicators):
        return False, 0.0, {}
    
    # Base probability from configuration
    base_probability = config['paragraph_probability']
    
    # Detect strategic moments
    is_strategic, moment_type, strategic_weight = detect_strategic_moment(paragraph_text)
    
    # Adjust probability based on strategic context
    if is_strategic:
        base_probability += strategic_weight * 0.3  # Boost for strategic moments
    
    # Dialectical context adjustments
    if coherence_manager and dialectical_context:
        # If we're in the middle of a dialectical progression, boost probability
        if dialectical_context.get('dialectical_stage') in ['antithesis', 'synthesis']:
            base_probability += 0.1
        
        # If coherence manager indicates an oppositional concept shift
        if dialectical_context.get('oppositional_shift'):
            base_probability += 0.15
    
    # Essay structure adjustments
    if config['prefer_later_placement'] and essay_length > 3:
        # Reduce probability for early sections, increase for later
        section_position = dialectical_context.get('section_index', 0) if dialectical_context else 0
        position_factor = section_position / max(essay_length - 1, 1)
        base_probability *= (0.5 + position_factor)
    
    # Cap probability
    final_probability = min(base_probability, 0.4)
    
    strategic_info = {
        'is_strategic': is_strategic,
        'moment_type': moment_type,
        'strategic_weight': strategic_weight
    }
    
    return random.random() < final_probability, final_probability, strategic_info

def generate_metafictional_element(theme_key=None, coherence_manager=None, 
                                 strategic_context=None, metafiction_level='moderate'):
    """Generate a metafictional element, potentially themed and contextually aware."""
    # Base templates remain the same, but we can select based on context
    templates = [
        "It bears asking whether this line of reasoning merely reproduces existing paradigms.",
        "This analysis acknowledges its own complicity in the very discourses it critiques.",
        "In doing so, this paper inevitably participates in the economy of academic knowledge production it seeks to interrogate.",
        "The inherent contradictions of such an approach will become apparent as the argument unfolds.",
        "To what extent can this investigation escape the very logic it seeks to critique?",
        "This paper remains aware of the paradox inherent in employing theoretical tools to critique those same tools.",
        "In articulating these critiques, I acknowledge the impossibility of a position fully exterior to the systems under examination.",
        "The methodology employed here is necessarily implicated in the structures it attempts to analyze.",
        "This text performs the very tensions it describes.",
        "Such an approach raises questions about the possibility of critical distance in theoretical discourse."
    ]
    
    # Add context-specific templates based on strategic moment
    if strategic_context and strategic_context.get('is_strategic'):
        moment_type = strategic_context.get('moment_type')
        
        if moment_type == 'bold_claim':
            templates.extend([
                "The confidence of this assertion perhaps conceals the uncertainty it attempts to master.",
                "Such definitiveness in theoretical discourse warrants suspicion of its own conditions of possibility.",
                "The rhetorical force of this claim may exceed its theoretical justification."
            ])
        elif moment_type == 'dense_theoretical':
            templates.extend([
                "The deployment of such theoretical machinery risks obscuring the very phenomena it purports to illuminate.",
                "This conceptual apparatus, for all its sophistication, remains embedded within the discursive field it seeks to map.",
                "The density of theoretical reference here perhaps betrays an anxiety about the solidity of the ground being traversed."
            ])
        elif moment_type == 'dialectical_transition':
            templates.extend([
                "This argumentative pivot reveals the extent to which the analysis remains captive to the binary logic it ostensibly transcends.",
                "The very gesture of transition here enacts the dialectical movement the text describes, while perhaps remaining unconscious of this performance.",
                "Such moments of theoretical reversal often mask the persistence of the assumptions they claim to overcome."
            ])
    
    # Theme-specific additions (expanded from previous version)
    if theme_key and theme_key in thematic_clusters:
        theme_data = thematic_clusters[theme_key]
        if theme_key == "Technology, Media, and Culture":
            templates.extend([
                "This textual analysis ironically attempts to grasp a digitally saturated, post-literate condition.",
                "The medium of academic prose struggles to represent the very media transformations it analyzes.",
                "Writing about digital culture necessarily involves an anachronistic gesture toward textual authority."
            ])
        elif theme_key == "Power and Knowledge":
            templates.extend([
                "The very act of articulating this critique of power is itself a discursive move within a field of power.",
                "Knowledge production about power/knowledge cannot escape the apparatus it describes.",
                "This genealogical analysis participates in the very regimes of truth it seeks to historicize."
            ])
        elif theme_key == "Decoloniality and Postcolonial Studies":
            templates.extend([
                "Can this analysis, framed within Western academic discourse, truly decenter dominant epistemologies?",
                "The institutional context of this critique may constrain its decolonial aspirations.",
                "Writing about decoloniality within the academy enacts a constitutive tension that cannot be simply resolved."
            ])
        elif theme_key == "Digital Subjectivity":
            templates.extend([
                "This analysis of digital subjectivity is itself mediated by the technological infrastructure it examines.",
                "The subject position of the author in digital networks complicates any claimed critical distance.",
                "Theorizing networked identity necessarily involves the entanglement of the theorist in digital assemblages."
            ])

    chosen_template = random.choice(templates)

    # If coherence_manager is available and template uses placeholders, populate them
    if coherence_manager and ("{concept}" in chosen_template or "{term}" in chosen_template or "{philosopher}" in chosen_template):
        try:
            mf_concept = coherence_manager.get_weighted_concept()
            mf_term = coherence_manager.get_weighted_term(exclude={mf_concept})
            mf_philosopher = coherence_manager.get_weighted_philosopher()
            
            chosen_template = chosen_template.format(
                concept=mf_concept,
                term=mf_term,
                philosopher=mf_philosopher
            )
        except (KeyError, AttributeError):
            # Template doesn't use these placeholders or coherence_manager method failed
            pass

    return chosen_template

def insert_metafiction_in_paragraph(paragraph_text, theme_key=None, coherence_manager=None,
                                  metafiction_level='moderate', section_context=None, dialectical_context=None):
    """Insert a metafictional element into an existing paragraph with enhanced contextual awareness."""
    
    # Enhanced section context handling
    section_length = section_context.get('section_length', 3) if section_context else 3
    essay_length = section_context.get('essay_length', 5) if section_context else 5
    metafiction_count = section_context.get('metafiction_count_this_section', 0) if section_context else 0
    
    # Check if we should insert metafiction
    should_insert, probability, strategic_info = should_insert_metafiction(
        paragraph_text, metafiction_level, section_length, essay_length, 
        metafiction_count, coherence_manager, dialectical_context
    )
    
    if not should_insert:
        return paragraph_text
    
    # Generate contextually appropriate metafictional element
    metafictional_text_template = random.choice(METAFICTIONAL_TEMPLATES)
    
    # Select concepts and terms with coherence manager if available
    if coherence_manager:
        mf_concept = coherence_manager.get_weighted_concept()
        mf_term = coherence_manager.get_weighted_term(exclude={mf_concept})
        mf_philosopher = coherence_manager.get_weighted_philosopher()
        
        # Further bias toward theme if available
        if coherence_manager.active_theme_key:
            theme_data = coherence_manager.active_theme_data
            if theme_data.get('key_concepts') and random.random() < 0.7:
                mf_concept = random.choice(theme_data['key_concepts'])
            if theme_data.get('relevant_terms') and random.random() < 0.7:
                mf_term = random.choice([t for t in theme_data['relevant_terms'] if t != mf_concept])
            if theme_data.get('core_philosophers') and random.random() < 0.7:
                mf_philosopher = random.choice(theme_data['core_philosophers'])
    else:
        mf_concept = random.choice(concepts)
        mf_term = random.choice([t for t in terms if t != mf_concept])
        mf_philosopher = random.choice(philosophers)
    
    try:
        metafictional_text = metafictional_text_template.format(
            concept=mf_concept,
            term=mf_term,
            philosopher=mf_philosopher
        )
    except KeyError:
        # Fallback for templates that don't use all placeholders
        metafictional_text = generate_metafictional_element(
            theme_key=theme_key, 
            coherence_manager=coherence_manager, 
            strategic_context=strategic_info,
            metafiction_level=metafiction_level
        )

    # Strategic placement within paragraph
    if paragraph_text.endswith('.'):
        paragraph_text = paragraph_text[:-1]

    sentences = re.split(r'(?<=[.?!])\s+(?=[A-Z])|(?<=[.?!])$\s*', paragraph_text.strip())
    sentences = [s.strip() for s in sentences if s.strip()]

    if not sentences:
        return metafictional_text

    if len(sentences) <= 1:
        if sentences and not sentences[-1].endswith(tuple('.!?')):
            return sentences[-1] + ". " + metafictional_text
        elif sentences:
            return sentences[-1] + " " + metafictional_text
        else:
            return metafictional_text
    else:
        # Strategic placement based on context
        if strategic_info.get('is_strategic'):
            # Place immediately after strategic moment if detected
            insert_position = len(sentences) - 1  # Near end for maximum impact
        else:
            # Default placement in latter half of paragraph
            insert_position = random.randint(len(sentences) // 2, len(sentences) - 1)
        
        if not sentences[insert_position - 1].endswith(tuple('.!?')):
            sentences[insert_position - 1] += '.'
        sentences.insert(insert_position, metafictional_text)
        return " ".join(sentences)

def generate_metafictional_conclusion(concepts_used, terms_used, theme_key=None, 
                                    coherence_manager=None, metafiction_level='moderate'):
    """
    Generate a metafictional conclusion with enhanced thematic awareness.
    """
    config = METAFICTION_LEVELS.get(metafiction_level, METAFICTION_LEVELS['moderate'])
    
    # Only generate if probability check passes
    if random.random() > config['conclusion_probability']:
        return None
    
    mf_concept = random.choice(list(concepts_used)) if concepts_used else random.choice(concepts)
    mf_term = random.choice(list(terms_used)) if terms_used else random.choice(terms)

    if coherence_manager:
        mf_concept = coherence_manager.get_weighted_concept(exclude=terms_used if terms_used else None)
        mf_term = coherence_manager.get_weighted_term(exclude=concepts_used.union({mf_concept}) if concepts_used else {mf_concept})
        if coherence_manager.active_theme_key:
            theme_data = coherence_manager.active_theme_data
            if theme_data.get('key_concepts') and random.random() < 0.8:
                potential_concepts = [c for c in theme_data['key_concepts'] if c in concepts_used]
                if potential_concepts: mf_concept = random.choice(potential_concepts)
            if theme_data.get('relevant_terms') and random.random() < 0.8:
                potential_terms = [t for t in theme_data['relevant_terms'] if t in terms_used and t != mf_concept]
                if potential_terms: mf_term = random.choice(potential_terms)
    
    # Fallback if mf_term became same as mf_concept due to limited themed choices
    if mf_concept == mf_term:
        mf_term = random.choice([t for t in (list(terms_used) if terms_used else terms) if t != mf_concept] or terms)

    conclusion_template = random.choice(METAFICTIONAL_CONCLUSIONS)
    
    try:
        return conclusion_template.format(concept=mf_concept, term=mf_term)
    except KeyError:
        return f"Ultimately, the very attempt to delineate {mf_concept} from {mf_term} underscores the constructed nature of this theoretical endeavor."