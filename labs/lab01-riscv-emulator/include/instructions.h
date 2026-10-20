#ifndef INSTRUCTIONS_H
#define INSTRUCTIONS_H

#include "riscv.h"

struct cpu_state;

typedef struct {
    uint32_t raw;
    uint8_t opcode;
    uint8_t rd;
    uint8_t funct3;
    uint8_t rs1;
    uint8_t rs2;
    uint8_t funct7;
    int32_t imm_i;
    int32_t imm_s;
    int32_t imm_b;
    int32_t imm_u;
    int32_t imm_j;
    uint16_t csr;
} instruction_t;

void decode_instruction(uint32_t raw, instruction_t *inst);
int execute_instruction(struct cpu_state *cpu, const instruction_t *inst);

#endif /* INSTRUCTIONS_H */
