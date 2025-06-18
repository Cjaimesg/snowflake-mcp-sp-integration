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


def validar_nombre_sp(nombre_sp: str) -> bool:
    patron = r'^[a-zA-Z_][\w]*\.[a-zA-Z_][\w]*\.[a-zA-Z_][\w]*$'
    if re.match(patron, nombre_sp.strip()):
        return True
    raise ValueError(f"El nombre del stored procedure {nombre_sp} no es válido.")


def split_nombre_sp(nombre_sp: str) -> tuple:
    patron = r'^(?P<db>[a-zA-Z_][\w]*)\.(?P<schema>[a-zA-Z_][\w]*)\.(?P<name>[a-zA-Z_][\w]*)$'
    match = re.match(patron, nombre_sp.strip())
    if not match:
        raise ValueError("Formato inválido.")
    return match.group('db'), match.group('schema'), match.group('name')


def validar_sp_existe(nombre_sp_completo: str) -> bool:
    conn = get_connection()
    validar_nombre_sp(nombre_sp_completo)
    db, schema, nombre_sp = split_nombre_sp(nombre_sp_completo)
    sql_base = f"SHOW PROCEDURES LIKE '{nombre_sp}' IN SCHEMA {db}.{schema}"
    try:
        cursor = conn.cursor()
        cursor.execute(sql_base)
        resultado = cursor.fetchone()
        return resultado is not None
    finally:
        cursor.close()
        conn.close()


def obtener_documentacion_sp(nombre_sp):
    conn = get_connection()
    validar_sp_existe(nombre_sp)
    db, schema, nombre_sp = split_nombre_sp(nombre_sp)
    sql_base = f"SHOW PROCEDURES LIKE '{nombre_sp}' IN SCHEMA {db}.{schema}"
    try:
        result = pd.read_sql(sql_base, conn)
        if result.empty:
            return f"No se encontraron procedimientos con el nombre '{nombre_sp}'"
        documentacion_completa = []
        documentacion_completa.append(f"=== PROCEDIMIENTOS ENCONTRADOS: {nombre_sp} ===")
        documentacion_completa.append(f"Base de datos: {db}")
        documentacion_completa.append(f"Esquema: {schema}")
        documentacion_completa.append(f"Total: {len(result)}\n")
        for index, row in result.iterrows():
            version_doc = [
                f"--- VERSIÓN {index + 1} ---",
                f"Nombre: {row.get('name', nombre_sp)}",
                f"Descripción: {row.get('description', 'No disponible')}",
                f"Argumentos: {row.get('arguments', 'No disponibles')}\n"
            ]
            documentacion_completa.extend(version_doc)
        return '\n'.join(documentacion_completa)
    finally:
        conn.close()
