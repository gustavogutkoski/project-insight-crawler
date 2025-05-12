from dataclasses import dataclass
from typing import Optional


@dataclass
class MethodInfo:
    class_id: Optional[int]
    method_name: str
    line_number: int
    return_type: Optional[str] = None
    modifier: Optional[str] = None
    is_static: bool = False

    def __str__(self) -> str:
        return f"{self.method_name} (Line {self.line_number})"
