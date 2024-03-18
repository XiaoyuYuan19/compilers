class SymTab:
    def __init__(self, parent=None):
        self.locals = {}
        self.parent = parent

    def add(self, name, value):
        self.locals[name] = value

    def get(self, name):
        if name in self.locals:
            return self.locals[name]
        elif self.parent:
            return self.parent.get(name)
        else:
            raise KeyError(name)
