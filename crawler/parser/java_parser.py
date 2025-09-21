import os
from typing import Generator, List, Optional, Tuple

from tree_sitter import Language, Node, Parser

from crawler.logger.logger import setup_logger
from crawler.models.ast_node_type import NODE_TYPE_MAP, ClassChildType
from crawler.models.class_info import ClassInfo
from crawler.models.field_info import FieldInfo
from crawler.models.method_info import MethodInfo

logger = setup_logger(__name__)

LIB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "build", "java-languages.so")

JAVA_LANGUAGE = Language(LIB_PATH, "java")

parser = Parser()
parser.set_language(JAVA_LANGUAGE)


def _extract_text(child: Node, code: bytes, keyword: str = "") -> str:
    text = code[child.start_byte : child.end_byte].decode("utf-8")
    return text.replace(keyword, "").strip()


def _get_child_identifier(node: Node) -> str:
    """
    Retrieve the identifier (name) from a class or method AST node.

    Args:
        node: AST node to extract the identifier from.

    Returns:
        The identifier string, or "unknown" if not found.
    """
    if node.type == "identifier":
        return str(node.text).replace("b'", "").replace("'", "")
    for child in node.children:
        result = _get_child_identifier(child)
        if result != "unknown":
            return result
    return "unknown"


def _parse_modifiers(node: Node, code: bytes) -> Tuple[Optional[str], bool]:
    modifier = None
    is_static = False
    for child in node.children:
        if child.type == "modifiers":
            for m in child.children:
                text = code[m.start_byte : m.end_byte].decode("utf-8").strip()
                if text == "static":
                    is_static = True
                elif text in {"public", "private", "protected"}:
                    modifier = text
        elif child.type == "modifier":
            text = code[child.start_byte : child.end_byte].decode("utf-8").strip()
            if text == "static":
                is_static = True
            elif text in {"public", "private", "protected"}:
                modifier = text
    return modifier, is_static


def _parse_code(
    code: bytes, file_path: str = "<memory>"
) -> List[Tuple[ClassInfo, List[MethodInfo]]]:
    """
    Parse raw Java source code into structured class and method information.
    """
    results = []

    tree = parser.parse(code)
    root_node = tree.root_node

    for class_node in _find_nodes(
        root_node, "class_declaration", "interface_declaration", "enum_declaration"
    ):
        class_info = _process_class_node(class_node, file_path, code)
        method_list = [
            _process_method_node(mtd_node, code)
            for mtd_node in _find_nodes(class_node, "method_declaration")
        ]
        results.append((class_info, method_list))

    return results


def _process_method_node(node: Node, code: bytes) -> MethodInfo:
    """
    Extract method information from a Tree-sitter AST node.
    """
    method_name = _get_child_identifier(node)

    type_node = next(
        (
            c
            for c in node.children
            if c.type
            in (
                "type",
                "integral_type",
                "floating_point_type",
                "void_type",
                "scoped_type_identifier",
            )
        ),
        None,
    )
    return_type = (
        code[type_node.start_byte : type_node.end_byte].decode("utf-8").strip()
        if type_node
        else None
    )

    modifier, is_static = _parse_modifiers(node, code)

    return MethodInfo(
        class_id=None,
        method_name=method_name,
        line_number=node.start_point[0] + 1,
        return_type=return_type,
        modifier=modifier,
        is_static=is_static,
    )


def _process_field_node(node: Node, code: bytes) -> FieldInfo:
    """
    Extract field information from a Tree-sitter AST node.
    """
    name = _get_child_identifier(node)
    type_node = next(
        (c for c in node.children if c.type in ("type", "integral_type", "floating_point_type")),
        None,
    )
    return_type = (
        code[type_node.start_byte : type_node.end_byte].decode("utf-8").strip()
        if type_node
        else None
    )

    modifier, is_static = _parse_modifiers(node, code)

    return FieldInfo(
        class_id=None,
        name=name,
        type=return_type,
        modifier=modifier,
        is_static=is_static,
        line_number=node.start_point[0] + 1,
    )


def _find_nodes(node: Node, *types: str) -> Generator[Node, None, None]:
    """
    Recursively yield AST nodes of the specified types.
    """
    if node.type in types:
        yield node
    for child in node.children:
        yield from _find_nodes(child, *types)


def _process_class_node(node: Node, file_path: str, code: bytes) -> ClassInfo:
    """
    Extract class information from a Tree-sitter AST node.
    """
    class_name = _get_child_identifier(node)
    class_type = node.type.replace("_declaration", "")
    superclass = None
    interfaces = None
    fields: List[FieldInfo] = []

    class_body = next((c for c in node.children if c.type == "class_body"), None)
    if class_body:
        for child in class_body.children:
            if child.type == "field_declaration":
                fields.append(_process_field_node(child, code))

    for child in node.children:
        child_type = NODE_TYPE_MAP.get(child.type)
        match child_type:
            case ClassChildType.EXTENDS:
                superclass = _extract_text(child, code, "extends")
            case ClassChildType.IMPLEMENTS:
                interfaces = _extract_text(child, code, "implements")
            case _:
                pass

    class_info = ClassInfo(
        id=None,
        name=class_name,
        file_path=file_path,
        line_number=node.start_point[0] + 1,
        superclass=superclass,
        interfaces=interfaces,
        class_type=class_type,
        fields=fields,
    )

    return class_info


def parse_java_file(file_path: str) -> List[Tuple[ClassInfo, List[MethodInfo]]]:
    """
    Parse a Java file from disk into class and method structures.
    """
    with open(file_path, "rb") as f:
        code = f.read()
    return _parse_code(code, file_path)
