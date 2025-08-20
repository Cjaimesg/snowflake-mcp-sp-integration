# Project Structure

This document explains the structure of the snowflake-mcp-sp-integration project.

## Directory Structure

```
snowflake-mcp-sp-integration/
├── main.py                 # Entry point for the application
├── server.py               # MCP server instance
├── pyproject.toml          # Project configuration
├── setup.cfg               # Additional setup configuration
├── requirements.txt        # Dependencies list
├── README.md               # Project documentation
├── LICENSE                 # License information
├── .env.example           # Example environment variables
├── .gitignore             # Git ignore patterns
├── .gitattributes         # Git attributes for line endings
├── Makefile               # Development commands
├── setup_dev.sh           # Development setup script (Unix)
├── setup_dev.bat          # Development setup script (Windows)
├── mcp_sp_snowflake_server/  # Main package
│   ├── __init__.py        # Package initializer
│   ├── config.py          # Configuration handling
│   ├── connection.py      # Snowflake connection management
│   ├── sps_config.py      # Deprecated configuration file
│   ├── utils.py           # Utility functions
│   └── wrapper.py         # Stored procedure wrapper functions
├── quickstart/            # Quickstart guides and examples
│   ├── 00_overview.md
│   ├── 01_env_config.sql
│   ├── 02_create_sp.sql
│   ├── 03_server_config.md
│   └── 04_cleanup.sql
└── tests/                 # Unit tests
    ├── __init__.py
    └── test_utils.py
```

## Component Descriptions

### Main Components

- `main.py`: The entry point that parses command-line arguments, collects stored procedures, and starts the MCP server.
- `server.py`: Initializes the FastMCP server instance.
- `mcp_sp_snowflake_server/`: The main package containing all the core functionality.

### Package Modules

- `config.py`: Handles environment variable configuration and validation.
- `connection.py`: Manages Snowflake connections and sessions.
- `utils.py`: Contains utility functions for validating names, splitting qualified names, and interacting with Snowflake metadata.
- `wrapper.py`: Creates MCP-compatible functions that wrap Snowflake stored procedures.
- `sps_config.py`: Deprecated configuration file (now handled via command-line arguments).

### Quickstart Guides

The `quickstart/` directory contains SQL scripts and documentation to help users set up a test environment:

- `01_env_config.sql`: Creates Snowflake roles, databases, schemas, and users for testing.
- `02_create_sp.sql`: Creates sample stored procedures for testing.
- `03_server_config.md`: Documents how to configure the MCP integration.
- `04_cleanup.sql`: Cleans up the test environment.

## Development

### Setup

1. Clone the repository
2. Run `setup_dev.sh` (Unix) or `setup_dev.bat` (Windows)
3. Copy `.env.example` to `.env` and configure your Snowflake credentials

### Testing

Run tests with:
```bash
python -m unittest discover tests
```

Or using the Makefile:
```bash
make test
```