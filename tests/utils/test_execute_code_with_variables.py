from textwrap import dedent

import pytest

from smarf.utils.execute_code_with_variables import (
    execute_code_with_variables,
)


def test_execute_code_with_variables_simple():
    code = "return a + b"
    variables = {"a": 5, "b": 3}

    result = execute_code_with_variables(code, variables)
    assert result == 8


def test_execute_code_with_variables_string_manipulation():
    code = dedent(
        """
        result = greeting + ' ' + name
        return result
    """
    )
    variables = {"greeting": "Hello", "name": "World"}

    result = execute_code_with_variables(code, variables)

    assert result == "Hello World"


def test_execute_code_with_variables_complex_operation():
    code = dedent(
        """
        result = []
        for i in range(num):
            if i % 2 == 0:
                result.append(i * multiplier)

        return result
    """
    )
    variables = {"num": 5, "multiplier": 3}

    result = execute_code_with_variables(code, variables)

    assert result == [0, 6, 12]


def test_execute_code_with_variables_exception():
    code = "result = 1 / 0"
    variables = {}

    with pytest.raises(ZeroDivisionError):
        execute_code_with_variables(code, variables)


def test_execute_code_with_variables_missing_variable():
    code = "result = x + y"
    variables = {"x": 5}

    with pytest.raises(NameError):
        execute_code_with_variables(code, variables)
