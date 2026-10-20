#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

/*
 * RISC-V RV32I Starter Scaffolding
 *
 * Exercise Instructions:
 * Implement instruction decoding and execution for RV32I base integer instructions.
 * Follow the RISC-V Unprivileged ISA Specification (Volume I: User-Level ISA).
 */

#define RAM_BASE 0x80000000U
#define RAM_SIZE 0x00100000U /* 1MB for starter */

typedef struct {
    uint32_t x[32];
    uint32_t pc;
    uint8_t *ram;
    int halted;
} starter_cpu_t;

void starter_cpu_init(starter_cpu_t *cpu) {
    memset(cpu, 0, sizeof(*cpu));
    cpu->pc = RAM_BASE;
    cpu->ram = (uint8_t *)calloc(RAM_SIZE, 1);
}

void starter_cpu_free(starter_cpu_t *cpu) {
    if (cpu && cpu->ram) {
        free(cpu->ram);
        cpu->ram = NULL;
    }
}

/*
 * Exercise 1: Instruction Decoding
 * Extract opcode (bits 6:0), rd (bits 11:7), funct3 (bits 14:12),
 * rs1 (bits 19:15), rs2 (bits 24:20), and funct7 (bits 31:25).
 */
void starter_decode(uint32_t raw, uint8_t *opcode, uint8_t *rd, uint8_t *funct3, uint8_t *rs1, uint8_t *rs2) {
    *opcode = (uint8_t)(raw & 0x7F);
    *rd = (uint8_t)((raw >> 7) & 0x1F);
    *funct3 = (uint8_t)((raw >> 12) & 0x07);
    *rs1 = (uint8_t)((raw >> 15) & 0x1F);
    *rs2 = (uint8_t)((raw >> 20) & 0x1F);
}

/*
 * Exercise 2: Immediate Sign-Extension
 * Sign-extend I-type immediate from 12 bits to 32 bits.
 */
int32_t starter_imm_i(uint32_t raw) {
    return (int32_t)raw >> 20;
}

/*
 * Exercise 3: Single Instruction Step Execution
 * Evaluate the decoded instruction, apply register state transition,
 * enforce x0 invariant (x0 always 0), and update program counter.
 */
int starter_cpu_step(starter_cpu_t *cpu) {
    if (!cpu || cpu->halted) return 0;
    uint32_t offset = cpu->pc - RAM_BASE;
    if (offset + 4 > RAM_SIZE) {
        cpu->halted = 1;
        return 0;
    }
    uint32_t raw = *(uint32_t *)(cpu->ram + offset);
    uint8_t opcode, rd, funct3, rs1, rs2;
    starter_decode(raw, &opcode, &rd, &funct3, &rs1, &rs2);

    /* Baseline support: OP_IMM (0x13) ADDI */
    if (opcode == 0x13 && funct3 == 0) {
        int32_t imm = starter_imm_i(raw);
        cpu->x[rd] = cpu->x[rs1] + (uint32_t)imm;
        cpu->x[0] = 0;
        cpu->pc += 4;
        return 1;
    }

    cpu->halted = 1;
    return 0;
}

int main(void) {
    starter_cpu_t cpu;
    starter_cpu_init(&cpu);
    printf("Starter RISC-V initialized at PC=0x%08X\n", cpu.pc);
    starter_cpu_free(&cpu);
    return 0;
}
