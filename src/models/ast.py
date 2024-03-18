from dataclasses import dataclass, field
from typing import Optional, List

from src.models.types import SourceLocation, Int, Bool
from src.models.types import Type, Unit

@dataclass
class Expression:
    """Base class for AST nodes representing expressions."""
    location: SourceLocation
    type: Type = field(default=Unit(), init=False)

@dataclass
class TypeExpr:
    """Base class for type expressions in the AST."""
    location: SourceLocation

    def __eq__(self, other):
        return type(self) == type(other)

@dataclass
class IntTypeExpr(TypeExpr):
    type : Type = field(default=Int(), init=0)

@dataclass
class BoolTypeExpr(TypeExpr):
    type : Type = field(default=Bool(), init=False)

@dataclass
class VarDecl(Expression):
    name: str
    type_annotation: Optional[TypeExpr]
    value: Expression



@dataclass
class Literal(Expression):
    value: int | bool | None
    # (value=None is used when parsing the keyword `unit`)

@dataclass
class Identifier(Expression):
    name: str

@dataclass
class BinaryOp(Expression):
    """AST node for a binary operation like `A + B`"""
    left: Expression
    op: str
    right: Expression

@dataclass
class IfExpr(Expression):
    condition: Expression
    then_branch: Expression
    else_branch: Optional[Expression] = None

@dataclass
class FunctionCall(Expression):
    name: str
    arguments: List[Expression]

@dataclass
class UnaryOp(Expression):
    operator: str
    operand: Expression

@dataclass
class BlockExpr(Expression):
    expressions: List[Expression]
    result_expression: Optional[Expression] = None

@dataclass
class VarDecl(Expression):
    name: str
    value: Expression
    type_annotation : type

