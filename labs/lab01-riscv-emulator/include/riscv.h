#ifndef RISCV_H
#define RISCV_H

#include <stdint.h>
#include <stddef.h>
#include <stdbool.h>

#define RAM_BASE        0x80000000U
#define RAM_SIZE        0x01000000U /* 16 MB */
#define UART_BASE       0x10000000U
#define UART_SIZE       0x00001000U

/* Standard RISC-V Traps & Causes */
#define CAUSE_MISALIGNED_FETCH    0x0U
#define CAUSE_FAULT_FETCH         0x1U
#define CAUSE_ILLEGAL_INSTRUCTION 0x2U
#define CAUSE_BREAKPOINT          0x3U
#define CAUSE_MISALIGNED_LOAD     0x4U
#define CAUSE_FAULT_LOAD          0x5U
#define CAUSE_MISALIGNED_STORE    0x6U
#define CAUSE_FAULT_STORE         0x7U
#define CAUSE_USER_ECALL          0x8U
#define CAUSE_SUPERVISOR_ECALL    0x9U
#define CAUSE_MACHINE_ECALL       0xBU

/* CSR Register Addresses */
#define CSR_MSTATUS     0x300U
#define CSR_MTVEC       0x305U
#define CSR_MEPC        0x341U
#define CSR_MCAUSE      0x342U

/* Opcode definitions */
#define OP_LOAD         0x03U
#define OP_IMM          0x13U
#define OP_AUIPC        0x17U
#define OP_STORE        0x23U
#define OP_REG          0x33U
#define OP_LUI          0x37U
#define OP_BRANCH       0x63U
#define OP_JALR         0x67U
#define OP_JAL          0x6FU
#define OP_SYSTEM       0x73U

#endif /* RISCV_H */
