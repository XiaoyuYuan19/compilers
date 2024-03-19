from src.models import ir



def get_all_ir_variables(instructions):
    variables = set()
    for insn in instructions:
        # 对于dest属性
        if hasattr(insn, "dest") and insn.dest is not None:
            variables.add(insn.dest)
        # 对于source属性
        if hasattr(insn, "source") and insn.source is not None:
            variables.add(insn.source)
        # 对于args属性，它是一个列表，需要遍历
        if hasattr(insn, "args"):
            for arg in insn.args:
                if arg is not None:
                    print('arg',arg)
                    variables.add(arg)
    return list(variables)

class Locals:
    """Knows the memory location of every local variable."""
    _var_to_location: dict[ir.IRVar, str]
    _stack_used: int

    def __init__(self, variables):
        self._stack_used = 0
        self._var_to_location = {}
        for var in variables:
            self._stack_used += 8  # 假设每个变量占8字节
            self._var_to_location[var] = f"-{self._stack_used}(%rbp)"

    def get_ref(self, var):
        return self._var_to_location[var]

    def stack_used(self):
        return self._stack_used

def generate_assembly(instructions: list[ir.Instruction]) -> str:
    lines = []
    def emit(line: str) -> None: lines.append(line)

    locals = Locals(
        variables=get_all_ir_variables(instructions)
    )

    # ... Emit initial declarations and stack setup here ...
    emit(".global main")
    emit(".type main, @function")
    emit(".section .text")
    emit("main:")
    emit("pushq %rbp")
    emit("movq %rsp, %rbp")
    stack_size = locals.stack_used()
    emit(f"subq ${stack_size}, %rsp")  # 为局部变量预留栈空间

    for insn in instructions:
        emit('# ' + str(insn))
        match insn:
            case ir.Label():
                emit("")
                # ".L" prefix marks the symbol as "private".
                # This makes GDB backtraces look nicer too:
                # https://stackoverflow.com/a/26065570/965979
                emit(f'.L{insn.name}:')
            case ir.LoadIntConst():
                if -2**31 <= insn.value < 2**31:
                    emit(f'movq ${insn.value}, {locals.get_ref(insn.dest)}')
                else:
                    # Due to a quirk of x86-64, we must use
                    # a different instruction for large integers.
                    # It can only write to a register,
                    # not a memory location, so we use %rax
                    # as a temporary.
                    emit(f'movabsq ${insn.value}, %rax')
                    emit(f'movq %rax, {locals.get_ref(insn.dest)}')

            case ir.LoadBoolConst():
                value = "1" if insn.value else "0"
                dest_ref = locals.get_ref(insn.dest)
                emit(f"movq ${value}, {dest_ref}")

            case ir.Copy():
                src_ref = locals.get_ref(insn.source)
                dest_ref = locals.get_ref(insn.dest)
                emit(f"movq {src_ref}, %rax")
                emit(f"movq %rax, {dest_ref}")

            case ir.CondJump():
                cond_ref = locals.get_ref(insn.cond)
                emit(f"cmpq $0, {cond_ref}")
                emit(f"jne .L{insn.then_label.name}")
                emit(f"jmp .L{insn.else_label.name}")

            case ir.Jump():
                emit(f'jmp .L{insn.label.name}')

    # 函数返回前恢复栈和寄存器的状态
    emit("movq %rbp, %rsp")
    emit("popq %rbp")
    emit("ret")

    return "\n".join(lines)