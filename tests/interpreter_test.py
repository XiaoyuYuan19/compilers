import unittest

from src.compiler.interpreter import interpret
from src.models import ast
from src.models.types import SourceLocation

L = SourceLocation()
class TestInterpreter(unittest.TestCase):
    def test_basic_arithmetic(self):
        # Test for "2 + 3"
        expr_ast = ast.BinaryOp(left=ast.Literal(value=2,location=L), op='+', right=ast.Literal(value=3,location=L),location=L)
        result = interpret(expr_ast)
        self.assertEqual(result, 5)

    def test_comparison(self):
        # Test for "2 < 3"
        expr_ast = ast.BinaryOp(left=ast.Literal(value=2,location=L), op='<', right=ast.Literal(value=3,location=L),location=L)
        result = interpret(expr_ast)
        self.assertTrue(result)

    def test_if_then_else_true_branch(self):
        # Test for "if true then 5 else 10"
        condition = ast.Literal(value=True,location=L)
        then_branch = ast.Literal(value=5,location=L)
        else_branch = ast.Literal(value=10,location=L)
        expr_ast = ast.IfExpr(condition=condition, then_branch=then_branch, else_branch=else_branch,location=L)
        result = interpret(expr_ast)
        self.assertEqual(result, 5)

    def test_if_then_else_false_branch(self):
        # Test for "if false then 5 else 10"
        condition = ast.Literal(value=False,location=L)
        then_branch = ast.Literal(value=5,location=L)
        else_branch = ast.Literal(value=10,location=L)
        expr_ast = ast.IfExpr(condition=condition, then_branch=then_branch, else_branch=else_branch,location=L)
        result = interpret(expr_ast)
        self.assertEqual(result, 10)


if __name__ == '__main__':
    unittest.main()
