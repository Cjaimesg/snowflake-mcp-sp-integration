import os
from dotenv import load_dotenv

load_dotenv()


def get_env_var(key: str, required: bool = True) -> str:
    value = os.getenv(key)
    if required and not value:
        raise EnvironmentError(f"The environment variable {key} is required but not defined.")
    return value


SNOWFLAKE_CONFIG = {
    "account": get_env_var("SNOWFLAKE_ACCOUNT"),
    "user": get_env_var("SNOWFLAKE_USER"),
    "password": get_env_var("SNOWFLAKE_PASSWORD"),
    "role": get_env_var("SNOWFLAKE_ROLE"),
    "warehouse": get_env_var("SNOWFLAKE_WAREHOUSE"),
    "database": get_env_var("SNOWFLAKE_DATABASE"),
    "schema": get_env_var("SNOWFLAKE_SCHEMA"),
    "host": get_env_var("SNOWFLAKE_HOST"),
}
