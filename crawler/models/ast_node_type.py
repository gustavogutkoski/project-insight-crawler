from enum import Enum, auto


class ClassChildType(Enum):
    EXTENDS = auto()
    IMPLEMENTS = auto()
    FIELD = auto()
    METHOD = auto()
    CONSTRUCTOR = auto()


NODE_TYPE_MAP = {
    "field_declaration": ClassChildType.FIELD,
    "method_declaration": ClassChildType.METHOD,
    "constructor_declaration": ClassChildType.CONSTRUCTOR,
    "extends_clause": ClassChildType.EXTENDS,
    "implements_clause": ClassChildType.IMPLEMENTS,
}
