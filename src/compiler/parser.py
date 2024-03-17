from src.models import ast
from src.models.types import Token

def parse(tokens: list[Token], right_associative=False) -> ast.Expression:

    # This keeps track of which token we're looking at.
    pos = 0

    # Let's first define two useful helper functions:
    # 'peek' and 'consume'.

    # 'peek()' returns the token at 'pos',
    # or a special 'end' token if we're past the end
    # of the token list.
    # This way we don't have to worry about going past
    # the end elsewhere.
    def peek() -> Token:
        if pos < len(tokens):
            return tokens[pos]
        else:
            return Token(
                loc=tokens[-1].loc,
                type="end",
                text="",
            )

    # 'consume(expected)' returns the token at 'pos'
    # and moves 'pos' forward.
    #
    # If the optional parameter 'expected' is given,
    # it checks that the token being consumed has that text.
    # If 'expected' is a list, then the token must have
    # one of the texts in the list.
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
        if peek().type != 'int_literal':
            raise Exception(f'{peek().loc}: expected an integer literal')
        token = consume()
        return ast.Literal(int(token.text))

    def parse_identifier() -> ast.Identifier:
        if peek().type != 'identifier':
            raise Exception(f'{peek().loc}: expected an identifier')
        token = consume()
        return ast.Identifier(name=token.text)

    # 假设这个函数已经定义好了，用于解析单个标识符或整数字面量
    def parse_primary() -> ast.Expression:
        if peek().type == 'identifier':
            return parse_identifier()
        elif peek().type == 'int_literal':
            return parse_int_literal()
        else:
            raise Exception('Unexpected token')

    def parse_expression() -> ast.Expression:
        # 先解析一个简单表达式或一个术语
        left = parse_primary()

        while peek().text in ['+', '-']:
            operator = consume().text
            right = parse_primary()  # 递归调用来处理右侧的表达式
            left = ast.BinaryOp(left=left, op=operator, right=right)

        return left

    def parse_expression_right() -> ast.Expression:
        left = parse_primary()

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
        left = parse_primary()
        while peek().text in ['+', '-']:
            operator = consume().text
            right = parse_primary()
            left = ast.BinaryOp(left=left, op=operator, right=right)
        return left

    # 右结合解析逻辑
    def parse_expression_right() -> ast.Expression:
        # 之前的 parse_expression_right() 代码
        left = parse_primary()
        if peek().text in ['+', '-']:
            operator_token = consume()
            operator = operator_token.text
            right = parse_expression()  # 注意这里递归调用 parse_expression()
            return ast.BinaryOp(left, operator, right)
        else:
            return left

    return parse_expression()