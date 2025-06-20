import re
import pandas as pd
from functools import singledispatch

from snowflake.snowpark import DataFrame as SnowparkDataFrame

from .connection import get_connection


@singledispatch
def render_output(arg):
    return arg


@render_output.register
def _(arg: SnowparkDataFrame):
    pdf = arg.to_pandas()
    return pdf.to_markdown(index=False)


def validate_sp_name(sp_name: str) -> bool:
    pattern = r'^[a-zA-Z_][\w]*\.[a-zA-Z_][\w]*\.[a-zA-Z_][\w]*$'
    if re.match(pattern, sp_name.strip()):
        return True
    raise ValueError(f"The stored procedure name {sp_name} is not valid.")


def split_sp_name(sp_name: str) -> tuple:
    pattern = r'^(?P<db>[a-zA-Z_][\w]*)\.(?P<schema>[a-zA-Z_][\w]*)\.(?P<name>[a-zA-Z_][\w]*)$'
    match = re.match(pattern, sp_name.strip())
    if not match:
        raise ValueError("Invalid format.")
    return match.group('db'), match.group('schema'), match.group('name')

def split_schema_name(schema_name: str) -> tuple:
    pattern = r'^(?P<db>[a-zA-Z_][\w]*)\.(?P<schema>[a-zA-Z_][\w]*)$'
    match = re.match(pattern, schema_name.strip())
    if not match:
        raise ValueError("Invalid format.")
    return match.group('db'), match.group('schema')

def validate_schema_name(schema_name: str) -> bool:
    pattern = r'^[a-zA-Z_][\w]*\.[a-zA-Z_][\w]*$'
    if re.match(pattern, schema_name.strip()):
        return True
    raise ValueError(f"The schema name {schema_name} is not valid.")


def validate_schema_exists(schema_name) -> bool:
    validate_schema_name(schema_name)
    db, schema = split_schema_name(schema_name)
    conn = get_connection()
    sql_query = f"SHOW SCHEMAS LIKE '{schema}' IN DATABASE {db}"
    try:
        cursor = conn.cursor()
        cursor.execute(sql_query)
        result = cursor.fetchone()
        return result is not None
    finally:
        cursor.close()
        conn.close()


def get_list_of_sps(schema_name: str) -> list:
    validate_schema_exists(schema_name)
    db, schema = split_schema_name(schema_name)
    conn = get_connection()
    sql_query = f"""SHOW PROCEDURES IN SCHEMA {db}.{schema}
    ->> SELECT DISTINCT CONCAT("catalog_name", '.', "schema_name", '.', "name") AS PROCEDURE_NAME
        FROM $1
        WHERE "catalog_name" = upper('{db}')
        AND "schema_name" = upper('{schema}')"""
    try:
        result = pd.read_sql(sql_query, conn)
        if result.empty:
            return []
        return [f"{row['PROCEDURE_NAME']}" for _, row in result.iterrows()]
    finally:
        conn.close()


def validate_sp_exists(full_sp_name: str) -> bool:
    conn = get_connection()
    validate_sp_name(full_sp_name)
    db, schema, sp_name = split_sp_name(full_sp_name)
    sql_query = f"SHOW PROCEDURES LIKE '{sp_name}' IN SCHEMA {db}.{schema}"
    try:
        cursor = conn.cursor()
        cursor.execute(sql_query)
        result = cursor.fetchone()
        return result is not None
    finally:
        cursor.close()
        conn.close()


def get_sp_documentation(sp_name):
    conn = get_connection()
    validate_sp_exists(sp_name)
    db, schema, sp_name = split_sp_name(sp_name)
    sql_query = f"SHOW PROCEDURES LIKE '{sp_name}' IN SCHEMA {db}.{schema}"
    try:
        result = pd.read_sql(sql_query, conn)
        if result.empty:
            return f"No procedures found with the name '{sp_name}'"
        full_doc = []
        full_doc.append(f"=== PROCEDURES FOUND: {sp_name} ===")
        full_doc.append(f"Database: {db}")
        full_doc.append(f"Schema: {schema}")
        full_doc.append(f"Total: {len(result)}\n")
        for index, row in result.iterrows():
            version_doc = [
                f"--- VERSION {index + 1} ---",
                f"Name: {row.get('name', sp_name)}",
                f"Description: {row.get('description', 'Not available')}",
                f"Arguments: {row.get('arguments', 'Not available')}\n"
            ]
            full_doc.extend(version_doc)
        return '\n'.join(full_doc)
    finally:
        conn.close()


