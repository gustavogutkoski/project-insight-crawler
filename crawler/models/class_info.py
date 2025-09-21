from dataclasses import dataclass, field
from typing import List, Optional

from crawler.models.field_info import FieldInfo


@dataclass
class ClassInfo:
    id: Optional[int]
    name: str
    file_path: str
    line_number: int
    superclass: Optional[str] = None
    interfaces: Optional[str] = None
    class_type: str = "class"
    fields: List[FieldInfo] = field(default_factory=list)

    def __str__(self) -> str:
        return f"{self.name} (Line {self.line_number})"
