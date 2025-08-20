"""MCP Server instance for Snowflake Stored Procedures."""
from mcp.server.fastmcp import FastMCP

# This is the shared MCP server instance
mcp = FastMCP("snowflake_sp_server")
