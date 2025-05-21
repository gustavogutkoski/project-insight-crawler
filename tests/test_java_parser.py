import tempfile

import pytest

from crawler.parser.java_parser import parse_java_file, process_method


def test_parse_java_file_single_class_and_method() -> None:
    java_code = """
    public class MyClass {
        public void myMethod() {
        }
    }
    """

    with tempfile.NamedTemporaryFile(suffix=".java", mode="w+", delete=False) as f:
        f.write(java_code)
        f.flush()
        results = parse_java_file(f.name)

    assert len(results) == 1
    for cls, methods in results:
        assert cls.name == "MyClass"
        assert len(methods) == 1
        assert methods[0].method_name == "myMethod"


def test_parse_java_file_ignores_method_outside_class() -> None:
    java_code = """
    public void myMethod() {
    }
    """
    with tempfile.NamedTemporaryFile(suffix=".java", mode="w+", delete=False) as f:
        f.write(java_code)
        f.flush()
        results = parse_java_file(f.name)

    assert results == []


def test_process_method_invalid_line_raises() -> None:
    with pytest.raises(ValueError):
        process_method("not a method line", 10)
