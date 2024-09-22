from unittest.mock import MagicMock, patch

import pytest

from smaf.smart_call.smart_call import smart_call


@pytest.fixture
def mock_openai():
    with patch("smaf.smart_call.smart_call.openai") as mock:
        yield mock


@pytest.fixture
def mock_get_data_around_call():
    with patch("smaf.smart_call.smart_call.get_data_around_call") as mock:
        yield mock


@pytest.fixture
def mock_execute_code_with_variables():
    with patch("smaf.smart_call.smart_call.execute_code_with_variables") as mock:
        yield mock


def test_smart_call_basic_functionality(
    mock_openai, mock_get_data_around_call, mock_execute_code_with_variables
):
    mock_get_data_around_call.return_value = MagicMock(variables={})
    mock_openai.chat.completions.create.return_value = MagicMock(
        choices=[
            MagicMock(
                message=MagicMock(
                    content="<output_code>return 'test result'</output_code>"
                )
            )
        ]
    )
    mock_execute_code_with_variables.return_value = "test result"

    result = smart_call()

    assert result == "test result"

    mock_get_data_around_call.assert_called_once()
    mock_openai.chat.completions.create.assert_called_once()
    mock_execute_code_with_variables.assert_called_once()


def test_smart_call_with_args_and_kwargs(
    mock_openai, mock_get_data_around_call, mock_execute_code_with_variables
):
    mock_get_data_around_call.return_value = MagicMock(
        variables={"arg1": "value1", "kwarg1": "value2"}
    )
    mock_openai.chat.completions.create.return_value = MagicMock(
        choices=[
            MagicMock(
                message=MagicMock(
                    content="<output_code>return f'{arg1} {kwarg1}'</output_code>"
                )
            )
        ]
    )
    mock_execute_code_with_variables.return_value = "value1 value2"

    result = smart_call("value1", kwarg1="value2")

    assert result == "value1 value2"

    mock_get_data_around_call.assert_called_once()
    mock_openai.chat.completions.create.assert_called_once()

    mock_execute_code_with_variables.assert_called_once_with(
        "return f'{arg1} {kwarg1}'", {"arg1": "value1", "kwarg1": "value2"}
    )
