#!/bin/bash
# Development setup script

echo "Setting up development environment..."

# Create virtual environment
echo "Creating virtual environment..."
uv venv

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
uv pip install -e .

echo "Development environment setup complete!"
echo "To activate the environment, run: source .venv/bin/activate (or .venv\Scripts\activate on Windows)"