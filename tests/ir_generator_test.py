import unittest
from src.compiler.parser import parse
from src.compiler.tokenizer import tokenize
from src.compiler.ir_generator import generate_ir
from src.models.ir import LoadIntConst, Call

class TestIRGenerator(unittest.TestCase):
    def test_simple_expression(self):
        source_code = "1 + 2"
        ast_root = parse(tokenize(source_code))
        ir_instructions = generate_ir(ast_root)

        # Verify the IR instructions
        self.assertIsInstance(ir_instructions[0], LoadIntConst)
        self.assertEqual(ir_instructions[0].value, 1)
        self.assertIsInstance(ir_instructions[1], LoadIntConst)
        self.assertEqual(ir_instructions[1].value, 2)
        self.assertIsInstance(ir_instructions[2], Call)
        self.assertEqual(ir_instructions[2].fun, '+')
        self.assertEqual(len(ir_instructions[2].args), 2)

        # Optionally, print IR for inspection (can be removed in actual tests)
        for instr in ir_instructions:
            print(instr)

    # Add more tests for other expressions and statements

if __name__ == '__main__':
    unittest.main()
