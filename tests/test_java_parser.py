from typing import Callable

from crawler.parser.java_parser import parse_java_file


def test_parse_java_file_class_without_methods(
    java_file: Callable[[str, str], str], java_class_empty: str
) -> None:
    file_path = java_file(java_class_empty, "EmptyClass.java")
    results = parse_java_file(file_path)

    assert len(results) == 1
    cls, methods = results[0]
    assert cls.name == "EmptyClass"
    assert methods == []


def test_parse_java_file_multiple_classes(
    java_file: Callable[[str, str], str], java_class_multiple: str
) -> None:
    file_path = java_file(java_class_multiple, "Multi.java")
    results = parse_java_file(file_path)

    assert len(results) == 2
    assert results[0][0].name == "First"
    assert results[1][0].name == "Second"


def test_parse_java_file_enum(java_file: Callable[[str, str], str], java_enum: str) -> None:
    file_path = java_file(java_enum, "MyEnum.java")
    results = parse_java_file(file_path)

    assert len(results) == 1
    cls, methods = results[0]
    assert cls.name == "MyEnum"
    assert cls.class_type == "enum"


def test_parse_java_file_interface(
    java_file: Callable[[str, str], str], java_interface: str
) -> None:
    file_path = java_file(java_interface, "MyInterface.java")
    results = parse_java_file(file_path)

    assert len(results) == 1
    cls, _ = results[0]
    assert cls.name == "MyInterface"
    assert cls.class_type == "interface"


def test_parse_java_file_method_with_params_and_return_type(
    java_file: Callable[[str, str], str], java_class_with_method: str
) -> None:
    file_path = java_file(java_class_with_method, "Calculator.java")
    results = parse_java_file(file_path)
    cls, methods = results[0]

    assert cls.name == "Calculator"
    assert methods[0].method_name == "add"
    assert methods[0].return_type == "int"
    assert methods[0].modifier == "public"
    assert methods[0].is_static is False


def test_parse_java_file_field_with_modifiers(
    java_file: Callable[[str, str], str], java_class_with_fields: str
) -> None:
    file_path = java_file(java_class_with_fields, "MyClass.java")
    results = parse_java_file(file_path)
    cls, _ = results[0]

    assert len(cls.fields) == 2

    counter_field = next(f for f in cls.fields if f.name == "counter")
    assert counter_field.modifier == "private"
    assert counter_field.is_static is True

    name_field = next(f for f in cls.fields if f.name == "name")
    assert name_field.modifier == "protected"
    assert name_field.is_static is False


def test_parse_java_file_empty_file(java_file: Callable[[str, str], str]) -> None:
    file_path = java_file("", "Empty.java")
    results = parse_java_file(file_path)
    assert results == []
