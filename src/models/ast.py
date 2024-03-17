from dataclasses import dataclass
from typing import Optional, List


@dataclass
class Expression:
    """Base class for AST nodes representing expressions."""

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
