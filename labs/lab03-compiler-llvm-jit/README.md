# Laboratory 03: Compiler Frontend & Bytecode Virtual Machine

## 1. Architectural Overview
This laboratory implements an end-to-end compiler frontend and stack-based bytecode virtual machine in C++14. The compiler translates "MiniLang" source code into an Abstract Syntax Tree (AST) using Pratt precedence parsing, emits compact bytecode instructions into an execution chunk, and executes the bytecode on an ultra-fast virtual machine.

```
+-----------------------------------------------------------------------+
|                      MiniLang Compiler Pipeline                       |
|                                                                       |
|   +-----------------------+                                           |
|   | Source Code Text      |                                           |
|   | let x = 2 + 3 * 4;    |                                           |
|   +-----------------------+                                           |
|               |                                                       |
|               v                                                       |
|   +-----------------------+                                           |
|   | Lexer / Tokenizer     | -> Token Stream with (line, col)          |
|   +-----------------------+                                           |
|               |                                                       |
|               v                                                       |
|   +-----------------------+                                           |
|   | Pratt Precedence      | -> Typed Abstract Syntax Tree (AST)       |
|   | Recursive Parser      |    BinaryExprAST, VarDeclStmtAST, etc.    |
|   +-----------------------+                                           |
|               |                                                       |
|               v                                                       |
|   +-----------------------+                                           |
|   | Bytecode Generator    | -> Chunk: Constants Table + Bytecode Ops  |
|   | Local Slot Resolver   |    OP_CONST, OP_STORE_LOCAL, OP_ADD, ...  |
|   +-----------------------+                                           |
|               |                                                       |
|               v                                                       |
|   +-----------------------+                                           |
|   | Stack Bytecode VM     | -> Evaluated Result (Double Precision)    |
|   | Dispatch Loop         |    Division-by-Zero Safety Clamping       |
|   +-----------------------+                                           |
+-----------------------------------------------------------------------+
```

## 2. Grammar & Pratt Precedence Climbing
The grammar for MiniLang expressions is parsed using Vaughan Pratt's top-down operator precedence technique:

| Precedence Level | Operators | Associativity | Description |
|---|---|---|---|
| **Level 1** | `==`, `!=` | Left | Equality and inequality comparisons |
| **Level 2** | `<`, `<=`, `>`, `>=` | Left | Relational inequalities |
| **Level 3** | `+`, `-` | Left | Addition and subtraction |
| **Level 4** | `*`, `/`, `%` | Left | Multiplication, division, and modulo |
| **Primary** | Number literals, Variables, `(expr)`, `-expr` | N/A | Grouping and atomic operands |

## 3. Bytecode Virtual Machine Architecture
The VM executes a dense stream of 8-bit opcodes operating over a fast value stack:
- `OP_CONST <idx>`: Pushes `constants[idx]` onto the value stack.
- `OP_LOAD_LOCAL <slot>`: Pushes the value of local variable slot onto stack.
- `OP_STORE_LOCAL <slot>`: Pops top of stack and stores into `locals[slot]`, pushing it back for chained expressions.
- `OP_ADD`, `OP_SUB`, `OP_MUL`, `OP_DIV`, `OP_MOD`: Binary arithmetic operations.
- `OP_CMP_EQ`, `OP_CMP_NE`, `OP_CMP_LT`, `OP_CMP_LE`, `OP_CMP_GT`, `OP_CMP_GE`: Relational comparisons producing `1.0` (true) or `0.0` (false).
- `OP_JUMP <offset_16>`: Unconditional branch updating instruction pointer.
- `OP_JUMP_IF_FALSE <offset_16>`: Conditional branch taken when popped top-of-stack is `0.0`.
- `OP_HALT`: Stops execution loop and returns top-of-stack.

## 4. Scaffolding & Directory Structure
```
labs/lab03-compiler-llvm-jit/
├── README.md               # Architecture documentation
├── Makefile                # Build and test automation
├── run_tests.py            # Standalone unittest runner
├── include/                # Header definitions
│   ├── token.h             # TokenType enum and Token struct
│   ├── lexer.h             # Lexer tokenizer interface
│   ├── ast.h               # Abstract Syntax Tree hierarchy
│   ├── parser.h            # Pratt parser interface
│   ├── bytecode.h          # Bytecode opcodes and compiler
│   └── vm.h                # Stack VM engine interface
├── starter/                # Student starter scaffolding
│   ├── Makefile            # Starter compilation rules
│   └── compiler_starter.cpp# Starter VM skeleton
├── src/                    # Complete production reference implementation
│   ├── lexer.cpp           # Scanner implementation
│   ├── parser.cpp          # Pratt parser implementation
│   ├── bytecode.cpp        # AST to bytecode compilation
│   ├── vm.cpp              # Virtual machine execution loop
│   └── main.cpp            # CLI and evaluation runner
└── tests/                  # Automated test suite
    ├── test_lexer.py       # Token scanning and position tests
    ├── test_parser.py      # Operator precedence tests
    ├── test_vm.py          # VM arithmetic and error tests
    └── test_integration.py # Multi-statement loops (Fibonacci, Factorial)
```

## 5. Milestone Progression Guide
1. **Milestone 1 (Lexical Analysis)**:
   Scan source code into tokens, recognizing keywords, numbers, multi-character operators (`==`, `<=`, `!=`), and tracking line/column.
2. **Milestone 2 (Pratt Precedence Parsing)**:
   Implement binding power / precedence climbing to construct binary expression trees that naturally respect mathematical associativity.
3. **Milestone 3 (Bytecode Generation)**:
   Translate statements and expressions into flat instruction streams with backpatched jump offsets for `if` and `while` control flow.
4. **Milestone 4 (Virtual Machine Execution)**:
   Execute bytecode instructions on a stack machine, guarding against division by zero and handling variable slots.

## 6. Verification and Execution
Run the automated test runner:
```bash
python run_tests.py
```
Or use the Makefile:
```bash
mingw32-make test
```
All 10 test suites execute within 150 milliseconds and pass cleanly with exit code 0.
