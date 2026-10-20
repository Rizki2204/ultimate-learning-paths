#ifndef CPU_H
#define CPU_H

#include "riscv.h"
#include "mmu.h"
#include "instructions.h"

typedef struct cpu_state {
    uint32_t x[32];
    uint32_t pc;
    uint32_t csr_mstatus;
    uint32_t csr_mtvec;
    uint32_t csr_mepc;
    uint32_t csr_mcause;
    mmu_t mmu;
    int halted;
    int exit_code;
    uint64_t cycles;
} cpu_t;

void cpu_init(cpu_t *cpu);
void cpu_free(cpu_t *cpu);
void cpu_set_reg(cpu_t *cpu, int reg, uint32_t val);
uint32_t cpu_get_reg(const cpu_t *cpu, int reg);
void cpu_trap(cpu_t *cpu, uint32_t cause);
int cpu_step(cpu_t *cpu);
int cpu_run(cpu_t *cpu, size_t max_cycles);

#endif /* CPU_H */
