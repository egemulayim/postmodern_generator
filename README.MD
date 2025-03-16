# The Postmodern Generator

Welcome to The Postmodern Generator project! This repository contains the source code for a unique text generator that produces postmodern-style content. This README file will guide you through the setup, usage, and contribution process for the project.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)
- [Known Issues](#known-issues)

## Introduction

The Postmodern Generator is a tool designed to generate text that mimics the style of The Postmodernism Generator, which was written by Andrew C. Bulhak using the Dada Engine. It uses concepts of postmodern theory to produce content that is both coherent and stylistically complex. You can learn more about the Dada Engine [here](https://dev.null.org/dadaengine/) and see a web-based preview of Bulhak's The Postmodernism Generator [here](https://www.elsewhere.org/journal/pomo).

## Features

- **Text Generation**: Generate postmodern-style text with a single command.
- **Customizable**: Adjust parameters to influence the style and complexity of the generated text.
- **Extensible**: Easily extend the generator with new datasets, functions, and algorithms.
- **Lightweight**: This project does not use large language models (LLMs) and is lightweight to run locally.

## Installation

To install the Postmodern Generator, follow these steps:

1. Ensure you have Python 3.11 or higher installed. You can download it from [python.org](https://www.python.org/).
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

To generate postmodern text, use the following command:

```bash
python main.py
```

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

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

I would like to thank Andrew C. Bulhak, the original creator of The Postmodernism Generator, for the inspiration and foundational work that made this project possible.

## Known Issues

- **Redundant Phrases**: The generated text may sometimes include redundant use of synonymous words and phrases back to back, which can hinder factuality and comprehension. This issue is known and is being actively worked on to improve the quality of the generated content.
- **Overly Generic Phrasing**: Some generated text may be overly generic, which can reduce the uniqueness and impact of the content. This issue is also being addressed.

## Roadmap

The following features and improvements are planned for future releases:

- Enhanced Text Generation: Improve the linguistic and contextual relevancy to generate more coherent and contextually diverse text.
- User Interface: Develop a web-based user interface for easier interaction with the generator.
- Additional Datasets: Incorporate more datasets to expand the variety of generated content.
- Configuration Options: Provide more configuration options to customize the text generation process.
- Add option to generate in HTML and Markdown formatting systems.