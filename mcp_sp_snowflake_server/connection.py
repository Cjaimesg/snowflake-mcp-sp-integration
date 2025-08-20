"""Module for managing Snowflake connections and sessions."""
import snowflake.connector
from snowflake.snowpark import Session
from typing import Any
from .config import SNOWFLAKE_CONFIG


def get_connection() -> snowflake.connector.SnowflakeConnection:
    """Create and return a Snowflake connector connection.
    
    Returns:
        A Snowflake connection object
    """
    return snowflake.connector.connect(
        user=SNOWFLAKE_CONFIG["user"],
        password=SNOWFLAKE_CONFIG["password"],
        host=SNOWFLAKE_CONFIG["host"],
        account=SNOWFLAKE_CONFIG["account"],
        warehouse=SNOWFLAKE_CONFIG["warehouse"],
        role=SNOWFLAKE_CONFIG["role"],
        port=443
    )


def get_session() -> Session:
    """Create and return a Snowflake Snowpark session.
    
    Returns:
        A Snowflake Snowpark session object
    """
    return Session.builder.configs(SNOWFLAKE_CONFIG).create()  # type: ignore
