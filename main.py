# main.py
from server import mcp

from mcp_sp_snowflake_server.wrapper import create_sp_function
from mcp_sp_snowflake_server.sps_config import STORED_PROCEDURES

for name_sp in STORED_PROCEDURES:
    name_fun = name_sp.replace('.', '_').lower()
    globals()[name_fun] = create_sp_function(name_sp)

if __name__ == "__main__":
    print("Starting Mix Server...")
    mcp.run()
