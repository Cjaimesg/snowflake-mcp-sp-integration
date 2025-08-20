# Makefile for snowflake_sp_server development

# Variables
PYTHON = python
UV = uv

# Default target
.PHONY: help
help:
	@echo "Available targets:"
	@echo "  install     - Install dependencies using uv"
	@echo "  dev-install - Install dependencies in development mode"
	@echo "  test        - Run tests"
	@echo "  lint        - Run code linting"
	@echo "  format      - Format code with black and isort"
	@echo "  type-check  - Run mypy type checking"
	@echo "  clean       - Clean Python cache files"
	@echo "  help        - Show this help message"

# Install dependencies
.PHONY: install
install:
	$(UV) pip install -r requirements.txt

# Install in development mode
.PHONY: dev-install
dev-install:
	$(UV) pip install -e .

# Run tests
.PHONY: test
test:
	$(PYTHON) -m unittest discover tests

# Run linting
.PHONY: lint
lint:
	flake8 .

# Format code
.PHONY: format
format:
	black .
	isort .

# Type checking
.PHONY: type-check
type-check:
	mypy .

# Clean cache files
.PHONY: clean
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +

# Run the server
.PHONY: run
run:
	$(UV) run main.py