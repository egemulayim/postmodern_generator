# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Additional citation styles (APA, Chicago)
- HTML and LaTeX output formats
- Web-based user interface
- API integration
- Expanded knowledge base with emerging theorists

## [0.1.2] - 2025-06-02

### Added
- **Dynamic Weight Adjustment**: Implemented a dynamic weighting system in `coherence.py` (specifically in the `record_usage` method). This system adjusts the selection probability of concepts, terms, and philosophers during essay generation by: 
    - Decaying the weight of items already used, reducing immediate repetition.
    - Boosting the weight of concepts related to a recently used concept, and concepts associated with a recently used philosopher, to enhance local thematic coherence.
    - Default decay factor is 0.8 and related boost factor is 1.2, configurable in `record_usage` calls.
- **Enhanced Sentence Complexity and Variety**: Implemented new sentence construction patterns in `sentence.py` and `postmodern_sentence.py` to generate more diverse and grammatically sophisticated sentence structures. This reduces repetition and enhances readability.
- **Refined Abstract Generation**: Updated algorithms in `abstract_generator.py` to produce abstracts that are more thematically focused, concise, and representative of the essay's core arguments.
- **CLI Export Option**: Added `--export` and `--no-export` command-line arguments to predetermine whether essays will be exported as Markdown files, eliminating the need for post-generation user prompts and enabling fully automated essay generation workflows.
- **Interactive Help System**: Added 'h' option during theme selection to display CLI command examples and usage tips. Enhanced the interactive interface with helpful prompts informing users about `--help` option for comprehensive command-line documentation.
- **Interactive Theme Information Screen**: Added a new feature in `main.py` accessible from the theme selection menu. Users can now input 'i' to view a dedicated screen displaying a numbered list of all available themes along with their full descriptions. The screen clears for readability and refreshes back to the theme selection menu upon exit, preserving the session's seed.

### Changed
- **Performance Optimization**: Optimized core logic in `coherence.py` and `essay.py`, particularly in theme selection and dialectical progression algorithms, leading to faster generation times for complex and lengthy essays.
- **Theme Selection UI**: Removed the short parenthetical descriptions from the theme selection list in `main.py` as full descriptions are now available on the new theme information screen.

### Fixed
- **Critical Import Issues in sentence.py**: Fixed improper local definitions of `citation_relationships` and `philosophical_movements` as empty dictionaries. These are now properly imported from `json_data_provider.py`, ensuring access to 20 philosophical movements and proper citation relationship mapping.
- **Coherence Manager Integration**: Fixed inconsistent key usage in `_populate_context_fields` function where coherence_manager was expected under `'_coherence_manager'` key but stored under `'coherence_manager'` key.
- **Template Field Processing**: Corrected field checking logic in `_populate_context_fields` to properly handle template placeholders without curly braces.
- **Markdown Export Formatting**: Resolved a minor issue in `md_export.py` where extremely long essay titles could cause minor formatting inconsistencies in the metadata block of exported Markdown files.

### Enhanced
- **Sentence-Level Thematic Guidance**: Improved integration between sentence generation and the coherence manager, ensuring philosopher and concept selection aligns with active themes and dynamic weight adjustments.
- **Error Handling**: Enhanced fallback mechanisms in sentence generation to gracefully handle missing data while maintaining thematic coherence.
- **Code Consistency**: Standardized data key usage across sentence generation functions for better maintainability.

### Tested
- Verified functionality with multiple themes ("Digital Subjectivity", "Queer Theory") and different seeds
- Confirmed proper philosopher relationship mapping and citation generation
- Validated coherence manager integration across all sentence types (introduction, general, conclusion)
- Tested CLI export options with various argument combinations

## [0.1.15] - 2025-06-01

### Added
- **Advanced Concept Relationships**: Implemented a more advanced system for defining relationships between concepts in `data.json` (via `concept_relation_details`) and `coherence.py`. This includes relationship types (e.g., 'critiques', 'is_foundational_to', 'complements') and strength modifiers.
- **Refined Dialectical Progression**: Enhanced the `develop_dialectic` method in `coherence.py` to leverage the new concept relationship strengths and types, enabling a more nuanced Thesis-Antithesis-Synthesis progression in essay structure. This logic is integrated into `essay.py` for section theme generation.
- **Expanded Concept Coverage**: Significantly increased the number of defined relationships in `concept_relation_details` within `data.json` to cover a broader range of concepts.

### Changed
- **Data File Path**: Modified `json_data_provider.py` to determine the `data.json` file path dynamically relative to the script's location. This removes the hardcoded absolute path, ensuring the project runs correctly in different environments and for various users.

## [0.1.1] - 2025-06-01 

### Fixed
- **Citation Generation Robustness**:
    - Enhanced fallbacks in `reference.py` for `generate_reference`, `generate_title`, and `generate_full_name` to prevent empty or malformed bibliographic entries.
    - Strengthened `NoteSystem` in `notes.py` (methods like `_create_parenthetical_citation_string`, `_generate_commentary`, `add_citation`, and author/topic extraction helpers) with robust fallbacks. This ensures complete and plausible parenthetical citations, substantive note content, and in-text markers, minimizing the possibility of missing or incomplete citations.
    - Improved citation handling in `sentence.py` (`_process_citation_placeholders`, `_handle_citation_marker`) to use clear, generic placeholders (e.g., `(General Citation Placeholder)`) if any underlying citation generation step were to result in an empty string, ensuring no invisible/empty citations.
- **MLA Punctuation for Quotes and Citations**:
    - Refined logic in `_format_quote_for_academic_style` (`sentence.py`) to correctly handle punctuation within quotes (periods, question marks, exclamation points, commas) according to MLA style.
    - Overhauled `_finalize_sentence` (`sentence.py`) to ensure correct placement of sentence-ending punctuation (periods after parenthetical citations, handling of ?/! within quotes followed by citation and final period).

### Changed
- Minor internal improvements to string formatting in `reference.py` to enhance linter compatibility.

## [0.1.0] - 2025-05-31

This version represents a fundamental architectural overhaul and the first stable release of the modernized Postmodern Generator.

### Added
- **Thematic Clustering System**: 11 thematic clusters for targeted essay generation
  - Power and Knowledge
  - Identity and Subjectivity  
  - Postmodernity and Critique of Metanarratives
  - Technology, Media, and Culture
  - Decoloniality and Postcolonial Studies
  - Affect, Materiality, and the Posthuman
  - Critical Pedagogy and Liberatory Education
  - Speculative Realism and Object-Oriented Ontology
  - Psychoanalysis and Culture
  - Feminist Epistemologies and Standpoint Theory
  - Digital Subjectivity (new contemporary theme)

- **Enhanced Command-Line Interface**: Professional CLI with argument parsing
  - `--seed` argument for reproducible generation
  - `--theme` argument for targeted thematic focus
  - Interactive theme selection with descriptions
  - Comprehensive error handling and user guidance

- **Markdown Export System**: Complete export functionality
  - Essay metadata tracking (seed, theme, timestamp)
  - Automatic file management in `essays/` directory
  - User-friendly filename input with validation
  - Export configuration preservation

- **JSON-Based Data Architecture**: Robust, extensible knowledge management
  - `data.json`: Comprehensive 2,847-line knowledge base
  - `json_data_provider.py`: Centralized data access with error handling
  - Default fallbacks for missing or corrupted data
  - Type validation and safety checks

- **Enhanced Academic Features**:
  - Expanded philosopher-concept relationship mapping
  - Advanced concept clustering and oppositional pairs
  - Enhanced citation relationships between philosophers
  - Philosophical movement categorizations
  - Extended academic vocabulary and rhetorical devices

### Changed
- **Complete Data System Overhaul**: Migrated from Python modules to JSON architecture
  - Consolidated `data.py` and `quotes.py` into unified `data.json`
  - Improved data organization and accessibility
  - Better error handling and recovery mechanisms

- **Enhanced Coherence Management**: Significantly improved thematic consistency
  - Theme-specific philosopher and concept selection
  - Better title theme extraction and prioritization
  - Improved dialectical progression development
  - Enhanced concept relationship tracking

- **Streamlined Code Organization**: 
  - Centralized data access patterns
  - Reduced code duplication across modules
  - Improved separation of concerns
  - Better error handling throughout codebase

- **Improved Essay Generation Pipeline**:
  - Better integration between components
  - Enhanced metafictional element integration
  - Improved citation system integration
  - More template variety management

- **Updated Documentation**:
  - Comprehensive README updates reflecting new features
  - Enhanced installation and usage instructions
  - Detailed thematic cluster documentation
  - Updated roadmap and feature descriptions

### Removed
- **Consolidated Template Files**: 
  - `enhanced_sentence.py`: Templates integrated into `postmodern_sentence.py`
  - Eliminated redundancy while preserving all functionality

- **Legacy Data Modules**:
  - `data.py`: Replaced by JSON-based system
  - `quotes.py`: Integrated into unified data structure

- **Minimal Utility Files**:
  - `section.py`: Functionality absorbed into other modules
  - Reduced file count while maintaining capabilities

- **Phantom Dependencies**: 
  - Identified numpy and nltk as unused dependencies (still in requirements.txt but unused)

### Technical Improvements
- **Error Handling**: Comprehensive try-catch blocks and graceful degradation
- **Data Validation**: Type checking and safety measures throughout
- **Performance**: More efficient data access and reduced memory footprint
- **Maintainability**: Better code organization and documentation
- **Extensibility**: JSON-based architecture supports easy expansion

### Academic Enhancements
- **Authentic Relationships**: Enhanced philosopher-concept mappings based on actual theoretical work
- **Thematic Sophistication**: Deep integration of theoretical frameworks and contexts
- **Citation Accuracy**: Improved MLA 9 compliance and authentic work attribution
- **Template Variety**: Expanded template collection with academic authenticity
- **Metafictional Integration**: Better self-referential element placement and variety

### User Experience Improvements
- **Interactive Theme Selection**: User-friendly theme browsing with descriptions
- **Professional CLI**: Intuitive command-line interface with helpful error messages
- **Export Functionality**: Seamless essay export with comprehensive metadata
- **Reproducibility**: Reliable seed-based generation for consistent output
- **Configuration Flexibility**: Multiple ways to specify generation parameters

---

## Development Notes

**Version 0.1.0** marks the transition from a proof-of-concept to a production-ready academic text generator. The architectural changes lay the foundation for future enhancements while significantly improving the quality and consistency of generated content.

**Breaking Changes**: This version requires Python 3.8+ and introduces a new command-line interface. Previous direct function calls may need updating to work with the new architecture.

**Migration Guide**: Users upgrading from pre-1.0 versions should note the new CLI interface and thematic clustering system. All previous functionality is preserved but accessed through the new interface.

**Contributor Notes**: The JSON-based data architecture makes it easier to contribute new content. See the contributing guidelines in README.md for details on extending the knowledge base.