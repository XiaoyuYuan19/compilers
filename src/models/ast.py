from dataclasses import dataclass
from typing import Optional, List

from src.models.types import SourceLocation


@dataclass
class Expression:
    """Base class for AST nodes representing expressions."""
    location: SourceLocation


@dataclass
class TypeExpr:
    """Base class for type expressions in the AST."""
    location: SourceLocation

@dataclass
class IntTypeExpr(TypeExpr):
    pass

@dataclass
class BoolTypeExpr(TypeExpr):
    pass

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
    type_annotation : TypeExpr

