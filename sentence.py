import random
import string
from citation_utils import get_citation_note 
from data import philosophers, concepts, terms, philosopher_concepts, contexts
from quotes import quotes

# Expanded introduction templates for variety and sophistication
introduction_templates = [
    "This paper examines {term} in relation to {concept} within {context}.",
    "The interplay between {concept} and {term} shapes our understanding of {context}.",
    "This paper explores the intricate relationship between {term} and {concept} within the discursive field of {context}.",
    "In recent scholarly endeavors, {term} has emerged as a focal point, particularly within the ambit of {context}.",
    "This study seeks to interrogate the modalities through which {concept} shapes {term} in {context}.",
    "The ensuing analysis situates {concept} within the broader epistemic terrain of {term} in {context}.",
    "It merits consideration that {concept} has assumed a pivotal role in elucidating {term} within {context}.",
    "Contemporary discourse increasingly gravitates toward {term}, especially when viewed through {context}.",
    "The confluence of {concept} and {term} yields novel insights into the fabric of {context}.",
    "By refracting {concept} through the prism of {term}, this paper enriches the discourse of {context}.",
    "To apprehend {term} fully, one must adopt a nuanced engagement with {concept} in {context}.",
    "This inquiry probes {concept}'s constitutive role in the reconfiguration of {term} within {context}.",
    "This essay, in its initial foray, navigates the contested terrain of {term} through {concept} in {context}, resisting closure.",
    "The opening salvo of this analysis foregrounds {concept}'s entanglement with {term} within {context}, a terrain of perpetual deferral.",
    "Here, we embark on an exploration of {term}, its nexus with {concept} unfolding within the fractured landscape of {context}."
]

# Expanded general templates with intertextuality, metafiction, and irony
general_templates = [
    "{philosopher} argues that {concept} redefines {term} in significant ways.",
    "According to {philosopher}, {term} is deeply tied to {concept}.",
    "As {philosopher} stated, \"{quote}\", highlighting {concept} in {context}.",
    "{philosopher1} and {philosopher2} offer contrasting views on {term} through {concept}.",
    "{philosopher} posits that {concept} serves as a linchpin in reimagining {term}.",
    "For {philosopher}, {concept} destabilizes the sedimented meanings of {term}.",
    "Within the ambit of {term}, {concept} emerges as a site of epistemic rupture. [citation]",
    "{concept}, as {philosopher} delineates, reorients our engagement with {term}.",
    "{philosopher1} and {philosopher2} proffer divergent readings of {concept} vis-à-vis {term}.",
    "Certain critics aver that {philosopher}'s {concept} elides critical dimensions of {term}. [citation]",
    "Can {concept}, as {philosopher} contemplates, fully encapsulate the complexities of {term}?",
    "In {philosopher}'s corpus, {concept} casts a revelatory light upon {term}.",
    "{term} functions as the ground against which {philosopher} articulates {concept}.",
    "Through the lens of {concept}, {philosopher} interrogates the foundational axioms of {term}. [citation]",
    "{philosopher} embeds {concept} within the expansive discourse of {term}.",
    "The dialectical interplay of {concept} and {term} recurs throughout {philosopher}'s oeuvre.",
    "This analysis probes the différance inherent in {concept}, per {philosopher}, relative to {term}.",
    "In {philosopher}'s schema, {concept} constitutes a contested terrain for {term}.",
    "The trace of {concept} within {philosopher}'s texts unveils its imbrication with {term}.",
    # Intertextual template
    "{philosopher} often cites {other_philosopher}'s work, particularly the idea of {other_concept}, saying, \"{quote}\", to support their argument on {term}.",
    # Metafiction templates
    "This essay, in its exploration of {term}, finds itself entangled in the very {concept} it seeks to unpack.",
    "The act of writing about {concept} inevitably entangles the author in the same discursive practices that {term} critiques.",
    # Irony and parody templates
    "It is ironic that, in an age obsessed with {term}, {concept} remains elusive.",
    "Any definitive statement about {concept} is inherently problematic, given its fluid and contested nature.",
    # Additional intertextual templates
    "{philosopher}'s engagement with {concept} resonates with {other_philosopher}'s exploration of {other_concept}, illuminating {term}.",
    "Echoing {other_philosopher}'s insights, {philosopher} frames {concept} as a {term} within {context}.",
    # Additional metafiction templates
    "In writing this essay, the author becomes complicit in the {concept} they analyze, a {term} without resolution.",
    "This text, in its interrogation of {term}, mirrors the very {concept} it seeks to deconstruct.",
    # Additional irony templates
    "The pursuit of {concept} as a {term} reveals its own impossibility, a paradox {philosopher} might appreciate.",
    "In the shadow of {concept}, {term} becomes a site of perpetual deferral, as {philosopher} might suggest."
]

conclusion_templates = [
    "In summation, this inquiry has elucidated the indelible role of {concept} in apprehension {term}.",
    "These findings bear profound implications for {context}, particularly through the prism of {concept}.",
    "To conclude, this analysis underscores the salience of {term} vis-à-vis {concept}.",
    "This study has demonstrated that {concept} fundamentally reconfigures our approach to {term} in {context}.",
    "Future scholarship might fruitfully explore {concept}'s ramification for {term} within {context}.",
    "The symbiosis of {concept} and {term} proves essential to grasping {context}, as evidenced herein.",
    "By traversing {term} through {concept}, this paper augments our understanding of {context}.",
    "The results intimate that {concept} is a decisive vector in the constitution of {term} within {context}.",
    "This examination reveals {term}'s profound entanglement with {concept}, upending orthodoxies in {context}.",
    "Ultimately, these insights affirm that {concept} is indispensable to any rigorous study of {term} in {context}.",
    # New metafiction template
    "This essay, in its attempt to {term}, has perhaps only succeeded in demonstrating the complexity and elusiveness of {concept}.",
    # New irony template
    "The very act of concluding this discussion underscores {concept}'s pervasive influence, as even in summarizing, we are entangled in its discursive web.",
    # Additional conclusion templates for variety
    "In closing, the interplay of {concept} and {term} within {context} remains a site of unending contestation.",
    "This analysis, in its final gesture, affirms {concept}'s centrality to {term}, yet leaves its resolution open.",
    "The conclusion, like {concept} itself, resists closure, echoing {term}'s fluidity in {context}."
]

def capitalize_first_word(sentence):
    """Capitalize the first word of a sentence."""
    if not sentence:
        return sentence
    words = sentence.split()
    if words:
        words[0] = words[0].capitalize()
    return ' '.join(words)

def generate_sentence(template_type, references, mentioned_philosophers, forbidden_philosophers=[], forbidden_concepts=[], forbidden_terms=[], used_quotes=set(), all_references=None, cited_references=[]):
    """
    Generate a sentence based on template type, handling philosopher names and quotes dynamically.
    
    Args:
        template_type (str): Type of sentence ('introduction', 'conclusion', or 'general').
        references: Unused parameter (retained for compatibility).
        mentioned_philosophers (set): Philosophers already mentioned in the essay.
        forbidden_philosophers (list): Philosophers to exclude.
        forbidden_concepts (list): Concepts to exclude.
        forbidden_terms (list): Terms to exclude.
        used_quotes (set): Quotes already used.
        all_references (list): List of references for citations.
        cited_references (list): References already cited.
    
    Returns:
        tuple: (sentence_list, used_philosophers, used_concepts, used_terms)
    """
    if template_type == "introduction":
        template = random.choice(introduction_templates)
        term = random.choice([t for t in terms if t not in forbidden_terms])
        concept = random.choice([c for c in concepts if c not in forbidden_concepts])
        context = random.choice(contexts)
        sentence = template.format(term=term, concept=concept, context=context)
        used_philosophers = []
        used_concepts = [concept]
        used_terms = [term]
    
    elif template_type == "conclusion":
        template = random.choice(conclusion_templates)
        term = random.choice([t for t in terms if t not in forbidden_terms])
        concept = random.choice([c for c in concepts if c not in forbidden_concepts])
        context = random.choice(contexts)
        sentence = template.format(term=term, concept=concept, context=context)
        used_philosophers = []
        used_concepts = [concept]
        used_terms = [term]
    
    else:  # general
        # Get available philosophers
        available_philosophers = [p for p in philosophers if p not in forbidden_philosophers]
        if not available_philosophers:
            raise ValueError("No available philosophers to choose from.")
        
        # Filter templates based on number of philosopher fields
        template_pool = [
            t for t in general_templates
            if len([f for _, f, _, _ in string.Formatter().parse(t) if f and (f.startswith('philosopher') or f == 'other_philosopher')]) <= len(available_philosophers)
        ]
        if not template_pool:
            raise ValueError("No suitable templates available for the current number of philosophers.")
        
        template = random.choice(template_pool)
        
        # Parse all fields in the template
        fields = [field for _, field, _, _ in string.Formatter().parse(template) if field]
        
        # Determine quote source
        quote_source_field = 'other_philosopher' if 'other_philosopher' in fields else ('philosopher' if 'philosopher' in fields else 'philosopher1')
        
        # Initialize data and tracking lists
        data = {}
        used_philosophers = []
        used_concepts = []
        used_terms = []
        
        # Populate philosopher fields
        for field in fields:
            if field.startswith('philosopher') or field == 'other_philosopher':
                available = [p for p in available_philosophers if p not in used_philosophers]
                if not available:
                    raise ValueError(f"Not enough philosophers available for field '{field}'.")
                phil = random.choice(available)
                phil_name = phil if phil not in mentioned_philosophers else phil.split()[-1]
                if phil not in mentioned_philosophers:
                    mentioned_philosophers.add(phil)
                data[field] = phil_name
                used_philosophers.append(phil)
        
        # Populate concept fields
        for field in fields:
            if field == 'concept':
                main_phil = data.get('philosopher', data.get('philosopher1'))
                if main_phil and main_phil in philosopher_concepts:
                    related_concepts = [c for c in philosopher_concepts[main_phil] if c not in forbidden_concepts and c not in used_concepts]
                    concept = random.choice(related_concepts) if related_concepts else random.choice([c for c in concepts if c not in forbidden_concepts and c not in used_concepts])
                else:
                    concept = random.choice([c for c in concepts if c not in forbidden_concepts and c not in used_concepts])
                data[field] = concept
                used_concepts.append(concept)
            elif field == 'other_concept':
                other_phil = data.get('other_philosopher')
                if other_phil and other_phil in philosopher_concepts:
                    related_concepts = [c for c in philosopher_concepts[other_phil] if c not in forbidden_concepts and c not in used_concepts]
                    other_concept = random.choice(related_concepts) if related_concepts else random.choice([c for c in concepts if c not in forbidden_concepts and c not in used_concepts])
                else:
                    other_concept = random.choice([c for c in concepts if c not in forbidden_concepts and c not in used_concepts])
                data[field] = other_concept
                used_concepts.append(other_concept)
        
        # Populate term field
        if 'term' in fields:
            term = random.choice([t for t in terms if t not in forbidden_terms and t not in used_terms])
            data['term'] = term
            used_terms.append(term)
        
        # Populate context field
        if 'context' in fields:
            data['context'] = random.choice(contexts)
        
        # Handle quote replacement
        if 'quote' in fields:
            quote_source = data.get(quote_source_field)
            if quote_source and quote_source in quotes:
                available_quotes = [q for q in quotes[quote_source] if q not in used_quotes]
                if available_quotes:
                    selected_quote = random.choice(available_quotes)
                    template = template.replace('{quote}', selected_quote)
                    used_quotes.add(selected_quote)
                else:
                    template = template.replace('"{quote}"', '')
            else:
                template = template.replace('"{quote}"', '')
        
        # Format the sentence
        sentence = template.format(**data)
        
        # Handle citations
        if '[citation]' in sentence and all_references:
            reference = random.choice(all_references)
            if reference not in cited_references:
                cited_references.append(reference)
            number = cited_references.index(reference) + 1
            citation_text = f"[^ {number}]"
            sentence = sentence.replace('[citation]', citation_text)
    
    # Finalize sentence
    sentence = capitalize_first_word(sentence)
    sentence = ' '.join(sentence.split())
    return [(sentence, None)], used_philosophers, used_concepts, used_terms