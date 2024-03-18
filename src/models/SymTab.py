from src.models import types
from src.models.types import FunctionType, Int, Bool, Unit


class SymTab:
    def __init__(self):
        self.scopes = [{}]

    def enter_scope(self):
        self.scopes.append({})

    def leave_scope(self):
        self.scopes.pop()

    # def define_variable(self, name, value):
    #     if self.scopes:
    #         self.scopes[-1][name] = value

    def lookup_variable(self, name):
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        raise KeyError(f"Variable '{name}' not found.")

    # def define_variable(self, name, value):
    #     # 只在当前作用域定义新变量
    #     self.scopes[-1][name] = value

    def update_variable(self, name, value):
        # 在现有作用域中更新变量的值，如果变量存在
        for scope in reversed(self.scopes):
            if name in scope:
                scope[name] = value
                return
        raise KeyError(f"Variable '{name}' not defined.")

    def define_variable(self, name, value, var_type):
        self.scopes[-1][name] = (value, var_type)

    def lookup_variable_type(self, name):
        for scope in reversed(self.scopes):
            if name in scope:
                _, var_type = scope[name]
                return var_type
        raise KeyError(f"Type for variable '{name}' not found.")

def add_builtin_symbols(symtab: SymTab):
    symtab.define_variable("true", True, types.Bool())
    symtab.define_variable("false", False, types.Bool())

    symtab.define_variable("+", lambda a, b: a + b, FunctionType([Int(), Int()], Int()))
    symtab.define_variable("-", lambda a, b: a + b, FunctionType([Int(), Int()], Int()))
    symtab.define_variable("*", lambda a, b: a + b, FunctionType([Int(), Int()], Int()))
    symtab.define_variable("/", lambda a, b: a + b, FunctionType([Int(), Int()], Int()))
    symtab.define_variable("%", lambda a, b: a + b, FunctionType([Int(), Int()], Int()))

    symtab.define_variable("==", lambda a, b: a < b, FunctionType([Int(), Int()], Bool()))
    symtab.define_variable("!=", lambda a, b: a < b, FunctionType([Int(), Int()], Bool()))
    symtab.define_variable("<", lambda a, b: a < b, FunctionType([Int(), Int()], Bool()))
    symtab.define_variable("<=", lambda a, b: a < b, FunctionType([Int(), Int()], Bool()))
    symtab.define_variable(">", lambda a, b: a < b, FunctionType([Int(), Int()], Bool()))
    symtab.define_variable(">=", lambda a, b: a < b, FunctionType([Int(), Int()], Bool()))

    symtab.define_variable("and", lambda a, b: a < b, FunctionType([Bool(), Bool()], Bool()))
    symtab.define_variable("or", lambda a, b: a or b, FunctionType([Bool(), Bool()], Bool()))
    symtab.define_variable("unary_not", lambda a, b: a or b, FunctionType([Bool()], Bool()))
    symtab.define_variable("unary_-", lambda a: -a, FunctionType([Int()], Int()))
    symtab.define_variable("print_int", print, FunctionType([Int()], Unit()))
