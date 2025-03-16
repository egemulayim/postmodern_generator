import random
import string
from citation_utils import get_citation_note 
from data import philosophers, concepts, terms, philosopher_concepts, contexts
from quotes import quotes

# A list of introduction templates for variety and sophistication
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

# A list of general templates containing intertextuality, metafiction, irony, and other postmodern elements
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

# A list of conclusion templates for generating sophisticated and nuanced conclusions
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
    sentence = ' '.join(sentence.split())
    return [(sentence, None)], used_philosophers, used_concepts, used_terms