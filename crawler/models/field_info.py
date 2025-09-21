from dataclasses import dataclass
from typing import Optional


@dataclass
class FieldInfo:
    class_id: Optional[int]
    name: str
    type: Optional[str] = None
    modifier: Optional[str] = None
    is_static: bool = False
    line_number: int = 0
