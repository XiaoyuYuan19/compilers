# src/compiler/ir_generator.py
from typing import List, Type
from src.models.ast import TypeExpr, Literal, BinaryOp, VarDecl, Identifier, IfExpr
from src.models.ir import (
    IRVar, Instruction, LoadIntConst, LoadBoolConst, Call, Copy, Label, Jump, CondJump
)
from src.models.SymTab import SymTab, add_builtin_symbols


def generate_ir(ast_root: TypeExpr) -> List[Instruction]:
    instructions: List[Instruction] = []
    symtab = SymTab()
    next_var_id = 0

    def new_var(t: Type) -> IRVar:
        nonlocal next_var_id
        var_name = f"x{next_var_id}"
        next_var_id += 1
        new_ir_var = IRVar(var_name)
        symtab.define_variable(var_name,var_name, t)  # 将新变量及其类型添加到符号表中
        return new_ir_var

    # 实现 new_label_name 函数来生成新的标签名
    def new_label_name() -> str:
        nonlocal next_var_id
        label_name = f"L{next_var_id}"
        next_var_id += 1
        return label_name

    def visit(node: TypeExpr) -> IRVar:
        location = node.location
        var_type = node.type  # 假设AST节点已包含类型注解

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

        elif isinstance(node, VarDecl):
            # 假设所有变量声明都将值存储在新变量中
            var_value = visit(node.value)
            result_var = new_var(var_type)
            instructions.append(Copy(source=var_value, dest=result_var, location=location))
            return result_var

        elif isinstance(node, Identifier):
            # 假设符号表可以根据标识符名返回对应的IR变量
            return symtab.lookup_variable(node.name)

        elif isinstance(node, BinaryOp):
            if node.op == "=":
                # 处理赋值操作
                var_dest = symtab.lookup_variable(node.left.name)  # 假设左侧是变量名
                var_value = visit(node.right)
                instructions.append(Copy(source=var_value, dest=var_dest, location=location))
                return var_dest
            # 添加逻辑操作符处理
            # ...

        elif isinstance(node, IfExpr):
            cond_var = visit(node.condition)
            then_label = Label(new_label_name())
            end_label = Label(new_label_name())
            instructions.append(CondJump(cond=cond_var, then_label=then_label, else_label=end_label, location=location))
            instructions.append(then_label)
            visit(node.then_clause)
            instructions.append(end_label)
            # 处理 else_clause



    visit(ast_root)
    return instructions


