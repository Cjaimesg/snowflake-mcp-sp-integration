# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive documentation including project structure and contributing guides
- Development setup scripts for both Unix and Windows
- Unit tests for utility functions
- Makefile for common development tasks
- Requirements.txt for dependency management
- .env.example file for environment configuration
- .gitattributes for proper line endings
- Setup.cfg for additional project configuration

### Changed
- Improved error handling and resource management in utility functions
- Fixed SQL query execution in `get_list_of_sps` function
- Enhanced type hints throughout the codebase
- Improved docstrings and code documentation
- Refactored main.py to use proper function structure
- Updated pyproject.toml with development tools configuration
- Enhanced connection management with proper typing
- Improved function naming and structure in wrapper.py
- Updated README.md with better installation and usage instructions

### Fixed
- SQL query syntax in `get_list_of_sps` function
- Resource cleanup in utility functions
- Error handling in stored procedure retrieval
- Type hinting inconsistencies

### Deprecated
- sps_config.py is now deprecated in favor of command-line arguments

### Removed
- Unused or redundant code patterns

### Security
- Improved environment variable handling