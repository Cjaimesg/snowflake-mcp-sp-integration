# Snowflake Stored Procedure Integration with MCP Server

This project simplifies the integration of Snowflake stored procedures with an MCP (Model Context Protocol) server. It provides a framework to define, manage, and execute Snowflake procedures from the MCP server environment.

## Requirements

- Python 3.8 or higher
- [`uv`](https://github.com/astral-sh/uv) installed

## Installation

1. Clone the repository:

```bash
git clone https://github.com/snowflake-mcp-sp-integration.git
cd snowflake-mcp-sp-integration
```

2. Install dependencies using `uv`:

```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

## Configuration

1. Create a `.env` file in the root directory (do not commit this file). Define all required Snowflake credentials:

```
SNOWFLAKE_ACCOUNT=<xxx>-<xxx>
SNOWFLAKE_USER=<xxx>
SNOWFLAKE_PASSWORD=<xxx>
SNOWFLAKE_ROLE=<xxx>
SNOWFLAKE_WAREHOUSE=<xxx>
SNOWFLAKE_DATABASE=<xxx>
SNOWFLAKE_SCHEMA=<xxx>
SNOWFLAKE_HOST=<xxx>-<xxx>.snowflakecomputing.com
```

> All variables are mandatory and must be defined by the user.

2. Configure the project as an MCP server. In your MCP configuration file, add an entry like the following, adjusting the paths to match your local environment. Both --schemas and --procedures are optional and default to empty lists.

 - Schemas: All store procedures in the specified schemas will be available to the MCP server.
 - Procedures: Only the specified procedures will be available to the MCP server.

```json
{
  "mcpServers": {
    "snowflake_sp_server": {
      "command": "absolute/path/to/your/uv/uv.exe",
      "args": [
        "--directory",
        "absolute/path/to/snowflake-mcp-sp-integration",
        "run",
        "main.py",
        "--schemas",
        "DB_NAME.SCHEMA_NAME",
        "--procedures",
        "DB_NAME.OTHER_SCHEMA_NAME.PROCEDURE_NAME"
      ]
    }
  }
}
```

> Replace `absolute/path/to/snowflake-mcp-sp-integration` with the actual directory where you cloned this repository.

## Quickstart - Setup Guide for Dev Environment

The `quickstart/` folder contains a step-by-step guide for setting up and testing this module in the **Dev Environment**.

## License

This project is licensed under the MIT License.
