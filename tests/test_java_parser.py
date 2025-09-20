from pathlib import Path

from crawler.parser.java_parser import parse_java_file


def test_parse_java_file_class_without_methods(tmp_path: Path) -> None:
    java_code = """
    public class EmptyClass {
    }
    """
    file = tmp_path / "EmptyClass.java"
    file.write_text(java_code)

    results = parse_java_file(str(file))

    assert len(results) == 1
    cls, methods = results[0]
    assert cls.name == "EmptyClass"
    assert methods == []


def test_parse_java_file_multiple_classes(tmp_path: Path) -> None:
    java_code = """
    public class First {
        public void one() {}
    }
    public class Second {
        public void two() {}
    }
    """
    file = tmp_path / "Multi.java"
    file.write_text(java_code)

    results = parse_java_file(str(file))

    assert len(results) == 2
    assert results[0][0].name == "First"
    assert results[1][0].name == "Second"


def test_parse_java_file_interface_and_enum(tmp_path: Path) -> None:
    java_code = """
    public interface MyInterface {
        void doSomething();
    }
    public enum MyEnum {
        ONE, TWO, THREE;
    }
    """
    file = tmp_path / "InterfaceEnum.java"
    file.write_text(java_code)

    results = parse_java_file(str(file))
    names = [cls.name for cls, _ in results]

    assert "MyInterface" in names
    assert "MyEnum" in names


def test_parse_java_file_method_with_params_and_return_type(tmp_path: Path) -> None:
    java_code = """
    public class Calculator {
        public int add(int a, int b) {
            return a + b;
        }
    }
    """
    file = tmp_path / "Calculator.java"
    file.write_text(java_code)

    results = parse_java_file(str(file))
    cls, methods = results[0]

    assert cls.name == "Calculator"
    assert methods[0].method_name == "add"
    if methods[0].return_type:
        assert "int" in methods[0].return_type


def test_parse_java_file_empty_file(tmp_path: Path) -> None:
    file = tmp_path / "Empty.java"
    file.write_text("")

    results = parse_java_file(str(file))
    assert results == []
