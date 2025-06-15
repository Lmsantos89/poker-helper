# Contributing to Poker Tournament Helper

Thank you for considering contributing to the Poker Tournament Helper project! This document provides guidelines and instructions for contributing.

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/poker-helper.git
   cd poker-helper
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   pip install -e .  # Install in development mode
   ```

## Code Style

- Follow PEP 8 style guidelines
- Use type hints for function parameters and return values
- Write docstrings for all functions, classes, and modules
- Keep line length to 100 characters or less

## Testing

- Write tests for all new functionality
- Ensure all tests pass before submitting a pull request
- Run tests with coverage to ensure adequate test coverage:
  ```bash
  ./scripts/run_tests.py
  ```

## Type Checking

- Use mypy for static type checking:
  ```bash
  mypy src
  ```

## Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and type checking
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Commit Message Guidelines

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests after the first line

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow

Thank you for contributing to Poker Tournament Helper!
