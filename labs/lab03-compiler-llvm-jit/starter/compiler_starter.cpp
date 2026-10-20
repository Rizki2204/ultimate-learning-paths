#include <iostream>
#include <string>
#include <vector>
#include <memory>

/*
 * Compiler & Bytecode VM Starter Scaffolding
 *
 * Exercise Instructions:
 * Implement recursive-descent tokenization, expression parsing,
 * and stack-based bytecode evaluation.
 */

enum class StarterOp {
    OP_CONST,
    OP_ADD,
    OP_HALT
};

struct StarterVM {
    std::vector<double> stack;

    void push(double v) { stack.push_back(v); }
    double pop() {
        if (stack.empty()) return 0.0;
        double v = stack.back();
        stack.pop_back();
        return v;
    }

    /*
     * Exercise: Execute Bytecode Instruction Loop
     * Handle OP_CONST, OP_ADD, and OP_HALT.
     */
    double execute(const std::vector<StarterOp> &ops, const std::vector<double> &constants) {
        size_t const_idx = 0;
        for (StarterOp op : ops) {
            if (op == StarterOp::OP_CONST) {
                push(constants[const_idx++]);
            } else if (op == StarterOp::OP_ADD) {
                double b = pop();
                double a = pop();
                push(a + b);
            } else if (op == StarterOp::OP_HALT) {
                break;
            }
        }
        return stack.empty() ? 0.0 : stack.back();
    }
};

int main() {
    StarterVM vm;
    std::vector<StarterOp> program = {
        StarterOp::OP_CONST,
        StarterOp::OP_CONST,
        StarterOp::OP_ADD,
        StarterOp::OP_HALT
    };
    std::vector<double> constants = { 10.0, 32.0 };
    double result = vm.execute(program, constants);
    std::cout << "Starter VM Result: " << result << std::endl;
    return 0;
}
