import re
from typing import List, Tuple, Dict

from crawler.models.class_info import ClassInfo
from crawler.models.method_info import MethodInfo

class_pattern = re.compile(
    r"^(?:public\s+|protected\s+|private\s+|abstract\s+|final\s+|static\s+)*"
    r"(class|interface|enum)\s+(\w+)"
    r"(?:\s+extends\s+(\w+))?"
    r"(?:\s+implements\s+([\w\s,]+))?"
)

method_pattern = re.compile(
    r"(public|private|protected)?\s*"
    r"(static\s+)?"
    r"([\w<>\[\]]+\s+)"
    r"(\w+)\s*"
    r"\("
)


def parse_java_file(file_path: str) -> List[Tuple[ClassInfo, List[MethodInfo]]]:
    results = []
    current_class = None
    method_list = []

    with open(file_path, "r", encoding="utf-8") as file:
        for idx, line in enumerate(file):
            class_match = class_pattern.search(line)
            if class_match:
                if current_class:
                    results.append((current_class, method_list))
                current_class = process_class(class_match, file_path, idx)
                method_list = []

            method_match = method_pattern.search(line)
            if method_match and current_class:
                method_info = process_method(line, idx)
                method_list.append(method_info)

    if current_class:
        results.append((current_class, method_list))

    return results


def process_class(class_match: re.Match[str], file_path: str, line_number: int) -> ClassInfo:
    class_type = class_match.group(1)
    class_name = class_match.group(2)
    superclass = class_match.group(3)
    interfaces = class_match.group(4)

    return ClassInfo(
        id=None,
        name=class_name,
        file_path=file_path,
        line_number=line_number + 1,
        superclass=superclass,
        interfaces=interfaces,
        class_type=class_type,
    )


def process_method(line: str, line_number: int) -> MethodInfo:
    method_match = method_pattern.search(line)
    if method_match:
        modifier = method_match.group(1)
        is_static = method_match.group(2) is not None
        return_type = method_match.group(3).strip()
        method_name = method_match.group(4)

        return MethodInfo(
            class_id=None,  # será preenchido depois
            method_name=method_name,
            line_number=line_number + 1,
            return_type=return_type,
            modifier=modifier,
            is_static=is_static,
        )

    raise ValueError("Could not parse method line")
