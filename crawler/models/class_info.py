from dataclasses import dataclass
from typing import Optional


@dataclass
class ClassInfo:
    id: Optional[int]
    name: str
    file_path: str
    line_number: int
    superclass: Optional[str] = None
    interfaces: Optional[str] = None
    class_type: str = "class"
