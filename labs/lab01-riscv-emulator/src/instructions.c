#include <stdio.h>
#include "instructions.h"
#include "cpu.h"

void decode_instruction(uint32_t raw, instruction_t *inst) {
    if (!inst) return;
    inst->raw = raw;
    inst->opcode = (uint8_t)(raw & 0x7FU);
    inst->rd     = (uint8_t)((raw >> 7) & 0x1FU);
    inst->funct3 = (uint8_t)((raw >> 12) & 0x07U);
    inst->rs1    = (uint8_t)((raw >> 15) & 0x1FU);
    inst->rs2    = (uint8_t)((raw >> 20) & 0x1FU);
    inst->funct7 = (uint8_t)((raw >> 25) & 0x7FU);

    /* Immediate extraction with sign extension */
    inst->imm_i = (int32_t)raw >> 20;

    inst->imm_s = ((int32_t)(raw & 0xFE000000U) >> 20) |
                  (int32_t)((raw >> 7) & 0x1FU);

    int32_t b12 = (int32_t)(raw & 0x80000000U) >> 19;
    uint32_t b11 = (raw & 0x00000080U) << 4;
    uint32_t b10_5 = (raw & 0x7E000000U) >> 20;
    uint32_t b4_1 = (raw & 0x00000F00U) >> 7;
    inst->imm_b = b12 | (int32_t)(b11 | b10_5 | b4_1);

    inst->imm_u = (int32_t)(raw & 0xFFFFF000U);

    int32_t j20 = (int32_t)(raw & 0x80000000U) >> 11;
    uint32_t j19_12 = raw & 0x000FF000U;
    uint32_t j11 = (raw & 0x00100000U) >> 9;
    uint32_t j10_1 = (raw & 0x7FE00000U) >> 20;
    inst->imm_j = j20 | (int32_t)(j19_12 | j11 | j10_1);

    inst->csr = (uint16_t)(raw >> 20);
}

static uint32_t *get_csr_ptr(cpu_t *cpu, uint16_t csr) {
    switch (csr) {
        case CSR_MSTATUS: return &cpu->csr_mstatus;
        case CSR_MTVEC:   return &cpu->csr_mtvec;
        case CSR_MEPC:    return &cpu->csr_mepc;
        case CSR_MCAUSE:  return &cpu->csr_mcause;
        default: return NULL;
    }
}

int execute_instruction(cpu_t *cpu, const instruction_t *inst) {
    if (!cpu || !inst) return -1;

    switch (inst->opcode) {
        case OP_LUI:
            cpu->x[inst->rd] = (uint32_t)inst->imm_u;
            break;

        case OP_AUIPC:
            cpu->x[inst->rd] = cpu->pc + (uint32_t)inst->imm_u;
            break;

        case OP_JAL:
            cpu->x[inst->rd] = cpu->pc + 4;
            cpu->pc = cpu->pc + (uint32_t)inst->imm_j;
            cpu->x[0] = 0;
            return 1;

        case OP_JALR: {
            uint32_t target = (cpu->x[inst->rs1] + (uint32_t)inst->imm_i) & ~1U;
            cpu->x[inst->rd] = cpu->pc + 4;
            cpu->pc = target;
            cpu->x[0] = 0;
            return 1;
        }

        case OP_BRANCH: {
            bool take = false;
            switch (inst->funct3) {
                case 0x0: take = (cpu->x[inst->rs1] == cpu->x[inst->rs2]); break; /* BEQ */
                case 0x1: take = (cpu->x[inst->rs1] != cpu->x[inst->rs2]); break; /* BNE */
                case 0x4: take = ((int32_t)cpu->x[inst->rs1] < (int32_t)cpu->x[inst->rs2]); break; /* BLT */
                case 0x5: take = ((int32_t)cpu->x[inst->rs1] >= (int32_t)cpu->x[inst->rs2]); break; /* BGE */
                case 0x6: take = (cpu->x[inst->rs1] < cpu->x[inst->rs2]); break; /* BLTU */
                case 0x7: take = (cpu->x[inst->rs1] >= cpu->x[inst->rs2]); break; /* BGEU */
                default:
                    cpu_trap(cpu, CAUSE_ILLEGAL_INSTRUCTION);
                    return 1;
            }
            if (take) {
                cpu->pc = cpu->pc + (uint32_t)inst->imm_b;
                cpu->x[0] = 0;
                return 1;
            }
            break;
        }

        case OP_LOAD: {
            uint32_t addr = cpu->x[inst->rs1] + (uint32_t)inst->imm_i;
            switch (inst->funct3) {
                case 0x0: { /* LB */
                    uint8_t val = 0;
                    if (mmu_read8(&cpu->mmu, addr, &val) != 0) {
                        cpu_trap(cpu, CAUSE_FAULT_LOAD);
                        return 1;
                    }
                    cpu->x[inst->rd] = (uint32_t)(int32_t)(int8_t)val;
                    break;
                }
                case 0x1: { /* LH */
                    uint16_t val = 0;
                    int rc = mmu_read16(&cpu->mmu, addr, &val);
                    if (rc == -2) { cpu_trap(cpu, CAUSE_MISALIGNED_LOAD); return 1; }
                    if (rc != 0) { cpu_trap(cpu, CAUSE_FAULT_LOAD); return 1; }
                    cpu->x[inst->rd] = (uint32_t)(int32_t)(int16_t)val;
                    break;
                }
                case 0x2: { /* LW */
                    uint32_t val = 0;
                    int rc = mmu_read32(&cpu->mmu, addr, &val);
                    if (rc == -2) { cpu_trap(cpu, CAUSE_MISALIGNED_LOAD); return 1; }
                    if (rc != 0) { cpu_trap(cpu, CAUSE_FAULT_LOAD); return 1; }
                    cpu->x[inst->rd] = val;
                    break;
                }
                case 0x4: { /* LBU */
                    uint8_t val = 0;
                    if (mmu_read8(&cpu->mmu, addr, &val) != 0) {
                        cpu_trap(cpu, CAUSE_FAULT_LOAD);
                        return 1;
                    }
                    cpu->x[inst->rd] = (uint32_t)val;
                    break;
                }
                case 0x5: { /* LHU */
                    uint16_t val = 0;
                    int rc = mmu_read16(&cpu->mmu, addr, &val);
                    if (rc == -2) { cpu_trap(cpu, CAUSE_MISALIGNED_LOAD); return 1; }
                    if (rc != 0) { cpu_trap(cpu, CAUSE_FAULT_LOAD); return 1; }
                    cpu->x[inst->rd] = (uint32_t)val;
                    break;
                }
                default:
                    cpu_trap(cpu, CAUSE_ILLEGAL_INSTRUCTION);
                    return 1;
            }
            break;
        }

        case OP_STORE: {
            uint32_t addr = cpu->x[inst->rs1] + (uint32_t)inst->imm_s;
            switch (inst->funct3) {
                case 0x0: /* SB */
                    if (mmu_write8(&cpu->mmu, addr, (uint8_t)cpu->x[inst->rs2]) != 0) {
                        cpu_trap(cpu, CAUSE_FAULT_STORE);
                        return 1;
                    }
                    break;
                case 0x1: { /* SH */
                    int rc = mmu_write16(&cpu->mmu, addr, (uint16_t)cpu->x[inst->rs2]);
                    if (rc == -2) { cpu_trap(cpu, CAUSE_MISALIGNED_STORE); return 1; }
                    if (rc != 0) { cpu_trap(cpu, CAUSE_FAULT_STORE); return 1; }
                    break;
                }
                case 0x2: { /* SW */
                    int rc = mmu_write32(&cpu->mmu, addr, cpu->x[inst->rs2]);
                    if (rc == -2) { cpu_trap(cpu, CAUSE_MISALIGNED_STORE); return 1; }
                    if (rc != 0) { cpu_trap(cpu, CAUSE_FAULT_STORE); return 1; }
                    break;
                }
                default:
                    cpu_trap(cpu, CAUSE_ILLEGAL_INSTRUCTION);
                    return 1;
            }
            break;
        }

        case OP_IMM: {
            uint32_t rs1_val = cpu->x[inst->rs1];
            switch (inst->funct3) {
                case 0x0: cpu->x[inst->rd] = rs1_val + (uint32_t)inst->imm_i; break; /* ADDI */
                case 0x2: cpu->x[inst->rd] = ((int32_t)rs1_val < inst->imm_i) ? 1 : 0; break; /* SLTI */
                case 0x3: cpu->x[inst->rd] = (rs1_val < (uint32_t)inst->imm_i) ? 1 : 0; break; /* SLTIU */
                case 0x4: cpu->x[inst->rd] = rs1_val ^ (uint32_t)inst->imm_i; break; /* XORI */
                case 0x6: cpu->x[inst->rd] = rs1_val | (uint32_t)inst->imm_i; break; /* ORI */
                case 0x7: cpu->x[inst->rd] = rs1_val & (uint32_t)inst->imm_i; break; /* ANDI */
                case 0x1: cpu->x[inst->rd] = rs1_val << (inst->imm_i & 0x1F); break; /* SLLI */
                case 0x5:
                    if (inst->funct7 == 0x20) {
                        /* SRAI */
                        cpu->x[inst->rd] = (uint32_t)((int32_t)rs1_val >> (inst->imm_i & 0x1F));
                    } else {
                        /* SRLI */
                        cpu->x[inst->rd] = rs1_val >> (inst->imm_i & 0x1F);
                    }
                    break;
                default:
                    cpu_trap(cpu, CAUSE_ILLEGAL_INSTRUCTION);
                    return 1;
            }
            break;
        }

        case OP_REG: {
            uint32_t rs1_val = cpu->x[inst->rs1];
            uint32_t rs2_val = cpu->x[inst->rs2];
            switch (inst->funct3) {
                case 0x0:
                    if (inst->funct7 == 0x20) {
                        cpu->x[inst->rd] = rs1_val - rs2_val; /* SUB */
                    } else {
                        cpu->x[inst->rd] = rs1_val + rs2_val; /* ADD */
                    }
                    break;
                case 0x1: cpu->x[inst->rd] = rs1_val << (rs2_val & 0x1FU); break; /* SLL */
                case 0x2: cpu->x[inst->rd] = ((int32_t)rs1_val < (int32_t)rs2_val) ? 1 : 0; break; /* SLT */
                case 0x3: cpu->x[inst->rd] = (rs1_val < rs2_val) ? 1 : 0; break; /* SLTU */
                case 0x4: cpu->x[inst->rd] = rs1_val ^ rs2_val; break; /* XOR */
                case 0x5:
                    if (inst->funct7 == 0x20) {
                        cpu->x[inst->rd] = (uint32_t)((int32_t)rs1_val >> (rs2_val & 0x1FU)); /* SRA */
                    } else {
                        cpu->x[inst->rd] = rs1_val >> (rs2_val & 0x1FU); /* SRL */
                    }
                    break;
                case 0x6: cpu->x[inst->rd] = rs1_val | rs2_val; break; /* OR */
                case 0x7: cpu->x[inst->rd] = rs1_val & rs2_val; break; /* AND */
                default:
                    cpu_trap(cpu, CAUSE_ILLEGAL_INSTRUCTION);
                    return 1;
            }
            break;
        }

        case OP_SYSTEM: {
            if (inst->funct3 == 0x0) {
                if (inst->raw == 0x00000073U) {
                    /* ECALL */
                    cpu_trap(cpu, CAUSE_MACHINE_ECALL);
                    return 1;
                } else if (inst->raw == 0x00100073U) {
                    /* EBREAK */
                    cpu_trap(cpu, CAUSE_BREAKPOINT);
                    return 1;
                } else if (inst->raw == 0x30200073U) {
                    /* MRET */
                    cpu->pc = cpu->csr_mepc;
                    cpu->x[0] = 0;
                    return 1;
                } else {
                    cpu_trap(cpu, CAUSE_ILLEGAL_INSTRUCTION);
                    return 1;
                }
            } else {
                /* CSR operations */
                uint32_t *csr_ptr = get_csr_ptr(cpu, inst->csr);
                if (!csr_ptr) {
                    cpu_trap(cpu, CAUSE_ILLEGAL_INSTRUCTION);
                    return 1;
                }
                uint32_t old_val = *csr_ptr;
                uint32_t rs1_val = cpu->x[inst->rs1];

                switch (inst->funct3) {
                    case 0x1: /* CSRRW */
                        *csr_ptr = rs1_val;
                        cpu->x[inst->rd] = old_val;
                        break;
                    case 0x2: /* CSRRS */
                        *csr_ptr = old_val | rs1_val;
                        cpu->x[inst->rd] = old_val;
                        break;
                    case 0x3: /* CSRRC */
                        *csr_ptr = old_val & ~rs1_val;
                        cpu->x[inst->rd] = old_val;
                        break;
                    default:
                        cpu_trap(cpu, CAUSE_ILLEGAL_INSTRUCTION);
                        return 1;
                }
            }
            break;
        }

        default:
            cpu_trap(cpu, CAUSE_ILLEGAL_INSTRUCTION);
            return 1;
    }

    cpu->x[0] = 0;
    return 0; /* Default PC increment */
}
