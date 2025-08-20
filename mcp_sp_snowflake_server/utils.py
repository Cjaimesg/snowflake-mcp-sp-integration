import re
import pandas as pd
from functools import singledispatch
from typing import Tuple, List, Union

from snowflake.snowpark import DataFrame as SnowparkDataFrame

from .connection import get_connection


@singledispatch
def render_output(arg):
    """Generic function to render output in a suitable format."""
    return arg


@render_output.register
def _(arg: SnowparkDataFrame) -> str:
    """Render Snowpark DataFrame as markdown table."""
    pdf = arg.to_pandas()
    return pdf.to_markdown(index=False)


def validate_sp_name(sp_name: str) -> bool:
    """Validate that a stored procedure name follows the format DB.SCHEMA.NAME.
    
    Args:
        sp_name: The stored procedure name to validate
        
    Returns:
        True if valid
        
    Raises:
        ValueError: If the name doesn't match the expected format
    """
    pattern = r'^[a-zA-Z_][\\w]*\\.[a-zA-Z_][\\w]*\\.[a-zA-Z_][\\w]*$'
    if re.match(pattern, sp_name.strip()):
        return True
    raise ValueError(f"The stored procedure name {sp_name} is not valid.")


def split_sp_name(sp_name: str) -> Tuple[str, str, str]:
    """Split a fully qualified stored procedure name into its components.
    
    Args:
        sp_name: The fully qualified stored procedure name (DB.SCHEMA.NAME)
        
    Returns:
        Tuple of (database, schema, procedure_name)
        
    Raises:
        ValueError: If the name doesn't match the expected format
    """
    pattern = r'^(?P<db>[a-zA-Z_][\\w]*)\\.(?P<schema>[a-zA-Z_][\\w]*)\\.(?P<name>[a-zA-Z_][\\w]*)$'
    match = re.match(pattern, sp_name.strip())
    if not match:
        raise ValueError("Invalid format.")
    return match.group('db'), match.group('schema'), match.group('name')


def split_schema_name(schema_name: str) -> Tuple[str, str]:
    """Split a fully qualified schema name into its components.
    
    Args:
        schema_name: The fully qualified schema name (DB.SCHEMA)
        
    Returns:
        Tuple of (database, schema)
        
    Raises:
        ValueError: If the name doesn't match the expected format
    """
    pattern = r'^(?P<db>[a-zA-Z_][\\w]*)\\.(?P<schema>[a-zA-Z_][\\w]*)$'
    match = re.match(pattern, schema_name.strip())
    if not match:
        raise ValueError("Invalid format.")
    return match.group('db'), match.group('schema')


def validate_schema_name(schema_name: str) -> bool:
    """Validate that a schema name follows the format DB.SCHEMA.
    
    Args:
        schema_name: The schema name to validate
        
    Returns:
        True if valid
        
    Raises:
        ValueError: If the name doesn't match the expected format
    """
    pattern = r'^[a-zA-Z_][\\w]*\\.[a-zA-Z_][\\w]*$'
    if re.match(pattern, schema_name.strip()):
        return True
    raise ValueError(f"The schema name {schema_name} is not valid.")


def validate_schema_exists(schema_name: str) -> bool:
    """Check if a schema exists in Snowflake.
    
    Args:
        schema_name: The fully qualified schema name (DB.SCHEMA)
        
    Returns:
        True if the schema exists, False otherwise
    """
    validate_schema_name(schema_name)
    db, schema = split_schema_name(schema_name)
    
    conn = get_connection()
    try:
        cursor = conn.cursor()
        sql_query = f"SHOW SCHEMAS LIKE '{schema}' IN DATABASE {db}"
        cursor.execute(sql_query)
        result = cursor.fetchone()
        return result is not None
    finally:
        cursor.close()
        conn.close()


def get_list_of_sps(schema_name: str) -> List[str]:
    """Get a list of stored procedures in a schema.
    
    Args:
        schema_name: The fully qualified schema name (DB.SCHEMA)
        
    Returns:
        List of fully qualified stored procedure names
    """
    validate_schema_exists(schema_name)
    db, schema = split_schema_name(schema_name)
    
    conn = get_connection()
    try:
        # First, get the procedures
        cursor = conn.cursor()
        show_query = f"SHOW PROCEDURES IN SCHEMA {db}.{schema}"
        cursor.execute(show_query)
        
        # Then fetch the results and process them
        procedures = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        
        # Create a DataFrame from the results
        df = pd.DataFrame(procedures, columns=column_names)
        
        if df.empty:
            return []
            
        # Extract procedure names
        procedure_names = []
        for _, row in df.iterrows():
            proc_name = f"{row['catalog_name']}.{row['schema_name']}.{row['name']}"
            procedure_names.append(proc_name)
            
        return procedure_names
    finally:
        cursor.close()
        conn.close()


def validate_sp_exists(full_sp_name: str) -> bool:
    """Check if a stored procedure exists in Snowflake.
    
    Args:
        full_sp_name: The fully qualified stored procedure name (DB.SCHEMA.NAME)
        
    Returns:
        True if the procedure exists, False otherwise
    """
    validate_sp_name(full_sp_name)
    db, schema, sp_name = split_sp_name(full_sp_name)
    
    conn = get_connection()
    try:
        cursor = conn.cursor()
        sql_query = f"SHOW PROCEDURES LIKE '{sp_name}' IN SCHEMA {db}.{schema}"
        cursor.execute(sql_query)
        result = cursor.fetchone()
        return result is not None
    finally:
        cursor.close()
        conn.close()


def get_sp_documentation(sp_name: str) -> str:
    """Get documentation for a stored procedure.
    
    Args:
        sp_name: The fully qualified stored procedure name (DB.SCHEMA.NAME)
        
    Returns:
        Documentation string for the procedure
    """
    validate_sp_exists(sp_name)
    db, schema, sp_name = split_sp_name(sp_name)
    
    conn = get_connection()
    try:
        cursor = conn.cursor()
        sql_query = f"SHOW PROCEDURES LIKE '{sp_name}' IN SCHEMA {db}.{schema}"
        cursor.execute(sql_query)
        
        # Get column names and data
        procedures = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        
        # Create DataFrame from results
        df = pd.DataFrame(procedures, columns=column_names)
        
        if df.empty:
            return f"No procedures found with the name '{sp_name}'"
            
        full_doc = []
        full_doc.append(f"=== PROCEDURES FOUND: {sp_name} ===")
        full_doc.append(f"Database: {db}")
        full_doc.append(f"Schema: {schema}")
        full_doc.append(f"Total: {len(df)}\n")
        
        for index, row in df.iterrows():
            version_doc = [
                f"--- VERSION {index + 1} ---",
                f"Name: {row.get('name', sp_name)}",
                f"Description: {row.get('description', 'Not available')}",
                f"Arguments: {row.get('arguments', 'Not available')}\n"
            ]
            full_doc.extend(version_doc)
            
        return '\n'.join(full_doc)
    finally:
        cursor.close()
        conn.close()