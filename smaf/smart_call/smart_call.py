import os
from typing import Any

import openai

from smaf.smart_call.prompts import SmartCallPrompt
from smaf.utils.execute_code_with_variables import (
    execute_code_with_variables,
)
from smaf.utils.get_data_around_call import get_data_around_call
from smaf.utils.logging import log

openai.api_key = os.getenv("OPENAI_API_KEY")

DEBUG = os.getenv("DEBUG", "false").lower() == "true"
MODEL = os.getenv("MODEL", "gpt-4o-mini")


def smart_call(*args, **kwargs) -> Any:
    """
    Call a smart, code-aware function.

    This function analyzes the context in which it's called and performs
    an appropriate operation based on the available variables and the
    inferred intent.

    Example:
        >>> def get_metadata(description: str):
        ...     result = smart_call()
        ...
        ...     return {
        ...         "title": result["title"],
        ...         "description": result["description"],
        ...     }

    Returns:
        The result of the operation determined by the AI based on the context.
    """

    context_data = get_data_around_call(target_depth=1)

    user_message = SmartCallPrompt.get_user_message(context_data)

    if DEBUG:
        log.info(
            f"Calling {MODEL}: {user_message}", extra={"markup": True, "color": "green"}
        )

    response = openai.chat.completions.create(
        model=MODEL,
        messages=[user_message],
    )

    if DEBUG:
        log.info(
            f"Received response from LLM:\n{response.choices[0].message.content}",
            extra={"markup": True, "color": "green"},
        )

    if response.choices[0].message.content is None:
        raise ValueError("No content in response from LLM")

    return execute_code_with_variables(
        _get_code_from_response(response.choices[0].message.content),
        context_data.variables,
    )


def _get_code_from_response(response: str) -> str:
    response = response.strip()
    start_blocks = ["```python", "```"]
    end_block = "```"

    for start_block in start_blocks:
        start = response.find(start_block)
        if start != -1:
            start += len(start_block)
            end = response[start:].find(end_block)

            if end != -1:
                return response[start : start + end].strip()

            return response[start:].strip()

    return response
