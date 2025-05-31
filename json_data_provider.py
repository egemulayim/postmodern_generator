"""
A module for providing data to the postmodern essay generator.
This module loads data from a JSON file and provides it to other modules.
It also provides default data if the JSON file is not found or corrupt.
"""

import json
import os

# Define the path to data.json in the workspace root
DATA_FILE_NAME = "data.json"
WORKSPACE_ROOT = "/Users/egemulayim/postmodern_generator-dev"  # Provided by user_info
ABSOLUTE_DATA_FILE_PATH = os.path.join(WORKSPACE_ROOT, DATA_FILE_NAME)

# Default empty structures for all expected data keys
DEFAULT_DATA = {
    "thematic_clusters": {},
    "philosophers": [],
    "concepts": [],
    "italicized_terms": [],
    "terms": [],
    "LOWERCASE_WORDS": [],
    "NAME_SUFFIXES": [],
    "philosopher_concepts": {},
    "contexts": [],
    "adjectives": [],
    "bibliography_title_templates": [],
    "publishers": [],
    "academic_journals": [],
    "conferences": [],
    "locations": [],
    "philosopher_key_works": {},
    "NON_STANDARD_AUTHOR_FORMATS": {},
    "quotes": {},
    "verbs": [],
    "nouns": [],
    "prepositions": [],
    "conjunctions": [],
    "title_templates": [],
    "academic_vocab": {"verbs": [], "nouns": [], "adjectives": [], "adverbs": []},
    "oppositional_pairs": [],
    "citation_relationships": {},
    "philosophical_movements": {},
    "METAFICTIONAL_TEMPLATES": [],
    "METAFICTIONAL_CONCLUSIONS": [],
    "rhetorical_devices": ["default rhetorical device"],  # Added back with a default
    "discursive_modes": ["default discursive mode"],    # Added back with a default
    "PROPER_NOUNS": []
}

_data_store = {}

try:
    with open(ABSOLUTE_DATA_FILE_PATH, 'r', encoding='utf-8') as f:
        _data_store = json.load(f)
    # print(f"Successfully loaded data from {ABSOLUTE_DATA_FILE_PATH}") # Optional: for debugging
except FileNotFoundError:
    print(f"Warning: {ABSOLUTE_DATA_FILE_PATH} not found. Using default empty data structures for all keys.")
    _data_store = DEFAULT_DATA # Use all defaults if file not found
except json.JSONDecodeError:
    print(f"Warning: Error decoding JSON from {ABSOLUTE_DATA_FILE_PATH}. Using default empty data structures for all keys.")
    _data_store = DEFAULT_DATA # Use all defaults if JSON is corrupt
except Exception as e:
    print(f"An unexpected error occurred while loading {ABSOLUTE_DATA_FILE_PATH}: {e}. Using default empty data structures for all keys.")
    _data_store = DEFAULT_DATA # Use all defaults on other errors

# Function to safely get data with a default
def _get_data(key, default_value_from_master_default):
    """
    Safely retrieves a key from the loaded _data_store,
    falling back to the default_value_from_master_default if the key is missing.
    Prints a warning if the key is not found in _data_store and the default is used.
    """
    value = _data_store.get(key) # Try to get value from potentially partially loaded data
    if value is None and key not in _data_store: # Check if key was missing entirely or value was literally None
        # If file was loaded but key is missing, or if file wasn't loaded (_data_store is DEFAULT_DATA)
        # and we're iterating through keys (which means key would be in DEFAULT_DATA).
        # This condition ensures we use the specific default for *this key* if it wasn't in the file.
        value = default_value_from_master_default
        # Avoid warning if _data_store is already DEFAULT_DATA (file not found/error scenarios)
        # because warnings for all keys would be too verbose. Only warn if file loaded but key missing.
        if _data_store is not DEFAULT_DATA:
            print(f"Warning: Key '{key}' not found in {DATA_FILE_NAME}. Using default value.")
    elif value is None and key in _data_store: # Key exists in file, but its value is null
        # print(f"Info: Key '{key}' found in {DATA_FILE_NAME} with a null value. Using it as None.")
        pass # Keep 'value' as None, as it's explicitly set so in the JSON
    return value

# Expose data as module-level variables
# For each key, try to get it from _data_store, if not found, use the specific default from DEFAULT_DATA.
thematic_clusters = _get_data("thematic_clusters", DEFAULT_DATA["thematic_clusters"])
philosophers = _get_data("philosophers", DEFAULT_DATA["philosophers"])
concepts = _get_data("concepts", DEFAULT_DATA["concepts"])
italicized_terms = _get_data("italicized_terms", DEFAULT_DATA["italicized_terms"])
terms = _get_data("terms", DEFAULT_DATA["terms"])
LOWERCASE_WORDS = _get_data("LOWERCASE_WORDS", DEFAULT_DATA["LOWERCASE_WORDS"])
NAME_SUFFIXES = _get_data("NAME_SUFFIXES", DEFAULT_DATA["NAME_SUFFIXES"])
philosopher_concepts = _get_data("philosopher_concepts", DEFAULT_DATA["philosopher_concepts"])
contexts = _get_data("contexts", DEFAULT_DATA["contexts"])
adjectives = _get_data("adjectives", DEFAULT_DATA["adjectives"])
bibliography_title_templates = _get_data("bibliography_title_templates", DEFAULT_DATA["bibliography_title_templates"])
publishers = _get_data("publishers", DEFAULT_DATA["publishers"])
academic_journals = _get_data("academic_journals", DEFAULT_DATA["academic_journals"])
conferences = _get_data("conferences", DEFAULT_DATA["conferences"])
locations = _get_data("locations", DEFAULT_DATA["locations"])
philosopher_key_works = _get_data("philosopher_key_works", DEFAULT_DATA["philosopher_key_works"])
NON_STANDARD_AUTHOR_FORMATS = _get_data("NON_STANDARD_AUTHOR_FORMATS", DEFAULT_DATA["NON_STANDARD_AUTHOR_FORMATS"])
quotes = _get_data("quotes", DEFAULT_DATA["quotes"])
verbs = _get_data("verbs", DEFAULT_DATA["verbs"])
nouns = _get_data("nouns", DEFAULT_DATA["nouns"])
prepositions = _get_data("prepositions", DEFAULT_DATA["prepositions"])
conjunctions = _get_data("conjunctions", DEFAULT_DATA["conjunctions"])
title_templates = _get_data("title_templates", DEFAULT_DATA["title_templates"])
academic_vocab = _get_data("academic_vocab", DEFAULT_DATA["academic_vocab"])
oppositional_pairs = _get_data("oppositional_pairs", DEFAULT_DATA["oppositional_pairs"])
citation_relationships = _get_data("citation_relationships", DEFAULT_DATA["citation_relationships"])
philosophical_movements = _get_data("philosophical_movements", DEFAULT_DATA["philosophical_movements"])
METAFICTIONAL_TEMPLATES = _get_data("METAFICTIONAL_TEMPLATES", DEFAULT_DATA["METAFICTIONAL_TEMPLATES"])
METAFICTIONAL_CONCLUSIONS = _get_data("METAFICTIONAL_CONCLUSIONS", DEFAULT_DATA["METAFICTIONAL_CONCLUSIONS"])
rhetorical_devices = _get_data("rhetorical_devices", DEFAULT_DATA.get("rhetorical_devices", ["fallback device"])) # Added back
discursive_modes = _get_data("discursive_modes", DEFAULT_DATA.get("discursive_modes", ["fallback mode"]))     # Added back
PROPER_NOUNS = _get_data("PROPER_NOUNS", DEFAULT_DATA["PROPER_NOUNS"])

# Ensure that key variables are of the expected type if they were loaded with a value of None from JSON
# For example, if philosophers is critical to be a list:
if philosophers is None:
    print(f"Warning: 'philosophers' was null in {DATA_FILE_NAME}. Defaulting to an empty list.")
    philosophers = []
if concepts is None:
    print(f"Warning: 'concepts' was null in {DATA_FILE_NAME}. Defaulting to an empty list.")
    concepts = []
if terms is None:
    print(f"Warning: 'terms' was null in {DATA_FILE_NAME}. Defaulting to an empty list.")
    terms = []
if PROPER_NOUNS is None:
    print(f"Warning: 'PROPER_NOUNS' was null in {DATA_FILE_NAME}. Defaulting to an empty list.")
    PROPER_NOUNS = []
# Add more checks like this for other critical variables if necessary

# print("json_data_provider.py loaded and data (or defaults) are set.") # Optional: for debugging 