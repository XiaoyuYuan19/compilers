from src.models import ast
from src.models.ast import IfExpr, FunctionCall
from src.models.types import Token


def parse(tokens: list[Token], right_associative=False) -> ast.Expression:

    # This keeps track of which token we're looking at.

    pos = 0

    def peek() -> Token:
        if pos < len(tokens):
            return tokens[pos]
        else:
            return Token(loc=tokens[-1].loc, type="end", text="")

    def consume(expected: str | list[str] | None = None) -> Token:
        nonlocal pos
        token = peek()
        if isinstance(expected, str) and token.text != expected:
            raise Exception(f'{token.loc}: expected "{expected}"')
        if isinstance(expected, list) and token.text not in expected:
            comma_separated = ", ".join([f'"{e}"' for e in expected])
            raise Exception(f'{token.loc}: expected one of: {comma_separated}')
        pos += 1
        return token


    # This is the parsing function for integer literals.
    # It checks that we're looking at an integer literal token,
    # moves past it, and returns a 'Literal' AST node
    # containing the integer from the token.
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


    def parse_factor() -> ast.Expression:
        if peek().text == '(':
            return parse_parenthesized()
        elif peek().text == 'if':
            return parse_if_expr()
        elif peek().type == 'identifier':
            identifier = consume().text
            if peek().text == '(':
                return parse_function_call(identifier)
            else:
                return ast.Identifier(name=identifier)
        elif peek().type == 'integer':
            return parse_int_literal()
        else:
            raise Exception(f'{peek().loc}: expected "(", an integer literal or an identifier')

    def parse_function_call(name: str) -> ast.Expression:
        consume('(')  # Consume the '(' starting the argument list
        arguments = []
        if peek().text != ')':
            while True:
                arguments.append(parse_expression())
                if peek().text == ')':
                    break
                consume(',')  # Consume ',' between arguments
        consume(')')  # Consume the ')' ending the argument list
        return FunctionCall(name, arguments)

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

    def parse_expression() -> ast.Expression:
        # 先解析一个简单表达式或一个术语
        left = parse_term()

        while peek().text in ['+', '-']:
            operator = consume().text
            right = parse_term()  # 递归调用来处理右侧的表达式
            left = ast.BinaryOp(left=left, op=operator, right=right)

        return left

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
            return parse_expression_left()

    # 左结合解析逻辑
    def parse_expression_left() -> ast.Expression:
        # 之前的 parse_expression() 代码
        left = parse_term()
        while peek().text in ['+', '-']:
            operator = consume().text
            right = parse_term()
            left = ast.BinaryOp(left=left, op=operator, right=right)
        return left

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