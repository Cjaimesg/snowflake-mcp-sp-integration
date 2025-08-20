# Contributing to Snowflake MCP SP Integration

Thank you for your interest in contributing to this project! This document provides guidelines and information to help you contribute effectively.

## Getting Started

1. Fork the repository
2. Clone your fork
3. Set up the development environment using `setup_dev.sh` or `setup_dev.bat`
4. Create a new branch for your feature or bug fix

## Development Guidelines

### Code Style

This project follows PEP 8 style guidelines. We use:
- `black` for code formatting
- `isort` for import sorting
- `flake8` for linting

Run the following commands to format and check your code:
```bash
make format
make lint
```

### Type Hints

All new code should include type hints where appropriate. We use `mypy` for type checking:
```bash
make type-check
```

### Testing

All new features and bug fixes should include appropriate unit tests. Run tests with:
```bash
make test
```

### Documentation

Update documentation when you change functionality. This includes:
- Docstrings for new functions and classes
- README.md updates for user-facing changes
- Comments for complex logic

## Pull Request Process

1. Ensure your code follows the style guidelines
2. Add tests for new functionality
3. Update documentation as needed
4. Run all tests to ensure nothing is broken
5. Submit a pull request with a clear description of your changes

## Reporting Issues

Please use the GitHub issue tracker to report bugs or suggest features. Include as much detail as possible, including:
- Steps to reproduce the issue
- Expected vs actual behavior
- Environment information (Python version, OS, etc.)

## Code of Conduct

This project follows a code of conduct focused on creating a welcoming and inclusive environment for all contributors. Please be respectful and professional in all interactions.