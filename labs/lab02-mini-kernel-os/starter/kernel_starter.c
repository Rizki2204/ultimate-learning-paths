#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

/*
 * Mini-Kernel OS Starter Scaffolding
 *
 * Exercise Instructions:
 * Implement page frame allocation, virtual-to-physical address translation,
 * and cooperative task yielding following OS kernel fundamentals.
 */

#define PAGE_SIZE       4096U
#define TOTAL_PAGES     1024U

typedef struct {
    uint8_t *ram;
    uint32_t bitmap[TOTAL_PAGES / 32];
    size_t free_pages;
} starter_palloc_t;

void starter_palloc_init(starter_palloc_t *alloc) {
    alloc->ram = (uint8_t *)calloc(TOTAL_PAGES, PAGE_SIZE);
    memset(alloc->bitmap, 0, sizeof(alloc->bitmap));
    alloc->free_pages = TOTAL_PAGES;
}

void starter_palloc_free(starter_palloc_t *alloc) {
    if (alloc && alloc->ram) {
        free(alloc->ram);
        alloc->ram = NULL;
    }
}

/*
 * Exercise 1: Frame Allocation
 * Find the first unset bit in the allocation bitmap, mark it, decrement
 * free_pages, and return the allocated frame index. Return -1 if exhausted.
 */
int32_t starter_alloc_frame(starter_palloc_t *alloc) {
    if (!alloc || alloc->free_pages == 0) return -1;
    for (size_t i = 0; i < TOTAL_PAGES; i++) {
        size_t w = i / 32;
        size_t b = i % 32;
        if (!(alloc->bitmap[w] & (1U << b))) {
            alloc->bitmap[w] |= (1U << b);
            alloc->free_pages--;
            return (int32_t)i;
        }
    }
    return -1;
}

/*
 * Exercise 2: Frame Deallocation
 * Verify that the frame was allocated, clear the bit, increment free_pages.
 */
int starter_free_frame(starter_palloc_t *alloc, uint32_t frame_idx) {
    if (!alloc || frame_idx >= TOTAL_PAGES) return -1;
    size_t w = frame_idx / 32;
    size_t b = frame_idx % 32;
    if (!(alloc->bitmap[w] & (1U << b))) return -2; /* Not allocated */
    alloc->bitmap[w] &= ~(1U << b);
    alloc->free_pages++;
    return 0;
}

int main(void) {
    starter_palloc_t alloc;
    starter_palloc_init(&alloc);
    int32_t frame = starter_alloc_frame(&alloc);
    printf("Starter kernel allocated physical frame %d (remaining free: %zu)\n", frame, alloc.free_pages);
    starter_free_frame(&alloc, (uint32_t)frame);
    starter_palloc_free(&alloc);
    return 0;
}
