"""
coherence.py - A module for maintaining thematic and conceptual coherence in generated essays.
This module manages the tracking of concepts, terms, and philosophers used in the essay,
ensuring that the generated content remains thematically consistent and coherent.
It includes functions for selecting weighted concepts, terms, and philosophers,
as well as generating dialectical progressions and oppositional concepts.
It also provides a system for recording usage and managing relationships between concepts.
It is designed to work in conjunction with other modules in the essay generation system,
allowing for a cohesive and sophisticated output.
"""

import random
from collections import Counter, defaultdict
from data import philosophers, concepts, terms, philosopher_concepts

class EssayCoherence:
    """
    Class for managing thematic unity and conceptual coherence in essay generation.
    Maintains weighted tracking of used concepts, terms, and philosophers to ensure
    consistent themes and references throughout the essay.
    """
    
    def __init__(self):
        """Initialize coherence manager with weights for concepts, terms, and philosophers."""
        # Set up tracking for concepts, terms and philosophers
        self.concept_weights = Counter()
        self.term_weights = Counter()
        self.philosopher_weights = Counter()
        
        # Keep track of actual usage
        self.used_concepts = set()
        self.used_terms = set()
        self.used_philosophers = set()
        
        # Store primary themes
        self.primary_concepts = []
        self.primary_terms = []
        self.primary_philosophers = []
        
        # Initialize with some primary themes
        self._initialize_primary_themes()
        
        # Relationship graph for concepts
        self.concept_relationships = self._build_concept_relationships()
    
    def _initialize_primary_themes(self):
        """Initialize primary themes for the essay."""
        # Select primary themes with good representation in philosopher_concepts
        potential_concepts = [
            concept for concept in concepts 
            if sum(1 for philo_concepts in philosopher_concepts.values() if concept in philo_concepts) >= 3
        ]
        
        # Fallback if no good matches
        if not potential_concepts:
            potential_concepts = concepts
        
        # Select 2-3 primary concepts
        num_primary = random.randint(2, 3)
        self.primary_concepts = random.sample(potential_concepts, min(num_primary, len(potential_concepts)))
        
        # Find philosophers associated with these concepts
        associated_philosophers = []
        for concept in self.primary_concepts:
            for philosopher, philo_concepts in philosopher_concepts.items():
                if concept in philo_concepts:
                    associated_philosophers.append(philosopher)
        
        # Select primary philosophers
        if associated_philosophers:
            self.primary_philosophers = random.sample(
                associated_philosophers, 
                min(3, len(associated_philosophers))
            )
        else:
            self.primary_philosophers = random.sample(philosophers, 3)
        
        # Select primary terms with some relation to concepts
        self.primary_terms = random.sample(terms, min(3, len(terms)))
        
        # Initialize weights for primary themes
        for concept in self.primary_concepts:
            self.concept_weights[concept] = 3
        
        for term in self.primary_terms:
            self.term_weights[term] = 3
            
        for philosopher in self.primary_philosophers:
            self.philosopher_weights[philosopher] = 3
    
    def _build_concept_relationships(self):
        """Build a graph of related concepts based on philosopher associations."""
        relationships = defaultdict(set)
        
        # For each philosopher, add relationships between concepts they work with
        for philo_concepts in philosopher_concepts.values():
            for concept in philo_concepts:
                for related in philo_concepts:
                    if concept != related:
                        relationships[concept].add(related)
        
        return relationships
    
    def record_usage(self, concepts=None, terms=None, philosophers=None):
        """
        Record usage of concepts, terms, and philosophers to maintain coherence.
        
        Args:
            concepts (list/set): Concepts used
            terms (list/set): Terms used
            philosophers (list/set): Philosophers referenced
        """
        if concepts:
            for concept in concepts:
                self.concept_weights[concept] += 1
                self.used_concepts.add(concept)
        
        if terms:
            for term in terms:
                self.term_weights[term] += 1
                self.used_terms.add(term)
                
        if philosophers:
            for philosopher in philosophers:
                self.philosopher_weights[philosopher] += 1
                self.used_philosophers.add(philosopher)
    
    def get_weighted_concept(self, exclude=None):
        """
        Get a concept weighted by previous usage and primary themes.
        
        Args:
            exclude (set): Concepts to exclude
            
        Returns:
            str: A selected concept
        """
        exclude = exclude or set()
        
        # Probability distribution for selection
        available = [c for c in concepts if c not in exclude]
        
        # Get weights, ensuring all concepts have at least a minimal weight
        weights = [max(self.concept_weights[c], 0.1) for c in available]
        
        # Select based on weights
        return random.choices(available, weights=weights, k=1)[0]
    
    def get_weighted_term(self, exclude=None):
        """
        Get a term weighted by previous usage and primary themes.
        
        Args:
            exclude (set): Terms to exclude
            
        Returns:
            str: A selected term
        """
        exclude = exclude or set()
        
        # Probability distribution for selection
        available = [t for t in terms if t not in exclude]
        
        # Get weights, ensuring all terms have at least a minimal weight
        weights = [max(self.term_weights[t], 0.1) for t in available]
        
        # Select based on weights
        return random.choices(available, weights=weights, k=1)[0]
    
    def get_weighted_philosopher(self, exclude=None):
        """
        Get a philosopher weighted by previous usage and primary themes.
        
        Args:
            exclude (set): Philosophers to exclude
            
        Returns:
            str: A selected philosopher
        """
        exclude = exclude or set()
        
        # Probability distribution for selection
        available = [p for p in philosophers if p not in exclude]
        
        # Get weights, ensuring all philosophers have at least a minimal weight
        weights = [max(self.philosopher_weights[p], 0.1) for p in available]
        
        # Select based on weights
        return random.choices(available, weights=weights, k=1)[0]
    
    def get_related_concept(self, concept):
        """
        Get a concept related to the provided concept.
        
        Args:
            concept (str): The concept to find relations for
            
        Returns:
            str: A related concept
        """
        if concept in self.concept_relationships and self.concept_relationships[concept]:
            return random.choice(list(self.concept_relationships[concept]))
        
        # Fallback to primary concepts or random
        if self.primary_concepts:
            return random.choice([c for c in self.primary_concepts if c != concept])
        
        return random.choice([c for c in concepts if c != concept])
    
    def get_oppositional_concept(self, concept):
        """
        Get a concept that can be positioned in opposition to the given concept.
        
        Args:
            concept (str): The concept to find an opposition for
            
        Returns:
            str: An oppositional concept
        """
        # Dictionary of some common conceptual oppositions
        oppositions = {
            "hyperreality": ["reality", "authenticity"],
            "deterritorialization": ["territorialization", "boundary"],
            "deconstruction": ["construction", "logocentrism"],
            "différance": ["presence", "identity"],
            "rhizome": ["hierarchy", "arborescence"],
            "simulacra": ["original", "authenticity"],
            "discourse": ["silence", "materiality"],
            "power/knowledge": ["truth", "objectivity"],
            "performativity": ["essence", "identity"],
            "subject": ["object", "structure"],
            "biopolitics": ["sovereignty", "autonomy"],
            "post-humanism": ["humanism", "anthropocentrism"],
            "capitalism": ["socialism", "commons"],
            "neoliberalism": ["collectivism", "social welfare"],
            "hegemony": ["resistance", "autonomy"],
            "signifier": ["signified", "referent"],
            "textuality": ["materiality", "presence"]
        }
        
        # Check if we have a defined opposition
        if concept in oppositions:
            return random.choice(oppositions[concept])
        
        # Otherwise, return a concept that hasn't been used much
        least_used = [c for c in concepts if c != concept and self.concept_weights[c] < 2]
        if least_used:
            return random.choice(least_used)
        
        # Fallback
        return random.choice([c for c in concepts if c != concept])
    
    def develop_dialectic(self, starting_concept, num_steps=3):
        """
        Develop a dialectical progression of concepts for section themes.
        
        Args:
            starting_concept (str): Initial concept
            num_steps (int): Number of steps in the dialectic
            
        Returns:
            list: A sequence of concepts forming a dialectic
        """
        progression = [starting_concept]
        current = starting_concept
        
        for _ in range(num_steps):
            # For each step, move either to a related or oppositional concept
            if random.random() < 0.7:  # 70% chance for opposition/synthesis
                next_concept = self.get_oppositional_concept(current)
            else:  # 30% chance for related concept
                next_concept = self.get_related_concept(current)
            
            progression.append(next_concept)
            current = next_concept
        
        return progression
    
    def get_section_theme(self):
        """
        Get a coherent theme for a section of the essay.
        
        Returns:
            dict: Thematic elements for the section
        """
        # Select a key concept, possibly from primary concepts
        if self.primary_concepts and random.random() < 0.7:  # 70% chance to use primary concept
            concept = random.choice(self.primary_concepts)
        else:
            concept = self.get_weighted_concept()
        
        # Find related philosophers
        potential_philosophers = []
        for philosopher, philo_concepts in philosopher_concepts.items():
            if concept in philo_concepts:
                potential_philosophers.append(philosopher)
        
        philosopher = random.choice(potential_philosophers) if potential_philosophers else self.get_weighted_philosopher()
        
        # Get a related philosopher
        related_philosopher = None
        for p, philo_concepts in philosopher_concepts.items():
            if p != philosopher and concept in philo_concepts:
                related_philosopher = p
                break
        
        if not related_philosopher:
            related_philosopher = self.get_weighted_philosopher(exclude={philosopher})
        
        # Get a term
        if self.primary_terms and random.random() < 0.6:  # 60% chance to use primary term
            term = random.choice(self.primary_terms)
        else:
            term = self.get_weighted_term()
        
        # Construct theme
        theme = {
            'concept': concept,
            'philosopher': philosopher,
            'related_philosopher': related_philosopher,
            'term': term
        }
        
        return theme