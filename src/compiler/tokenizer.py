import re
from typing import List
from src.models.types import Token, SourceLocation

def tokenize(source_code: str) -> List[Token]:
    source_code = source_code.replace('//','#')
    token_pattern = r'(\s+)|(\d+\.\d*|\.\d+|\d+)|(\b(True|False|true|false)\b)|([A-Za-z_][A-Za-z0-9_]*)|(\*\*|==|!=|<=|>=|&&|\|\||[\+\-*/%=<>!]{1,2})|([\(\)\{\},;])|(//.*|#.*)'
    # token_pattern = r'(\s+)|(\d+\.\d*|\.\d+|\d+)|(\b(True|False|true|false)\b)|(\b(and|or|not)\b)|([A-Za-z_][A-Za-z0-9_]*)|(\*\*|==|!=|<=|>=|&&|\|\||[\+\-*/=<>!])|([\(\)\{\},;])|(//.*|#.*)'

    tokens = []
    line = 1
    last_match_end = 0

    for match in re.finditer(token_pattern, source_code):
        text = match.group(0)

        start, end = match.start(), match.end()
        # Update line and column based on the content since the last match
        pre_text = source_code[last_match_end:start]
        line_increment = pre_text.count('\n')
        if line_increment:
            line += line_increment
            column = len(pre_text) - pre_text.rfind('\n') - 1
            last_match_end = start - column + 1
        else:
            column = len(pre_text) + 1


        if text.strip() == '' or text.startswith(("//", "#")):  # Skip whitespace or comments
            continue

        # Determine token type
        token_type = "unknown"
        if match.group(2):
            token_type = "float" if '.' in text else "integer"
        elif match.group(4):
            token_type = "bool"  # 处理布尔类型
        elif match.group(5):
            token_type = "identifier"
        elif match.group(6):
            token_type = "operator"
        elif match.group(7):
            token_type = "punctuation"


        tokens.append(Token(text=text, type=token_type, loc=SourceLocation(file="<unknown>", line=line, column=column)))

    return tokens
