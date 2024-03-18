import unittest

from src.compiler.parser import parse
from src.compiler.tokenizer import tokenize
from src.compiler.type_checker import typecheck
from src.models import ast, types
from src.models.SymTab import SymTab, add_builtin_symbols
from src.models.types import Unit, Int, Bool
from tests.interpreter_test import L


class TestTypeChecker(unittest.TestCase):
    def setUp(self):
        self.symtab = SymTab()
        add_builtin_symbols(self.symtab)

    def test_int_literal(self):
        node = parse(tokenize("42"))
        self.assertIsInstance(typecheck(node, self.symtab), types.Int)

    def test_bool_literal(self):
        node = parse(tokenize("True"))
        self.assertIsInstance(typecheck(node, self.symtab), types.Bool)

    def test_binary_op_ints(self):
        node = parse(tokenize("42 + 1"))
        self.assertIsInstance(typecheck(node, self.symtab), types.Int)

    def test_binary_op_type_mismatch(self):
        node = parse(tokenize("42 + True"))
        with self.assertRaises(TypeError):
            typecheck(node, self.symtab)

    def test_variable_lookup(self):
        self.symtab.define_variable("x", 10, types.Int())
        node = ast.Identifier(name="x",location=L)
        self.assertIsInstance(typecheck(node, self.symtab), types.Int)

    def test_if_expr(self):
        node = parse(tokenize("if True then 42 else 1"))
        self.assertIsInstance(typecheck(node, self.symtab), types.Int)

    def test_if_expr_type_mismatch(self):
        node = parse(tokenize("if True then 42 else False"))
        with self.assertRaises(TypeError):
            typecheck(node, self.symtab)


class TestUnitTypeChecker(unittest.TestCase):
    def setUp(self):
        self.symtab = SymTab()
        # 添加内置符号，如果有的话

    # def test_while_loop(self):
    #     source_code = "while true do {}"
    #     node = parse(tokenize(source_code))
    #     self.assertIsInstance(typecheck(node, self.symtab), Unit)

    def test_if_then_no_else(self):
        source_code = "if true then { 1 }"
        node = parse(tokenize(source_code))
        print(typecheck(node, self.symtab))
        self.assertIsInstance(typecheck(node, self.symtab), Unit)

# tests/test_type_checker.py
# src/tests/type_checker_test.py

# Updates for the TestTypeChecker class remain the same.

# Additional updates for TestUnitTypeChecker class:

class TestTypeCheckerWithFunctionTypes(unittest.TestCase):
    def setUp(self):
        # 在每个测试用例开始前初始化符号表和添加内置符号
        self.symtab = SymTab()
        add_builtin_symbols(self.symtab)  # 确保你已经实现了这个函数

    def test_function_call_with_correct_types(self):
        source_code = "print_int(42)"
        node = parse(tokenize(source_code))
        self.assertIsInstance(typecheck(node, self.symtab), Unit)

    def test_binary_op_with_correct_types(self):
        source_code = "42 + 1"
        node = parse(tokenize(source_code))
        self.assertIsInstance(typecheck(node, self.symtab), Int)

    def test_function_call_with_incorrect_argument_type(self):
        source_code = "print_int(True)"
        node = parse(tokenize(source_code))
        with self.assertRaises(TypeError):
            typecheck(node, self.symtab)

class TestUnaryOpTypeCheck(unittest.TestCase):
    def setUp(self):
        self.symtab = SymTab()
        # 假设 add_builtin_symbols 已经定义，用于添加内置类型和函数
        add_builtin_symbols(self.symtab)

    def test_not_operator_with_bool(self):
        source_code = "not true"
        node = parse(tokenize(source_code))
        result_type = typecheck(node, self.symtab)
        self.assertIsInstance(result_type, Bool)

    def test_not_operator_with_int(self):
        source_code = "not 42"
        node = parse(tokenize(source_code))
        with self.assertRaises(TypeError):
            typecheck(node, self.symtab)

class TestBlockTypeCheck(unittest.TestCase):
    def setUp(self):
        self.symtab = SymTab()
        add_builtin_symbols(self.symtab)

    def test_empty_block(self):
        source_code = "{}"
        node = parse(tokenize(source_code))
        result_type = typecheck(node, self.symtab)
        self.assertIsInstance(result_type, Unit)

    def test_block_with_last_expression_int(self):
        source_code = "{ true; 42 }"
        node = parse(tokenize(source_code))
        result_type = typecheck(node, self.symtab)
        self.assertIsInstance(result_type, Int)

    def test_block_with_last_expression_bool(self):
        source_code = "{ 42; false }"
        node = parse(tokenize(source_code))
        result_type = typecheck(node, self.symtab)
        self.assertIsInstance(result_type, Bool)

    def test_block_with_variable_declaration(self):
        source_code = "{ var x = true; x }"
        self.symtab.define_variable("x","x", Bool())  # 在测试中显式定义变量类型
        node = parse(tokenize(source_code))
        result_type = typecheck(node, self.symtab)
        self.assertIsInstance(result_type, Bool)


class TestBlockExpr(unittest.TestCase):
    def setUp(self):
        self.symtab = SymTab()
        add_builtin_symbols(self.symtab)

    def test_empty_block(self):
        source_code = "{}"
        node = parse(tokenize(source_code))
        result_type = typecheck(node, self.symtab)
        self.assertIsInstance(result_type, Unit)

    def test_block_with_multiple_statements(self):
        source_code = "{var x: Int = 42; var y: Bool = true; x}"
        node = parse(tokenize(source_code))
        result_type = typecheck(node, self.symtab)
        self.assertIsInstance(result_type, Int)

    def test_block_with_type_mismatch(self):
        source_code = "{var z : Int = 42; z = true}"
        node = parse(tokenize(source_code))
        with self.assertRaises(TypeError):
            typecheck(node, self.symtab)


if __name__ == '__main__':
    unittest.main()
