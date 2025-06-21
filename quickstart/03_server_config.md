# MCP Snowflake SP Server Configuration

To configure this project as an MCP server, you must pass the desired schemas and/or stored procedures as command-line arguments in your MCP configuration file.

## Step-by-step

1. Locate your MCP configuration file (typically in JSON format).
2. Add or update the entry for this server using the following structure:

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
        "--procedures",
        "SAMPLE_MCP_DB.SAMPLE_MCP_SCHEMA.SOME_TABLE",
        "SAMPLE_MCP_DB.SAMPLE_MCP_SCHEMA.SAMPLE_MESAGE",
        "SAMPLE_MCP_DB.SAMPLE_MCP_SCHEMA.RETURN_MESSAGE"
      ]
    }
  }
}
```
