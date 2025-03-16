# sentence.py

import random
from citation_utils import get_citation_note  # Assumed utility for citations
from data import philosophers, concepts, terms, philosopher_concepts, contexts, quotes

# Sentence templates
introduction_templates = [
    "This paper examines {term} in relation to {concept} within {context}.",
    "The interplay between {concept} and {term} shapes our understanding of {context}."
    "This paper explores the intricate relationship between {term} and {concept} within the discursive field of {context}.",
    "In recent scholarly endeavors, {term} has emerged as a focal point, particularly within the ambit of {context}.",
    "This study seeks to interrogate the modalities through which {concept} shapes {term} in {context}.",
    "The ensuing analysis situates {concept} within the broader epistemic terrain of {term} in {context}.",
    "It merits consideration that {concept} has assumed a pivotal role in elucidating {term} within {context}.",
    "Contemporary discourse increasingly gravitates toward {term}, especially when viewed through {context}.",
    "The confluence of {concept} and {term} yields novel insights into the fabric of {context}.",
    "By refracting {concept} through the prism of {term}, this paper enriches the discourse of {context}.",
    "To apprehend {term} fully, one must adopt a nuanced engagement with {concept} in {context}.",
    "This inquiry probes {concept}'s constitutive role in the reconfiguration of {term} within {context}."
]

general_templates = [
    "{philosopher} argues that {concept} redefines {term} in significant ways.",
    "According to {philosopher}, {term} is deeply tied to {concept}.",
    "As {philosopher} stated, '{quote}', highlighting {concept} in {context}.",
    "{philosopher1} and {philosopher2} offer contrasting views on {term} through {concept}."
    "{philosopher} posits that {concept} serves as a linchpin in reimagining {term}.",
    "For {philosopher}, {concept} destabilizes the sedimented meanings of {term}.",
    "Within the ambit of {term}, {concept} emerges as a site of epistemic rupture. [citation]",
    "{concept}, as {philosopher} delineates, reorients our engagement with {term}.",
    "{philosopher1} and {philosopher2} proffer divergent readings of {concept} vis-à-vis {term}.",
    "Certain critics aver that {philosopher}'s {concept} elides critical dimensions of {term}. [citation]",
    "Can {concept}, as {philosopher} contends, fully encapsulate the complexities of {term}?",
    "In {philosopher}'s corpus, {concept} casts a revelatory light upon {term}.",
    "{term} functions as the ground against which {philosopher} articulates {concept}.",
    "Through the lens of {concept}, {philosopher} interrogates the foundational axioms of {term}. [citation]",
    "{philosopher} embeds {concept} within the expansive discourse of {term}.",
    "The dialectical interplay of {concept} and {term} recurs throughout {philosopher}'s oeuvre.",
    "This analysis probes the différance inherent in {concept}, per {philosopher}, relative to {term}.",
    "In {philosopher}'s schema, {concept} constitutes a contested terrain for {term}.",
    "The trace of {concept} within {philosopher}'s texts unveils its imbrication with {term}."
]

conclusion_templates = [
    "In summation, this inquiry has elucidated the indelible role of {concept} in apprehending {term}.",
    "These findings bear profound implications for {context}, particularly through the prism of {concept}.",
    "To conclude, this analysis underscores the salience of {term} vis-à-vis {concept}.",
    "This study has demonstrated that {concept} fundamentally reconfigures our approach to {term} in {context}.",
    "Future scholarship might fruitfully explore {concept}'s ramifications for {term} within {context}.",
    "The symbiosis of {concept} and {term} proves essential to grasping {context}, as evidenced herein.",
    "By traversing {term} through {concept}, this paper augments our understanding of {context}.",
    "The results intimate that {concept} is a decisive vector in the constitution of {term} within {context}.",
    "This examination reveals {term}'s profound entanglement with {concept}, upending orthodoxies in {context}.",
    "Ultimately, these insights affirm that {concept} is indispensable to any rigorous study of {term} in {context}."
]

def capitalize_first_word(sentence):
    """Capitalize the first word of a sentence."""
    if not sentence:
        return sentence
    words = sentence.split()
    if words:
        words[0] = words[0].capitalize()
    return ' '.join(words)

def generate_sentence(template_type, references, mentioned_philosophers, forbidden_philosophers=[], forbidden_concepts=[], forbidden_terms=[]):
    """
    Generate a sentence based on template type, handling philosopher names and quotes.
    
    Args:
        template_type (str): 'introduction', 'general', or 'conclusion'
        references (list): List of references for citations
        mentioned_philosophers (set): Set of philosophers already mentioned
        forbidden_philosophers (list): Philosophers to exclude
        forbidden_concepts (list): Concepts to exclude
        forbidden_terms (list): Terms to exclude
    
    Returns:
        tuple: ([(sentence, None)], list of used items)
    """
    if template_type == "introduction":
        template = random.choice(introduction_templates)
        term = random.choice([t for t in terms if t not in forbidden_terms])
        concept = random.choice([c for c in concepts if c not in forbidden_concepts])
        context = random.choice(contexts)
        sentence = template.format(term=term, concept=concept, context=context)
        used_items = [term, concept]
    
    elif template_type == "conclusion":
        template = random.choice(conclusion_templates)
        term = random.choice([t for t in terms if t not in forbidden_terms])
        concept = random.choice([c for c in concepts if c not in forbidden_concepts])
        context = random.choice(contexts)
        sentence = template.format(term=term, concept=concept, context=context)
        used_items = [term, concept]
    
    else:  # general
        template = random.choice(general_templates)
        philosopher = random.choice([p for p in philosophers if p not in forbidden_philosophers])
        
        # Select concept
        if philosopher in philosopher_concepts:
            related_concepts = [c for c in philosopher_concepts[philosopher] if c not in forbidden_concepts]
            concept = random.choice(related_concepts) if related_concepts else random.choice([c for c in concepts if c not in forbidden_concepts])
        else:
            concept = random.choice([c for c in concepts if c not in forbidden_concepts])
        
        term = random.choice([t for t in terms if t not in forbidden_terms])
        
        # Handle philosopher name
        if philosopher not in mentioned_philosophers:
            philosopher_name = philosopher  # Full name on first mention
            mentioned_philosophers.add(philosopher)
        else:
            philosopher_name = philosopher.split()[-1]  # Last name on subsequent mentions
        
        data = {
            'philosopher': philosopher_name,
            'philosopher1': philosopher_name,  # Same as philosopher
            'concept': concept,
            'term': term
        }
        used_philosophers = [philosopher]
        
       
        # Handle quote if needed
        if '{quote}' in template:
            if philosopher in quotes:
                selected_quote = random.choice(quotes[philosopher])
                template = template.replace('{quote}', selected_quote)
            else:
                # Fallback to a template without quote
                while '{quote}' in template:
                    template = random.choice(general_templates)
         
        # Handle second philosopher if needed
        if '{philosopher2}' in template:
            available_philosophers = [p for p in philosophers if p != philosopher and p not in forbidden_philosophers]
            if available_philosophers:
                philosopher2 = random.choice(available_philosophers)
                if philosopher2 not in mentioned_philosophers:
                    philosopher2_name = philosopher2
                    mentioned_philosophers.add(philosopher2)
                else:
                    philosopher2_name = philosopher2.split()[-1]
                data['philosopher2'] = philosopher2_name
                used_philosophers.append(philosopher2)
            else:
                # Fallback: Choose a template without {philosopher2}
                while '{philosopher2}' in template:
                 template = random.choice(general_templates)
        
        # Add context if required
        if '{context}' in template:
            data['context'] = random.choice(contexts)
        
        sentence = template.format(**data)
        used_items = used_philosophers + [concept, term]
    
    # Add citation if present
    if '[citation]' in sentence:
        reference = random.choice(references)
        citation_note = get_citation_note(reference)
        sentence = sentence.replace('[citation]', citation_note)
    
    sentence = capitalize_first_word(sentence)
    sentence = ' '.join(sentence.split())  # Normalize spacing
    return [(sentence, None)], used_items