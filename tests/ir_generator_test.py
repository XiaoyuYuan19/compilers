import unittest
from src.compiler.parser import parse
from src.compiler.tokenizer import tokenize
from src.compiler.ir_generator import generate_ir
from src.models.ir import (
    LoadIntConst, LoadBoolConst, Call, Copy, Label, Jump, CondJump, IRVar
)

class IRGeneratorTestCase(unittest.TestCase):
    def setUp(self):
        # 此处可以添加任何初始化逻辑，例如加载测试数据等
        pass

    def test_literal_int(self):
        source_code = "42"

        ast_root = parse(tokenize(source_code))
        ir_instructions = generate_ir(ast_root)

        for i in ir_instructions:
            print(i)
        self.assertIsInstance(ir_instructions[0], LoadIntConst)
        self.assertEqual(ir_instructions[0].value, 42)

    def test_literal_bool(self):
        source_code = "true"
        ast_root = parse(tokenize(source_code))
        ir_instructions = generate_ir(ast_root)
        self.assertIsInstance(ir_instructions[0], LoadBoolConst)
        self.assertTrue(ir_instructions[0].value)

    def test_binary_op_addition(self):
        source_code = "1 + 2"
        ast_root = parse(tokenize(source_code))
        ir_instructions = generate_ir(ast_root)
        self.assertEqual(len(ir_instructions), 4)
        self.assertIsInstance(ir_instructions[2], Call)
        self.assertEqual(ir_instructions[2].fun, "+")

    def test_var_decl_with_assignment(self):
        source_code = "{ var x: Int = 42 ;  }"
        ast_root = parse(tokenize(source_code))
        print(ast_root)
        ir_instructions = generate_ir(ast_root)
        print(ir_instructions)
        self.assertIsInstance(ir_instructions[0], LoadIntConst)
        self.assertIsInstance(ir_instructions[1], Copy)
        self.assertEqual(ir_instructions[0].value, 42)

    def test_if_true_then_42_else_43(self):
        source_code = "if true then 42 else 43"
        ast_root = parse(tokenize(source_code))
        print(ast_root)
        ir_instructions = generate_ir(ast_root)

        # 检查布尔常量加载指令
        self.assertIsInstance(ir_instructions[0], LoadBoolConst)
        self.assertTrue(ir_instructions[0].value)
        self.assertIsInstance(ir_instructions[0].dest, IRVar)

        # 检查条件跳转指令
        self.assertIsInstance(ir_instructions[1], CondJump)
        self.assertEqual(ir_instructions[1].cond.name, ir_instructions[0].dest.name)

        # 检查then分支的加载常量指令
        self.assertIsInstance(ir_instructions[3], LoadIntConst)
        self.assertEqual(ir_instructions[3].value, 42)

        # 检查then分支的结果复制指令
        self.assertIsInstance(ir_instructions[4], Copy)

        # 检查跳转到结束标签的跳转指令
        self.assertIsInstance(ir_instructions[5], Jump)

        # 检查else分支的加载常量指令
        self.assertIsInstance(ir_instructions[7], LoadIntConst)
        self.assertEqual(ir_instructions[7].value, 43)

        # 检查else分支的结果复制指令
        self.assertIsInstance(ir_instructions[8], Copy)

        # 检查是否包含结束标签
        self.assertIsInstance(ir_instructions[9], Label)

class TestIRGeneratorScopes(unittest.TestCase):
    def test_nested_scope_var_decl_with_assignment(self):
        source_code = "{ var x: Int = 42  { var x: Int = 1 } x }"
        ast_root = parse(tokenize(source_code))
        print(ast_root)
        ir_instructions = generate_ir(ast_root)

        # 检查全局变量x被初始化为42
        self.assertIsInstance(ir_instructions[0], LoadIntConst, "首条指令应该是 LoadIntConst 初始化全局x为42")
        self.assertEqual(ir_instructions[0].value, 42, "全局x的值应为42")

        # 检查嵌套作用域内的变量x被初始化为1
        self.assertIsInstance(ir_instructions[2], LoadIntConst, "第三条指令应该是 LoadIntConst 初始化局部x为1")
        self.assertEqual(ir_instructions[2].value, 1, "局部x的值应为1")
        # self.assertIsInstance(ir_instructions[-1], Copy, "最后一条指令应该是Copy，表示引用了x的值")


if __name__ == '__main__':
    unittest.main()
