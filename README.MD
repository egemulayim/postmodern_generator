# The Postmodern Generator

Welcome to The Postmodern Generator project! This repository contains the source code for a text generator that produces postmodern-style academic essays with sophisticated theoretical framing, proper citations, and thematic coherence. This README file will guide you through the setup, usage, and contribution process for the project.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [Known Issues](#known-issues)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Introduction

The Postmodern Generator is a tool designed to generate text that mimics the style of postmodern academic writing. It creates sophisticated theoretical essays complete with citations, dialectical progressions, and self-referential elements characteristic of postmodern discourse. This project is inspired by the Dada Engine run The Postmodernism Generator that was developed by Andrew C. Bulhak. You can learn more about the original Dada Engine [here](https://dev.null.org/dadaengine/) and see a web-based preview of Bulhak's The Postmodernism Generator [here](https://www.elsewhere.org/journal/pomo).

## Features

- **Complete Essay Generation**: Produces fully-formed academic essays with title, abstract, introduction, body sections, conclusion, notes, and works cited sections
- **Theoretical Sophistication**: Incorporates postmodern concepts, philosophers, and theoretical frameworks
- **MLA 9 Compliant Citations**: Generates proper in-text citations and formatted works cited sections
- **Thematic Coherence**: Maintains conceptual and thematic unity throughout the essay
- **Dialectical Progressions**: Develops ideas through dialectical movement
- **Metafictional Elements**: Includes self-referential passages typical of postmodern writing
- **Academic Abstracts**: Generates sophisticated abstracts with keywords and theoretical framing
- **Proper Formatting**: Handles capitalization, italicization, and academic conventions
- **Reproducible Output**: Flexible seed input (specific integer or random via Enter key) for generating consistent or varied results. The actual seed used (even if random) is recorded.
- **Lightweight and Efficient**: Does not rely on large language models, ensuring quick and resource-efficient text generation
- **Markdown Export**: Option to save generated essays as `.md` files in an `essays/` directory, with accurate seed and clean theme information in the metadata.

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
4. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

To generate a postmodern essay, execute the following command in your terminal:

```bash
python main.py
```

When running the script, you will first be prompted for a random seed:
- You can enter a specific integer as a seed. This allows for reproducability.
- Alternatively, simply press Enter to use a randomly generated seed.

Next, you will be presented with a list of available themes:
- Enter `0` to have a theme randomly selected for you.
- Enter the corresponding number (starting from `1`) to choose a specific theme from the list.

### Command-Line Arguments

You can also specify the seed and theme directly via command-line arguments using named options:

- To use a specific seed (e.g., 42) and be prompted for the theme:
  ```bash
  python main.py --seed 42
  ```
- To use a specific theme (e.g., "Power and Knowledge") with a randomly generated seed (ensure the theme key is one of the available themes and use quotes if it contains spaces):
  ```bash
  python main.py --theme "Power and Knowledge"
  ```
- To use a specific seed (e.g., 42) and a specific theme (e.g., "Power and Knowledge"):
  ```bash
  python main.py --seed 42 --theme "Power and Knowledge"
  ```

If no arguments are provided, the script will guide you through interactive selection for both seed and theme.
If only `--seed` is provided, you will be interactively prompted for the theme.
If only `--theme` is provided, a random seed will be used, and you will not be prompted for a seed.

The generator will output a complete academic essay including:
- Title with theoretical framing
- Abstract with keywords
- Introduction with guiding questions
- Several body sections with dialectical development
- Conclusion with metafictional elements
- Notes section
- Works cited in MLA 9 format

When prompted, you can choose to export the generated essay as a `.md` file. These files will be saved in an `essays/` directory within the project root. The exported metadata will accurately reflect the seed used (displaying the value of both user-specified and randomly generated seeds), present clear theme information, and include a timestamp of when the essay was generated.

## Roadmap

The following features and improvements are planned for future releases:

- **Enhanced Output Formats**: Add options to generate in HTML or LaTeX formatting
- **Additional Citation Styles**: Support for APA, Chicago, and possibly other academic citation formats
- **UI Improvements**: Develop a web-based user interface for easier interaction
- **Advanced Configuration**: More extensive options to customize output length, complexity, and thematic focus
- **API Integration**: Build an API to allow integration with other tools and services
- **Expanded Philosopher Database**: Add more contemporary theorists and their key concepts
- **Improved Semantic Coherence**: Further enhance thematic unity and realistic conceptual relationships

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

## Known Issues

- **Capitalization Inconsistencies**: Occasional capitalization issues with first words of sentences, proper nouns, and philosopher names
- **Redundant Phrases**: The generated text may sometimes include redundant use of synonymous words and phrases
- **Terminology Classification**: Some words appear in both concepts and terms categories, leading to inconsistent italicization
- **Citation Format Variations**: Minor inconsistencies in citation formatting might occur
- **Citation Discrepancies**: Minor discrepancies in-text citation might occur, where quotes are attributed to authors properly but may not be consistently cited with relevant paranthetical citation information
- **Thematic Coherence at Scale**: For very long essays, thematic coherence may diminish in later sections

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

Special thanks to Andrew C. Bulhak, the original creator of The Postmodernism Generator, for the inspiration and foundational work that made this project possible. This project builds on that legacy to create a more sophisticated, coherent, and academically authentic text generator for postmodern discourse.