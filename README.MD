# The Postmodern Generator

Welcome to The Postmodern Generator project. This repository contains the source code for a text generator that produces postmodern-style academic essays with theoretical framing, proper citations, and thematic coherence. This README file will guide you through the setup, usage, and contribution process for the project.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Recent Changes (v0.1.5)](#recent-changes-v015)
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

## Features

- **Complete Essay Generation**: Produces fully-formed academic essays with title, abstract, introduction, body sections, conclusion, notes, and works cited sections
- **Thematic Coherence System**: Advanced clustering with 16 predefined themes for theoretical focus
- **Concept Relationships and Dialectic**: Advanced system for defining concept relations (type and strength), which powers a nuanced dialectical (Thesis-Antithesis-Synthesis) progression in essay structure.
- **Dynamic Weight Adjustment**: A system that dynamically adjusts the selection weights of concepts, terms, and philosophers during essay generation. This includes decaying weights of used items to reduce repetition and boosting related items to enhance local thematic coherence.
- **Theme-Based Generation**: Choose from specialized themes like "Digital Subjectivity," "Decoloniality and Postcolonial Studies," or "Speculative Realism"
- **Interactive Theme Selection**: User-friendly interface for selecting specific themes or random generation
- **Command-Line Interface**: Easy-to-use CLI with seed and theme arguments for reproducible and targeted output
- **Theoretical Sophistication**: Incorporates postmodern concepts, philosophers, and theoretical frameworks with authentic relationships
- **MLA 9 Compliant Citations**: Generates proper in-text citations, endnotes, and formatted works cited sections
- **Dialectical Progressions**: Develops ideas through dialectical movement across essay sections
- **Metafictional Elements**: Includes self-referential passages typical of postmodern writing
- **Academic Abstracts**: Generates abstracts with keywords and theoretical framing
- **Proper Formatting**: Handles capitalization, italicization, and academic conventions
- **Reproducible Output**: Flexible seed input (specific integer or random) for generating consistent or varied results
- **Lightweight and Efficient**: Does not rely on large language models, ensuring quick and resource-efficient text generation
- **Markdown Export**: Save generated essays as `.md` files with comprehensive metadata including seed, theme, metafiction level, and generation timestamp
- **Enhanced Export Metadata**: Exported essays include detailed YAML frontmatter with generation parameters for reproducibility and analysis
- **JSON-Based Data Architecture**: Robust, extensible knowledge base with advanced error handling and dynamic data file path loading.

## Recent Changes (v0.1.5)

Version 0.1.5 focuses on comprehensive code quality improvements and maintainability enhancements:

### **Code Quality and Maintenance**
- **Duplicate Function Elimination**: Removed redundant `_select_theme()` function in `main.py`, replacing it with a streamlined `_select_theme_simple()` wrapper while preserving all functionality and improving code organization
- **Legacy Code Cleanup**: Removed commented-out legacy code in `sentence.py` and `coherence.py` that was previously overriding proper imports from `json_data_provider`
- **Debug Code Removal**: Cleaned up commented debug print statements in `json_data_provider.py` for cleaner production code
- **Import Consistency**: Ensured all modules properly use centralized imports from `json_data_provider.py` without local overrides
- **Function Organization**: Streamlined theme selection logic with clear separation between interactive navigation and programmatic selection

### **Technical Validation**
- **Compilation Verification**: All core modules now compile cleanly without warnings or errors
- **Citation System Integrity**: Verified that `citation_relationships` and `philosophical_movements` are properly imported from data provider
- **Data Loading Robustness**: Maintained all error handling and fallback mechanisms
- **Functionality Testing**: Confirmed all essay generation features work correctly after cleanup (16 themes, 91 philosophers, 97 concepts)
- **CLI Compatibility**: Tested all command-line arguments and interactive features maintain full functionality

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

## Previous Changes

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
2. Select from available themes (or choose 0 for random theme selection)

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

# Generate with random seed parameters and auto-export
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

Available themes can be found in the [Thematic Clusters](#thematic-clusters) section.

**Argument behavior:**
- If no arguments are provided: Interactive selection for both seed and theme, with export prompt
- If only `--seed` is provided: Interactive theme selection with specified seed, with export prompt
- If only `--theme` is provided: Random seed with specified theme, with export prompt
- If both provided: Direct generation with specified parameters, with export prompt
- If `--export` is added: Automatically exports the essay as Markdown without prompting
- If `--no-export` is added: Skips export and doesn't prompt for export decision
- Export arguments (`--export` and `--no-export`) are mutually exclusive
- If `--metafiction` is not specified: Uses moderate level as default
- Metafiction levels: `subtle` (minimal, strategic), `moderate` (balanced), `highly_self_aware` (frequent, varied)

### Generated Output

The generator produces a complete academic essay including:
- **Title** with theoretical framing
- **Abstract** with keywords and theoretical context
- **Introduction** with guiding questions and framework establishment
- **Body Sections** with dialectical development and argumentation
- **Conclusion** with metafictional elements and theoretical synthesis
- **Notes** section with substantive academic commentary
- **Works Cited** in MLA 9 format

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

7. **Feminist Epistemologies and Standpoint Theory**: Critiques traditional epistemologies as inherently biased and explores how gender and social location shape knowledge production, advocating for situated knowledges and perspectives from marginalized standpoints. (Core Philosophers: Sandra Harding, Donna Haraway, Nancy Hartsock)

8. **Feminist Theory and Gender Studies**: Examines gender performativity, patriarchy, intersectionality, the social construction of gender, and challenges to traditional gender roles, drawing from diverse feminist traditions. (Core Philosophers: Judith Butler, Simone de Beauvoir, bell hooks)

9. **Queer Theory**: Challenges normativity, explores performativity, affect, destabilizing identity categories and challenging heteronormative assumptions while exploring the fluidity of desire and identification. (Core Philosophers: Judith Butler, Eve Kosofsky Sedgwick, Michel Foucault)

10. **Decoloniality and Postcolonial Studies**: Critiques the enduring legacies of colonialism and imperialism, focusing on power, knowledge, representation, and resistance from the perspectives of formerly colonized peoples and their diasporas. (Core Philosophers: Frantz Fanon, Edward Said, Gayatri Chakravorty Spivak)

11. **Technology, Media, and Culture**: Investigates the profound impact of technology and media on society, culture, perception, and the human condition, exploring surveillance, virtuality, the network society, and how technology shapes power and identity. (Core Philosophers: Jean Baudrillard, Paul Virilio, Donna Haraway)

12. **Digital Subjectivity**: Examines how digital technologies, networked environments, and online interactions are reshaping concepts of the self, identity, and community, exploring the performative and datafied nature of digital existence. (Core Philosophers: Sherry Turkle, Byung-Chul Han, Wendy Hui Kyong Chun)

13. **Science and Technology Studies (STS)**: Investigates technoscience, cyborgs, Actor-Network Theory, focusing on the co-production of science and society rather than technological determinism, examining the entanglement of nature and culture. (Core Philosophers: Bruno Latour, Donna Haraway, Katherine Hayles)

14. **Affect, Materiality, and the Posthuman**: Explores the role of affect, emotions, and bodily experience in shaping social and political life, engaging with new materialisms, posthumanism, and the entanglements of human and non-human entities. (Core Philosophers: Gilles Deleuze, Brian Massumi, Rosi Braidotti)

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
- Sophisticated metafiction system with user-controlled intensity levels
- Strategic placement detection for contextual metafiction
- Dialectical progression tracking and oppositional concept development
- Comprehensive code quality improvements and maintainability

### Planned Improvements
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

- **Citation Discrepancies**: While significantly improved, minor edge cases in complex in-text citation scenarios (e.g. deeply nested quotes or highly specific source types not yet fully modeled) might occasionally arise, though overall robustness and MLA adherence for common academic use cases are high.
- **Thematic Coherence at Scale**: For very long essays, thematic coherence may diminish in later sections
- **Template Repetition**: With extensive use, some template patterns may repeat, though the system actively manages variety

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

Special thanks to Andrew C. Bulhak, the original creator of The Postmodernism Generator, for the inspiration and foundational work that made this project possible. This project builds on that legacy to create a more sophisticated, coherent, and academically authentic text generator for postmodern discourse.

Additional recognition to the open-source community and the philosophers whose work forms the theoretical foundation of this generator.