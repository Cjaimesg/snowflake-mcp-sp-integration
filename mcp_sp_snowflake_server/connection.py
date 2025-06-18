import snowflake.connector
from snowflake.snowpark import Session
from .config import SNOWFLAKE_CONFIG


def get_connection():
    return snowflake.connector.connect(
        user=SNOWFLAKE_CONFIG["user"],
        password=SNOWFLAKE_CONFIG["password"],
        host=SNOWFLAKE_CONFIG["host"],
        account=SNOWFLAKE_CONFIG["account"],
        warehouse=SNOWFLAKE_CONFIG["warehouse"],
        role=SNOWFLAKE_CONFIG["role"],
        port=443
    )


def get_session():
    return Session.builder.configs(SNOWFLAKE_CONFIG).create()
