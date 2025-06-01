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
    citation_relationships, philosophical_movements,
    concept_relation_details
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
        """Build a graph of related concepts with strength and type, including explicit typed relations."""
        relationships = defaultdict(lambda: defaultdict(lambda: {"strength": 0, "type": "related"}))
        
        # 1. From philosopher_concepts (co-occurrence)
        for philo_concepts_list in self.philosopher_concepts.values():
            for i in range(len(philo_concepts_list)):
                for j in range(i + 1, len(philo_concepts_list)):
                    c1, c2 = philo_concepts_list[i], philo_concepts_list[j]
                    if c1 in self.concepts and c2 in self.concepts:
                        relationships[c1][c2]["strength"] += 1
                        relationships[c2][c1]["strength"] += 1
        
        # 2. From thematic_clusters (co-occurrence in themes)
        for theme_data in thematic_clusters.values():
            core_concepts = [c for c in theme_data.get('key_concepts', []) if c in self.concepts]
            relevant_terms_as_concepts = [t for t in theme_data.get('relevant_terms', []) if t in self.concepts]
            all_theme_related_concepts = list(set(core_concepts + relevant_terms_as_concepts))
            for i in range(len(all_theme_related_concepts)):
                for j in range(i + 1, len(all_theme_related_concepts)):
                    c1, c2 = all_theme_related_concepts[i], all_theme_related_concepts[j]
                    boost = 1
                    if c1 in core_concepts and c2 in core_concepts: boost = 3
                    elif c1 in core_concepts or c2 in core_concepts: boost = 2
                    relationships[c1][c2]["strength"] += boost
                    relationships[c2][c1]["strength"] += boost

        # 3. From oppositional_pairs (explicit opposition)
        for c1, c2 in oppositional_pairs:
            if c1 in self.concepts and c2 in self.concepts:
                relationships[c1][c2]["type"] = "oppositional"
                relationships[c1][c2]["strength"] += 5 
                relationships[c2][c1]["type"] = "oppositional"
                relationships[c2][c1]["strength"] += 5

        # 4. From concept_relation_details (explicit typed relationships from data.json)
        for relation in concept_relation_details: # Assumes concept_relation_details is imported
            c1 = relation.get("concept1")
            c2 = relation.get("concept2")
            rel_type = relation.get("relation_type")
            strength_mod = relation.get("strength_modifier", 0)
            if c1 in self.concepts and c2 in self.concepts and rel_type:
                # Apply the primary relationship
                relationships[c1][c2]["type"] = rel_type
                relationships[c1][c2]["strength"] += strength_mod
                
                # Attempt to define an inverse relationship type if not explicitly provided
                # This is heuristic and can be expanded.
                inverse_type = None
                if rel_type.startswith("is_") and "_by" not in rel_type and "_of" not in rel_type and "_for" not in rel_type:
                    inverse_type = rel_type[3:] # e.g., "is_critiqued_by" -> "critiqued"
                elif "_by" in rel_type:
                    inverse_type = rel_type.replace("_by", "s") # e.g., "is_critiqued_by" -> "critiques"
                elif rel_type.endswith("s"): # e.g., critiques
                    inverse_type = "is_" + rel_type[:-1] + "ed_by" # critiques -> is_critiqued_by
                # Add more sophisticated inverse type mapping as needed

                if inverse_type: # If an inverse type could be determined or was predefined for symmetry
                    relationships[c2][c1]["type"] = inverse_type
                    relationships[c2][c1]["strength"] += strength_mod # Apply strength modifier symmetrically
                else: # If no obvious inverse, mark as generically related but still apply strength
                    if relationships[c2][c1]["type"] == "related": # Only overwrite if it's still generic
                         relationships[c2][c1]["type"] = "related_to_typed" # Mark as related due to an explicit typed relation from c1
                    relationships[c2][c1]["strength"] += strength_mod
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
        """Get a philosopher based on current weights and thematic relevance."""
        # Ensure `philosophers` (the global list) is accessible or use `self.philosophers`
        theme_philosophers = self.active_theme_data.get('core_philosophers', []) if self.active_theme_data else []
        return self._get_weighted_items(self.philosophers, self.philosopher_weights, exclude, theme_philosophers, subset=subset)

    def get_related_concept(self, concept_name, exclude=None): # Renamed arg from concept to concept_name
        """Get a concept related to concept_name, favoring stronger relationships."""
        if concept_name not in self.concept_relationships:
            # Fallback: if no relationships known, pick a random concept not in exclude or self.
            available_concepts = [c for c in self.concepts if c != concept_name and (not exclude or c not in exclude)]
            return random.choice(available_concepts) if available_concepts else None

        related_options = self.concept_relationships[concept_name]
        
        # Filter out excluded concepts and the concept itself
        valid_options = {
            rel_concept: data
            for rel_concept, data in related_options.items()
            if rel_concept != concept_name and (not exclude or rel_concept not in exclude) and data.get("type", "related") == "related"
        }

        if not valid_options:
            # Fallback if no valid *related* options, try any non-excluded concept
            available_concepts = [c for c in self.concepts if c != concept_name and (not exclude or c not in exclude)]
            return random.choice(available_concepts) if available_concepts else None

        # Weigh by strength
        choices = []
        weights = []
        for concept, data in valid_options.items():
            choices.append(concept)
            weights.append(data.get("strength", 1)) # Default strength 1 if somehow missing
        
        if not choices: # Should be covered by valid_options check, but as safeguard
            return random.choice([c for c in self.concepts if c != concept_name and (not exclude or c not in exclude)] or [None])

        return random.choices(choices, weights=weights, k=1)[0]

    def get_oppositional_concept(self, concept_name, exclude=None): # Renamed arg
        """Get a concept oppositional to concept_name."""
        # 1. Check explicit oppositional_pairs first (via concept_relationships type)
        if concept_name in self.concept_relationships:
            oppositional_options = {
                rel_concept: data
                for rel_concept, data in self.concept_relationships[concept_name].items()
                if rel_concept != concept_name and (not exclude or rel_concept not in exclude) and data.get("type") == "oppositional"
            }
            if oppositional_options:
                # Weigh by strength if multiple explicit oppositions exist (though usually direct pairs)
                choices = []
                weights = []
                for concept, data in oppositional_options.items():
                    choices.append(concept)
                    weights.append(data.get("strength", 1))
                if choices:
                    return random.choices(choices, weights=weights, k=1)[0]

        # 2. Fallback: if no explicit oppositional relationship found in concept_relationships,
        #    look for the original oppositional_pairs list from data.json
        for c1, c2 in oppositional_pairs:
            if c1 == concept_name and (not exclude or c2 not in exclude):
                return c2
            if c2 == concept_name and (not exclude or c1 not in exclude):
                return c1
        
        # 3. Further Fallback: if no direct opposition, pick a concept that is NOT strongly related (low strength or not related)
        # This is a more complex heuristic. For now, let's keep it simpler.
        # If no explicit opposition, we might return a weakly related concept or a random one not strongly related.
        # For now, if no explicit opposition, pick a random concept not in exclude or self, and not strongly related.
        
        potential_opposites = []
        if concept_name in self.concept_relationships:
            related_concepts_data = self.concept_relationships[concept_name]
            for c in self.concepts:
                if c == concept_name or (exclude and c in exclude):
                    continue
                # If not related, or weakly related, consider it a potential (weak) opposite
                if c not in related_concepts_data or related_concepts_data[c].get("strength", 0) <= 1: # Threshold for "weakly related"
                    potential_opposites.append(c)
        else: # If concept_name has no relationships recorded, any other concept is a potential opposite
            potential_opposites = [c for c in self.concepts if c != concept_name and (not exclude or c not in exclude)]

        if potential_opposites:
            return random.choice(potential_opposites)
        
        # Absolute fallback: a random concept different from concept_name
        fallback_concepts = [c for c in self.concepts if c != concept_name and (not exclude or c not in exclude)]
        return random.choice(fallback_concepts) if fallback_concepts else None

    def develop_dialectic(self, starting_concept, num_steps=3):
        """
        Develop an advanced dialectical progression of concepts for essay sections.
        Uses relationship strengths and explicitly defined types for a nuanced progression.
        Aims for Thesis -> Antithesis -> Synthesis/Development(s).
        """
        if not starting_concept or starting_concept not in self.concepts:
            starting_concept = self.get_weighted_concept() or (random.choice(self.concepts) if self.concepts else "postmodernism")

        progression = [starting_concept]
        excluded_from_progression = {starting_concept}

        current_thesis = starting_concept

        for i in range(num_steps - 1): # num_steps includes the initial thesis
            next_concept_in_dialectic = None
            
            # Step 1: Find Antithesis to the current_thesis
            if i == 0:
                # Priority: 1. Explicit "oppositional", 2. Explicit "critiques" current_thesis
                # 3. Fallback to general get_oppositional_concept (which has its own fallbacks)
                found_antithesis = False
                if current_thesis in self.concept_relationships:
                    candidates = []
                    for rel_concept, data in self.concept_relationships[current_thesis].items():
                        if rel_concept not in excluded_from_progression:
                            if data.get("type") == "oppositional":
                                candidates.append((rel_concept, data.get("strength", 0) + 10)) # Prioritize oppositional
                            elif data.get("type") == "critiques": # Assuming c1 critiques c2 is stored as rel[c2][c1] type="critiques"
                                candidates.append((rel_concept, data.get("strength", 0) + 5))
                    if candidates:
                        candidates.sort(key=lambda x: x[1], reverse=True)
                        next_concept_in_dialectic = candidates[0][0]
                        found_antithesis = True
                
                if not found_antithesis:
                    next_concept_in_dialectic = self.get_oppositional_concept(current_thesis, exclude=excluded_from_progression)
                
                if next_concept_in_dialectic:
                    current_antithesis = next_concept_in_dialectic # Store for synthesis step
                else: # Major fallback if no antithesis can be found
                    next_concept_in_dialectic = self.get_weighted_concept(exclude=excluded_from_progression)
                    if not next_concept_in_dialectic: break # Cannot continue progression
                    current_antithesis = next_concept_in_dialectic # Treat this as the antithesis for next step

            # Step 2+: Synthesis or Further Development
            else:
                previous_concept = progression[-1] # The result of the last step (could be an antithesis or a synthesis)
                
                synthesis_candidates = []
                # Try to find concepts that EXTEND or offer a RESOLUTION/SYNTHESIS related to previous_concept (antithesis or prior synthesis)
                # Or concepts strongly related to BOTH original thesis and current antithesis/previous_concept

                # Option A: Find concepts that extend/resolve the previous_concept
                if previous_concept in self.concept_relationships:
                    for rel_c, data in self.concept_relationships[previous_concept].items():
                        if rel_c not in excluded_from_progression:
                            rel_type = data.get("type", "related")
                            strength = data.get("strength", 0)
                            if rel_type in ["extends", "resolves", "synthesizes_with"]:
                                synthesis_candidates.append((rel_c, strength + 10, "direct_development"))
                            elif rel_type == "related" and strength > 3: # Strong general relation
                                synthesis_candidates.append((rel_c, strength, "strong_related"))
                
                # Option B: Bridge between original thesis and current antithesis/previous_concept
                if 'current_antithesis' in locals() and current_antithesis: # Ensure antithesis was set
                    thesis_relations = self.concept_relationships.get(current_thesis, {})
                    antithesis_relations = self.concept_relationships.get(current_antithesis, {})
                    
                    for rel_to_thesis, data_thesis in thesis_relations.items():
                        if rel_to_thesis in antithesis_relations and rel_to_thesis not in excluded_from_progression:
                            # Found a concept related to both
                            combined_strength = data_thesis.get("strength",0) + antithesis_relations[rel_to_thesis].get("strength",0)
                            synthesis_candidates.append((rel_to_thesis, combined_strength, "bridge"))

                # Option C: Example or Context for the previous concept
                if previous_concept in self.concept_relationships:
                     for rel_c, data in self.concept_relationships[previous_concept].items():
                        if rel_c not in excluded_from_progression:
                            rel_type = data.get("type", "related")
                            strength = data.get("strength", 0)
                            if rel_type in ["is_example_of", "provides_context_for"]:
                                synthesis_candidates.append((rel_c, strength + 5, "elaboration"))
                
                if synthesis_candidates:
                    synthesis_candidates.sort(key=lambda x: x[1], reverse=True) # Sort by strength
                    next_concept_in_dialectic = synthesis_candidates[0][0]
                else:
                    # Fallback: get a concept generally related to the previous one
                    next_concept_in_dialectic = self.get_related_concept(previous_concept, exclude=excluded_from_progression)
                    if not next_concept_in_dialectic: # Broader fallback
                        next_concept_in_dialectic = self.get_weighted_concept(exclude=excluded_from_progression)
            
            # Add to progression
            if next_concept_in_dialectic and next_concept_in_dialectic not in excluded_from_progression:
                progression.append(next_concept_in_dialectic)
                excluded_from_progression.add(next_concept_in_dialectic)
                # Update current_thesis for the next potential antithesis if we are in a multi-stage development that resets the dialectic.
                # For a simple T-A-S, current_thesis remains the original. For T-A-S1-A2-S2, it might shift.
                # For now, we keep current_thesis as the original starting_concept for finding antitheses for simplicity in T-A-S structure.
                # If further development steps (i > 1) should treat the previous synthesis as a new thesis, this logic would need adjustment.
            else:
                # If truly stuck (e.g. ran out of concepts or all valid ones excluded)
                final_fallback = self.get_weighted_concept(exclude=excluded_from_progression)
                if final_fallback and final_fallback not in excluded_from_progression:
                    progression.append(final_fallback)
                    excluded_from_progression.add(final_fallback)
                else:
                    break # Stop if no new concept can be added
        
        # Final check for uniqueness, though `excluded_from_progression` should handle it.
        final_progression = []
        seen_in_final = set()
        for concept in progression:
            if concept not in seen_in_final:
                final_progression.append(concept)
                seen_in_final.add(concept)
        return final_progression

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