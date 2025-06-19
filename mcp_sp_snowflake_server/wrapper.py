from .utils import get_sp_documentation, render_output
from .connection import get_session
from server import mcp


def create_sp_function(sp_name):
    docstring = get_sp_documentation(sp_name)

    def function(*args, **kwargs):
        session = get_session()
        try:
            if not args and 'args' in kwargs:
                args = kwargs['args']
                if not isinstance(args, (list, tuple)):
                    args = [args]
            print(f"Calling {sp_name} with arguments: {args}")
            return render_output(session.call(sp_name, *args))
        finally:
            session.close()

    docstring += (
        "\n\n"
        "Usage instructions:\n"
        "- If passing multiple arguments, they must be provided in a list or tuple.\n"
        "- Example: function(args=[value1, value2, value3])\n"
        "- A single value can also be passed as a single-element list: function(args=[value])\n"
    )
    function.__name__ = sp_name.replace('.', '_').lower()
    function.__doc__ = docstring
    return mcp.tool()(function)
