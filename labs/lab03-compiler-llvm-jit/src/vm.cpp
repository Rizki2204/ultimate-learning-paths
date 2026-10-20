#include <cmath>
#include <iostream>
#include "vm.h"

VM::VM() : last_result_(0.0) {
    stack_.reserve(1024);
    locals_.resize(256, 0.0);
}

double VM::get_last_result() const {
    return last_result_;
}

const std::vector<double> &VM::get_stack() const {
    return stack_;
}

VMResult VM::run(const Chunk &chunk) {
    size_t ip = 0;
    stack_.clear();

    auto push = [this](double val) {
        stack_.push_back(val);
    };

    auto pop = [this]() -> double {
        if (stack_.empty()) return 0.0;
        double v = stack_.back();
        stack_.pop_back();
        return v;
    };

    while (ip < chunk.code.size()) {
        OpCode op = static_cast<OpCode>(chunk.code[ip++]);
        switch (op) {
            case OpCode::OP_CONST: {
                uint8_t c_idx = chunk.code[ip++];
                push(chunk.constants[c_idx]);
                break;
            }

            case OpCode::OP_LOAD_LOCAL: {
                uint8_t slot = chunk.code[ip++];
                push(locals_[slot]);
                break;
            }

            case OpCode::OP_STORE_LOCAL: {
                uint8_t slot = chunk.code[ip++];
                double val = pop();
                locals_[slot] = val;
                push(val); /* Keep on stack as result */
                break;
            }

            case OpCode::OP_POP: {
                pop();
                break;
            }

            case OpCode::OP_ADD: {
                double b = pop();
                double a = pop();
                push(a + b);
                break;
            }

            case OpCode::OP_SUB: {
                double b = pop();
                double a = pop();
                push(a - b);
                break;
            }

            case OpCode::OP_MUL: {
                double b = pop();
                double a = pop();
                push(a * b);
                break;
            }

            case OpCode::OP_DIV: {
                double b = pop();
                double a = pop();
                if (b == 0.0) return VMResult::RUNTIME_ERROR;
                push(a / b);
                break;
            }

            case OpCode::OP_MOD: {
                double b = pop();
                double a = pop();
                if (b == 0.0) return VMResult::RUNTIME_ERROR;
                push(std::fmod(a, b));
                break;
            }

            case OpCode::OP_CMP_EQ: {
                double b = pop();
                double a = pop();
                push(a == b ? 1.0 : 0.0);
                break;
            }

            case OpCode::OP_CMP_NE: {
                double b = pop();
                double a = pop();
                push(a != b ? 1.0 : 0.0);
                break;
            }

            case OpCode::OP_CMP_LT: {
                double b = pop();
                double a = pop();
                push(a < b ? 1.0 : 0.0);
                break;
            }

            case OpCode::OP_CMP_LE: {
                double b = pop();
                double a = pop();
                push(a <= b ? 1.0 : 0.0);
                break;
            }

            case OpCode::OP_CMP_GT: {
                double b = pop();
                double a = pop();
                push(a > b ? 1.0 : 0.0);
                break;
            }

            case OpCode::OP_CMP_GE: {
                double b = pop();
                double a = pop();
                push(a >= b ? 1.0 : 0.0);
                break;
            }

            case OpCode::OP_JUMP: {
                uint8_t low = chunk.code[ip++];
                uint8_t high = chunk.code[ip++];
                ip = low | (high << 8);
                break;
            }

            case OpCode::OP_JUMP_IF_FALSE: {
                uint8_t low = chunk.code[ip++];
                uint8_t high = chunk.code[ip++];
                size_t target = low | (high << 8);
                double cond = pop();
                if (cond == 0.0) {
                    ip = target;
                }
                break;
            }

            case OpCode::OP_HALT:
                if (!stack_.empty()) {
                    last_result_ = stack_.back();
                }
                return VMResult::OK;

            default:
                return VMResult::RUNTIME_ERROR;
        }
    }

    if (!stack_.empty()) {
        last_result_ = stack_.back();
    }
    return VMResult::OK;
}
