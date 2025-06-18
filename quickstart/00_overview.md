# Overview of MCP Procedure Configuration and Validation Process

This set of files sets up a demonstration environment in Snowflake to validate the capability of the MCP to correctly handle stored procedures, including repeated creation of procedures with the same name but different signatures.

## Included Files

### 1. `01_env_config.sql`
- Configures the Snowflake environment.
- Creates:
  - Role (`sample_mcp_role`)
  - Database and schema (`sample_mcp_db.sample_mcp_schema`)
  - Warehouse (`sample_mcp_warehouse`)
  - User (`sample_mcp_user`)
- Assigns appropriate permissions to the role and user.

### 2. `02_create_sp.sql`
- Defines several stored procedures:
  - `SOME_TABLE(VARCHAR, INT)` which returns a table.
  - Two versions of `SAMPLE_MESAGE`: one with a single parameter and one with two parameters.
- **Key Note**: Some procedures are deliberately created more than once (with different signatures) to demonstrate that MCP can handle such cases without errors or conflicts.

### 3. `03_sps_config.py`
- Lists the stored procedures to be used by the MCP:
  - `SOME_TABLE`
  - `SAMPLE_MESAGE`
- Specifies their full path in the database for proper reference.

### 4. `04_cleanup.sql`
- Cleans up the test environment by removing:
  - Database
  - Role
  - User
  - Warehouse

## Key Considerations

- The main goal is to validate MCP's robustness when dealing with procedure redefinitions.
- All scripts are designed to be idempotent or safe to execute multiple times without causing errors.

---

This setup and configuration should be used exclusively in test or development environments.

