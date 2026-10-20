#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include "mmu.h"

int mmu_init(mmu_t *mmu, size_t size) {
    if (!mmu) return -1;
    mmu->ram_size = (size == 0) ? RAM_SIZE : size;
    mmu->ram_base = RAM_BASE;
    mmu->ram = (uint8_t *)calloc(mmu->ram_size, 1);
    if (!mmu->ram) return -1;
    mmu->uart_len = 0;
    memset(mmu->uart_out, 0, sizeof(mmu->uart_out));
    return 0;
}

void mmu_free(mmu_t *mmu) {
    if (mmu && mmu->ram) {
        free(mmu->ram);
        mmu->ram = NULL;
        mmu->ram_size = 0;
    }
}

int mmu_read8(mmu_t *mmu, uint32_t addr, uint8_t *val) {
    if (!mmu || !val) return -1;
    if (addr >= mmu->ram_base && addr < mmu->ram_base + mmu->ram_size) {
        *val = mmu->ram[addr - mmu->ram_base];
        return 0;
    }
    if (addr >= UART_BASE && addr < UART_BASE + UART_SIZE) {
        *val = 0; /* Receiver empty */
        return 0;
    }
    return -1; /* Access fault */
}

int mmu_read16(mmu_t *mmu, uint32_t addr, uint16_t *val) {
    if (!mmu || !val) return -1;
    if (addr & 1U) return -2; /* Misaligned */
    if (addr >= mmu->ram_base && addr + 1 < mmu->ram_base + mmu->ram_size) {
        uint32_t offset = addr - mmu->ram_base;
        *val = (uint16_t)mmu->ram[offset] | ((uint16_t)mmu->ram[offset + 1] << 8);
        return 0;
    }
    return -1;
}

int mmu_read32(mmu_t *mmu, uint32_t addr, uint32_t *val) {
    if (!mmu || !val) return -1;
    if (addr & 3U) return -2; /* Misaligned */
    if (addr >= mmu->ram_base && addr + 3 < mmu->ram_base + mmu->ram_size) {
        uint32_t offset = addr - mmu->ram_base;
        *val = (uint32_t)mmu->ram[offset] |
               ((uint32_t)mmu->ram[offset + 1] << 8) |
               ((uint32_t)mmu->ram[offset + 2] << 16) |
               ((uint32_t)mmu->ram[offset + 3] << 24);
        return 0;
    }
    return -1;
}

int mmu_write8(mmu_t *mmu, uint32_t addr, uint8_t val) {
    if (!mmu) return -1;
    if (addr >= mmu->ram_base && addr < mmu->ram_base + mmu->ram_size) {
        mmu->ram[addr - mmu->ram_base] = val;
        return 0;
    }
    if (addr == UART_BASE) {
        if (mmu->uart_len < sizeof(mmu->uart_out) - 1) {
            mmu->uart_out[mmu->uart_len++] = (char)val;
            mmu->uart_out[mmu->uart_len] = '\0';
        }
        return 0;
    }
    return -1;
}

int mmu_write16(mmu_t *mmu, uint32_t addr, uint16_t val) {
    if (!mmu) return -1;
    if (addr & 1U) return -2; /* Misaligned */
    if (addr >= mmu->ram_base && addr + 1 < mmu->ram_base + mmu->ram_size) {
        uint32_t offset = addr - mmu->ram_base;
        mmu->ram[offset] = (uint8_t)(val & 0xFF);
        mmu->ram[offset + 1] = (uint8_t)((val >> 8) & 0xFF);
        return 0;
    }
    return -1;
}

int mmu_write32(mmu_t *mmu, uint32_t addr, uint32_t val) {
    if (!mmu) return -1;
    if (addr & 3U) return -2; /* Misaligned */
    if (addr >= mmu->ram_base && addr + 3 < mmu->ram_base + mmu->ram_size) {
        uint32_t offset = addr - mmu->ram_base;
        mmu->ram[offset]     = (uint8_t)(val & 0xFF);
        mmu->ram[offset + 1] = (uint8_t)((val >> 8) & 0xFF);
        mmu->ram[offset + 2] = (uint8_t)((val >> 16) & 0xFF);
        mmu->ram[offset + 3] = (uint8_t)((val >> 24) & 0xFF);
        return 0;
    }
    return -1;
}

int mmu_load_binary(mmu_t *mmu, uint32_t addr, const uint8_t *data, size_t len) {
    if (!mmu || !data) return -1;
    if (addr < mmu->ram_base || addr + len > mmu->ram_base + mmu->ram_size) {
        return -1;
    }
    memcpy(mmu->ram + (addr - mmu->ram_base), data, len);
    return 0;
}
