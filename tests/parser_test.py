import unittest

from src.compiler.tokenizer import tokenize
from src.models import ast
from src.models.ast import IfExpr, FunctionCall, BinaryOp, Identifier, UnaryOp, BlockExpr, VarDecl, Literal
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


class TestBlockExpressions(unittest.TestCase):
    def test_empty_block(self):
        tokens = tokenize("{}")
        expr = parse(tokens)
        self.assertIsInstance(expr, BlockExpr)
        self.assertEqual(len(expr.expressions), 0)
        self.assertIsNone(expr.result_expression)

    def test_block_with_result_expression(self):
        tokens = tokenize("{ a ; b }")
        expr = parse(tokens)
        print(expr)
        self.assertIsInstance(expr, BlockExpr)
        # Expecting 2 expressions in the list, since the block parsing logic
        # does not currently distinguish 'b' as a result expression implicitly.
        self.assertEqual(len(expr.expressions), 1)
        self.assertIsInstance(expr.result_expression, ast.Identifier)
        self.assertEqual(expr.result_expression.name, "b")

    def test_block_missing_semicolon(self):
        tokens = tokenize("{ a b }")
        with self.assertRaises(Exception):
            parse(tokens)


class TestVarDeclarations(unittest.TestCase):
    def test_var_declaration_in_block(self):
        tokens = tokenize("{ var x = 123; }")
        expr = parse(tokens)
        print(expr)
        self.assertIsInstance(expr, BlockExpr)
        self.assertIsInstance(expr.expressions[0], VarDecl)
        self.assertEqual(expr.expressions[0].name, "x")
        self.assertIsInstance(expr.expressions[0].value, Literal)
        self.assertEqual(expr.expressions[0].value.value, 123)

class TestFlexibleSemicolons(unittest.TestCase):
    def test_blocks_without_semicolons(self):
        expression = "{ { a } { b } }"
        tokens = tokenize(expression)
        expr = parse(tokens)
        # Assert the block structure is correctly parsed
        # The specifics of the assertion depend on your AST structure

    def test_disallowed_consecutive_statements(self):
        expression = "{ a b }"
        with self.assertRaises(Exception):
            tokens = tokenize(expression)
            parse(tokens)

    def test_if_then_block_without_semicolon(self):
        expression = "{ if true then { a } b }"
        tokens = tokenize(expression)
        expr = parse(tokens)
        # Assert the correct parsing of the if-then structure and following statement

    def test_if_then_block_with_semicolon(self):
        expression = "{ if true then { a }; b }"
        tokens = tokenize(expression)
        expr = parse(tokens)
        # Similar assertions to the previous test, ensuring the semicolon doesn't disrupt parsing

    def test_if_then_else_with_result_expression(self):
        expression = "{ if true then { a } else { b } 3 }"
        tokens = tokenize(expression)
        expr = parse(tokens)
        print(expr)
        # Assert the correct parsing of the if-then-else structure and the result expression

    def test_nested_blocks_assignment(self):
        expression = "x = { { f(a) } { b } }"
        tokens = tokenize(expression)
        expr = parse(tokens)
        # Assert that the assignment to x correctly includes the nested block structure as its value

class TestWhileLoop(unittest.TestCase):
    def test_while_loop(self):
        expression = "while x do { x = x - 1 }"
        tokens = tokenize(expression)
        expr = parse(tokens)
        print(expr)
        expected_while_expr = ast.WhileExpr(
            condition=ast.Identifier(name='x', location=SourceLocation(file='<unknown>', line=1, column=7)),
            body=ast.BlockExpr(
                expressions=[],
                result_expression=ast.BinaryOp(
                    left=ast.Identifier(name='x', location=SourceLocation(file='<unknown>', line=1, column=14)),
                    op='=',
                    right=ast.BinaryOp(
                        left=ast.Identifier(name='x', location=SourceLocation(file='<unknown>', line=1, column=18)),
                        op='-',
                        right=ast.Literal(value=1, location=SourceLocation(file='<unknown>', line=1, column=22)),
                        location=SourceLocation(file='<unknown>', line=1, column=20)
                    ),
                    location=SourceLocation(file='<unknown>', line=1, column=16)
                ),
                location=SourceLocation(file='<unknown>', line=1, column=12)
            ),
            location=SourceLocation(file='<unknown>', line=1, column=1)
        )

        self.assertEqual(expr, expected_while_expr)

if __name__ == '__main__':
    unittest.main()
