import random
from data import philosophers, concepts, terms, philosopher_concepts, contexts

introduction_templates = [
    "This paper explores the relationship between {term} and {concept} in the context of {context}.",
    "In recent years, there has been a growing interest in {term}, particularly in the field of {context}.",
    "This study aims to examine how {concept} influences {term} within {context}.",
    "The following analysis situates {concept} within the broader discourse of {term} in {context}.",
    "It is worth noting that {concept} has become central to understanding {term} in {context}."
]

general_templates = [
    "{philosopher} argues that {concept} is pivotal to rethinking {term}.",
    "According to {philosopher}, {concept} disrupts conventional understandings of {term}.",
    "In the framework of {term}, {concept} emerges as a critical lens. [citation]",
    "{concept}, as articulated by {philosopher}, reconfigures our approach to {term}.",
    "{philosopher1} and {philosopher2} offer contrasting interpretations of {concept} within {term}.",
    "Critics suggest that {philosopher}'s {concept} fails to account for nuances in {term}. [citation]",
    "Does {concept} adequately address {term}, as {philosopher} contends?",
    "The notion of {concept} in {philosopher}'s oeuvre illuminates {term}.",
    "{term} serves as a backdrop for {philosopher}'s exploration of {concept}.",
    "Through {concept}, {philosopher} critiques the underpinnings of {term}. [citation]",
    "{philosopher} situates {concept} within a broader discourse of {term}.",
    "The interplay between {concept} and {term} is a recurring theme in {philosopher}'s work."
]

conclusion_templates = [
    "In conclusion, this study has demonstrated that {concept} plays a crucial role in understanding {term}.",
    "These findings have significant implications for {context}, particularly in relation to {concept}.",
    "In summary, the analysis highlights the importance of {term} in the context of {concept}.",
    "This paper has shown that {concept} reshapes our approach to {term} within {context}.",
    "Future research should explore the implications of {concept} for {term} in {context}."
]

def generate_sentence(template_type, references, forbidden_philosophers=[], forbidden_concepts=[], forbidden_terms=[]):
    if template_type == "introduction":
        template = random.choice(introduction_templates)
        term = random.choice([t for t in terms if t not in forbidden_terms])
        concept = random.choice([c for c in concepts if c not in forbidden_concepts])
        context = random.choice(contexts)
        sentence = template.format(term=term, concept=concept, context=context)
        return [(sentence, None)], [term, concept]
    elif template_type == "conclusion":
        template = random.choice(conclusion_templates)
        term = random.choice([t for t in terms if t not in forbidden_terms])
        concept = random.choice([c for c in concepts if c not in forbidden_concepts])
        context = random.choice(contexts)
        sentence = template.format(term=term, concept=concept, context=context)
        return [(sentence, None)], [term, concept]
    else:  # general
        template = random.choice(general_templates)
        philosopher = random.choice([p for p in philosophers if p not in forbidden_philosophers])
        if philosopher in philosopher_concepts:
            related_concepts = [c for c in philosopher_concepts[philosopher][0] if c not in forbidden_concepts]
            concept = random.choice(related_concepts) if related_concepts else random.choice([c for c in concepts if c not in forbidden_concepts])
        else:
            concept = random.choice([c for c in concepts if c not in forbidden_concepts])
        term = random.choice([t for t in terms if t not in forbidden_terms])
        data = {
            "philosopher": philosopher,
            "concept": concept,
            "term": term,
            "philosopher1": philosopher,
            "philosopher2": random.choice([p for p in philosophers if p != philosopher and p not in forbidden_philosophers])
        }
        sentence_parts = []
        if "[citation]" in template:
            reference = random.choice(references)
            sentence = template.replace("[citation]", "").format(**data)
            sentence_parts.append((sentence, None))
            sentence_parts.append(("[citation]", str(reference)))
        else:
            sentence = template.format(**data)
            sentence_parts.append((sentence, None))
        used_items = [philosopher, concept, term]
        return sentence_parts, used_items