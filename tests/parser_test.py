import unittest
from _ast import IfExp

from src.compiler.tokenizer import tokenize
from src.models import ast
from src.models.ast import IfExpr, FunctionCall, BinaryOp, Identifier, UnaryOp
from src.models.types import Token, SourceLocation

# 假设你的解析器和AST定义在以下模块中
from src.compiler.parser import parse

class TestParserFunc(unittest.TestCase):
    def test_parse_int_literal(self):
        tokens = tokenize("123")
        result = parse(tokens)
        self.assertIsInstance(result, ast.Literal)
        self.assertEqual(result.value, 123)

    def test_parse_identifier(self):
        tokens = tokenize("x")
        result = parse(tokens)
        self.assertIsInstance(result, ast.Identifier)
        self.assertEqual(result.name, 'x')

class TestLeftRightExpression(unittest.TestCase):
    def test_parse_simple_expression(self):
        tokens = tokenize("x + 1")
        result = parse(tokens)
        self.assertIsInstance(result, ast.BinaryOp)
        self.assertEqual(result.op, '+')
        self.assertIsInstance(result.left, ast.Identifier)
        self.assertEqual(result.left.name, 'x')
        self.assertIsInstance(result.right, ast.Literal)
        self.assertEqual(result.right.value, 1)

    def test_right_associative_expression(self):
        # 测试表达式 "1 - 2 + 3" 应被解析为 "1 - (2 + 3)"
        tokens = tokenize("1 - 2 + 3")
        expr = parse(tokens, right_associative=True)
        self.assertIsInstance(expr, ast.BinaryOp)
        self.assertEqual(expr.op, '-')
        self.assertIsInstance(expr.right, ast.BinaryOp)
        self.assertEqual(expr.right.op, '+')

class TestMathExpressions(unittest.TestCase):
    def test_simple_addition(self):
        tokens = tokenize("1 + 2")
        expr = parse(tokens)
        self.assertIsInstance(expr, ast.BinaryOp)
        self.assertEqual(expr.op, '+')

    def test_expression_with_parentheses(self):
        tokens = tokenize("( 1 + 2 ) * 3")
        expr = parse(tokens)
        self.assertIsInstance(expr, ast.BinaryOp)
        self.assertEqual(expr.op, '*')
        self.assertIsInstance(expr.left, ast.BinaryOp)
        self.assertEqual(expr.left.op, '+')


class TestParserFailures(unittest.TestCase):
    def test_garbage_at_end(self):
        tokens = tokenize("a + b c")
        with self.assertRaises(Exception):
            parse(tokens)

    def test_empty_input(self):
        tokens = []
        with self.assertRaises(Exception):
            parse(tokens)

    def test_unclosed_parenthesis(self):
        tokens = tokenize("a + ( b")
        with self.assertRaises(Exception):
            parse(tokens)

class TestIfExpressions(unittest.TestCase):
    def test_if_then_else(self):
        tokens = tokenize("if a then b + c else x * y")
        expr = parse(tokens)
        self.assertIsInstance(expr, IfExpr)
        # 进一步测试 expr 的结构以确保正确解析了条件、then 分支和 else 分支

    def test_if_then(self):
        tokens = tokenize("if a then b + c")
        expr = parse(tokens)
        self.assertIsInstance(expr, IfExpr)
        # 测试 expr 结构，确保正确解析并处理缺少 else 分支的情况

    def test_if_in_expression(self):
        tokens = tokenize("1 + if true then 2 else 3")
        expr = parse(tokens)
        # 测试 expr 结构，确保 if-then-else 表达式能作为其他表达式的一部分被正确解析

class TestFunctionCalls(unittest.TestCase):
    def test_simple_function_call(self):
        tokens = tokenize("f(x, y + z)")
        expr = parse(tokens)
        self.assertIsInstance(expr, FunctionCall)
        self.assertEqual(expr.name, "f")
        self.assertEqual(len(expr.arguments), 2)

class TestParser(unittest.TestCase):
    def test_function_call(self):
        expression = "f(x, y + z)"
        tokens = tokenize(expression)
        expr = parse(tokens)
        self.assertIsInstance(expr, FunctionCall)
        self.assertEqual(expr.name, "f")
        self.assertEqual(len(expr.arguments), 2)

    def test_binary_operators_precedence(self):
        expression = "a + b * c"
        tokens = tokenize(expression)
        expr = parse(tokens)
        self.assertIsInstance(expr, ast.BinaryOp)
        self.assertEqual(expr.op, '+')
        self.assertIsInstance(expr.right, ast.BinaryOp)
        self.assertEqual(expr.right.op, '*')

    def test_unary_operator(self):
        expression = "not not x"
        tokens = tokenize(expression)
        expr = parse(tokens)
        self.assertIsInstance(expr, ast.UnaryOp)
        self.assertEqual(expr.operator, 'not')
        self.assertIsInstance(expr.operand, ast.UnaryOp)

    def test_assignment_right_associative(self):
        expression = "a = b = c"
        tokens = tokenize(expression)
        expr = parse(tokens)
        self.assertIsInstance(expr, ast.BinaryOp)
        self.assertEqual(expr.op, '=')
        self.assertIsInstance(expr.right, ast.BinaryOp)
        self.assertEqual(expr.right.op, '=')

    def test_parentheses(self):
        expression = "(a + b) * c"
        tokens = tokenize(expression)
        expr = parse(tokens)
        self.assertIsInstance(expr, ast.BinaryOp)
        self.assertEqual(expr.op, '*')
        self.assertIsInstance(expr.left, ast.BinaryOp)
        self.assertEqual(expr.left.op, '+')

if __name__ == '__main__':
    unittest.main()
