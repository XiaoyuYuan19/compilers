import unittest


from src.compiler.interpreter import interpret
from src.compiler.parser import parse
from src.compiler.tokenizer import tokenize
from src.models import ast
from src.models.SymTab import SymTab, add_builtin_symbols
from src.models.types import SourceLocation

L = SourceLocation()


class TestInterpreter(unittest.TestCase):
    def setUp(self):
        # 在每个测试用例开始前初始化符号表和添加内置符号
        self.symtab = SymTab()
        add_builtin_symbols(self.symtab)  # 确保你已经实现了这个函数

    def test_arithmetic_operations(self):
        # 测试基本的算术运算
        source_code = "3 + 4 * 2 - 1"
        tokens = tokenize(source_code)
        ast = parse(tokens)
        result = interpret(ast, self.symtab)
        self.assertEqual(result, 10)

    def test_variable_declaration_and_use(self):
        # 测试变量声明和使用
        source_code = "{ var x = 5; x * 2 }"
        tokens = tokenize(source_code)
        ast = parse(tokens)
        result = interpret(ast, self.symtab)
        self.assertEqual(result, 10)

    def test_conditional_logic(self):
        # 测试条件逻辑
        source_code = "if true then 42 else 0"
        tokens = tokenize(source_code)
        ast = parse(tokens)
        result = interpret(ast, self.symtab)
        self.assertEqual(result, 42)

    def test_arithmetic_operators(self):
        tests = [
            ("1 + 2", 3),
            ("4 - 2", 2),
            ("6 * 2", 12),
            ("8 / 2", 4),
            ("10 % 3", 1),
        ]
        for source_code, expected in tests:
            with self.subTest(source_code=source_code):
                print(source_code)
                block = parse(tokenize(source_code))
                result = interpret(block, self.symtab)
                self.assertEqual(result, expected)

    def test_comparison_operators(self):
        tests = [
            ("1 == 1", True),
            ("2 != 1", True),
            ("3 < 4", True),
            ("5 <= 5", True),
            ("6 > 5", True),
            ("7 >= 7", True),
        ]
        for source_code, expected in tests:
            with self.subTest(source_code=source_code):
                block = parse(tokenize(source_code))
                result = interpret(block, self.symtab)
                self.assertEqual(result, expected)

    def test_logical_operators(self):
        tests = [
            ("true and false", False),
            ("true or false", True),
            ("not true", False),
        ]
        for source_code, expected in tests:
            with self.subTest(source_code=source_code):
                block = parse(tokenize(source_code))
                result = interpret(block, self.symtab)
                self.assertEqual(result, expected)

    def test_variable_scope(self):
        source_code = "{var x = 10; {var x = 20;} x}"
        block = parse(tokenize(source_code))
        result = interpret(block, self.symtab)
        self.assertEqual(result, 10)

    def test_if_statement(self):
        tests = [
            ("if true then 42 else 0", 42),
            ("if false then 42 else 0", 0),
        ]
        for source_code, expected in tests:
            with self.subTest(source_code=source_code):
                block = parse(tokenize(source_code))
                result = interpret(block, self.symtab)
                self.assertEqual(result, expected)

    # def test_while_loop(self):
    #     source_code = "{var x = 0; while x < 5 do var x = x + 1; x}"
    #     block = parse(tokenize(source_code))
    #     result = interpret(block, self.symtab)
    #     self.assertEqual(result, 5)

    def test_short_circuit_logic(self):
        # 测试'or'的短路行为
        source_code = """{
        var evaluated_right_hand_side = false;
        true or { evaluated_right_hand_side = true; true };
        evaluated_right_hand_side}# 应该为false
        """
        block = parse(tokenize(source_code))
        result = interpret(block, self.symtab)
        self.assertEqual(result, False)  # 确认右侧未被评估

        # 测试'and'的短路行为
        source_code = """{
        var evaluated_right_hand_side = false;
        false and { evaluated_right_hand_side = true; false };
        evaluated_right_hand_side} #应该为false
        """
        block = parse(tokenize(source_code))
        result = interpret(block, self.symtab)
        self.assertEqual(result, False)  # 确认右侧未被评估

if __name__ == '__main__':
    unittest.main()
