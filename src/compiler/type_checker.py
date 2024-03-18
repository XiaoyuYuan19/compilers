# from src.compiler.interpreter import interpret
from src.models import ast, types
from src.models.SymTab import SymTab
from src.models.types import FunctionType, Type

def typecheck_var_decl(node: ast.VarDecl, symtab: SymTab) -> types.Type:
    value_type = typecheck(node.value, symtab)
    if node.type_annotation:
        # Map AST type expression to type checker's type
        annotated_type = map_ast_type_expr_to_type(node.type_annotation)
        if type(value_type) != type(annotated_type):
            raise TypeError(f"Type of initializer does not match variable type annotation in declaration of '{node.name}'")
    symtab.define_variable(node.name,node.value, annotated_type)
    return types.Unit()

def map_ast_type_expr_to_type(type_expr: ast.TypeExpr) -> types.Type:
    if isinstance(type_expr, ast.IntTypeExpr):
        return types.Int()
    elif isinstance(type_expr, ast.BoolTypeExpr):
        return types.Bool()
    else:
        raise Exception("Unknown type expression")
def typecheck(node: ast.Expression, symtab: SymTab) -> Type:
    node.type = _determine_type(node, symtab)
    return node.type

def _determine_type(node: ast.Expression, symtab: SymTab) -> Type:
    match node:
        case ast.Literal(value=bool()):
            return types.Bool()
        case ast.Literal(value=int()):
            return types.Int()
        case ast.Identifier():
            return symtab.lookup_variable_type(node.name)

        case ast.UnaryOp():
            operand_type = typecheck(node.operand, symtab)
            op_type = symtab.lookup_variable_type(f"unary_{node.operator}")

            if isinstance(op_type, FunctionType) and str(operand_type) == str(op_type.param_types[0]):
                return op_type.return_type
            else:
                raise TypeError(f"Unsupported unary operation: {node.operator} for {operand_type}")

        case ast.BinaryOp():
            if node.op == "=":
                # 确保左侧是标识符
                if isinstance(node.left, ast.Identifier):
                    # 计算右侧表达式的值
                    value = _determine_type(node.right, symtab)
                    # 在符号表中更新或定义变量
                    symtab.define_variable(node.left.name, value)
                    return value
                else:
                    raise TypeError("Left side of assignment must be an identifier.")
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
        case ast.IfExpr():
            cond_type = typecheck(node.condition, symtab)
            if not isinstance(cond_type, types.Bool):
                raise TypeError("Condition in 'if' must be a Bool")
            then_type = typecheck(node.then_branch, symtab)
            if node.else_branch is None:
                # if not isi    nstance(then_type, types.Unit):
                #     raise TypeError("Then branch of 'if' without 'else' must not produce a value")
                return types.Unit()
            else:
                # 处理有else分支的情况
                else_type = typecheck(node.else_branch, symtab)
                if type(then_type) != type(else_type):
                    raise TypeError("'then' and 'else' branches must have the same type")
                return then_type


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
        case ast.BlockExpr():
            symtab.enter_scope()
            for expr in node.expressions[:-1]:
                typecheck(expr, symtab)  # Discard types of non-final expressions
            result_type = types.Unit() if not node.result_expression else typecheck(node.result_expression, symtab)
            symtab.leave_scope()
            return result_type

        case ast.VarDecl():
            return typecheck_var_decl(node, symtab)
        # case ast.WhileLoop():
        #     cond_type = typecheck(node.condition, symtab)
        #     if not isinstance(cond_type, types.Bool):
        #         raise TypeError("Condition in 'while' must be a Bool")
        #     body_type = typecheck(node.body, symtab)
        #     if not isinstance(body_type, types.Unit):
        #         raise TypeError("Body of 'while' must not produce a value")
        #     return types.Unit()
