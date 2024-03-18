from src.models import ast, types
from src.models.SymTab import SymTab
from src.models.types import FunctionType


def typecheck(node: ast.Expression, symtab: SymTab) -> types.Type:
    match node:
        case ast.Literal(value=bool()):
            return types.Bool()
        case ast.Literal(value=int()):
            return types.Int()
        case ast.Identifier():
            return symtab.lookup_variable_type(node.name)
        # case ast.BinaryOp():
        #     left_type = typecheck(node.left, symtab)
        #     right_type = typecheck(node.right, symtab)
        #     if isinstance(left_type, types.Int) and isinstance(right_type, types.Int):
        #         return types.Int()
        #     else:
        #         raise TypeError("Binary operation '+' requires integer operands")
        #
        case ast.BinaryOp():
            op_func = symtab.lookup_variable(node.op)
            op_type = symtab.lookup_variable_type(node.op)
            left_type = typecheck(node.left, symtab)
            right_type = typecheck(node.right, symtab)

            if isinstance(op_type, FunctionType):
                # Validate operand types
                if [type(left_type), type(right_type)] != [type(t) for t in op_type.param_types]:
                    raise TypeError(f"Operand type mismatch for operator '{node.op}'")
                return op_type.return_type

            else:
                raise TypeError(f"Operator '{node.op}' not defined")
        # case ast.IfExpr():
        #     cond_type = typecheck(node.condition, symtab)
        #     then_type = typecheck(node.then_branch, symtab)
        #     else_type = typecheck(node.else_branch, symtab) if node.else_branch else then_type
        #     if not isinstance(cond_type, types.Bool):
        #         raise TypeError("Condition in 'if' must be a boolean")
        #     if type(then_type) != type(else_type):
        #         raise TypeError("'then' and 'else' branches must have the same type")
        #     return then_type

        case ast.IfExpr():
            cond_type = typecheck(node.condition, symtab)
            if not isinstance(cond_type, types.Bool):
                raise TypeError("Condition in 'if' must be a Bool")
            then_type = typecheck(node.then_branch, symtab)
            if node.else_branch is None:
                # if not isinstance(then_type, types.Unit):
                #     raise TypeError("Then branch of 'if' without 'else' must not produce a value")
                return types.Unit()
            else:
                # 处理有else分支的情况
                else_type = typecheck(node.else_branch, symtab)
                if type(then_type) != type(else_type):
                    raise TypeError("'then' and 'else' branches must have the same type")
                return then_type

        # case ast.WhileLoop():
        #     cond_type = typecheck(node.condition, symtab)
        #     if not isinstance(cond_type, types.Bool):
        #         raise TypeError("Condition in 'while' must be a Bool")
        #     body_type = typecheck(node.body, symtab)
        #     if not isinstance(body_type, types.Unit):
        #         raise TypeError("Body of 'while' must not produce a value")
        #     return types.Unit()

        case ast.FunctionCall():
            func_type = symtab.lookup_variable_type(node.name)
            if not isinstance(func_type, FunctionType):
                raise TypeError(f"{node.name} is not a function")

            if len(node.arguments) != len(func_type.param_types):
                raise TypeError("Incorrect number of arguments")

            for arg, param_type in zip(node.arguments, func_type.param_types):
                arg_type = typecheck(arg, symtab)
                if type(arg_type) != type(param_type):
                    raise TypeError("Argument type mismatch")

            return func_type.return_type
