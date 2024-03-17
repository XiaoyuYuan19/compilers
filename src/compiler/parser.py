from src.models import ast
from src.models.ast import IfExpr, FunctionCall, BlockExpr, VarDecl
from src.models.types import Token

precedence_levels = [
    ['='],
    ['or'],
    ['and'],
    ['==', '!='],
    ['<', '<=', '>', '>='],
    ['+', '-', '%'],
    ['*', '/'],
    ['not'],  # 一元操作符的优先级
]

def parse(tokens: list[Token], right_associative=False) -> ast.Expression:

    # This keeps track of which token we're looking at.

    pos = 0

    def peek() -> Token:
        if pos < len(tokens):
            return tokens[pos]
        else:
            return Token(loc=tokens[-1].loc, type="end", text="")

    def consume(expected:  str | list[str] | None = None) -> Token:
        nonlocal pos
        token = peek()
        if isinstance(expected, str) and token.text != expected:
            raise Exception(f'{token.loc}: expected "{expected}"')
        if isinstance(expected, list) and token.text not in expected:
            comma_separated = ", ".join([f'"{e}"' for e in expected])
            raise Exception(f'{token.loc}: expected one of: {comma_separated}')
        pos += 1
        return token


    def parse_int_literal() -> ast.Literal:
        if peek().type != 'integer':
            raise Exception(f'{peek().loc}: expected an integer literal')
        token = consume()
        return ast.Literal(int(token.text))

    def parse_identifier() -> ast.Identifier:
        if peek().type != 'identifier':
            raise Exception(f'{peek().loc}: expected an identifier')
        token = consume()
        return ast.Identifier(name=token.text)

    def parse_term() -> ast.Expression:
        # 处理乘法和除法
        left = parse_factor()
        while peek().text in ['*', '/']:
            operator_token = consume()
            operator = operator_token.text
            right = parse_factor()
            left = ast.BinaryOp(left, operator, right)
        return left

    def parse_binary_expression(level=0) -> ast.Expression:
        if level == len(precedence_levels):
            return parse_unary_expression()

        left_expr = parse_binary_expression(level + 1)
        while peek().text in precedence_levels[level]:
            op_token = consume()
            if op_token.text == '=':
                # Special handling for right associativity of assignment
                right_expr = parse_binary_expression(level)  # Use the same level for right associativity
            else:
                right_expr = parse_binary_expression(level + 1)
            left_expr = ast.BinaryOp(left_expr, op_token.text, right_expr)

        return left_expr

    def parse_unary_expression() -> ast.Expression:
        if peek().text == 'not':
            op_token = consume('not')
            expr = parse_unary_expression()  # 递归以支持链式一元操作符
            return ast.UnaryOp(op_token.text, expr)
        else:
            return parse_factor()

    def parse_factor() -> ast.Expression:
        if peek().text == '(':
            return parse_parenthesized()
        elif peek().text == '{':
            return parse_block()
        elif peek().text == 'if':
            return parse_if_expr()
        elif peek().type == 'identifier':
            next_pos = pos + 1
            if next_pos < len(tokens) and tokens[next_pos].text == '(':
                return parse_function_call()
            else:
                return parse_identifier()
        elif peek().type == 'integer':
            return parse_int_literal()
        else:
            raise Exception(f'{peek().loc}: unexpected token "{peek().text}"')


    # def parse_block() -> ast.BlockExpr:
    #     consume('{')
    #     expressions = []
    #     result_expression = None
    #
    #     while not peek().text == '}':
    #         if peek().text == 'var':
    #             expr = parse_var_decl()
    #         else:
    #             expr = parse_expression()
    #         if peek().text == ';':
    #             consume(';')
    #             expressions.append(expr)
    #         elif peek().text == '}':
    #             result_expression = expr
    #         else:
    #             raise Exception(f"{peek().loc}: Expected ';' or '}}'")
    #
    #     consume('}')
    #     return BlockExpr(expressions, result_expression)

    # def parse_block() -> ast.BlockExpr:
    #     consume('{')
    #     expressions = []
    #     while not peek().text == '}':
    #         expr = parse_expression()
    #         expressions.append(expr)
    #         print(peek().text,peek().type)
    #         # Look ahead to decide whether to consume a semicolon
    #         if peek().text == ';':
    #             consume(';')  # Optional semicolon
    #         elif peek().text not in ['}', 'if', 'while', '{', 'var']:  # Adjust based on valid start tokens
    #             raise Exception(f"{peek().loc}: Expected ';' or '}}'")
    #
    #     consume('}')
    #     return ast.BlockExpr(expressions)

    def parse_block() -> ast.BlockExpr:
        consume('{')
        expressions = []
        result_expression = None

        while not peek().text == '}':

            if peek().text in ['if', 'while', '{']:  # Starting a new block or control structure
                expr = parse_expression()
                expressions.append(expr)
                # Check if next token is '}', in which case, this block/expression might be the result_expression
                if peek().text == '}':
                    result_expression = expressions.pop()  # Last expression is result_expression
                elif peek().text == ';':  # Optional semicolon after a block/control structure
                    consume(';')
            else:
                if peek().text == 'var':
                    expr = parse_var_decl()
                else:
                    expr = parse_expression()
                if peek().text == ';':
                    consume(';')
                    expressions.append(expr)
                elif peek().text in ['}', 'if', 'while', '{']:  # No semicolon required before these
                    expressions.append(expr)
                else:
                    raise Exception(f"{peek().loc}: Expected ';' or '}}' but found '{peek().text}'")

        consume('}')

        return BlockExpr(expressions, result_expression)

    def parse_function_call() -> ast.Expression:
        name_token = consume()  # 函数名
        consume('(')  # 消费左括号
        arguments = []
        if peek().text != ')':
            while True:
                arg = parse_expression()
                arguments.append(arg)
                if peek().text == ',':
                    consume(',')  # 消费逗号，继续读取下一个参数
                else:
                    break
        consume(')')  # 消费右括号
        return FunctionCall(name=name_token.text, arguments=arguments)

    def parse_if_expr() -> ast.Expression:
        consume('if')
        condition = parse_expression()
        consume('then')
        then_branch = parse_expression()
        else_branch = None
        if peek().text == 'else':
            consume('else')
            else_branch = parse_expression()
        return IfExpr(condition, then_branch, else_branch)

    def parse_parenthesized() -> ast.Expression:
        consume('(')
        # Recursively call the top level parsing function
        # to parse whatever is inside the parentheses.
        expr = parse_expression()
        consume(')')
        return expr

    def parse_var_decl() -> ast.VarDecl:
        consume('var')  # Consume the 'var' keyword
        name_token = consume()  # Expect an identifier next
        consume('=')  # Expect an '=' after the identifier
        value = parse_expression()  # Parse the initialization expression
        return VarDecl(name=name_token.text, value=value)

    def parse_expression_right() -> ast.Expression:
        left = parse_term()

        if peek().text in ['+', '-']:
            operator_token = consume()
            operator = operator_token.text

            # 通过递归调用 `parse_expression` 来解析右边的表达式，
            # 实现右结合性
            right = parse_expression()

            # 构建并返回一个二元操作的AST节点，左边是`left`，右边是`right`的结果
            return ast.BinaryOp(
                left,
                operator,
                right
            )
        else:
            return left


    # 根据 right_associative 参数选择解析函数
    def parse_expression() -> ast.Expression:
        if right_associative:
            return parse_expression_right()
        else:
            return parse_binary_expression(0)


    # 右结合解析逻辑
    def parse_expression_right() -> ast.Expression:
        # 之前的 parse_expression_right() 代码
        left = parse_term()
        if peek().text in ['+', '-']:
            operator_token = consume()
            operator = operator_token.text
            right = parse_expression()  # 注意这里递归调用 parse_expression()
            return ast.BinaryOp(left, operator, right)
        else:
            return left

    res = parse_expression()
    if peek().type != 'end':
        raise Exception(f"Unexpected token at {peek().loc}: '{peek().text}'")

    return res