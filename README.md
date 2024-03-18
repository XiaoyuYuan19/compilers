
## Setup

Requirements:

- [Pyenv](https://github.com/pyenv/pyenv) for installing Python 3.11+
    - Recommended installation method: the "automatic installer"
      i.e. `curl https://pyenv.run | bash`
- [Poetry](https://python-poetry.org/) for installing dependencies
    - Recommended installation method: the "official installer"
      i.e. `curl -sSL https://install.python-poetry.org | python3 -`

Install dependencies:

    # Install Python specified in `.python-version`
    pyenv install
    # Install dependencies specified in `pyproject.toml`
    poetry install

If `pyenv install` gives an error about `_tkinter`, you can ignore it.
If you see other errors, you may have to investigate.

If you have trouble with Poetry not picking up pyenv's python installation,
try `poetry env remove --all` and then `poetry install` again.

Typecheck and run tests:

    ./check.sh
    # or individually:
    poetry run mypy .
    poetry run pytest -vv

Run the compiler on a source code file:

    ./compiler.sh COMMAND path/to/source/code

where `COMMAND` may be one of these:

    interpret
    TODO(student): add more

## IDE setup

Recommended VSCode extensions:

- Python
- Pylance
- autopep8

## Code overview

### `types.py`. 
- Defines base types, such as `SourceLocation` and `Token`, which provide support structures for lexical and syntactic analysis.
- `SourceLocation` is used to track the location of elements in the source code (filename, line number, column number).
- `Token` represents the individual units into which the source code is broken down, including text, type, and location.

### `ast.py` 
- Defines the node classes of an Abstract Syntax Tree (AST), such as `Expression`, `Literal`, `Identifier`, `BinaryOp`, and so on, to provide a structured programmatic representation for syntactic analysis and interpreted execution.

### `tokenizer.py` 
- Implements a lexical analyzer that breaks down source code strings into `Token` lists.
- Uses regular expressions to match different types of tokens, such as identifiers, operators, literals, and so on.

### `parser.py` 
- Implements a syntax parser that converts `Token` lists into ASTs.
- Contains logic for recursive descent parsing, supporting parsing of language constructs such as expressions, control flow structures, function calls, etc.
- Supports operator precedence and associativity handling.

### `SymTab.py` 
- Implements a symbol table for keeping track of the scopes of variable and function definitions.
- Supports entering and leaving scopes, defining and finding variables.
- Extended to support updating variables and defining built-in symbols.

### `interpreter.py` 
- Implements interpreter logic to execute programs based on ASTs.
- Uses symbol tables to handle variable scoping and assignment.
- Supports basic expression computation, conditional logic, scope blocks, etc.

### Test file (`*_test.py`)
- Contains unit tests for different components (e.g., lexical analyzer, syntax analyzer, interpreter).
- The tests cover basic functionality such as arithmetic operations, conditional logic, and scope rules.
- Use the `unittest` framework to ensure that each component works as expected.

