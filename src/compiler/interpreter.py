from typing import Any

from src.models import ast

Value = int | bool | None

def interpret(node: ast.IfExpr) -> Value:
    match node:

        case ast.Literal():
            return node.value

        case ast.BinaryOp():
            a: Any = interpret(node.left)
            b: Any = interpret(node.right)
            if node.op == '+':
                return a + b
            elif node.op == '<':
                return a < b
            else:
                raise ...

        case ast.IfExpr():
            print(node.condition)
            if interpret(node.condition):
                print(node.then_branch)
                return interpret(node.then_branch)
            else:
                return interpret(node.else_branch)
