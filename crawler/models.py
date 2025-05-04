from dataclasses import dataclass
from typing import Optional

@dataclass
class ClassInfo:
    name: str
    file_path: str
    line_number: int
    superclass: Optional[str] = None
    interfaces: Optional[str] = None
    class_type: str = "class"

@dataclass
class MethodInfo:
    class_id: int
    method_name: str
    line_number: int
    return_type: Optional[str] = None
    modifier: Optional[str] = None
    is_static: bool = False
