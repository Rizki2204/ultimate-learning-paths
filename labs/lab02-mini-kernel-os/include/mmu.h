#ifndef MMU_H
#define MMU_H

#include "types.h"
#include "palloc.h"

#define PDE_INDEX(va)   (((va) >> 22) & 0x3FFU)
#define PTE_INDEX(va)   (((va) >> 12) & 0x3FFU)
#define PAGE_OFFSET(va) ((va) & 0xFFFU)

typedef struct {
    palloc_t *alloc;
    uint32_t *kernel_pgdir;
} mmu_context_t;

int mmu_init(mmu_context_t *ctx, palloc_t *alloc);
uint32_t *mmu_create_page_dir(mmu_context_t *ctx);
void mmu_destroy_page_dir(mmu_context_t *ctx, uint32_t *pgdir);
int mmu_map(mmu_context_t *ctx, uint32_t *pgdir, uint32_t va, uint32_t pa, uint32_t flags);
int mmu_unmap(mmu_context_t *ctx, uint32_t *pgdir, uint32_t va);
int mmu_translate(mmu_context_t *ctx, uint32_t *pgdir, uint32_t va, uint32_t req_flags, uint32_t *out_pa);

#endif /* MMU_H */
