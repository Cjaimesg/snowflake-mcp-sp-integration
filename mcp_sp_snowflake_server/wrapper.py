from .utils import obtener_documentacion_sp, render_output
from .connection import get_session
from server import mcp


def crear_funcion_sp(nombre_sp):
    docstring = obtener_documentacion_sp(nombre_sp)

    def funcion(*args, **kwargs):
        session = get_session()
        try:
            if not args and 'args' in kwargs:
                args = kwargs['args']
                if not isinstance(args, (list, tuple)):
                    args = [args]
            print(f"Llamando a {nombre_sp} con argumentos: {args}")
            return render_output(session.call(nombre_sp, *args))
        finally:
            session.close()

    docstring += (
        "\n\n"
        "Instrucciones de uso:\n"
        "- Si se van a pasar múltiples argumentos, deben colocarse dentro de una lista o tupla.\n"
        "- Ejemplo: funcion(args=[valor1, valor2, valor3])\n"
        "- También se puede pasar un único valor como lista de un solo elemento: funcion(args=[valor])\n"
        )
    funcion.__name__ = nombre_sp.replace('.', '_').lower()
    funcion.__doc__ = docstring
    return mcp.tool()(funcion)
