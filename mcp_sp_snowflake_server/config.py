"""Configuration module for Snowflake connection settings."""
import os
from typing import Dict, Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def get_env_var(key: str, required: bool = True) -> Optional[str]:
    """Get an environment variable value.
    
    Args:
        key: The environment variable name
        required: Whether the variable is required
        
    Returns:
        The environment variable value or None if not required and not set
        
    Raises:
        EnvironmentError: If required variable is not defined
    """
    value = os.getenv(key)
    if required and not value:
        raise EnvironmentError(f"The environment variable {key} is required but not defined.")
    return value


# Snowflake connection configuration
SNOWFLAKE_CONFIG: Dict[str, Optional[str]] = {
    "account": get_env_var("SNOWFLAKE_ACCOUNT"),
    "user": get_env_var("SNOWFLAKE_USER"),
    "password": get_env_var("SNOWFLAKE_PASSWORD"),
    "role": get_env_var("SNOWFLAKE_ROLE"),
    "warehouse": get_env_var("SNOWFLAKE_WAREHOUSE"),
    "database": get_env_var("SNOWFLAKE_DATABASE"),
    "schema": get_env_var("SNOWFLAKE_SCHEMA"),
    "host": get_env_var("SNOWFLAKE_HOST"),
}
