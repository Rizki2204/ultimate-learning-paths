#ifndef MMU_H
#define MMU_H

#include "riscv.h"

typedef struct {
    uint8_t *ram;
    size_t ram_size;
    uint32_t ram_base;
    char uart_out[4096];
    size_t uart_len;
} mmu_t;

int mmu_init(mmu_t *mmu, size_t size);
void mmu_free(mmu_t *mmu);
int mmu_read8(mmu_t *mmu, uint32_t addr, uint8_t *val);
int mmu_read16(mmu_t *mmu, uint32_t addr, uint16_t *val);
int mmu_read32(mmu_t *mmu, uint32_t addr, uint32_t *val);
int mmu_write8(mmu_t *mmu, uint32_t addr, uint8_t val);
int mmu_write16(mmu_t *mmu, uint32_t addr, uint16_t val);
int mmu_write32(mmu_t *mmu, uint32_t addr, uint32_t val);
int mmu_load_binary(mmu_t *mmu, uint32_t addr, const uint8_t *data, size_t len);

#endif /* MMU_H */
