"""
A module for maintaining thematic and conceptual coherence in generated essays.
This module manages the tracking of concepts, terms, and philosophers used in the essay,
ensuring that the generated content remains thematically consistent and coherent.
It includes functions for selecting weighted concepts, terms, and philosophers,
as well as generating dialectical progressions and oppositional concepts.
It also provides a system for recording usage and managing relationships between concepts.
"""

import random
from collections import Counter, defaultdict
from json_data_provider import (
    philosophers, concepts, terms, contexts, adjectives,
    philosopher_concepts, quotes,
    bibliography_title_templates, academic_journals, academic_vocab, thematic_clusters,
    oppositional_pairs, philosopher_key_works,
    citation_relationships, philosophical_movements
)

# Placeholder definitions for variables previously imported but not found in data.py
# philosopher_key_works = {}  # Will be imported from data.py
# concept_clusters = {}       # We will use thematic_clusters from data.py instead
# citation_relationships = {} # REMOVE - Now defined in data.py
# philosophical_movements = {} # REMOVE - Now defined in data.py
# oppositional_pairs = []     # Will be imported from data.py

class EssayCoherence:
    """
    Class for managing thematic unity and conceptual coherence in essay generation.
    Maintains weighted tracking of used concepts, terms, and philosophers to ensure
    consistent themes and references throughout the essay.
    Can operate with or without a predefined theme.
    """
    
    def __init__(self, theme_key=None):
        """Initialize coherence manager with weights for concepts, terms, and philosophers."""
        # Import here to ensure they are in the class's scope if needed, or pass as args
        from json_data_provider import concepts as all_concepts, terms as all_terms, philosophers as all_philosophers
        self.concepts = all_concepts
        self.terms = all_terms
        self.philosophers = all_philosophers

        self.active_theme_key = None
        self.active_theme_data = {}
        self.primary_concepts = []
        self.primary_philosophers = []
        self.used_concepts = set()
        self.used_philosophers = set()
        self.used_terms = set()
        self.concept_weights = Counter()
        self.philosopher_weights = Counter()
        self.term_weights = Counter()

        # Initialize philosopher_concepts and philosopher_key_works BEFORE building relationships
        self.philosopher_concepts = philosopher_concepts # Imported from data.py
        self.philosopher_key_works = philosopher_key_works # Imported from data.py

        self.concept_relationships = self._build_concept_relationships()

        if theme_key and theme_key in thematic_clusters:
            self.set_active_theme(theme_key)
        else:
            self._initialize_primary_themes_generic()
            if theme_key:
                print(f"Warning: Theme key '{theme_key}' not found. Initializing with generic themes.")

    def set_active_theme(self, theme_key):
        """Sets the active theme and initializes primary items based on it."""
        self.philosopher_concepts = philosopher_concepts # Re-ensure it's available
        self.philosopher_key_works = philosopher_key_works # Re-ensure it's available

        if theme_key and theme_key in thematic_clusters:
            self.active_theme_key = theme_key
            self.active_theme_data = thematic_clusters[theme_key]
            
            # Reset primary lists and weights before setting from theme
            self.primary_concepts = []
            self.primary_terms = []
            self.primary_philosophers = []
            self.concept_weights.clear()
            self.term_weights.clear()
            self.philosopher_weights.clear()

            # Set primary philosophers from theme
            self.primary_philosophers = list(self.active_theme_data.get('core_philosophers', []))
            # Filter out short names from theme-based primary_philosophers
            self.primary_philosophers = [p for p in self.primary_philosophers if p and len(p.strip().replace(".", "")) > 1]

            if not self.primary_philosophers: # Fallback if theme has no core philosophers or all were short
                self.primary_philosophers = random.sample([p for p in philosophers if p and len(p.strip().replace(".", "")) > 1], min(3, len(philosophers)))

            # Set primary concepts from theme
            self.primary_concepts = list(self.active_theme_data.get('key_concepts', []))
            if not self.primary_concepts: # Fallback
                self.primary_concepts = random.sample(concepts, 2)


            # Set primary terms from theme
            self.primary_terms = list(self.active_theme_data.get('relevant_terms', []))
            if not self.primary_terms: # Fallback
                self.primary_terms = random.sample(terms, 2)

            # Assign high initial weights to thematic elements
            for philosopher in self.primary_philosophers:
                # Ensure only valid philosophers get weights (already filtered, but good practice)
                if philosopher and len(philosopher.strip().replace(".", "")) > 1:
                    self.philosopher_weights[philosopher] = 10 # Strong weight for theme philosophers
            for concept in self.primary_concepts:
                self.concept_weights[concept] = 10 # Strong weight for theme concepts
            for term in self.primary_terms:
                self.term_weights[term] = 10      # Strong weight for theme terms
            
            # Add related concepts/terms from theme with slightly lower, but still high, weight
            for concept in self.active_theme_data.get('key_concepts', []):
                 if concept not in self.primary_concepts: # Avoid double counting
                    self.concept_weights[concept] = 7
            for term in self.active_theme_data.get('relevant_terms', []):
                 if term not in self.primary_terms: # Avoid double counting
                    self.term_weights[term] = 7
            
            self.record_usage(concepts=self.primary_concepts, terms=self.primary_terms, philosophers=self.primary_philosophers)

        else:
            print(f"Warning: Theme key '{theme_key}' not found or invalid. Coherence manager remains on generic themes or previous theme.")
            if not self.active_theme_key: # If no theme was previously active, initialize generically
                 self._initialize_primary_themes_generic()


    def _initialize_primary_themes_generic(self):
        """Initialize primary themes for the essay when no specific theme is active."""
        # Select primary concepts with good representation in philosopher_concepts
        potential_concepts = [
            concept for concept in concepts 
            if sum(1 for philo_concepts_list in philosopher_concepts.values() if concept in philo_concepts_list) >= 2 # Reduced threshold
        ]
        
        if not potential_concepts:
            potential_concepts = list(concepts) # Ensure it's a list
        
        num_primary_concepts = random.randint(2, 3)
        self.primary_concepts = random.sample(potential_concepts, min(num_primary_concepts, len(potential_concepts)))
        
        associated_philosophers = []
        for concept_item in self.primary_concepts:
            for philosopher, philo_concepts_list in philosopher_concepts.items():
                if concept_item in philo_concepts_list:
                    associated_philosophers.append(philosopher)
        
        if associated_philosophers:
            # Use set to get unique philosophers before sampling
            unique_associated_philosophers = list(set(associated_philosophers))
            self.primary_philosophers = random.sample(
                unique_associated_philosophers, 
                min(3, len(unique_associated_philosophers))
            )
        else:
            self.primary_philosophers = random.sample(philosophers, 3)
        
        # Filter out short names from generically initialized primary_philosophers
        self.primary_philosophers = [p for p in self.primary_philosophers if p and len(p.strip().replace(".", "")) > 1]
        # Ensure we still have primary philosophers after filtering
        if not self.primary_philosophers and philosophers:
            self.primary_philosophers = random.sample([p for p in philosophers if p and len(p.strip().replace(".", "")) > 1], min(3, len(philosophers)))
        elif not self.primary_philosophers: # Absolute fallback if philosophers list is empty or all were short
            self.primary_philosophers = ["Michel Foucault"] 

        self.primary_terms = random.sample(terms, min(3, len(terms)))
        
        # Initialize weights for primary themes
        for concept_item in self.primary_concepts:
            self.concept_weights[concept_item] = 5 # Base weight for generic
        for term_item in self.primary_terms:
            self.term_weights[term_item] = 5
        for philosopher_item in self.primary_philosophers:
            # Ensure only valid philosophers get weights
            if philosopher_item and len(philosopher_item.strip().replace(".", "")) > 1:
                self.philosopher_weights[philosopher_item] = 5
        
        self.record_usage(concepts=self.primary_concepts, terms=self.primary_terms, philosophers=self.primary_philosophers)
        print("Coherence manager initialized with generic themes.")

    def prioritize_title_themes(self, title_themes):
        """
        Prioritize themes from the title for stronger coherence.
        This is called *after* initial theme setting (generic or specific).
        """
        if not title_themes or not isinstance(title_themes, dict):
            return

        # Highly weight primary concepts from title
        for concept in title_themes.get('primary_concepts', []):
            self.concept_weights[concept] = self.concept_weights.get(concept, 0) + 15 # Additive boost
            if concept not in self.primary_concepts:
                self.primary_concepts.append(concept)
        
        # Highly weight primary terms from title
        for term in title_themes.get('primary_terms', []):
            self.term_weights[term] = self.term_weights.get(term, 0) + 15 # Additive boost
            if term not in self.primary_terms:
                self.primary_terms.append(term)
        
        # Include related concepts with medium weight
        for concept in title_themes.get('related_concepts', []):
            self.concept_weights[concept] = self.concept_weights.get(concept, 0) + 8 # Additive boost
            if concept not in self.primary_concepts and len(self.primary_concepts) < 5: # Limit expansion
                self.primary_concepts.append(concept)
        
        # Potentially add philosophers mentioned in title themes if any logic for that exists
        # For now, primarily focusing on concepts and terms from title.

    def _build_concept_relationships(self):
        """Build a graph of related concepts based on philosopher associations and thematic_clusters."""
        relationships = defaultdict(set)
        
        # From philosopher_concepts
        for philo_concepts_list in self.philosopher_concepts.values(): # Use self.philosopher_concepts
            for i in range(len(philo_concepts_list)):
                for j in range(i + 1, len(philo_concepts_list)):
                    c1, c2 = philo_concepts_list[i], philo_concepts_list[j]
                    relationships[c1].add(c2)
                    relationships[c2].add(c1)
        
        # From thematic_clusters (imported from data.py)
        for theme_name, theme_data in thematic_clusters.items():
            cluster_concepts_list = theme_data.get('key_concepts', [])
            # Also consider relevant_terms if they are also in the main concepts list
            cluster_concepts_list.extend([term for term in theme_data.get('relevant_terms', []) if term in concepts])
            unique_cluster_concepts = list(set(cluster_concepts_list))

            for i in range(len(unique_cluster_concepts)):
                for j in range(i + 1, len(unique_cluster_concepts)):
                    c1, c2 = unique_cluster_concepts[i], unique_cluster_concepts[j]
                    if c1 in concepts and c2 in concepts: # Ensure they are actual concepts
                        relationships[c1].add(c2)
                        relationships[c2].add(c1)
        return relationships
    
    def record_usage(self, concepts=None, terms=None, philosophers=None):
        """
        Record usage of concepts, terms, and philosophers to maintain coherence.
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
                # Add a filter to ignore very short philosopher names
                if philosopher and len(philosopher.strip().replace(".", "")) > 1:
                    self.philosopher_weights[philosopher] += 1
                    self.used_philosophers.add(philosopher)
                # else: implicitly ignore the short/invalid philosopher name
    
    def _get_weighted_items(self, item_list, item_weights, exclude_set, theme_specific_items=None, subset=None):
        """Helper function to get weighted items, applying thematic boost if a theme is active.
           If subset is provided, only items from that subset are considered.
        """
        target_item_list = item_list
        if subset is not None:
            # Ensure subset is a set for efficient lookup
            subset_as_set = set(subset)
            target_item_list = [item for item in item_list if item in subset_as_set]

        exclude_set = exclude_set or set()
        available_items = [item for item in target_item_list if item not in exclude_set]

        if not available_items: # Fallback if all items are excluded or list is empty
            # Return a random item from the original target_item_list (respecting subset if provided), ignoring excludes if necessary
            if target_item_list:
                return random.choice(list(target_item_list)) 
            elif item_list: # Broader fallback if target_item_list was empty (e.g. empty subset)
                return random.choice(list(item_list))
            return None 

        weights = []
        for item in available_items:
            base_weight = max(item_weights.get(item, 0), 0.1) # Ensure minimum weight
            if self.active_theme_key and theme_specific_items and item in theme_specific_items:
                base_weight *= 2.5 # Boost for items specifically part of the active theme
            weights.append(base_weight)
        
        if not weights or sum(weights) == 0: # Fallback if all weights are zero
             if available_items:
                return random.choice(available_items)
             return None # Should ideally not happen if available_items is not empty

        selected_item = random.choices(available_items, weights=weights, k=1)[0]
        return selected_item

    def get_weighted_concept(self, exclude=None, subset=None):
        """Get a concept weighted by previous usage and primary themes, with thematic boost."""
        theme_concepts = self.active_theme_data.get('key_concepts', []) if self.active_theme_key else []
        return self._get_weighted_items(self.concepts, self.concept_weights, exclude, theme_concepts, subset=subset)
    
    def get_weighted_term(self, exclude=None, subset=None):
        """Get a term weighted by previous usage and primary themes, with thematic boost."""
        theme_terms = self.active_theme_data.get('relevant_terms', []) if self.active_theme_key else []
        return self._get_weighted_items(self.terms, self.term_weights, exclude, theme_terms, subset=subset)
    
    def get_weighted_philosopher(self, exclude=None, subset=None):
        """Get a philosopher weighted by previous usage and primary themes, with thematic boost."""
        theme_philosophers = self.active_theme_data.get('core_philosophers', []) if self.active_theme_key else []
        selected_philosopher = self._get_weighted_items(self.philosophers, self.philosopher_weights, exclude, theme_philosophers, subset=subset)

        # Validate the selected_philosopher. If it's too short, pick a valid fallback.
        if selected_philosopher and len(selected_philosopher.strip().replace(".", "")) <= 1:
            # Fallback: pick a random philosopher from the main list, respecting exclusions
            valid_fallback_philosophers = [p for p in philosophers if p not in (exclude or set()) and len(p.strip().replace(".","")) > 1]
            if valid_fallback_philosophers:
                selected_philosopher = random.choice(valid_fallback_philosophers)
            elif philosophers: # If all valid ones are excluded, pick any from main list (should be rare)
                selected_philosopher = random.choice([p for p in philosophers if len(p.strip().replace(".","")) > 1] or ["Michel Foucault"])
            else: # Absolute fallback
                selected_philosopher = "Michel Foucault"
        elif selected_philosopher is None: # if _get_weighted_items returned None
            valid_fallback_philosophers = [p for p in philosophers if p not in (exclude or set()) and len(p.strip().replace(".","")) > 1]
            if valid_fallback_philosophers:
                selected_philosopher = random.choice(valid_fallback_philosophers)
            elif philosophers:
                selected_philosopher = random.choice([p for p in philosophers if len(p.strip().replace(".","")) > 1] or ["Michel Foucault"])
            else:
                selected_philosopher = "Michel Foucault" # Absolute fallback

        # Chance to pick a related philosopher if a theme is active
        if self.active_theme_key and selected_philosopher in theme_philosophers and random.random() < 0.3:
            secondary_options = []
            # Use .get() for safer access to citation_relationships and philosophical_movements
            related_by_citation = citation_relationships.get(selected_philosopher, [])
            secondary_options.extend([p for p in related_by_citation if p not in (exclude or set()) and p != selected_philosopher])
            
            for movement, movement_philosophers_list in philosophical_movements.items():
                if selected_philosopher in movement_philosophers_list:
                    secondary_options.extend([p for p in movement_philosophers_list if p not in (exclude or set()) and p != selected_philosopher and p not in secondary_options])
            
            if secondary_options:
                return random.choice(secondary_options)
        return selected_philosopher

    def get_related_concept(self, concept_name, exclude=None): # Renamed arg from concept to concept_name
        """
        Get a concept related to the given concept, using relationship graph, 
        concept_clusters, and active theme.
        """
        exclude = exclude or set()
        exclude.add(concept_name) # Exclude the concept itself

        options = list(self.concept_relationships.get(concept_name, []))
        
        for cluster_concepts in thematic_clusters.values():
            if concept_name in cluster_concepts:
                options.extend([c for c in cluster_concepts if c != concept_name])
        
        if self.active_theme_key:
            options.extend([c for c in self.active_theme_data.get('key_concepts', []) if c != concept_name])
            options.extend([c for c in self.active_theme_data.get('relevant_terms', []) if c != concept_name and c in concepts]) # if a term is also a concept

        # Filter out excluded and duplicate options
        valid_options = [opt for opt in list(set(options)) if opt not in exclude and opt in concepts] # Ensure options are actual concepts
        
        if not valid_options:
            # Fallback: get any weighted concept not excluded
            return self.get_weighted_concept(exclude=exclude)
            
        # Weight options: prefer those also in concept_weights or highly related
        option_weights = [max(self.concept_weights.get(opt, 0.1) + (5 if opt in self.concept_relationships.get(concept_name, []) else 0), 0.1) for opt in valid_options]

        if not option_weights or sum(option_weights) == 0:
            return random.choice(valid_options) if valid_options else self.get_weighted_concept(exclude=exclude)

        return random.choices(valid_options, weights=option_weights, k=1)[0]

    def get_oppositional_concept(self, concept_name, exclude=None): # Renamed arg
        """
        Get a concept that is oppositionally related to the given concept.
        Prioritizes oppositional_pairs, then looks for contrasting elements within theme.
        """
        exclude = exclude or set()
        exclude.add(concept_name)

        for pair in oppositional_pairs:
            if concept_name == pair[0] and pair[1] not in exclude and pair[1] in concepts:
                return pair[1]
            if concept_name == pair[1] and pair[0] not in exclude and pair[0] in concepts:
                return pair[0]
        
        # Fallback: if no direct oppositional pair, try to find a contrasting concept
        # This is a placeholder for more sophisticated contrast logic.
        # For now, just return a random concept not closely related or not the same.
        related_to_concept_name = self.concept_relationships.get(concept_name, set())
        potential_opposites = [c for c in concepts if c not in exclude and c not in related_to_concept_name]
        
        if potential_opposites:
            return self.get_weighted_concept(exclude=exclude.union({concept_name}).union(related_to_concept_name))

        return self.get_weighted_concept(exclude=exclude) # Last resort

    def develop_dialectic(self, starting_concept, num_steps=3):
        """
        Develop a dialectical progression of concepts.
        
        Args:
            starting_concept (str): The initial concept (thesis)
            num_steps (int): Number of steps in the dialectic (thesis, antithesis, synthesis)
            
        Returns:
            list: A list of concepts representing the dialectical progression
        """
        if num_steps < 2: return [starting_concept]

        dialectic = [starting_concept]
        current_concept = starting_concept
        
        # Antithesis
        antithesis = self.get_oppositional_concept(current_concept, exclude=set(dialectic))
        if antithesis:
            dialectic.append(antithesis)
            current_concept = antithesis
        else: # Could not find a good antithesis, just get a related one
            related = self.get_related_concept(current_concept, exclude=set(dialectic))
            if related: dialectic.append(related)
            return dialectic # End early if no good antithesis

        if num_steps < 3: return dialectic

        # Synthesis: find a concept related to both thesis and antithesis, or a broader concept
        synthesis_candidates = []
        thesis_relations = set(self.concept_relationships.get(dialectic[0], [])).union(
            *[set(cluster) for cluster in thematic_clusters.values() if dialectic[0] in cluster]
        )
        antithesis_relations = set(self.concept_relationships.get(dialectic[1], [])).union(
            *[set(cluster) for cluster in thematic_clusters.values() if dialectic[1] in cluster]
        )
        
        common_relations = list(thesis_relations.intersection(antithesis_relations) - set(dialectic))
        
        if common_relations:
            synthesis_candidates.extend(common_relations)

        # Also consider broader concepts from active theme if available
        if self.active_theme_key:
            theme_concepts_for_synthesis = [
                c for c in self.active_theme_data.get('key_concepts', []) 
                if c not in dialectic
            ]
            synthesis_candidates.extend(theme_concepts_for_synthesis)

        valid_synthesis_candidates = [c for c in list(set(synthesis_candidates)) if c not in dialectic and c in concepts]

        if valid_synthesis_candidates:
            # Weight synthesis candidates: prefer those with higher existing weights
            synthesis_weights = [max(self.concept_weights.get(c, 0.1), 0.1) for c in valid_synthesis_candidates]
            if synthesis_weights and sum(synthesis_weights) > 0 :
                 synthesis = random.choices(valid_synthesis_candidates, weights=synthesis_weights, k=1)[0]
                 dialectic.append(synthesis)
            elif valid_synthesis_candidates: # Fallback if all weights zero
                 dialectic.append(random.choice(valid_synthesis_candidates))
            else: # Fallback if no valid candidates
                related_to_last = self.get_related_concept(current_concept, exclude=set(dialectic))
                if related_to_last: dialectic.append(related_to_last)

        elif len(dialectic) < num_steps: # Still need more steps but no clear synthesis
            related_to_last = self.get_related_concept(current_concept, exclude=set(dialectic))
            if related_to_last: dialectic.append(related_to_last)
            
        return dialectic[:num_steps]

    def get_section_theme(self, avoid_recent=False, is_conclusion=False, specific_concept=None):
        """Generate a theme for a section, optionally guided by a specific concept."""
        primary_concept = None
        primary_philosopher = None
        primary_term = None

        if specific_concept and specific_concept in self.concepts:
            primary_concept = specific_concept
            # Try to find a philosopher related to this specific concept
            related_philosophers = [p for p, p_concepts in self.philosopher_concepts.items() if primary_concept in p_concepts]
            if related_philosophers:
                primary_philosopher = random.choice(related_philosophers)
            else:
                primary_philosopher = self.get_weighted_philosopher(exclude=self.used_philosophers if avoid_recent else set())
            # Try to get a term related to the primary concept, or a weighted term
            related_terms = list(self.concept_relationships.get(primary_concept, []))
            if related_terms:
                primary_term = random.choice([t for t in related_terms if t in self.terms and t != primary_concept] or [self.get_weighted_term(exclude={primary_concept})])
            else:
                primary_term = self.get_weighted_term(exclude={primary_concept})
        
        elif is_conclusion:
            # For conclusions, try to pick from highly weighted, already used concepts/philosophers for synthesis
            if list(self.used_concepts):
                primary_concept = self.get_weighted_concept(subset=self.used_concepts)
            else:
                primary_concept = self.get_weighted_concept() # Fallback
            
            if list(self.used_philosophers):
                primary_philosopher = self.get_weighted_philosopher(subset=self.used_philosophers)
            else:
                primary_philosopher = self.get_weighted_philosopher() # Fallback
            
            if list(self.used_terms):
                primary_term = self.get_weighted_term(subset=self.used_terms, exclude={primary_concept})
            else:
                primary_term = self.get_weighted_term(exclude={primary_concept}) # Fallback
        else:
            # Default behavior: get weighted items, avoiding recent if specified
            exclude_concepts = self.used_concepts if avoid_recent else set()
            primary_concept = self.get_weighted_concept(exclude=exclude_concepts)
            
            exclude_philosophers = self.used_philosophers if avoid_recent else set()
            # Try to link philosopher to primary_concept if possible
            if primary_concept and primary_concept in self.philosopher_concepts:
                candidates = [p for p, c_list in self.philosopher_concepts.items() if primary_concept in c_list and p not in exclude_philosophers]
                if candidates:
                    primary_philosopher = random.choice(candidates)
                else: # Fallback to general weighted philosopher
                    primary_philosopher = self.get_weighted_philosopher(exclude=exclude_philosophers)
            else: # General weighted philosopher if no primary_concept or no links
                primary_philosopher = self.get_weighted_philosopher(exclude=exclude_philosophers)
            
            exclude_terms = self.used_terms if avoid_recent else set()
            primary_term = self.get_weighted_term(exclude=exclude_terms.union({primary_concept}))

        # Ensure fallbacks if any primary element is still None
        if primary_concept is None: primary_concept = random.choice(self.concepts)
        if primary_philosopher is None: primary_philosopher = random.choice(self.philosophers)
        if primary_term is None: primary_term = random.choice([t for t in self.terms if t != primary_concept] or self.terms)

        # Record usage of the chosen theme elements for this section
        self.record_usage(
            concepts=[primary_concept],
            philosophers=[primary_philosopher],
            terms=[primary_term]
        )
        
        return {
            'primary_concept': primary_concept,
            'primary_philosopher': primary_philosopher,
            'primary_term': primary_term,
            'context_phrase': self.get_theme_context_phrase(),
            'related_adjective': self.get_theme_related_adjective()
        }

    def get_theme_context_phrase(self):
        """Returns a random context phrase from the active theme, if any."""
        if self.active_theme_key and self.active_theme_data.get('context_phrases'):
            return random.choice(self.active_theme_data['context_phrases'])
        return "" # Return empty if no active theme or no phrases

    def get_theme_related_adjective(self):
        """Returns a random related adjective from the active theme, if any."""
        if self.active_theme_key and self.active_theme_data.get('related_adjectives'):
            return random.choice(self.active_theme_data['related_adjectives'])
        return "" # Return empty
        
    def get_philosopher_key_work_citation(self, philosopher_name):
        """ Returns a formatted citation for a key work of a philosopher. """
        if philosopher_name in self.philosopher_key_works and self.philosopher_key_works[philosopher_name]:
            work_title, year = random.choice(self.philosopher_key_works[philosopher_name])
            # Basic citation, could be expanded to full MLA/Chicago if needed
            return f"{philosopher_name}'s *{work_title}* ({year})"
        return philosopher_name # Fallback to just philosopher name

    def get_random_quote(self, philosopher_name=None):
        """ Gets a random quote, optionally for a specific philosopher from active theme or primary list. """
        from json_data_provider import quotes # Import here to avoid circular dependency if data.py imports this module
        
        options = []
        if philosopher_name and philosopher_name in quotes:
            options.extend(quotes[philosopher_name])
        elif self.active_theme_key:
            for p in self.active_theme_data.get('core_philosophers', []):
                if p in quotes:
                    options.extend(quotes[p])
        
        if not options: # Fallback to any philosopher in primary list or then any quote
            for p in self.primary_philosophers:
                if p in quotes:
                    options.extend(quotes[p])
        
        if not options: # Wider fallback
             all_quotes = [q for q_list in quotes.values() for q in q_list]
             if all_quotes: return random.choice(all_quotes), "Unknown" # Philosopher unknown if general fallback

        if options:
            # Try to attribute the quote correctly
            chosen_quote = random.choice(options)
            for p, q_list in quotes.items():
                if chosen_quote in q_list:
                    return f"\"{chosen_quote}\" - {p}", p # Return quote and philosopher
            return f"\"{chosen_quote}\"", "Attributed" # Fallback attribution
            
        return None, None # No quote found

    def get_theme_specific_term(self, term_type, fallback_to_general=True):
        """Get a term specific to the active theme, or a general term if none are available."""
        if self.active_theme_key and self.active_theme_data.get(term_type):
            return random.choice(self.active_theme_data[term_type])
        elif fallback_to_general:
            return self.get_weighted_term()
        return None