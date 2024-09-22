from scaf.utils.get_data_around_call import get_data_around_call


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
