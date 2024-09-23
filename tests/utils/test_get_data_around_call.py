import pytest

from smaf.utils.get_data_around_call import get_data_around_call


def test_get_data_around_call():
    def save_record(greeting: str):
        test_variable = "aloha"  # noqa: F841
        data_of_this_fuction = get_data_around_call()

        return data_of_this_fuction

    call_data = save_record("hello")
    assert "def save_record(greeting: str)" in call_data.code
    assert 'test_variable = "aloha"' in call_data.code
    assert "data_of_this_fuction = get_data_around_call()" in call_data.code
    assert "return data_of_this_fuction" in call_data.code

    assert call_data.variables["greeting"] == "hello"
    assert call_data.variables["test_variable"] == "aloha"


def test_get_data_around_parent_call():
    def smart_call():
        data_of_parent_fuction = get_data_around_call(target_depth=1)

        return data_of_parent_fuction

    def save_record(greeting: str):
        test_variable = "aloha"  # noqa: F841
        data_of_this_fuction = smart_call()

        return data_of_this_fuction

    call_data = save_record("hello")

    assert "def save_record(greeting: str)" in call_data.code
    assert 'test_variable = "aloha"' in call_data.code
    assert "data_of_this_fuction = smart_call()" in call_data.code
    assert "return data_of_this_fuction" in call_data.code

    assert call_data.variables["greeting"] == "hello"
    assert call_data.variables["test_variable"] == "aloha"


def test_get_data_around_module_level_call(tmp_path):
    test_file = tmp_path / "test_module.py"
    test_file.write_text(
        """
from smaf.utils.get_data_around_call import get_data_around_call

variable1 = "test"
variable2 = 42

call_data = get_data_around_call()

assert "variable1 = \"test\"" in call_data.code
assert "variable2 = 42" in call_data.code
assert "call_data = get_data_around_call()" in call_data.code

assert call_data.variables["variable1"] == "test"
assert call_data.variables["variable2"] == "42"
assert call_data.variables["__file__"].endswith("test_module.py")
"""
    )

    pytest.main([str(test_file)])


def test_multiple_calls_line_number():
    def multiple_calls():
        first_call = get_data_around_call()
        second_call = get_data_around_call()
        third_call = get_data_around_call()

        return first_call, second_call, third_call

    first, second, third = multiple_calls()

    assert (
        first.variables["__current_call_line_number__"]
        == second.variables["__current_call_line_number__"] - 1
    )

    assert (
        second.variables["__current_call_line_number__"]
        == third.variables["__current_call_line_number__"] - 1
    )
