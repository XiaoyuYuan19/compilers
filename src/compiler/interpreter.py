from typing import Any

from src.models import ast
from src.models.SymTab import SymTab

# Value = int | bool | None
from typing import Union, Callable, Any

Value = Union[int, bool, None, Callable[..., Any]]


def interpret(node: ast.IfExpr, symtab: SymTab) -> Value:
    # symtab = SymTab()

    match node:
        case ast.Literal():
            return node.value

        # case ast.BinaryOp():
        #     a: Any = interpret(node.left, symtab)
        #     b: Any = interpret(node.right, symtab)
        #     if node.op == '+':
        #         return a + b
        #     elif node.op == '<':
        #         return a < b
        #     else:
        #         raise ...

        case ast.BinaryOp():
            a: Value = interpret(node.left, symtab)
            b: Value = interpret(node.right, symtab)
            op_func = symtab.lookup_variable(node.op)
            return op_func(a, b)

        case ast.UnaryOp():
            a: Value = interpret(node.operand, symtab)
            op_func = symtab.lookup_variable(f"unary_{node.operator}")
            return op_func(a)

        case ast.IfExpr():
            print(node.condition)
            if interpret(node.condition,symtab):
                print(node.then_branch)
                return interpret(node.then_branch,symtab)
            else:
                return interpret(node.else_branch,symtab)
        # Handle Literal, BinaryOp, and IfExpr as before
        # Add new cases for variable declaration and block expression

        case ast.VarDecl():
            value = interpret(node.value, symtab)
            symtab.define_variable(node.name, value)
            return value

        case ast.Identifier():
            return symtab.lookup_variable(node.name)

        case ast.BlockExpr():
            symtab.enter_scope()
            for expr in node.expressions:
                interpret(expr, symtab)
            if node.result_expression is not None:
                result = interpret(node.result_expression, symtab)
            else:
                result = None
            symtab.leave_scope()
            return result

        # Extend other cases as needed
