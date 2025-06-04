# Changelog

All notable changes to The Postmodern Generator project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.5] - 2025-06-04

### Fixed
- **Code Quality Improvements**: Comprehensive code review and cleanup to eliminate redundancies and improve maintainability
- **Duplicate Function Removal**: Removed duplicate `_select_theme()` function in `main.py`, replacing with simplified `_select_theme_simple()` wrapper that preserves functionality while improving code organization
- **Legacy Code Cleanup**: Removed commented-out legacy code in `sentence.py` and `coherence.py` that was previously overriding proper imports from `json_data_provider`
- **Debug Code Removal**: Cleaned up commented debug print statements in `json_data_provider.py` for cleaner production code

### Enhanced
- **Function Organization**: Streamlined theme selection logic in `main.py` with clear separation between interactive navigation (`_select_theme_with_navigation`) and simple programmatic selection (`_select_theme_simple`)
- **Import Consistency**: Ensured all modules properly use centralized imports from `json_data_provider.py` without local overrides
- **Code Documentation**: Improved inline documentation and removed outdated comments

### Technical Details
- **Main.py Optimization**: Eliminated redundant theme selection functions while preserving full CLI functionality and interactive navigation
- **Citation System Integrity**: Verified that `citation_relationships` and `philosophical_movements` are properly imported from data provider rather than using empty local dictionaries
- **Data Loading Robustness**: Maintained all error handling and fallback mechanisms in data loading system
- **Compilation Verification**: All core modules now compile cleanly without warnings or errors

### Validation
- **Functionality Testing**: Verified that all essay generation features work correctly after code cleanup
- **Data Integrity**: Confirmed that thematic clusters, philosophers, and concepts load properly (16 themes, 91 philosophers, 97 concepts)
- **CLI Compatibility**: Tested all command-line arguments and interactive features maintain full functionality

## [0.1.4] - 2025-06-04

### Added
- **Sophisticated Metafiction System**: Complete overhaul of metafictional elements with contextual awareness and user control
- **CLI Metafiction Parameter**: New `--metafiction [subtle|moderate|highly_self_aware]` option for controlling self-reflexive intensity
- **Interactive Metafiction Selection**: Added metafiction level selection to interactive CLI mode for complete user control
- **Enhanced Interactive Navigation**: Added comprehensive navigation system with fallback options (`s`, `m`, `i`, `h`) allowing users to modify seed, metafiction level, and theme during interactive mode without restarting
- **Enhanced Export Metadata**: Exported essays now include metafiction level in YAML frontmatter alongside seed, theme, and generation timestamp for complete parameter tracking and reproducibility
- **Strategic Placement Detection**: Advanced linguistic analysis for optimal metafiction placement after bold claims, dense theoretical content, and dialectical transitions
- **Enhanced Template Library**: 50+ new metafictional templates organized by context type and thematic relevance
- **Dialectical Tracking**: Integration with coherence manager to detect thesis/antithesis/synthesis progressions and adjust metafiction accordingly
- **Metafiction Usage Tracking**: Prevention of over-saturation through intelligent distribution tracking
- **Examples Documentation**: Comprehensive examples showing different intensity levels in README

### Enhanced
- **CoherenceManager Integration**: Advanced tracking of dialectical moments and oppositional concept usage
- **Context-Aware Template Selection**: Dynamic selection based on strategic moment type (bold claims, theoretical density, dialectical transitions)
- **Essay Generation Pipeline**: Seamless integration through enhanced `section_context` and `dialectical_context` parameters

### Changed
- **Metafiction Content Focus**: Removed AI/computational references from metafiction templates and replaced with literary, theoretical, and critical self-reflexive elements focusing on textuality, discourse, and academic form rather than machine production
- **CLI Argument Integration**: Updated interactive mode to include metafiction level selection when no CLI arguments are provided

### Technical Implementation
- **`detect_strategic_moment()` Function**: Analyzes paragraph text and calculates strategic scores for placement
- **`should_insert_metafiction()` Function**: Multi-factor decision engine considering section length, essay position, existing metafiction count, and dialectical context
- **Interactive Navigation System**: New `interactive_setup()` and `_select_theme_with_navigation()` functions providing seamless parameter modification during interactive mode
- **Enhanced Export System**: Updated `export_to_markdown()` function to include metafiction level in YAML frontmatter
- **Strategic Placement Indicators**: New data structures defining linguistic patterns for optimal insertion moments
- **Metafiction Configuration System**: Comprehensive configuration with probability thresholds and placement preferences

### Data Architecture
- **METAFICTIONAL_TEMPLATES**: Expanded from basic templates to 50+ context-aware options
- **METAFICTIONAL_CONCLUSIONS**: New templates for sophisticated essay conclusions
- **STRATEGIC_PLACEMENT_INDICATORS**: Linguistic pattern definitions for strategic moment detection
- **METAFICTION_LEVELS**: Configuration system defining behavior for each intensity level

## [0.1.3] - 2025-06-04

### Enhanced
- **Expanded Oppositional Pairs**: Significantly enhanced the `oppositional_pairs` dataset from 20 to 60 high-quality philosophical oppositions
- **Contemporary Theory Integration**: Added oppositions spanning intersectional and decolonial theory, digital/technological dialectics, affect theory and new materialism, climate and Anthropocene studies, queer and trans studies, surveillance capitalism vs. commons concepts, Lacanian psychoanalysis, emergence vs. reductionism, and feminist epistemology
- **Enhanced Dialectical Progression**: Improved `get_oppositional_concept` method and `develop_dialectic` feature with richer conceptual oppositions
- **Improved Thematic Coherence**: Better support for contemporary themes like "Digital Subjectivity," "Decoloniality and Postcolonial Studies," and "Affect, Materiality, and the Posthuman"

### Added
- New oppositional pairs covering 2000-2024 theoretical developments:
  - `surveillance capitalism/digital commons`
  - `racial capitalism/abolition`  
  - `coloniality of power/decoloniality`
  - `settler colonialism/indigenous sovereignty`
  - `cisnormativity/trans becoming`
  - `algorithmic governance/digital resistance`
  - `platform capitalism/cooperative networks`
  - `the Anthropocene/chthulucene`
  - And many others

## [0.1.2] - 2025-06-02

### Added
- **Dynamic Weight Adjustment**: Introduced system for adjusting selection probabilities to improve thematic development and reduce repetition
- **CLI Export Options**: Added `--export` and `--no-export` command-line arguments for automated workflows
- **Interactive Help System**: Added 'h' option during theme selection for CLI examples and usage tips
- **Interactive Theme Details**: Added 'i' option to display detailed, numbered list of all available themes
- **Enhanced Sentence Complexity**: New algorithms for diverse and intricate sentence structures

### Enhanced
- **Abstract Generation Logic**: Improved to produce more thematically focused and representative summaries
- **Performance Optimization**: Optimized core algorithms for faster generation times
- **Coherence Manager Integration**: Improved integration between sentence generation and coherence manager

### Fixed
- **Sentence.py Integration**: Fixed critical import issues where `citation_relationships` and `philosophical_movements` were locally defined instead of imported from `json_data_provider.py`
- **Markdown Export**: Fixed formatting bug for very long titles in metadata section

## [0.1.15] - 2025-06-01

### Added
- **Advanced Concept Relationships**: Implemented system for defining relationships between concepts with types ('critiques', 'is_foundational_to', 'complements') and strength modifiers
- **Refined Dialectical Progression**: New dialectical development system using concept relationship strengths and types for Thesis-Antithesis-Synthesis progression
- **Dynamic Data File Path**: Updated dataset location method to be relative to script location for improved portability

### Enhanced
- **Expanded Concept Relations**: Substantially expanded concept relationships for comprehensive links between concepts
- **Section Theme Generation**: Integrated relationship system for generating section themes

## [0.1.1] - 2025-06-01

### Enhanced
- **Citation Generation**: Significantly improved fallback mechanisms to prevent empty or incomplete bibliographic entries
- **MLA Punctuation**: Updated logic for precise adherence to MLA 9 style punctuation within quotes and sentence-ending punctuation
- **Overall Stability**: Improved reliability and academic authenticity of generated citations

## [0.1.0] - 2025-05-31

### Added
- **Complete Architectural Overhaul**: First stable release of modernized Postmodern Generator
- **JSON-Based Data Architecture**: Migration from Python modules to `data.json` and `json_data_provider.py`
- **Thematic Clustering System**: Introduction of 11 thematic clusters for targeted essay generation
- **Command-Line Interface**: Professional CLI with argparse, theme selection, and export functionality
- **Markdown Export System**: Complete export functionality with essay metadata and file management
- **MLA 9 Citation Compliance**: Proper academic citation formatting

### Enhanced
- **Code Organization**: Centralized data access, better error handling, reduced code duplication
- **Academic Authenticity**: Expanded philosopher-concept relationships and template variety

### Removed
- **Dependencies**: Removed unnecessary dependencies for improved efficiency and self-containment

---

## Version History Summary

- **v0.1.5**: Comprehensive code review and cleanup
- **v0.1.4**: Sophisticated metafiction system with contextual awareness
- **v0.1.3**: Expanded oppositional pairs and enhanced dialectical progression  
- **v0.1.2**: Dynamic weight adjustment and improved user experience
- **v0.1.15**: Advanced concept relationships and dialectical development
- **v0.1.1**: Enhanced citation system and MLA compliance
- **v0.1.0**: Complete architectural overhaul and first stable release

Each version builds upon the previous to create an increasingly sophisticated and academically authentic postmodern essay generator.