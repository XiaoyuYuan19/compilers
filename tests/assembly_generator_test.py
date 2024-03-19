import unittest
from src.compiler.tokenizer import tokenize
from src.compiler.parser import parse
from src.compiler.ir_generator import generate_ir
from src.compiler.assembly_generator import generate_assembly
from src.models.SymTab import SymTab, add_builtin_symbols


class AssemblyGeneratorDetailedTest(unittest.TestCase):
    def setUp(self):
        # 在每个测试用例开始前初始化符号表和添加内置符号
        self.symtab = SymTab()
        add_builtin_symbols(self.symtab)  # 确保你已经实现了这个函数

    def test_load_bool_const_true(self):
        source_code = "true"
        tokens = tokenize(source_code)
        ast_root = parse(tokens)
        ir_instructions = generate_ir(ast_root)
        assembly_code = generate_assembly(ir_instructions)
        self.assertIn("movq $1", assembly_code)

    def test_load_bool_const_false(self):
        source_code = "false"
        tokens = tokenize(source_code)
        ast_root = parse(tokens)
        ir_instructions = generate_ir(ast_root)
        assembly_code = generate_assembly(ir_instructions)
        self.assertIn("movq $0", assembly_code)

    def test_conditional_jump(self):
        source_code = "if true then 1 else 2"
        tokens = tokenize(source_code)
        ast_root = parse(tokens)
        ir_instructions = generate_ir(ast_root)
        assembly_code = generate_assembly(ir_instructions)
        self.assertIn("jne", assembly_code)
        self.assertIn("jmp", assembly_code)

    def test_variable_declaration_and_usage(self):
        source_code = "{ var x = true; x; }"
        tokens = tokenize(source_code)
        ast_root = parse(tokens)
        ir_instructions = generate_ir(ast_root)
        assembly_code = generate_assembly(ir_instructions)
        self.assertIn("movq $1", assembly_code)  # 检查变量x赋值为true
        # 此测试可能需要更详细的检查来确认变量x的使用

    def test_if_else_logic(self):
        source_code = "{ var x : Int = 1; if x == 1 then 1 else 2; }"
        # source_code = "{ var x : Bool = true; if x then 1 else 2; }"
        tokens = tokenize(source_code)
        ast_root = parse(tokens)
        ir_instructions = generate_ir(ast_root)
        assembly_code = generate_assembly(ir_instructions)
        # self.assertIn("movq $1", assembly_code)  # 检查x为true时的情况
        # self.assertIn("jne", assembly_code)  # 检查条件跳转指令
        # 这个测试可能需要更多的逻辑来完全验证if-else的行为


if __name__ == "__main__":
    unittest.main()
