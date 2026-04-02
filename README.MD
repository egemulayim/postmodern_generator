# The Postmodern Generator

Welcome to The Postmodern Generator project. This repository contains the source code for a text generator that produces postmodern-style academic essays with theoretical framing, fictional MLA-like citations, and thematic coherence. This README file will guide you through the setup, usage, and contribution process for the project.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Release Highlights (0.2.0)](#release-highlights-020)
- [Upgrade Notes](#upgrade-notes)
- [Previous Changes](#previous-changes)
- [Installation](#installation)
- [Usage](#usage)
- [Thematic Clusters](#thematic-clusters)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [Known Issues](#known-issues)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Introduction

The Postmodern Generator is a tool designed to generate text that mimics the style of postmodern academic writing. It creates theoretical essays complete with citations, dialectical progressions, and self-referential elements characteristic of postmodern discourse. This project is inspired by the Dada Engine run The Postmodernism Generator that was developed by Andrew C. Bulhak. You can learn more about the original Dada Engine [here](https://dev.null.org/dadaengine/) and see a web-based preview of Bulhak's The Postmodernism Generator [here](https://www.elsewhere.org/journal/pomo).

## Current Project Status

- **Canonical theme contract**: All 16 themes now use one schema in `data.json` with `core_philosophers`, `key_concepts`, `relevant_terms`, `context_phrases`, `academic_sub_fields`, and `title_context_labels`.
- **Theme-core corpus coverage**: All current theme-core philosophers now have supporting `philosopher_concepts`, `philosopher_key_works`, and `quotes` entries, and the active validation suite passes with no warnings.
- **Non-interactive CLI flows**: Any CLI invocation now bypasses interactive setup. `--list-themes` prints the valid theme keys with descriptions, `--export` writes directly to `essays/`, and `--output <filename>` lets you choose the export filename explicitly.
- **Selective notes**: Substantive notes are now capped and reused more aggressively so the essay body remains primary.
- **Validation, smoke tests, and seeded regression fixtures**: `python3 scripts/validate_data.py` validates the data contract, `python3 -m unittest` covers schema validation, theme smoke tests, heading limits, note caps, CLI export behavior, and seeded surface regressions for historically noisy themes, and `python3 scripts/capture_surface_regressions.py` refreshes the local fixture baseline when intentional title/keyword changes are made.
- **Normalized lexical contract**: `academic_vocab` is now treated consistently as a flat lexical pool (`list[str]`) across the loader, validator, and tests.
- **Curated concept/term contract**: `concepts` now serve as the essay's argumentative spine, `terms` serve as the surrounding discursive vocabulary, and overlap is allowed only through an explicit `hybrid_concept_terms` set. Within each theme, `key_concepts` and `relevant_terms` are now locally disjoint.
- **Complete movement coverage for theme-core philosophers**: `philosophical_movements` now covers every current theme-core philosopher with canonical names only, and movement-based related-philosopher selection now aggregates across multiple shared memberships instead of stopping at the first matching bucket.
- **Canonical citation-relationship coverage**: `citation_relationships` now uses canonical philosopher names only, covers every current theme-core philosopher, and related-philosopher selection now prefers direct citation links before falling back to broader movement proximity.
- **Theme-surface containment**: Titles, abstract keywords, introductions, and first body paragraphs now prefer theme-local concepts, terms, and philosophers before falling back to the global corpus.
- **Stricter first-surface locality**: Quote fallback, paragraph-level companion concept/term selection, and abstract keyword selection now stay inside the active theme more aggressively, reducing residual bleed from adjacent corpora in first-section surfaces.
- **Theme-aware fabricated references**: Generated citations now resolve key works through canonical philosopher names, reuse existing bibliography entries more aggressively, and keep paragraph-level filler citations closer to the active theme.
- **Targeted corpus curation for noisy adjacent themes**: STS, speculative realism, media theory, and psychoanalysis now use narrower theme inventories and cleaner philosopher-concept mappings so they bleed into one another less often.
- **Follow-up corpus tightening for residual drift**: `Power and Knowledge` and `Digital Subjectivity` now use cleaner core concept anchors, reducing recurrent title drift toward `decoloniality` and `cyborg`.
- **Broader seeded review and later-section locality tuning**: Wider post-stabilization seed sweeps now feed targeted sentence and reference locality fixes so later fabricated references stay much closer to the active theme instead of drifting to detached outsider authors.
- **Targeted sentence-layer cleanup**: `sentence.py` now centralizes active-theme/context philosopher selection through small helper utilities, reducing duplicated fallback logic while preserving the stabilized behavior.
- **Citation stance**: Citations and works cited entries are intentionally fictional parody, not factual bibliography.

## Upgrade Notes

Version `0.2.0` is a substantial release. The data contract, validation layer, test suite, CLI surface, and several core generation paths were tightened or reorganized, and the repo now includes new tracked files under `scripts/`, `tests/`, and `tests/fixtures/` while some older paths were removed.

If you already have an older version checked out:

- A normal `git pull` is usually enough if your checkout is clean. Git will handle tracked file additions, deletions, and moves for you.
- You do not need to wipe the codebase just because you are upgrading.
- A fresh clone is only worth doing if your local checkout has extensive uncommitted changes, stale untracked artifacts, or a generally messy worktree that you do not want to reconcile manually.

If you maintain local edits, run the current validation and test entry points after pulling:

- `python3 scripts/validate_data.py`
- `python3 -m unittest`

## Features

- **Complete Essay Generation**: Produces fully-formed academic essays with title, abstract, introduction, body sections, conclusion, notes, and works cited sections
- **Thematic Coherence System**: Advanced clustering with 16 predefined themes for theoretical focus
- **Concept Relationships and Dialectic**: Advanced system for defining concept relations (type and strength), which powers a nuanced dialectical (Thesis-Antithesis-Synthesis) progression in essay structure.
- **Dynamic Weight Adjustment**: A system that dynamically adjusts the selection weights of concepts, terms, and philosophers during essay generation. This includes decaying weights of used items to reduce repetition and boosting related items to enhance local thematic coherence.
- **Theme-Based Generation**: Choose from specialized themes like "Digital Subjectivity," "Decoloniality and Postcolonial Studies," or "Speculative Realism"
- **Interactive Theme Selection**: User-friendly interface for selecting specific themes or random generation
- **Command-Line Interface**: Easy-to-use CLI with seed and theme arguments for reproducible and targeted output
- **CLI Theme Discovery**: `--list-themes` prints the currently available themes and their descriptions without entering interactive mode
- **Theoretical Sophistication**: Incorporates postmodern concepts, philosophers, and theoretical frameworks with authentic relationships
- **MLA-Like Parody Citations**: Generates in-text citations, endnotes, and works cited sections in a deliberately fictional scholarly-parody style
- **Dialectical Progressions**: Develops ideas through dialectical movement across essay sections
- **Metafictional Elements**: Includes self-referential passages typical of postmodern writing
- **Academic Abstracts**: Generates abstracts with keywords and theoretical framing
- **Proper Formatting**: Handles capitalization, italicization, and academic conventions
- **Reproducible Output**: Flexible seed input (specific integer or random) for generating consistent or varied results
- **Lightweight and Efficient**: Does not rely on large language models, ensuring quick and resource-efficient text generation
- **Markdown Export**: Save generated essays as `.md` files with comprehensive metadata including seed, theme, metafiction level, and generation timestamp
- **Enhanced Export Metadata**: Exported essays include detailed YAML frontmatter with generation parameters for reproducibility and analysis
- **JSON-Based Data Architecture**: Robust, extensible knowledge base with advanced error handling and dynamic data file path loading.

## Release Highlights (0.2.0)

Version `0.2.0` is a substantial stabilization and corpus-reconciliation release on top of the historical `0.1.6` baseline.

### **Data Contract And Corpus**
- **Canonical theme schema**: All 16 themes now use one enforced schema in `data.json`, and legacy theme keys are no longer part of the runtime contract.
- **Validator-backed data discipline**: `scripts/validate_data.py` now enforces theme schema, corpus membership, title-label constraints, and root-key integrity.
- **Theme-core philosopher support**: Current theme-core philosophers now have aligned `philosopher_concepts`, `philosopher_key_works`, and `quotes` coverage, eliminating validation warnings for active theme data.
- **Theme restoration and corpus expansion**: Reintroduced and fully supported a number of removed or under-supported figures, including `Simone de Beauvoir`, `Sherry Turkle`, `Sheila Jasanoff`, `John Law`, `Andrew Pickering`, `Marshall McLuhan`, `Walter Benjamin`, `Max Horkheimer`, `Jack Halberstam`, `José Esteban Muñoz`, and `Jane Bennett`.
- **Loader/schema normalization**: `academic_vocab` is now explicitly treated as a flat lexical pool (`list[str]`) in the loader, validator, and tests.
- **Lexical-role curation**: `concepts` and `terms` now overlap only through an explicit `hybrid_concept_terms` set, and theme-local concept/term duplication is rejected by validation.
- **Movement taxonomy normalization**: `philosophical_movements` now uses canonical philosopher names only, covers every active theme-core philosopher, and no longer contains dead runtime entries that were absent from the root philosopher pool.
- **Citation-relationship normalization**: `citation_relationships` now uses canonical philosopher names only, covers every active theme-core philosopher, and no longer contains legacy aliases or sparse theme-core gaps.

### **Generator Behavior**
- **Selective notes policy**: Notes are now capped and reused more aggressively, reducing note inflation and keeping the main essay body primary.
- **Title and heading cleanup**: Section titles now use title-safe theme labels rather than raw context phrases, and the smoke tests enforce a body-heading length cap.
- **Coherence fixes**: Repetition control now uses real usage counters instead of set-based pseudo-counting, and high-visibility essay surfaces lean more reliably on active-theme material.
- **Related-philosopher selection cleanup**: Sentence generation now prefers direct outgoing and reverse incoming citation links before falling back to aggregated movement matches.
- **Theme-surface containment pass**: Title generation, abstract keyword curation, introduction sentences, and opening body paragraphs now enforce stronger theme-local selection before allowing global fallback.
- **Qualitative corpus-curation pass**: Pruned over-broad bridge-philosopher mappings and tightened STS, speculative realism, media-theory, and psychoanalytic inventories to reduce adjacent-theme bleed.
- **Second corpus-tightening pass**: Removed the strongest residual title-anchor drift in `Power and Knowledge` and `Digital Subjectivity` by narrowing their active concept inventories.
- **Surface-local fallback tightening**: Quote generation, paragraph setup, and abstract keyword selection now keep first-section companion concepts, terms, and philosophers inside the active theme before broader fallback is considered.
- **Theme-aware reference generation**: `NoteSystem` now resolves curated key works through canonical philosopher names, reuses exact existing references when the same author/title recurs, and keeps generated bibliography titles closer to paragraph context.
- **Broader seeded qualitative review**: A wider post-stabilization seed sweep now informs follow-up quality work instead of relying on isolated spot checks.
- **Later-section bibliography locality fixes**: Sentence-level contextual reference generation now keeps detached fabricated references inside the active theme when the cited author is not actually present in the paragraph context.
- **Sentence-layer cleanup**: `sentence.py` now uses shared helper utilities for active-theme and contextual philosopher selection, reducing duplicated fallback logic while preserving current output behavior.
- **CLI/export cleanup**: Any CLI argument triggers non-interactive execution, `--export` no longer prompts, and `--output` supports explicit filenames while implying export.
- **CLI surface organization**: The parser help, interactive help view, theme validation, and export argument rules now follow the same contract, including a dedicated `--list-themes` discovery path and explicit rejection of `--output` with `--no-export`.

### **Validation And Testing**
- **Data validation now passes cleanly**: `python3 scripts/validate_data.py` exits successfully with no warnings on the current dataset.
- **Smoke and CLI tests**: `python3 -m unittest` verifies schema integrity, note budgets, heading limits, and non-interactive export behavior.
- **Surface-local smoke tests**: The smoke suite now explicitly checks theme-local retention in titles, abstract keywords, introductions, and first body sections for historically noisy themes.
- **Seeded regression fixtures**: `tests/fixtures/theme_surface_regressions.json` stores seeded title and keyword baselines plus reference first-heading/first-paragraph samples for the noisiest themes, and `tests/test_generation_regression.py` enforces exact title/keyword continuity alongside theme-retention floors for those surfaces.
- **Relationship validation**: Validation and tests now enforce canonical `citation_relationships`, reject self-links and duplicate targets, and require citation coverage for every current theme-core philosopher.
- **Documentation refresh**: `README.MD` and `CHANGELOG.md` now describe the stabilized generator rather than the earlier recovery-state codebase.

## Previous Changes

<details>
<summary><strong>Click to expand previous version history</strong></summary>

### **v0.1.6 - Introduction and Notes Overhaul**

Version 0.1.6 focused on fixing the missing introduction content and dramatically expanding the quality and variety of generated notes.

### **Fixed**
- **Empty Introduction Section**: Resolved the critical issue where the Introduction section appeared with a header but no content. Added proper introduction paragraph generation with thematic context and relevant philosophers, ensuring substantial content.
- **Essay Structure Completeness**: The introduction now properly follows the abstract and precedes the body sections, with coherent thematic development that connects to the overall essay themes.

### **Enhanced**
- **Notes Section Variety**: Dramatically expanded note template diversity to eliminate repetitive and generic commentary, increasing from a handful of basic categories to a much broader set of academic commentary modes.
- **Enhanced Template Selection**: Improved the note-template selection logic to avoid repetition of recently used categories and templates.
- **Template Tracking System**: Added stronger tracking of recently used note templates and formatted commentaries to maximize variety across generated notes.

### **Technical Implementation**
- **Introduction Generation**: Added complete introduction section generation in `essay.py` with proper paragraph structure, sentence-count management, and thematic coherence.
- **Note Template Architecture**: Expanded the note-template system in `notes.py` into a much larger and more diverse library.
- **Variety Tracking**: Enhanced note-system tracking so recently used note categories, note templates, and formatted commentaries are reused less aggressively.
- **Context-Aware Selection**: Introduction generation now passes title themes, relevant philosophers, and section-positioning context correctly.

### **Quality Improvements**
- **Essay Completeness**: All essay sections now generate proper content, including abstract, introduction, body sections, conclusion, notes, and works cited.
- **Note Authenticity**: Notes now read more like genuine academic commentary instead of generic filler.
- **Thematic Consistency**: The introduction now establishes the essay’s themes more clearly and connects back to the title elements.

### **v0.1.5 - Code Quality and Maintenance**

Version 0.1.5 focused on comprehensive code quality improvements and maintainability enhancements.

### **Fixed**
- **Code Quality Improvements**: Comprehensive code review and cleanup to eliminate redundancies and improve maintainability.
- **Duplicate Function Removal**: Removed duplicate `_select_theme()` function in `main.py`, replacing it with a simplified `_select_theme_simple()` wrapper that preserves functionality while improving code organization.
- **Legacy Code Cleanup**: Removed commented-out legacy code in `sentence.py` and `coherence.py` that was previously overriding proper imports from `json_data_provider.py`.
- **Debug Code Removal**: Cleaned up commented debug print statements in `json_data_provider.py` for cleaner production code.

### **Enhanced**
- **Function Organization**: Streamlined theme selection logic in `main.py` with clear separation between interactive navigation and simple programmatic selection.
- **Import Consistency**: Ensured all modules properly use centralized imports from `json_data_provider.py` without local overrides.
- **Code Documentation**: Improved inline documentation and removed outdated comments.

### **Technical Details**
- **Main.py Optimization**: Eliminated redundant theme-selection functions while preserving full CLI functionality and interactive navigation.
- **Citation System Integrity**: Verified that `citation_relationships` and `philosophical_movements` are properly imported from the data provider rather than using empty local dictionaries.
- **Data Loading Robustness**: Maintained all error handling and fallback mechanisms in the data-loading system.
- **Compilation Verification**: All core modules now compile cleanly without warnings or errors.

### **Validation**
- **Functionality Testing**: Verified that all essay-generation features work correctly after code cleanup.
- **Data Integrity**: Confirmed that thematic clusters, philosophers, and concepts load properly.
- **CLI Compatibility**: Tested all command-line arguments and interactive features to ensure they maintain full functionality.

### **Previous Changes (v0.1.4)**

Version 0.1.4 introduces a comprehensive enhancement to the metafiction system, dramatically improving the sophistication and contextual awareness of self-reflexive elements:

### **Enhanced Metafiction System**
- **Contextual Awareness**: Metafiction now features strategic placement after bold claims, dense theoretical points, and dialectical transitions. The system detects these moments through linguistic analysis and adjusts placement accordingly.
- **User-Controlled Intensity Levels**: New CLI option `--metafiction [subtle|moderate|highly_self_aware]` allows users to control the frequency and type of metafictional elements. Each level has different probability thresholds and section limits.
- **Interactive Navigation**: Added complete navigation system allowing users to change seed, metafiction level, and theme selection with fallback options (`s`, `m`, `i`, `h`) during interactive mode.
- **Enhanced Export Metadata**: Exported essays now include metafiction level in YAML frontmatter alongside seed, theme, and generation timestamp for complete reproducibility.
- **Variety and Depth of Metafictional Tropes**: Significantly expanded METAFICTIONAL_TEMPLATES and METAFICTIONAL_CONCLUSIONS in data.json with 40+ new templates covering:
  - **Authorial Intrusion**: Direct reader address ("Dear reader, you might be wondering...")
  - **Critique of Form**: Commentary on essay structure and academic conventions
  - **Dialectical Self-Reflexivity**: Recognition of the essay's own dialectical structure and limitations
  - **Thematic Metafiction**: Theme-specific templates for each thematic cluster
- **Enhanced CoherenceManager Integration**: The coherence system now tracks dialectical moments, oppositional concept usage, and provides contextual information for metafiction placement decisions.
- **Dialectical Tracking**: New methods detect dialectical progression stages (thesis/antithesis/synthesis) and adjust metafiction frequency and type accordingly.

### **Technical Implementation Details**
- **Strategic Placement Detection**: New `detect_strategic_moment()` function analyzes paragraph text for bold claims, dense theoretical content, dialectical transitions, and oppositional moments, calculating strategic scores for optimal metafiction placement.
- **Enhanced Decision Engine**: The `should_insert_metafiction()` function now considers multiple contextual factors including section length, essay position, existing metafiction count, and dialectical context to make sophisticated placement decisions.
- **Dynamic Template Selection**: Context-aware template selection system that chooses appropriate metafictional elements based on the specific strategic moment type (bold claims, theoretical density, dialectical transitions).
- **Integration with Essay Generation**: Seamless integration with the main essay generation pipeline through enhanced `section_context` and `dialectical_context` parameters passed to metafiction functions.
- **Metafiction Usage Tracking**: New tracking system in CoherenceManager to prevent over-saturation and ensure balanced distribution of metafictional elements throughout essays.

### **Data Architecture Enhancements**
- **Expanded Template Library**: Over 50 new metafictional templates organized by context type and thematic relevance
- **Strategic Placement Indicators**: New data structures defining linguistic patterns that signal optimal moments for metafictional insertion
- **Metafiction Configuration**: Comprehensive configuration system defining probability thresholds, placement preferences, and section limits for each intensity level

### **Previous Changes (v0.1.3)**

Version 0.1.3 focuses on enhancing dialectical reasoning and conceptual sophistication:

- **Expanded Oppositional Pairs**: Significantly enhanced the `oppositional_pairs` dataset in `data.json`, expanding from 20 to 60 high-quality philosophical oppositions. The new additions cover contemporary theoretical developments (2000-2024), including surveillance capitalism/digital commons, racial capitalism/abolition, cisnormativity/trans becoming, and numerous other cutting-edge dialectical pairs.
- **Enhanced Dialectical Progression**: The `get_oppositional_concept` method and `develop_dialectic` feature now benefit from a much richer set of conceptual oppositions, enabling more sophisticated thesis-antithesis-synthesis progressions in essay structure and more nuanced theoretical argumentation.
- **Contemporary Theory Integration**: Added oppositions spanning intersectional and decolonial theory, digital/technological dialectics, affect theory and new materialism, climate and Anthropocene studies, queer and trans studies, surveillance capitalism vs. commons concepts, Lacanian psychoanalysis, emergence vs. reductionism in scientific theory, and feminist epistemology.
- **Improved Thematic Coherence**: The expanded oppositional pairs provide better support for contemporary themes like "Digital Subjectivity," "Decoloniality and Postcolonial Studies," and "Affect, Materiality, and the Posthuman," resulting in more theoretically sophisticated and current essays.

### v0.1.2

Version 0.1.2 focuses on enhancing the quality of generated text and improving performance:

- **Dynamic Weight Adjustment**: Introduced a dynamic weighting system for concepts, terms, and philosophers to improve thematic development and reduce repetition by adjusting selection probabilities on the fly.
- **Enhanced Sentence Complexity and Variety**: Introduced new algorithms to generate more diverse and intricate sentence structures, moving beyond simpler templates. This results in more engaging and less repetitive prose.
- **Refined Abstract Generation Logic**: Improved the abstract generation to produce summaries that are more thematically focused, concise, and accurately representative of the essay's core arguments and theoretical positioning.
- **CLI Export Options**: Added `--export` and `--no-export` command-line arguments to predetermine whether essays will be exported as Markdown files, eliminating the need for post-generation user prompts and enabling fully automated essay generation workflows.
- **Interactive Help System**: Added 'h' option during theme selection to display CLI command examples and usage tips, plus helpful prompts throughout the interface to inform users about available help options.
- **Interactive Theme Details**: Added a feature to the theme selection menu where users can type 'i' to display a detailed, numbered list of all available themes and their full descriptions. This clears the terminal for focused reading and returns to the theme selection menu, preserving the current seed and refreshing the previous view.
- **Performance Optimization in Core Logic**: Optimized key algorithms related to coherence and essay structuring, leading to noticeably faster generation times, especially for longer and more thematically complex essays.
- **Sentence.py Integration Fixes**: Fixed critical import issues in sentence.py where `citation_relationships` and `philosophical_movements` were locally defined as empty dictionaries instead of importing from `json_data_provider.py`. This ensures proper philosopher relationship mapping and citation functionality.
- **Enhanced Coherence Manager Integration**: Improved the integration between sentence generation and the coherence manager, ensuring consistent data key usage and proper thematic guidance throughout sentence construction.
- **Markdown Export Fix**: Addressed a minor bug related to the formatting of very long titles in the metadata section of exported Markdown files, ensuring consistent output.

### v0.1.15

Version 0.1.15 introduces key enhancements to the generator's logical core and portability:

- **Advanced Concept Relationships**: Implemented a more advanced system for defining relationships between concepts. This includes various relationship types (e.g., 'critiques', 'is_foundational_to', 'complements') and strength modifiers, which allows for richer thematic development.
- **Refined Dialectical Progression**: There is a new dialectical development system targeting concept relationship strengths and types to create a more nuanced and logically sound Thesis-Antithesis-Synthesis progression for essay sections. This is integrated for generating section themes.
- **Expanded Concept Relation Coverage**: Concept relationships have been substantially expanded to provide more comprehensive links between concepts.
- **Dynamic Data File Path**: The method for locating the dataset has been updated to be dynamic. It now determines the path relative to the script's own location, rather than relying on a hardcoded absolute path. This enhancement ensures that the project can be run correctly by different users on different systems without requiring manual path adjustments, improving portability and ease of use.

### v0.1.1

Version 0.1.1 focuses on enhancing the robustness and accuracy of the citation system. Key improvements include:

- **Enhanced Citation Generation**: Significantly improved fallback mechanisms to prevent empty or incomplete bibliographic entries and in-text citations. This ensures that all generated citations are plausible and complete.
- **MLA Punctuation Refinements**: Updated logic for precise adherence to MLA 9 style for punctuation within quotes and for sentence-ending punctuation following parenthetical citations.
- **Overall Stability**: These changes contribute to a more reliable and academically sound output from the generator.

### v0.1.0

This version represents a fundamental architectural overhaul and the first stable release of the modernized Postmodern Generator. Key improvements include:

- **Data Architecture Overhaul**: Complete migration from Python modules to JSON-based data management with `data.json` and `json_data_provider.py`
- **Thematic Clustering System**: Introduction of 11 thematic clusters for targeted essay generation
- **Enhanced Command-Line Interface**: Professional CLI with argparse, theme selection, and export functionality
- **Markdown Export System**: Complete export functionality with essay metadata and file management
- **Improved Code Organization**: Centralized data access, better error handling, and reduced code duplication
- **Enhanced Academic Authenticity**: Expanded philosopher-concept relationships and more template variety
- **Dependencies Cleanup**: Removed unnecessary dependencies for improved efficiency

</details>

## Installation

To install the Postmodern Generator, follow these steps:

1. Ensure you have Python 3.8 or higher installed. You can download it from [python.org](https://www.python.org/).
2. Clone the repository:
    ```bash
    git clone https://github.com/egemulayim/postmodern_generator.git
    ```
3. Navigate to the project directory:
    ```bash
    cd postmodern_generator
    ```
4. The generator requires no external dependencies beyond Python's standard library, it is therefore completely self-contained.

## Usage

### Basic Usage

To generate a postmodern essay with interactive prompts:

```bash
python main.py
```

When running the script, you will be prompted to:
1. Enter a random seed (or press Enter for random generation)
2. Select a metafiction level (subtle, moderate, or highly self-aware)
3. Select from available themes (or choose 0 for random theme selection)

**Interactive Help Options:**
- Type `h` during theme selection to view CLI command examples
- Type `i` during theme selection to view detailed theme descriptions
- Use `python main.py --help` anytime to see all available command-line arguments

### Command-Line Arguments

You can specify the seed and theme directly via command-line arguments:

**Get help:**
```bash
python main.py --help
```

**List available themes:**
```bash
python main.py --list-themes
```

**Specify a seed:**
```bash
python main.py --seed 42
```

**Specify a theme:**
```bash
python main.py --theme "Digital Subjectivity"
```

**Specify both seed and theme:**
```bash
python main.py --seed 42 --theme "Poststructuralism and Deconstruction"
```

**Control export behavior:**
```bash
# Automatically export without prompting
python main.py --seed 123 --theme "Identity and Subjectivity" --export

# Generate without exporting and skip export prompt
python main.py --seed 456 --theme "Power and Knowledge" --no-export

# Export to a specific filename
python main.py --seed 202 --theme "Digital Subjectivity" --export --output digital-subjectivity.md

# Generate with random seed parameters and auto-export using an auto-generated filename
python main.py --theme "Speculative Realism and Object-Oriented Ontology" --export
```

**Control metafiction intensity:**
```bash
# Generate with subtle metafictional elements (minimal, strategic placement)
python main.py --seed 789 --theme "Poststructuralism and Deconstruction" --metafiction subtle

# Generate with moderate metafictional elements (default level)
python main.py --seed 101 --theme "Digital Subjectivity" --metafiction moderate

# Generate with highly self-aware metafictional elements (frequent, varied placement)
python main.py --seed 202 --theme "Technology, Media, and Culture" --metafiction highly_self_aware
```

**Combine all options:**
```bash
# Full command with all parameters
python main.py --seed 314 --theme "Power and Knowledge" --metafiction moderate --export
```

Available themes can be found either in the [Thematic Clusters](#thematic-clusters) section or directly through:

```bash
python main.py --list-themes
```

**Argument behavior:**
- If no arguments are provided: Interactive selection for seed, metafiction level, and theme, with export prompt
- If any CLI argument is provided: The run is non-interactive
- If `--list-themes` is added: Prints theme keys with descriptions and exits
- If `--export` is added: Automatically exports the essay as Markdown without prompting
- If `--output` is added: It implies export and writes to the provided filename inside `essays/`
- If `--no-export` is added: Skips export and doesn't prompt for export decision
- Export arguments (`--export` and `--no-export`) are mutually exclusive
- `--output` and `--no-export` cannot be used together
- If `--metafiction` is not specified: Uses moderate level as default
- Metafiction levels: `subtle` (minimal, strategic), `moderate` (balanced), `highly_self_aware` (frequent, varied)

### Generated Output

The generator produces a complete academic essay including:
- **Title** with theoretical framing
- **Abstract** with keywords and theoretical context
- **Introduction** with guiding questions and framework establishment
- **Body Sections** with dialectical development and argumentation
- **Conclusion** with metafictional elements and theoretical synthesis
- **Notes** section with capped, selectively reused academic commentary
- **Works Cited** in fictional MLA-like parody format

### Metafictional Elements

One of the defining features of postmodern academic writing is its self-reflexive, metafictional quality. The generator incorporates sophisticated metafictional elements that can be customized through the `--metafiction` parameter:

#### **Metafiction Intensity Levels**

**Subtle (`--metafiction subtle`)**
- **Frequency**: ~8% of paragraphs, 25% chance of metafictional conclusion
- **Placement Strategy**: Strategic placement after bold theoretical claims or dense conceptual passages
- **Style**: Understated self-awareness, academic restraint
- **Use Case**: Professional academic writing with minimal self-reflexivity

**Moderate (`--metafiction moderate`)** *(Default)*
- **Frequency**: ~15% of paragraphs, 40% chance of metafictional conclusion
- **Placement Strategy**: Balanced throughout essay sections
- **Style**: Classical postmodern self-reflexivity
- **Use Case**: Traditional postmodern academic discourse

**Highly Self-Aware (`--metafiction highly_self_aware`)**
- **Frequency**: ~25% of paragraphs, 60% chance of metafictional conclusion
- **Placement Strategy**: Frequent, varied placement including experimental forms
- **Style**: Maximum self-consciousness, experimental academic writing
- **Use Case**: Avant-garde theoretical experiments, creative academic writing

#### **Types of Metafictional Elements**

**Authorial Intrusion**
- Direct reader address ("Dear reader, you might be wondering...")
- Commentary on the reading experience
- Acknowledgment of theoretical difficulties

**Critique of Academic Form**
- Self-commentary on essay structure and conventions
- Questioning of linear argumentation
- Reflection on the limitations of academic prose

**Methodological Self-Awareness**
- Acknowledgment of theoretical complicity
- Recognition of the impossibility of critical distance
- Commentary on the conditions of knowledge production

**Dialectical Self-Reflexivity**
- Recognition of the essay's own dialectical structure
- Commentary on the movement between thesis, antithesis, and synthesis
- Reflection on the limitations of academic argumentation

**Thematic Metafiction**
- Theme-specific self-reflexive elements
- Integration with the essay's chosen theoretical cluster
- Contextually appropriate metafictional templates

#### **Examples by Intensity Level**

**Subtle Level Example:**
> "The reflexive awareness that biopower both enables and delimits this analysis does not escape the author."

**Moderate Level Example:**
> "Dear reader, you might be wondering why this analysis keeps returning to the problem of representation. The author finds themselves in the uncomfortable position of critiquing discourse while employing the very framework that generates it."

**Highly Self-Aware Level Example:**
> "This theoretical meditation on posthumanism concludes with an awareness of its own discursive conditions of possibility. The literary architecture underlying this text participates in the very concepts it has attempted to theorize. The reader should know that this conclusion emerges from a tradition of theoretical inquiry rather than direct experiential knowledge."

### Markdown Export

After generation, you can export the essay as a `.md` file with:
- **Comprehensive metadata**: YAML frontmatter including seed, theme, metafiction level, and generation timestamp
- **Complete reproducibility**: All generation parameters are preserved for exact replication
- **Clean formatting**: Optimized for easy editing and sharing
- **Automatic file management**: Essays saved in dedicated `essays/` directory
- **Non-interactive CLI export**: `--export` auto-generates a filename when `--output` is omitted

**Example metadata format:**
```yaml
---
Seed: 42
Theme: Digital Subjectivity  
Metafiction Level: moderate
Generated: 2024-01-15 14:30:22
---
```

## Thematic Clusters

The generator features 16 thematic clusters, each providing a distinct theoretical framework with specialized philosophers, concepts, and contextual elements:

1. **Postmodernity and Critique of Metanarratives**: Focuses on the cultural, social, and philosophical condition of postmodernity, characterized by skepticism towards grand narratives, a focus on fragmentation, irony, pastiche, and the blurring of high and low culture. It often involves critiques of enlightenment reason and universal truth claims. (Core Philosophers: Jean-François Lyotard, Jean Baudrillard, Fredric Jameson)

2. **Poststructuralism and Deconstruction**: Focuses on deconstruction, logocentrism, différance, and the works of Derrida, Foucault, Barthes, exploring the instability of meaning and challenging traditional notions of textuality and representation. (Core Philosophers: Jacques Derrida, Michel Foucault, Roland Barthes)

3. **Marxism and Critical Theory**: Analyzes capitalism, class struggle, ideology, hegemony, drawing from Marx, Adorno, Gramsci, and the Frankfurt School, examining the contradictions of capitalism and the potential for revolutionary praxis. (Core Philosophers: Karl Marx, Theodor Adorno, Antonio Gramsci)

4. **Power and Knowledge**: Examines the relationship between power structures and the production, dissemination, and validation of knowledge, critiquing traditional epistemologies and highlighting subjugated forms of knowing. Explores concepts like biopower, governmentality, and necropolitics. (Core Philosophers: Michel Foucault, Judith Butler, Achille Mbembe)

5. **Identity and Subjectivity**: Explores the construction of identity and the self, challenging essentialist notions and emphasizing the role of social, cultural, linguistic, and political forces in shaping subjectivity. Delves into psychoanalysis, performativity, and intersectional experiences. (Core Philosophers: Judith Butler, Frantz Fanon, Slavoj Žižek)

6. **Psychoanalysis and Culture**: Applies psychoanalytic theories (Freudian, Lacanian, etc.) to interpret cultural phenomena, literature, film, art, and social dynamics, focusing on the unconscious, desire, trauma, and symbolic structures. (Core Philosophers: Sigmund Freud, Jacques Lacan, Julia Kristeva)

7. **Feminist Epistemologies and Standpoint Theory**: Critiques traditional epistemologies as inherently biased and explores how gender and social location shape knowledge production, advocating for situated knowledges and perspectives from marginalized standpoints. (Core Philosophers: Sandra Harding, Patricia Hill Collins, Donna Haraway)

8. **Feminist Theory and Gender Studies**: Examines gender performativity, patriarchy, intersectionality, the social construction of gender, and challenges to traditional gender roles, drawing from diverse feminist traditions. (Core Philosophers: Judith Butler, bell hooks, Audre Lorde)

9. **Queer Theory**: Challenges normativity, explores performativity, affect, destabilizing identity categories and challenging heteronormative assumptions while exploring the fluidity of desire and identification. (Core Philosophers: Judith Butler, Eve Kosofsky Sedgwick, Michel Foucault)

10. **Decoloniality and Postcolonial Studies**: Critiques the enduring legacies of colonialism and imperialism, focusing on power, knowledge, representation, and resistance from the perspectives of formerly colonized peoples and their diasporas. (Core Philosophers: Frantz Fanon, Edward Said, Gayatri Chakravorty Spivak)

11. **Technology, Media, and Culture**: Investigates the profound impact of technology and media on society, culture, perception, and the human condition, exploring surveillance, virtuality, the network society, and how technology shapes power and identity. (Core Philosophers: Jean Baudrillard, Paul Virilio, Donna Haraway)

12. **Digital Subjectivity**: Examines how digital technologies, networked environments, and online interactions are reshaping concepts of the self, identity, and community, exploring the performative and datafied nature of digital existence. (Core Philosophers: Katherine Hayles, Jodi Dean, Wendy Hui Kyong Chun)

13. **Science and Technology Studies (STS)**: Investigates technoscience, cyborgs, Actor-Network Theory, focusing on the co-production of science and society rather than technological determinism, examining the entanglement of nature and culture. (Core Philosophers: Bruno Latour, Donna Haraway, Katherine Hayles)

14. **Affect, Materiality, and the Posthuman**: Explores the role of affect, emotions, and bodily experience in shaping social and political life, engaging with new materialisms, posthumanism, and the entanglements of human and non-human entities. (Core Philosophers: Félix Guattari, Brian Massumi, Rosi Braidotti)

15. **Speculative Realism and Object-Oriented Ontology**: Rejects post-Kantian correlationism, arguing for the independent existence of objects beyond human perception and challenging the human-world correlate. (Core Philosophers: Quentin Meillassoux, Graham Harman, Ray Brassier)

16. **Critical Pedagogy and Liberatory Education**: Focuses on educational theories that empower students to critique oppressive social structures and foster social justice, emphasizing dialogue, praxis, and the development of critical consciousness. (Core Philosophers: Paulo Freire, bell hooks, Henry Giroux)

Each theme includes specific philosophers, concepts, terms, and contextual frameworks for authentic theoretical engagement.

## Roadmap

### Completed Features
- Enhanced thematic clustering system
- Easy-to-use command-line interface
- Markdown export functionality
- JSON-based data architecture
- MLA 9 citation compliance
- Canonical theme schema across all 16 themes
- Validator-backed data contract with local smoke tests
- Full support coverage for current theme-core philosophers, including quotes
- Canonical citation-relationship coverage for current theme-core philosophers
- Seeded surface-regression fixtures for historically noisy themes
- Sophisticated metafiction system with user-controlled intensity levels
- Strategic placement detection for contextual metafiction
- Dialectical progression tracking and oppositional concept development
- Comprehensive code quality improvements and maintainability

### Planned Improvements
- **Hybrid Lexicon Review**: Continue curating the `hybrid_concept_terms` set and the surrounding lexical pools as new themes and theorists are added
- **Deeper Corpus Curation**: Continue tightening philosopher-concept associations and secondary theme inventories where residual adjacent-theme bleed still appears under wider seed coverage
- **Seeded Quality Review**: Continue broad seeded generation review across all themes and refresh the local surface-regression fixtures only when intentional baseline changes are accepted
- **Additional Citation Styles**: Support for APA, Chicago, and other academic citation formats
- **Enhanced Output Formats**: HTML and LaTeX formatting options
- **Web Interface**: Browser-based user interface for easier interaction
- **Advanced Configuration**: More extensive customization options for output length and complexity
- **API Integration**: API for integration with other tools and services
- **Expanded Knowledge Base**: Additional contemporary theorists and emerging concepts
- **Advanced Metafiction Features**: 
  - Reader response simulation and incorporation
  - Dynamic metafictional dialogue between theoretical positions
- **Collaborative Essay Generation**: Multi-perspective essay generation simulating academic debates
- **Citation Network Analysis**: Visualization of conceptual relationships and citation patterns

## Contributing

Contributions to The Postmodern Generator project are welcome! To contribute, follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix:
    ```bash
    git checkout -b feature-name
    ```
3. Make your changes and commit them:
    ```bash
    git commit -m "Description of your changes"
    ```
4. Push your changes to your fork:
    ```bash
    git push origin feature-name
    ```
5. Create a pull request on the main repository.

### Development Guidelines
- Maintain the JSON data structure when adding new content
- Follow existing code patterns for consistency
- Test new features with multiple themes and seeds
- Update documentation for any new functionality

## Known Issues

- **Movement Taxonomy Curation**: Coverage is now complete for theme-core philosophers, but the movement buckets remain a rhetorical proximity map rather than a final scholarly taxonomy and will need periodic curation as the corpus grows.
- **Hybrid Lexical Judgment**: The concept/term boundary is now explicit, but the exact contents of `hybrid_concept_terms` will still need periodic curation as the corpus evolves.
- **Broad Historical README**: This document is accurate at the feature and workflow level, but it is still a broad historical overview rather than a narrowly scoped operator manual.
- **Thematic Coherence at Scale**: For very long essays, thematic coherence may still diminish in later sections.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

Special thanks to Andrew C. Bulhak, the original creator of The Postmodernism Generator, for the inspiration and foundational work that made this project possible. This project builds on that legacy to create a more sophisticated, coherent, and academically styled text generator for postmodern discourse.

Additional recognition to the open-source community and the philosophers whose work forms the theoretical foundation of this generator.
