#ifndef VM_H
#define VM_H

#include <vector>
#include <cstdint>
#include "bytecode.h"

enum class VMResult {
    OK = 0,
    COMPILE_ERROR,
    RUNTIME_ERROR
};

class VM {
public:
    VM();
    VMResult run(const Chunk &chunk);
    double get_last_result() const;
    const std::vector<double> &get_stack() const;

private:
    std::vector<double> stack_;
    std::vector<double> locals_;
    double last_result_;
};

#endif /* VM_H */
