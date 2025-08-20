from typing import Any, Callable, Union, List

from .utils import get_sp_documentation, render_output
from .connection import get_session
from server import mcp


def create_sp_function(sp_name: str) -> Callable:
    """Create a function that wraps a Snowflake stored procedure for use with MCP.
    
    Args:
        sp_name: The fully qualified name of the stored procedure (DB.SCHEMA.NAME)
        
    Returns:
        A function that can be registered as an MCP tool
    """
    docstring = get_sp_documentation(sp_name)

    def function(*args: Any, **kwargs: Any) -> Any:
        """Execute the Snowflake stored procedure with the provided arguments.
        
        Args:
            *args: Positional arguments to pass to the stored procedure
            **kwargs: Keyword arguments, supports 'args' key for list/tuple of arguments
            
        Returns:
            The result of the stored procedure execution
        """
        session = get_session()
        try:
            # Handle the case where arguments are passed via kwargs['args']
            if not args and 'args' in kwargs:
                args = kwargs['args']
                if not isinstance(args, (list, tuple)):
                    args = [args]
                    
            print(f"Calling {sp_name} with arguments: {args}")
            return render_output(session.call(sp_name, *args))
        finally:
            session.close()

    # Add usage instructions to the docstring
    docstring += (
        "\n"
        "Usage instructions:\n"
        "- These functions are implemented in Python and expect Python-native data types.\n"
        "- If passing multiple arguments, they must be provided in a list or tuple.\n"
        "- Example: function(args=[value1, value2, value3])\n"
        "- A single value can also be passed as a single-element list: function(args=[value])\n"
        "- CRITICAL: All values must match the expected type exactly in JSON format.\n"
        "- For VARCHAR parameters: use strings with quotes: \"example text\"\n"
        "- For NUMBER parameters: use Python numbers: 123 or 123.45 (NOT \"123\")\n"
        "- Example for mixed types: function(args=[\"text string\", 123, True])\n"
        "- Passing values with incorrect types will result in an error.\n"
        )
        
    function.__name__ = sp_name.replace('.', '_').lower()
    function.__doc__ = docstring
    return mcp.tool()(function)