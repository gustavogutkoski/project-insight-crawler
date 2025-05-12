from crawler.models.method_info import MethodInfo


def test_method_info_str() -> None:
    method = MethodInfo(class_id=None,method_name="doSomething", line_number=15)
    assert str(method) == "doSomething (Line 15)"

def test_method_info_str_with_all_fields() -> None:
    method = MethodInfo(
        class_id=1,
        method_name="processData",
        line_number=42,
        return_type="void",
        modifier="public",
        is_static=True
    )
    assert str(method) == "processData (Line 42)"

