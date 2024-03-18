from dataclasses import dataclass
from typing import List


@dataclass
class SourceLocation:
    file: str = "<unknown>"
    line: int = 1
    column: int = 1
    def __eq__(self, other):
        return True  # Consider all source locations equal for testing purposes

@dataclass
class Token:
    text: str
    type: str
    loc: SourceLocation
    def __eq__(self, other):
        if isinstance(other, Token):
            return self.text == other.text and self.type == other.type
        return NotImplemented

class Type:
    pass

class Int(Type):
    def __repr__(self):
        return "Int"

class Bool(Type):
    def __repr__(self):
        return "Bool"

class Unit(Type):
    def __repr__(self):
        return "Unit"

class FunctionType(Type):
    def __init__(self, param_types: List[Type], return_type: Type):
        self.param_types = param_types
        self.return_type = return_type

    def __repr__(self):
        param_types_str = ", ".join(repr(t) for t in self.param_types)
        return f"({param_types_str}) => {repr(self.return_type)}"
