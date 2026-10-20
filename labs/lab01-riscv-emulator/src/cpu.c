#include <stdio.h>
#include <string.h>
#include "cpu.h"

void cpu_init(cpu_t *cpu) {
    if (!cpu) return;
    memset(cpu, 0, sizeof(*cpu));
    cpu->pc = RAM_BASE;
    mmu_init(&cpu->mmu, RAM_SIZE);
}

void cpu_free(cpu_t *cpu) {
    if (cpu) {
        mmu_free(&cpu->mmu);
    }
}

void cpu_set_reg(cpu_t *cpu, int reg, uint32_t val) {
    if (!cpu || reg <= 0 || reg >= 32) return;
    cpu->x[reg] = val;
}

uint32_t cpu_get_reg(const cpu_t *cpu, int reg) {
    if (!cpu || reg <= 0 || reg >= 32) return 0;
    return cpu->x[reg];
}

void cpu_trap(cpu_t *cpu, uint32_t cause) {
    if (!cpu) return;
    cpu->csr_mcause = cause;
    cpu->csr_mepc = cpu->pc;
    if (cpu->csr_mtvec != 0) {
        cpu->pc = cpu->csr_mtvec;
    } else {
        cpu->halted = 1;
        cpu->exit_code = (int)cause;
    }
}

int cpu_step(cpu_t *cpu) {
    if (!cpu || cpu->halted) return 0;

    /* Fetch */
    uint32_t raw_inst = 0;
    int rc = mmu_read32(&cpu->mmu, cpu->pc, &raw_inst);
    if (rc == -2) {
        cpu_trap(cpu, CAUSE_MISALIGNED_FETCH);
        return 1;
    }
    if (rc != 0) {
        cpu_trap(cpu, CAUSE_FAULT_FETCH);
        return 1;
    }

    /* Decode */
    instruction_t inst;
    decode_instruction(raw_inst, &inst);

    /* Execute */
    uint32_t current_pc = cpu->pc;
    int jump_or_branch = execute_instruction(cpu, &inst);

    if (jump_or_branch == 0) {
        cpu->pc = current_pc + 4;
    }

    cpu->cycles++;
    return 1;
}

int cpu_run(cpu_t *cpu, size_t max_cycles) {
    if (!cpu) return -1;
    size_t count = 0;
    while (!cpu->halted && (max_cycles == 0 || count < max_cycles)) {
        if (!cpu_step(cpu)) break;
        count++;
    }
    return (int)count;
}
