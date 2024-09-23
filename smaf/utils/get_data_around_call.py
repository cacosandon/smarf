import inspect
from typing import Optional

from pydantic import BaseModel


class CallData(BaseModel):
    code: str
    variables: dict


def get_data_around_call(
    target_depth: Optional[int] = None,
) -> CallData:
    """
    Get the code and variables around the call to this function.

    Args:
        target_depth (Optional[int]): The number of frames to go back from the caller.
            If None, it will return the direct caller's frame.
    """

    current_frame = inspect.currentframe()
    if current_frame is None:
        raise ValueError("No current frame found")

    caller_frame = current_frame.f_back
    if caller_frame is None:
        raise ValueError("No caller frame found")

    target_frame = caller_frame
    if target_depth is not None:
        for _ in range(target_depth):
            if target_frame.f_back is None:
                break

            target_frame = target_frame.f_back

    if target_frame is None:
        raise ValueError(f"No target frame found at depth {target_depth}")

    file_path = inspect.getfile(target_frame)
    is_module_level = target_frame.f_code.co_name == "<module>"

    if is_module_level:
        with open(file_path, "r") as file:
            code = file.read()
    else:
        source_lines, start_line = inspect.getsourcelines(target_frame.f_code)
        code = "\n".join(source_lines)

    variables: dict[str, str | int] = {
        name: str(value)
        for name, value in target_frame.f_locals.items()
        if not name.startswith("__")
    }

    # Add some useful context variables
    variables["__file__"] = file_path
    variables["__call_line_number__"] = target_frame.f_lineno - start_line + 1

    variables["__call_line__"] = (
        inspect.getsource(target_frame)
        .strip()
        .split("\n")[variables["__call_line_number__"] - 1]
    )

    return CallData(code=code, variables=variables)
