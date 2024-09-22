import inspect
from typing import Optional

from pydantic import BaseModel


class CallData(BaseModel):
    code: str
    variables: dict


def get_data_around_call(target_depth: Optional[int] = None) -> CallData:
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

    source_lines, _ = inspect.getsourcelines(target_frame.f_code)
    code = "\n".join(source_lines)
    variables = {name: str(value) for name, value in target_frame.f_locals.items()}

    return CallData(code=code, variables=variables)
