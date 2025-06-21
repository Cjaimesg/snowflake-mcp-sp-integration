import hashlib
import argparse

from server import mcp

from mcp_sp_snowflake_server.wrapper import create_sp_function
from mcp_sp_snowflake_server.utils import get_list_of_sps


import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def parse_arguments():
    parser = argparse.ArgumentParser(description="Run Snowflake SP server")
    parser.add_argument(
        "--schemas",
        nargs="+",
        default=[],
        help="List of schemas to load stored procedures from (e.g., DB1.SCHEMA1 DB2.SCHEMA2)"
    )
    parser.add_argument(
        "--procedures",
        nargs="*",
        default=[],
        help="Optional list of fully qualified stored procedures (e.g., DB1.SCHEMA1.PROC1 DB2.SCHEMA2.PROC2)"
    )
    return parser.parse_args()


def generate_safe_function_name(name_sp: str) -> str:
    base_name = name_sp.replace('.', '_').lower()
    hash_suffix = hashlib.sha1(name_sp.encode()).hexdigest()[:5]
    return f"{base_name}_{hash_suffix}"


args = parse_arguments()

collected_sps = args.procedures.copy()

for name_schema in args.schemas:
    try:
        sp_list = get_list_of_sps(name_schema)
        if sp_list:
            collected_sps.extend(sp_list)
    except Exception as e:
        logger.error(f"Failed to retrieve stored procedures from schema '{name_schema}': {e}")


seen = set()
unique_sps = []
for sp in collected_sps:
    if sp not in seen:
        seen.add(sp)
        unique_sps.append(sp)

logger.info(f"Found {len(unique_sps)} unique stored procedures to create functions for.")
logger.info(f"Unique stored procedures: {unique_sps}")

created_names = set()
for name_sp in unique_sps:
    name_fun = generate_safe_function_name(name_sp)
    if name_fun in created_names:
        logger.warning(f"Unexpected duplicate function name: {name_fun} (from {name_sp}) — skipping")
        continue
    try:
        globals()[name_fun] = create_sp_function(name_sp)
        created_names.add(name_fun)
    except Exception as e:
        logger.error(f"Failed to create function for stored procedure '{name_sp}': {e}")

if __name__ == "__main__":
    print("Starting Mix Server...")
    try:
        mcp.run()
    except Exception as e:
        logger.critical(f"Failed to start the server: {e}")
