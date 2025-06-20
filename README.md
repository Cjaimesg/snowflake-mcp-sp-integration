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

2. Define the stored procedures to be managed by the MCP server in the following file:

```
mcp_sp_snowflake_server/sps_config.py
```

Example:

```python
STORED_PROCEDURES = [
  "DB.SCH.SP_NAME",
  "DB.SCH.SP_NAME_2"
  ]

SCHEMAS = [
  "DB.OTHER_SCHEMA"
  ]
```

> Replace the example entries with your actual stored procedures.

3. Configure the project as an MCP server. In your MCP configuration file, add an entry like the following, adjusting the paths to match your local environment:

```json
{
  "mcpServers": {
    "snowflake_sp_server": {
      "command": "absolute/path/to/your/uv/uv.exe",
      "args": [
        "--directory",
        "absolute/path/to/snowflake-mcp-sp-integration",
        "run",
        "main.py"
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
