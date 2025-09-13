# Project Insight - Crawler

Python module responsible for parsing Java source code and extracting structured information about classes and methods.
This is the first core component of **Project Insight**, an open source system for interactive technical documentation
powered by AI.

---

## Overview

`project-insight-crawler` is a reusable Python module that can be added as a dependency in other projects, such as the
main Project Insight API. It analyzes `.java` files line by line and extracts:

- Class name, type (class/interface/enum), inheritance, and line number
- Method name, modifiers, return type, and line number

The extracted data can be saved in a SQLite database by default and serve as the foundation for generating automated
documentation, training LLMs, and more.

---

## Requirements

- **Python 3.11 or higher**
- [**Poetry**](https://python-poetry.org/) for dependency and environment management
- [**tree-sitter-java**](https://github.com/tree-sitter/tree-sitter-java) for parsing Java code

Ensure you have Python 3.11+ installed. Then, install Poetry (if not already installed):

```bash
  pip install poetry
```

To install dependencies and automatically create a virtual environment:

```bash
  poetry install
```

To activate the virtual environment:

```bash
  poetry shell
```

Or run commands directly with:

```bash
  poetry run python main.py ./path/to/java/project
```

---

## Installation

Clone the repository manually:

```bash
    git clone https://github.com/gustavogutkoski/project-insight-crawler.git
    cd project-insight-crawler
    poetry install
```

Also clone the Java grammar:
```bash
  git clone https://github.com/tree-sitter/tree-sitter-java.git
```

Export the env file with the path to the grammar:
```bash
  TREE_SITTER_JAVA_PATH=path/to/grammar/tree-sitter-java
```

Load the environment variables and build the grammar:
```bash
  poetry run build-grammar
```

---

## How to Use

You can run the crawler from the command line using the provided CLI entrypoint:

```bash
  make run path=./path/to/your/java/project
```

This command will:

- Recursively scan all `.java` files inside the provided directory
- Extract class and method data using the parser
- Store the extracted data into a local SQLite database (`crawler.db` by default)

You'll see logs like:

```
Analyzing /path/to/your/java/project/MyClass.java...
Crawler done!
```

By default, the data is saved in a file called `crawler.db` in the root directory. \
You can later use this database for documentation generation, API consumption, or machine learning purposes.

> Note: You can customize the entrypoint script if needed, or integrate this module into a broader application by
> importing its components directly.
---

# Project Structure

```
crawler/
├── database/      # Table creation and SQL logic
├── models/        # Data models for extracted entities
├── parser/        # Java file parsing logic
├── use_cases/     # Business logic (e.g. saving data)
tests/             # Unit tests
scripts/           # Utility scripts (e.g. build_grammar)
pyproject.toml     # Dependencies and dev tool configuration
```

---

# Tooling & Automation

This project is configured for development with:

- **ruff**: Linter and formatter
- **mypy**: Static type checking
- **pytest** + **pytest-cov**: Testing and coverage reports
- **pre-commit**: Git hooks for auto-checks before commits

You can run the tools using:

```bash
    make test       # Run unit tests with coverage
    make lint       # Run linter and auto-fix issues
    make format     # Format code
    make typecheck  # Run static type checks
```

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
