from crawler.models.class_info import ClassInfo


def test_class_info_str() -> None:
    cls = ClassInfo(id=None, name="TestClass", file_path="src/TestClass.java", line_number=10)
    assert str(cls) == "TestClass (Line 10)"
