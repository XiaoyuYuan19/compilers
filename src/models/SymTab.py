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

    def define_variable(self, name, value):
        # 只在当前作用域定义新变量
        self.scopes[-1][name] = value

    def update_variable(self, name, value):
        # 在现有作用域中更新变量的值，如果变量存在
        for scope in reversed(self.scopes):
            if name in scope:
                scope[name] = value
                return
        raise KeyError(f"Variable '{name}' not defined.")

def add_builtin_symbols(symtab: SymTab):
    symtab.define_variable("+", lambda a, b: a + b)
    symtab.define_variable("-", lambda a, b: a - b)
    symtab.define_variable("*", lambda a, b: a * b)
    symtab.define_variable("/", lambda a, b: a / b)
    symtab.define_variable("%", lambda a, b: a % b)
    symtab.define_variable("==", lambda a, b: a == b)
    symtab.define_variable("!=", lambda a, b: a != b)
    symtab.define_variable("<", lambda a, b: a < b)
    symtab.define_variable("<=", lambda a, b: a <= b)
    symtab.define_variable(">", lambda a, b: a > b)
    symtab.define_variable(">=", lambda a, b: a >= b)
    symtab.define_variable("and", lambda a, b: a and b)
    symtab.define_variable("or", lambda a, b: a or b)
    symtab.define_variable("unary_-", lambda a: -a)
    symtab.define_variable("unary_not", lambda a: not a)