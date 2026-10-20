#ifndef BYTECODE_H
#define BYTECODE_H

#include <vector>
#include <string>
#include <cstdint>
#include <map>
#include "ast.h"

enum class OpCode : uint8_t {
    OP_CONST = 0,
    OP_LOAD_LOCAL,
    OP_STORE_LOCAL,
    OP_POP,
    OP_ADD,
    OP_SUB,
    OP_MUL,
    OP_DIV,
    OP_MOD,
    OP_CMP_EQ,
    OP_CMP_NE,
    OP_CMP_LT,
    OP_CMP_LE,
    OP_CMP_GT,
    OP_CMP_GE,
    OP_JUMP,
    OP_JUMP_IF_FALSE,
    OP_CALL,
    OP_RETURN,
    OP_HALT
};

struct Chunk {
    std::vector<uint8_t> code;
    std::vector<double> constants;
    std::vector<int> lines;

    size_t add_constant(double val);
    void write_byte(uint8_t byte, int line = 0);
    void write_opcode(OpCode op, int line = 0);
};

class BytecodeCompiler {
public:
    BytecodeCompiler();
    bool compile(const ProgramAST &program, Chunk &chunk);
    bool compile_expression(const ExprAST &expr, Chunk &chunk);

private:
    void compile_stmt(const StmtAST &stmt, Chunk &chunk);
    void compile_expr(const ExprAST &expr, Chunk &chunk);
    int resolve_local(const std::string &name);
    int add_local(const std::string &name);

    std::map<std::string, int> locals_;
    int next_local_slot_;
};

#endif /* BYTECODE_H */
