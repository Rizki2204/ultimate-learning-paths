#include <stdexcept>
#include "bytecode.h"

size_t Chunk::add_constant(double val) {
    constants.push_back(val);
    return constants.size() - 1;
}

void Chunk::write_byte(uint8_t byte, int line) {
    code.push_back(byte);
    lines.push_back(line);
}

void Chunk::write_opcode(OpCode op, int line) {
    write_byte(static_cast<uint8_t>(op), line);
}

BytecodeCompiler::BytecodeCompiler() : next_local_slot_(0) {}

int BytecodeCompiler::resolve_local(const std::string &name) {
    auto it = locals_.find(name);
    if (it != locals_.end()) {
        return it->second;
    }
    throw std::runtime_error("Compiler Error: Undefined variable '" + name + "'");
}

int BytecodeCompiler::add_local(const std::string &name) {
    int slot = next_local_slot_++;
    locals_[name] = slot;
    return slot;
}

void BytecodeCompiler::compile_expr(const ExprAST &expr, Chunk &chunk) {
    if (auto num = dynamic_cast<const NumberExprAST *>(&expr)) {
        size_t c_idx = chunk.add_constant(num->value);
        chunk.write_opcode(OpCode::OP_CONST);
        chunk.write_byte(static_cast<uint8_t>(c_idx));
        return;
    }

    if (auto var = dynamic_cast<const VariableExprAST *>(&expr)) {
        int slot = resolve_local(var->name);
        chunk.write_opcode(OpCode::OP_LOAD_LOCAL);
        chunk.write_byte(static_cast<uint8_t>(slot));
        return;
    }

    if (auto bin = dynamic_cast<const BinaryExprAST *>(&expr)) {
        compile_expr(*bin->lhs, chunk);
        compile_expr(*bin->rhs, chunk);

        if (bin->op == "+") chunk.write_opcode(OpCode::OP_ADD);
        else if (bin->op == "-") chunk.write_opcode(OpCode::OP_SUB);
        else if (bin->op == "*") chunk.write_opcode(OpCode::OP_MUL);
        else if (bin->op == "/") chunk.write_opcode(OpCode::OP_DIV);
        else if (bin->op == "%") chunk.write_opcode(OpCode::OP_MOD);
        else if (bin->op == "==") chunk.write_opcode(OpCode::OP_CMP_EQ);
        else if (bin->op == "!=") chunk.write_opcode(OpCode::OP_CMP_NE);
        else if (bin->op == "<") chunk.write_opcode(OpCode::OP_CMP_LT);
        else if (bin->op == "<=") chunk.write_opcode(OpCode::OP_CMP_LE);
        else if (bin->op == ">") chunk.write_opcode(OpCode::OP_CMP_GT);
        else if (bin->op == ">=") chunk.write_opcode(OpCode::OP_CMP_GE);
        else throw std::runtime_error("Compiler Error: Unknown binary operator " + bin->op);
        return;
    }

    throw std::runtime_error("Compiler Error: Unsupported expression node");
}

void BytecodeCompiler::compile_stmt(const StmtAST &stmt, Chunk &chunk) {
    if (auto decl = dynamic_cast<const VarDeclStmtAST *>(&stmt)) {
        compile_expr(*decl->init, chunk);
        int slot = add_local(decl->name);
        chunk.write_opcode(OpCode::OP_STORE_LOCAL);
        chunk.write_byte(static_cast<uint8_t>(slot));
        return;
    }

    if (auto assign = dynamic_cast<const AssignStmtAST *>(&stmt)) {
        compile_expr(*assign->val, chunk);
        int slot = resolve_local(assign->name);
        chunk.write_opcode(OpCode::OP_STORE_LOCAL);
        chunk.write_byte(static_cast<uint8_t>(slot));
        return;
    }

    if (auto expr_st = dynamic_cast<const ExprStmtAST *>(&stmt)) {
        compile_expr(*expr_st->expr, chunk);
        /* Keep result on stack as expression result */
        return;
    }

    if (auto if_st = dynamic_cast<const IfStmtAST *>(&stmt)) {
        compile_expr(*if_st->cond, chunk);
        chunk.write_opcode(OpCode::OP_JUMP_IF_FALSE);
        size_t jump_false_idx = chunk.code.size();
        chunk.write_byte(0); /* placeholder offset low */
        chunk.write_byte(0); /* placeholder offset high */

        compile_stmt(*if_st->then_branch, chunk);

        chunk.write_opcode(OpCode::OP_JUMP);
        size_t jump_end_idx = chunk.code.size();
        chunk.write_byte(0);
        chunk.write_byte(0);

        /* Patch jump_false_idx */
        size_t else_target = chunk.code.size();
        chunk.code[jump_false_idx] = static_cast<uint8_t>(else_target & 0xFF);
        chunk.code[jump_false_idx + 1] = static_cast<uint8_t>((else_target >> 8) & 0xFF);

        if (if_st->else_branch) {
            compile_stmt(*if_st->else_branch, chunk);
        }

        /* Patch jump_end_idx */
        size_t end_target = chunk.code.size();
        chunk.code[jump_end_idx] = static_cast<uint8_t>(end_target & 0xFF);
        chunk.code[jump_end_idx + 1] = static_cast<uint8_t>((end_target >> 8) & 0xFF);
        return;
    }

    if (auto while_st = dynamic_cast<const WhileStmtAST *>(&stmt)) {
        size_t loop_start = chunk.code.size();
        compile_expr(*while_st->cond, chunk);

        chunk.write_opcode(OpCode::OP_JUMP_IF_FALSE);
        size_t jump_exit_idx = chunk.code.size();
        chunk.write_byte(0);
        chunk.write_byte(0);

        compile_stmt(*while_st->body, chunk);

        chunk.write_opcode(OpCode::OP_JUMP);
        chunk.write_byte(static_cast<uint8_t>(loop_start & 0xFF));
        chunk.write_byte(static_cast<uint8_t>((loop_start >> 8) & 0xFF));

        size_t exit_target = chunk.code.size();
        chunk.code[jump_exit_idx] = static_cast<uint8_t>(exit_target & 0xFF);
        chunk.code[jump_exit_idx + 1] = static_cast<uint8_t>((exit_target >> 8) & 0xFF);
        return;
    }

    if (auto block_st = dynamic_cast<const BlockStmtAST *>(&stmt)) {
        for (const auto &s : block_st->statements) {
            compile_stmt(*s, chunk);
        }
        return;
    }

    if (auto ret_st = dynamic_cast<const ReturnStmtAST *>(&stmt)) {
        if (ret_st->expr) {
            compile_expr(*ret_st->expr, chunk);
        } else {
            size_t c = chunk.add_constant(0.0);
            chunk.write_opcode(OpCode::OP_CONST);
            chunk.write_byte(static_cast<uint8_t>(c));
        }
        chunk.write_opcode(OpCode::OP_RETURN);
        return;
    }
}

bool BytecodeCompiler::compile(const ProgramAST &program, Chunk &chunk) {
    for (const auto &stmt : program.top_level_stmts) {
        compile_stmt(*stmt, chunk);
    }
    chunk.write_opcode(OpCode::OP_HALT);
    return true;
}

bool BytecodeCompiler::compile_expression(const ExprAST &expr, Chunk &chunk) {
    compile_expr(expr, chunk);
    chunk.write_opcode(OpCode::OP_HALT);
    return true;
}
