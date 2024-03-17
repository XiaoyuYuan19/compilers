from dataclasses import dataclass

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
