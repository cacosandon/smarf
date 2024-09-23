import textwrap
from typing import Any


def execute_code_with_variables(code: str, variables: dict) -> Any:
    """
    Execute the code and return the result.
    """
    exec_function = ["def _execute_code():"]
    exec_function.extend(
        f"    {var_name} = variables['{var_name}']" for var_name in variables
    )

    # Dedent the code first, then indent it
    dedented_code = textwrap.dedent(code)
    exec_function.extend(textwrap.indent(dedented_code, "    ").splitlines())

    local_vars = {}
    exec("\n".join(exec_function), {"variables": variables}, local_vars)
    return local_vars["_execute_code"]()
