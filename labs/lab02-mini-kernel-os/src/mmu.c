#include <stdlib.h>
#include <string.h>
#include "mmu.h"

int mmu_init(mmu_context_t *ctx, palloc_t *alloc) {
    if (!ctx || !alloc) return -1;
    ctx->alloc = alloc;

    int32_t frame = palloc_alloc_frame(alloc);
    if (frame < 0) return -1;

    ctx->kernel_pgdir = (uint32_t *)palloc_frame_to_ptr(alloc, (uint32_t)frame);
    memset(ctx->kernel_pgdir, 0, PAGE_SIZE);

    /* Identity map first 1MB for kernel (256 pages) */
    for (uint32_t addr = 0; addr < 0x00100000U; addr += PAGE_SIZE) {
        mmu_map(ctx, ctx->kernel_pgdir, addr, addr, PTE_P | PTE_W);
    }

    return 0;
}

uint32_t *mmu_create_page_dir(mmu_context_t *ctx) {
    if (!ctx || !ctx->alloc) return NULL;
    int32_t frame = palloc_alloc_frame(ctx->alloc);
    if (frame < 0) return NULL;

    uint32_t *pgdir = (uint32_t *)palloc_frame_to_ptr(ctx->alloc, (uint32_t)frame);
    memset(pgdir, 0, PAGE_SIZE);

    /* Share kernel page mappings */
    for (size_t i = 0; i < 1024; i++) {
        if (ctx->kernel_pgdir[i] & PTE_P) {
            pgdir[i] = ctx->kernel_pgdir[i];
        }
    }
    return pgdir;
}

void mmu_destroy_page_dir(mmu_context_t *ctx, uint32_t *pgdir) {
    if (!ctx || !ctx->alloc || !pgdir) return;

    /* Free page tables created exclusively for this page directory (user mappings) */
    for (size_t i = 0; i < 1024; i++) {
        if ((pgdir[i] & PTE_P) && pgdir[i] != ctx->kernel_pgdir[i]) {
            uint32_t pt_frame = pgdir[i] >> PAGE_SHIFT;
            palloc_free_frame(ctx->alloc, pt_frame);
        }
    }

    int32_t dir_frame = palloc_ptr_to_frame(ctx->alloc, pgdir);
    if (dir_frame >= 0) {
        palloc_free_frame(ctx->alloc, (uint32_t)dir_frame);
    }
}

int mmu_map(mmu_context_t *ctx, uint32_t *pgdir, uint32_t va, uint32_t pa, uint32_t flags) {
    if (!ctx || !ctx->alloc || !pgdir) return -1;

    uint32_t pde_idx = PDE_INDEX(va);
    uint32_t pte_idx = PTE_INDEX(va);

    if (!(pgdir[pde_idx] & PTE_P)) {
        /* Allocate new page table */
        int32_t pt_frame = palloc_alloc_frame(ctx->alloc);
        if (pt_frame < 0) return -1;
        uint32_t *new_pt = (uint32_t *)palloc_frame_to_ptr(ctx->alloc, (uint32_t)pt_frame);
        memset(new_pt, 0, PAGE_SIZE);

        pgdir[pde_idx] = ((uint32_t)pt_frame << PAGE_SHIFT) | PTE_P | PTE_W | (flags & PTE_U);
    } else {
        /* If mapping user page, ensure directory also has user bit set */
        if (flags & PTE_U) {
            pgdir[pde_idx] |= PTE_U;
        }
    }

    uint32_t pt_frame = pgdir[pde_idx] >> PAGE_SHIFT;
    uint32_t *pt = (uint32_t *)palloc_frame_to_ptr(ctx->alloc, pt_frame);
    pt[pte_idx] = (pa & ~0xFFFU) | (flags & 0xFFFU) | PTE_P;

    return 0;
}

int mmu_unmap(mmu_context_t *ctx, uint32_t *pgdir, uint32_t va) {
    if (!ctx || !ctx->alloc || !pgdir) return -1;

    uint32_t pde_idx = PDE_INDEX(va);
    uint32_t pte_idx = PTE_INDEX(va);

    if (!(pgdir[pde_idx] & PTE_P)) return -1;

    uint32_t pt_frame = pgdir[pde_idx] >> PAGE_SHIFT;
    uint32_t *pt = (uint32_t *)palloc_frame_to_ptr(ctx->alloc, pt_frame);
    pt[pte_idx] = 0;
    return 0;
}

int mmu_translate(mmu_context_t *ctx, uint32_t *pgdir, uint32_t va, uint32_t req_flags, uint32_t *out_pa) {
    if (!ctx || !ctx->alloc || !pgdir || !out_pa) return -1;

    uint32_t pde_idx = PDE_INDEX(va);
    uint32_t pte_idx = PTE_INDEX(va);
    uint32_t offset  = PAGE_OFFSET(va);

    uint32_t pde = pgdir[pde_idx];
    if (!(pde & PTE_P)) {
        return -1; /* Page fault: page directory entry not present */
    }

    if ((req_flags & PTE_U) && !(pde & PTE_U)) {
        return -2; /* Page fault: user privilege violation at directory */
    }

    uint32_t pt_frame = pde >> PAGE_SHIFT;
    uint32_t *pt = (uint32_t *)palloc_frame_to_ptr(ctx->alloc, pt_frame);
    if (!pt) return -1;

    uint32_t pte = pt[pte_idx];
    if (!(pte & PTE_P)) {
        return -1; /* Page fault: page table entry not present */
    }

    if ((req_flags & PTE_U) && !(pte & PTE_U)) {
        return -2; /* Page fault: user privilege violation at table */
    }

    if ((req_flags & PTE_W) && !(pte & PTE_W)) {
        return -3; /* Page fault: write to read-only page */
    }

    *out_pa = (pte & ~0xFFFU) | offset;
    return 0;
}
