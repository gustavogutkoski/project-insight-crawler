from dataclasses import dataclass

@dataclass
class ClassInfo:
    name: str
    file_path: str

@dataclass
class MethodInfo:
    class_name: str
    method_name: str
    line_number: int
