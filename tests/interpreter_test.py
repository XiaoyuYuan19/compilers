import unittest


from src.compiler.interpreter import interpret
from src.compiler.parser import parse
from src.compiler.tokenizer import tokenize
from src.models import ast
from src.models.SymTab import SymTab
from src.models.types import SourceLocation

L = SourceLocation()


class TestInterpreter(unittest.TestCase):
    def test_basic_arithmetic(self):
        # Test for "2 + 3"
        expr_ast = parse(tokenize("2 + 3"))
        result = interpret(expr_ast)
        self.assertEqual(result, 5)

    def test_comparison(self):
        # Test for "2 < 3"
        expr_ast = parse(tokenize("2 < 3"))
        result = interpret(expr_ast)
        self.assertTrue(result)

    def test_if_then_else_true_branch(self):
        expr_ast = parse(tokenize("if true then 5 else 10"))
        result = interpret(expr_ast)
        self.assertEqual(result, 5)

    def test_if_then_else_false_branch(self):
        expr_ast = parse(tokenize("if false then 5 else 10"))
        print(expr_ast)
        result = interpret(expr_ast)
        self.assertEqual(result, 10)


if __name__ == '__main__':
    unittest.main()
