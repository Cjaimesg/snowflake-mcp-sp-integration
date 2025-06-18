-- This script sets up the environment for the MCP demo in Snowflake.

USE ROLE accountadmin;

-- Create a role for the MCP demo
CREATE ROLE IF NOT EXISTS sample_mcp_role;

-- Create a database and schema for the MCP demo
CREATE DATABASE IF NOT EXISTS sample_mcp_db;
CREATE SCHEMA IF NOT EXISTS sample_mcp_db.sample_mcp_schema;

GRANT USAGE ON DATABASE sample_mcp_db TO ROLE sample_mcp_role;
GRANT USAGE ON SCHEMA sample_mcp_db.sample_mcp_schema TO ROLE sample_mcp_role;

-- Create a warehouse for the MCP demo
CREATE OR REPLACE WAREHOUSE sample_mcp_warehouse
    WAREHOUSE_SIZE = 'x-small'
    WAREHOUSE_TYPE = 'standard'
    AUTO_SUSPEND = 60
    AUTO_RESUME = TRUE
    INITIALLY_SUSPENDED = TRUE
COMMENT = 'Warehouse for MCP demo';

GRANT USAGE ON WAREHOUSE sample_mcp_warehouse TO ROLE sample_mcp_role;

-- Create a user for the MCP demo
CREATE OR REPLACE USER sample_mcp_user
    PASSWORD = 'XXXXXXXXXXXXXXXX'
    DEFAULT_ROLE = sample_mcp_role
    DEFAULT_WAREHOUSE = sample_mcp_warehouse;

-- Assign the role to the user
GRANT ROLE sample_mcp_role TO USER sample_mcp_user;