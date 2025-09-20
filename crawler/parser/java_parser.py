import os
from typing import Generator, List, Tuple, cast

from tree_sitter import Language, Node, Parser

from crawler.logger.logger import setup_logger
from crawler.models.class_info import ClassInfo
from crawler.models.method_info import MethodInfo

logger = setup_logger(__name__)

LIB_PATH = os.path.join(
    os.path.dirname(__file__),
    "..", "..", "build", "java-languages.so"
)

JAVA_LANGUAGE = Language(LIB_PATH, "java")

parser = Parser()
parser.set_language(JAVA_LANGUAGE)


def parse_code(
    code: bytes, file_path: str = "<memory>"
) -> List[Tuple[ClassInfo, List[MethodInfo]]]:
    """
    Parse raw Java source code into structured class and method information.

    Args:
        code: Java source code as bytes.
        file_path: Optional file path for reference or logging.

    Returns:
        A list of tuples containing ClassInfo and a list of MethodInfo objects for each class.
    """
    results = []

    tree = parser.parse(code)
    root_node = tree.root_node

    for class_node in find_nodes(
        root_node, "class_declaration", "interface_declaration", "enum_declaration"
    ):
        class_info = process_class_node(class_node, file_path, code)
        method_list = []

        for method_node in find_nodes(class_node, "method_declaration"):
            method_info = process_method_node(method_node, code)
            method_list.append(method_info)

        results.append((class_info, method_list))

    return results


def parse_java_file(file_path: str) -> List[Tuple[ClassInfo, List[MethodInfo]]]:
    """
    Parse a Java file from disk into class and method structures.

    Args:
        file_path: Path to the Java source file.

    Returns:
        A list of tuples containing ClassInfo and a list of MethodInfo objects for each class.
    """
    with open(file_path, "rb") as f:
        code = f.read()
    return parse_code(code, file_path)


def find_nodes(node: Node, *types: str) -> Generator[Node, None, None]:
    """
    Recursively yield AST nodes of the specified types.

    Args:
        node: The root AST node to start searching from.
        *types: One or more node type strings to match.

    Yields:
        AST nodes matching any of the provided types.
    """
    if node.type in types:
        yield node
    for child in node.children:
        yield from find_nodes(child, *types)


def process_class_node(node: Node, file_path: str, code: bytes) -> ClassInfo:
    """
    Extract class information from a Tree-sitter AST node.

    Args:
        node: AST node representing a class, interface, or enum.
        file_path: Path to the source file.
        code: Full source code as bytes for extracting text.

    Returns:
        A ClassInfo object.
    """

    class_name = get_child_identifier(node)
    class_type = node.type.replace("_declaration", "")
    superclass = None
    interfaces = None

    for child in node.children:
        if child.type == "extends_clause":
            superclass = (
                code[child.start_byte : child.end_byte]
                .decode("utf-8")
                .replace("extends", "")
                .strip()
            )
        if child.type == "implements_clause":
            interfaces = (
                code[child.start_byte : child.end_byte]
                .decode("utf-8")
                .replace("implements", "")
                .strip()
            )

    return ClassInfo(
        id=None,
        name=class_name,
        file_path=file_path,
        line_number=node.start_point[0] + 1,
        superclass=superclass,
        interfaces=interfaces,
        class_type=class_type,
    )


def process_method_node(node: Node, code: bytes) -> MethodInfo:
    """
    Extract method information from a Tree-sitter AST node.

    Args:
        node: AST node representing a method.
        code: Full source code as bytes for extracting text.

    Returns:
        A MethodInfo object.
    """

    method_name = get_child_identifier(node)

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

    modifiers = [
        c
        for c in node.children
        if c.type in ("modifier", "public", "private", "protected", "static")
    ]
    modifier = None
    is_static = False
    for m in modifiers:
        text = code[m.start_byte : m.end_byte].decode("utf-8")
        if text == "static":
            is_static = True
        else:
            modifier = text

    return MethodInfo(
        class_id=None,
        method_name=method_name,
        line_number=node.start_point[0] + 1,
        return_type=return_type,
        modifier=modifier,
        is_static=is_static,
    )

def get_child_identifier(node: Node) -> str:
    """
    Retrieve the identifier (name) from a class or method AST node.

    Args:
        node: AST node to extract the identifier from.

    Returns:
        The identifier string, or "unknown" if not found.
    """
    for child in node.children:
        if child.type == "identifier":
            return cast(bytes, child.text).decode("utf-8")
    return "unknown"
