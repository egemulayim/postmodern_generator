# The Postmodern Generator

Welcome to The Postmodern Generator project. This repository contains the source code for a text generator that produces postmodern-style academic essays with theoretical framing, proper citations, and thematic coherence. This README file will guide you through the setup, usage, and contribution process for the project.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Recent Changes (v0.1.0)](#recent-changes-v010)
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
- **Thematic Coherence System**: Advanced clustering system with 11 predefined themes for theoretical focus
- **Theme-Based Generation**: Choose from specialized themes like "Digital Subjectivity," "Decoloniality and Postcolonial Studies," or "Speculative Realism"
- **Interactive Theme Selection**: User-friendly interface for selecting specific themes or random generation
- **Enhanced Command-Line Interface**: Professional CLI with seed and theme arguments for reproducible and targeted output
- **Theoretical Sophistication**: Incorporates postmodern concepts, philosophers, and theoretical frameworks with authentic relationships
- **MLA 9 Compliant Citations**: Generates proper in-text citations, endnotes, and formatted works cited sections
- **Dialectical Progressions**: Develops ideas through dialectical movement across essay sections
- **Metafictional Elements**: Includes self-referential passages typical of postmodern writing
- **Academic Abstracts**: Generates abstracts with keywords and theoretical framing
- **Proper Formatting**: Handles capitalization, italicization, and academic conventions
- **Reproducible Output**: Flexible seed input (specific integer or random) for generating consistent or varied results
- **Lightweight and Efficient**: Does not rely on large language models, ensuring quick and resource-efficient text generation
- **Markdown Export**: Save generated essays as `.md` files with comprehensive metadata including seed, theme, and generation timestamp
- **JSON-Based Data Architecture**: Robust, extensible knowledge base with advanced error handling

## Recent Changes (v0.1.0)

This version introduces a fundamental architectural overhaul with a new JSON-based data system and thematic clustering. Key improvements include:

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

### Command-Line Arguments

You can specify the seed and theme directly via command-line arguments:

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
python main.py --seed 42 --theme "Power and Knowledge"
```

**Argument behavior:**
- If no arguments are provided: Interactive selection for both seed and theme
- If only `--seed` is provided: Interactive theme selection with specified seed
- If only `--theme` is provided: Random seed with specified theme
- If both provided: Direct generation with specified parameters

### Generated Output

The generator produces a complete academic essay including:
- **Title** with theoretical framing
- **Abstract** with keywords and theoretical context
- **Introduction** with guiding questions and framework establishment
- **Body Sections** with dialectical development and argumentation
- **Conclusion** with metafictional elements and theoretical synthesis
- **Notes** section with substantive academic commentary
- **Works Cited** in MLA 9 format

### Markdown Export

After generation, you can export the essay as a `.md` file with:
- Comprehensive metadata (seed, theme, generation timestamp)
- Clean formatting for easy editing and sharing
- Automatic file management in `essays/` directory

## Thematic Clusters

The generator features 11 thematic clusters:

1. **Power and Knowledge** - Foucauldian analysis, biopolitics, surveillance studies
2. **Identity and Subjectivity** - Butler, psychoanalysis, intersectionality, affect theory
3. **Postmodernity and Critique of Metanarratives** - Lyotard, Jameson, incredulity toward grand narratives
4. **Technology, Media, and Culture** - Baudrillard, Virilio, platform capitalism, digital surveillance
5. **Decoloniality and Postcolonial Studies** - Said, Spivak, Fanon, epistemic violence, subaltern studies
6. **Affect, Materiality, and the Posthuman** - Deleuze & Guattari, new materialism, assemblage theory
7. **Critical Pedagogy and Liberatory Education** - Freire, hooks, transformative learning
8. **Speculative Realism and Object-Oriented Ontology** - Meillassoux, Harman, correlationism
9. **Psychoanalysis and Culture** - Lacan, Žižek, unconscious, cultural interpretation
10. **Feminist Epistemologies and Standpoint Theory** - Haraway, situated knowledges, strong objectivity
11. **Digital Subjectivity** - Online identity, algorithmic governance, datafication, virtual embodiment

Each theme includes specific philosophers, concepts, terms, and contextual frameworks for authentic theoretical engagement.

## Roadmap

### Completed Features
- ✅ Enhanced thematic clustering system
- ✅ Professional command-line interface
- ✅ Markdown export functionality
- ✅ JSON-based data architecture
- ✅ MLA 9 citation compliance

### Planned Improvements
- **Additional Citation Styles**: Support for APA, Chicago, and other academic citation formats
- **Enhanced Output Formats**: HTML and LaTeX formatting options
- **Web Interface**: Browser-based user interface for easier interaction
- **Advanced Configuration**: More extensive customization options for output length and complexity
- **API Integration**: API for integration with other tools and services
- **Expanded Knowledge Base**: Additional contemporary theorists and emerging concepts

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

- **Citation Discrepancies**: Minor inconsistencies in in-text citations may occur where quotes are properly attributed but parenthetical citations may not always align perfectly
- **Thematic Coherence at Scale**: For very long essays, thematic coherence may diminish in later sections
- **Template Repetition**: With extensive use, some template patterns may repeat, though the system actively manages variety

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

Special thanks to Andrew C. Bulhak, the original creator of The Postmodernism Generator, for the inspiration and foundational work that made this project possible. This project builds on that legacy to create a more sophisticated, coherent, and academically authentic text generator for postmodern discourse.

Additional recognition to the open-source community and the philosophers whose work forms the theoretical foundation of this generator.