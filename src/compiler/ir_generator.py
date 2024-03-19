# src/compiler/ir_generator.py
from typing import List, Type

from src.compiler.type_checker import typecheck
from src.models.ast import TypeExpr, Literal, BinaryOp, VarDecl, Identifier, IfExpr, FunctionCall, BlockExpr, WhileExpr
from src.models.ir import (
    IRVar, Instruction, LoadIntConst, LoadBoolConst, Call, Copy, Label, Jump, CondJump
)
from src.models.SymTab import SymTab, add_builtin_symbols
from src.models.types import Unit, Int, Bool, SourceLocation


def generate_ir(ast_root: TypeExpr) -> List[Instruction]:

    instructions: List[Instruction] = []
    symtab = SymTab()
    add_builtin_symbols(symtab)

    next_var_id = 0

    var_types: dict[IRVar, Type] = {}

    var_types = {}  # 初始化 var_types 字典

    var_unit = IRVar("unit")
    var_types[var_unit] = Unit()

    # 新变量的创建和类型记录
    def new_var(t: Type) -> IRVar:
        nonlocal next_var_id, var_types
        var_name = f"x{next_var_id}"
        next_var_id += 1
        new_ir_var = IRVar(var_name)
        var_types[new_ir_var] = t  # 将新变量及其类型添加到var_types中
        return new_ir_var

    # 实现 new_label_name 函数来生成新的标签名
    def new_label_name() -> str:
        nonlocal next_var_id
        label_name = f"L{next_var_id}"
        next_var_id += 1
        return label_name

    def visit(node: TypeExpr) -> IRVar:

        # print( 'vis', node)
        location = node.location
        # var_type = node.type  # 假设AST节点已包含类型注解
        # print('bf check',node)
        var_type = typecheck(node, symtab)


        if isinstance(node, Literal):
            var = new_var(var_type)
            if isinstance(node.value, bool):
                instructions.append(LoadBoolConst(value=node.value, dest=var,location=location))
            elif isinstance(node.value, int):
                instructions.append(LoadIntConst(value=node.value, dest=var,location=location))
            return var

        elif isinstance(node, BinaryOp):
            left_var = visit(node.left)
            right_var = visit(node.right)
            result_var = new_var(var_type)
            instructions.append(Call(fun=node.op, args=[left_var, right_var], dest=result_var,location=location))
            return result_var

        elif isinstance(node, BlockExpr):
            symtab.enter_scope()  # 进入新的作用域
            for expr in node.expressions:
                visit(expr)  # 为块中的每个表达式生成IR代码
            if node.result_expression:
                result_var = visit(node.result_expression)  # 为结果表达式生成IR代码，并获取其结果变量
            else:
                result_var = new_var(Unit())  # 如果块没有结果表达式，默认为Unit类型
            symtab.leave_scope()  # 离开作用域
            return result_var

        elif isinstance(node, VarDecl):
            # print('var', node)
            # 假设所有变量声明都将值存储在新变量中

            nonlocal var_types
            var_value = visit(node.value)
            print(var_value,var_types)
            symtab.define_variable(node.name,node.value,var_types[var_value])
            result_var = new_var(var_type)
            instructions.append(Copy(source=var_value, dest=result_var, location=location))
            return result_var


        elif isinstance(node, Identifier):
            return symtab.lookup_variable(node.name)
        # elif isinstance(node, Identifier):
        #     # 从符号表中查找变量，这里假设返回的始终是一个IRVar实例
        #     var_from_symtab = symtab.lookup_variable(node.name)
        #     # 检查是否需要生成Copy指令
        #     # 这里的逻辑取决于你的具体需求，以下是一个基本的示例
        #     result_var = new_var(var_types[var_from_symtab])  # 创建一个新的IR变量
        #     instructions.append(Copy(source=var_from_symtab, dest=result_var, location=node.location))  # 生成一个复制指令
        #     return result_var

        elif isinstance(node, BinaryOp):
            if node.op == "=":
                # 处理赋值操作
                var_dest = symtab.lookup_variable(node.left.name)  # 假设左侧是变量名
                var_value = visit(node.right)
                instructions.append(Copy(source=var_value, dest=var_dest, location=location))
                return var_dest

            if node.op in ["and", "or"]:
                var_left = visit(node.left)
                var_right = visit(node.right)
                result_var = new_var(var_type)  # 假设 node.type 已经是正确的类型
                instructions.append(
                    Call(fun=IRVar(node.op), args=[var_left, var_right], dest=result_var, location=location))
                return result_var

        elif isinstance(node, IfExpr):
            cond_var = visit(node.condition)
            then_label = Label(name=new_label_name(), location=location)
            else_label = Label(name=new_label_name(), location=location) if node.else_branch else None
            end_label = Label(name=new_label_name(), location=location)
            result_var = new_var(var_type)  # 假设 IfExpr 节点有一个类型属性

            instructions.append(
                CondJump(cond=cond_var, then_label=then_label, else_label=else_label if else_label else end_label,
                         location=location))

            instructions.append(then_label)
            then_result_var = visit(node.then_branch)  # 访问then分支，并获取结果变量
            instructions.append(
                Copy(source=then_result_var, dest=result_var, location=location))  # 将then分支的结果复制到result_var
            instructions.append(Jump(label=end_label, location=location))  # 跳转到结束标签，避免执行else分支

            if else_label:
                instructions.append(else_label)
                else_result_var = visit(node.else_branch)  # 访问else分支，并获取结果变量
                instructions.append(
                    Copy(source=else_result_var, dest=result_var, location=location))  # 将else分支的结果复制到result_var

            instructions.append(end_label)

            return result_var  # 返回存储最终结果的IR变量

        elif isinstance(node, WhileExpr):
            loop_start_label = Label(name=new_label_name(), location=location)
            loop_end_label = Label(name=new_label_name(), location=location)

            instructions.append(loop_start_label)
            cond_var = visit(node.condition)
            instructions.append(CondJump(cond=cond_var, then_label=Label(name=new_label_name(), location=location),
                                         else_label=loop_end_label, location=location))

            visit(node.body)
            instructions.append(Jump(label=loop_start_label, location=location))  # Loop back to start
            instructions.append(loop_end_label)

    var_final_result = visit(ast_root)

    # 假设我们有两个全局函数print_int和print_bool的IR变量
    print_int_irvar = IRVar("print_int")
    print_bool_irvar = IRVar("print_bool")
    L = SourceLocation()


    if 'src.models.ast' not in str(type(var_final_result)):
        if str(var_types[var_final_result]) == 'Int':
            instructions.append(Call(fun=print_int_irvar, args=[var_final_result], dest=var_unit, location=L))
        elif str(var_types[var_final_result]) == 'Bool':
            instructions.append(Call(fun=print_bool_irvar, args=[var_final_result], dest=var_unit, location=L))

    return instructions


