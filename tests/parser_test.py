import unittest
from src.models import ast
from src.models.types import Token, SourceLocation

# 假设你的解析器和AST定义在以下模块中
from src.compiler.parser import parse

class TestParser(unittest.TestCase):
    def test_parse_int_literal(self):
        tokens = [Token(text='123', type='int_literal', loc=SourceLocation())]
        result = parse(tokens)
        self.assertIsInstance(result, ast.Literal)
        self.assertEqual(result.value, 123)

    def test_parse_identifier(self):
        tokens = [Token(text='x', type='identifier', loc=SourceLocation())]
        result = parse(tokens)
        self.assertIsInstance(result, ast.Identifier)
        self.assertEqual(result.name, 'x')

    def test_parse_simple_expression(self):
        tokens = [
            Token(text='x', type='identifier', loc=SourceLocation()),
            Token(text='+', type='operator', loc=SourceLocation()),
            Token(text='1', type='int_literal', loc=SourceLocation())
        ]
        result = parse(tokens)
        self.assertIsInstance(result, ast.BinaryOp)
        self.assertEqual(result.op, '+')
        self.assertIsInstance(result.left, ast.Identifier)
        self.assertEqual(result.left.name, 'x')
        self.assertIsInstance(result.right, ast.Literal)
        self.assertEqual(result.right.value, 1)

    def test_right_associative_expression(self):
        # 测试表达式 "1 - 2 + 3" 应被解析为 "1 - (2 + 3)"
        tokens = [
            Token(text='1', type='int_literal', loc=None),
            Token(text='-', type='operator', loc=None),
            Token(text='2', type='int_literal', loc=None),
            Token(text='+', type='operator', loc=None),
            Token(text='3', type='int_literal', loc=None),
        ]
        expr = parse(tokens, right_associative=True)
        self.assertIsInstance(expr, ast.BinaryOp)
        self.assertEqual(expr.op, '-')
        self.assertIsInstance(expr.right, ast.BinaryOp)
        self.assertEqual(expr.right.op, '+')

if __name__ == '__main__':
    unittest.main()
