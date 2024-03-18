class SymTab:
    def __init__(self):
        self.scopes = [{}]

    def enter_scope(self):
        self.scopes.append({})

    def leave_scope(self):
        print(self.scopes)
        self.scopes.pop()

    def define_variable(self, name, value):
        if self.scopes:
            self.scopes[-1][name] = value
        print(self.scopes)

    def lookup_variable(self, name):
        print(self.scopes)
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        raise KeyError(f"Variable '{name}' not found.")
