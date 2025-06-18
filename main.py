# main.py
from server import mcp

from mcp_sp_snowflake_server.wrapper import crear_funcion_sp
from mcp_sp_snowflake_server.sps_config import STORED_PROCEDURES

for name_sp in STORED_PROCEDURES:
    name_fun = name_sp.replace('.', '_').lower()
    globals()[name_fun] = crear_funcion_sp(name_sp)

if __name__ == "__main__":
    print("Starting Mix Server...")
    mcp.run()
