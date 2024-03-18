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

        # case ast.BinaryOp():
        #     a: Value = interpret(node.left, symtab)
        #     b: Value = interpret(node.right, symtab)
        #     op_func = symtab.lookup_variable(node.op)
        #     return op_func(a, b)

        case ast.BinaryOp():
            if node.op == "=":
                # 确保左侧是标识符
                if isinstance(node.left, ast.Identifier):
                    # 计算右侧表达式的值
                    value = interpret(node.right, symtab)
                    # 更新现有变量的值
                    symtab.update_variable(node.left.name, value)
                    return value
                else:
                    raise TypeError("Left side of assignment must be an identifier.")
            if node.op == 'and':
                left_value = interpret(node.left, symtab)
                if not left_value:  # 如果左侧为假，则不需要评估右侧
                    return False
                return interpret(node.right, symtab)
            elif node.op == 'or':
                left_value = interpret(node.left, symtab)
                if left_value:  # 如果左侧为真，则不需要评估右侧
                    return True
                return interpret(node.right, symtab)
            else:
                a: Value = interpret(node.left, symtab)
                b: Value = interpret(node.right, symtab)
                op_func = symtab.lookup_variable(node.op)
                return op_func(a, b)
        # 处理其他二元操作符

        case ast.UnaryOp():
            a: Value = interpret(node.operand, symtab)
            op_func = symtab.lookup_variable(f"unary_{node.operator}")
            return op_func(a)

        case ast.IfExpr():
            if interpret(node.condition,symtab):
                return interpret(node.then_branch,symtab)
            else:
                return interpret(node.else_branch,symtab)
        # Handle Literal, BinaryOp, and IfExpr as before
        # Add new cases for variable declaration and block expression


        case ast.VarDecl():
            # 变量声明应该只在当前作用域中定义新变量
            value = interpret(node.value, symtab)
            symtab.define_variable(node.name, value,node.type)
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

        # case ast.WhileLoop():
        #     while interpret(node.condition, symtab):
        #         interpret(node.body, symtab)
        #     return None

        # case ast.FunctionCall():
        #     # 例子：调用内置函数
        #     if node.name in builtin_functions:
        #         arguments = [interpret(arg, symtab) for arg in node.arguments]
        #         return builtin_functions[node.name](*arguments)
        #     # 添加对用户定义函数的支持...
