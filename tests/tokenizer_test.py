import unittest

from src.models.types import Token, SourceLocation
from src.compiler.tokenizer import tokenize

# Define a special source location for simplified comparison in tests
L = SourceLocation()


class TokenizerTest(unittest.TestCase):
    def test_tokenizer_functionality(self):
        code = "\n var \nx = (100 + 20) * 2.1; // 1 \n if false then 5 "
        expected_tokens = [
            Token("var", "identifier", L),
            Token("x", "identifier", L),
            Token("=", "operator", L),
            Token("(", "punctuation", L),
            Token("100", "integer", L),
            Token("+", "operator", L),
            Token("20", "integer", L),
            Token(")", "punctuation", L),
            Token("*", "operator", L),
            Token("2.1", "float", L),
            Token(";", "punctuation", L),
            Token("if", "identifier", L),
            Token("false", "bool", L),
            Token("then", "identifier", L),
            Token("5", "integer", L),
        ]

        tokens = tokenize(code)

        self.assertEqual(len(tokens), len(expected_tokens), "Number of tokens mismatch")

        for token, expected in zip(tokens, expected_tokens):
            with self.subTest(token=token, expected=expected):
                self.assertEqual(token, expected)


if __name__ == "__main__":
    unittest.main()
