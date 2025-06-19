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
