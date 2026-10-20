#include <stdlib.h>
#include <string.h>
#include "palloc.h"

int palloc_init(palloc_t *alloc, size_t total_pages) {
    if (!alloc) return -1;
    alloc->total_pages = (total_pages == 0) ? TOTAL_PAGES : total_pages;
    alloc->free_pages = alloc->total_pages;
    alloc->ram_base = (uint8_t *)calloc(alloc->total_pages, PAGE_SIZE);
    if (!alloc->ram_base) return -1;

    memset(alloc->bitmap, 0, sizeof(alloc->bitmap));
    return 0;
}

void palloc_free_pool(palloc_t *alloc) {
    if (alloc && alloc->ram_base) {
        free(alloc->ram_base);
        alloc->ram_base = NULL;
        alloc->total_pages = 0;
        alloc->free_pages = 0;
    }
}

int32_t palloc_alloc_frame(palloc_t *alloc) {
    if (!alloc || alloc->free_pages == 0) return -1;

    for (size_t i = 0; i < alloc->total_pages; i++) {
        size_t word_idx = i / 32;
        size_t bit_idx = i % 32;
        if (!(alloc->bitmap[word_idx] & (1U << bit_idx))) {
            /* Found free page */
            alloc->bitmap[word_idx] |= (1U << bit_idx);
            alloc->free_pages--;
            /* Zero page memory */
            memset(alloc->ram_base + (i * PAGE_SIZE), 0, PAGE_SIZE);
            return (int32_t)i;
        }
    }
    return -1;
}

int palloc_free_frame(palloc_t *alloc, uint32_t frame_idx) {
    if (!alloc || frame_idx >= alloc->total_pages) return -1;

    size_t word_idx = frame_idx / 32;
    size_t bit_idx = frame_idx % 32;

    if (!(alloc->bitmap[word_idx] & (1U << bit_idx))) {
        return -2; /* Double free error */
    }

    alloc->bitmap[word_idx] &= ~(1U << bit_idx);
    alloc->free_pages++;
    return 0;
}

void *palloc_frame_to_ptr(palloc_t *alloc, uint32_t frame_idx) {
    if (!alloc || !alloc->ram_base || frame_idx >= alloc->total_pages) return NULL;
    return alloc->ram_base + (frame_idx * PAGE_SIZE);
}

int32_t palloc_ptr_to_frame(palloc_t *alloc, const void *ptr) {
    if (!alloc || !alloc->ram_base || !ptr) return -1;
    const uint8_t *p = (const uint8_t *)ptr;
    if (p < alloc->ram_base || p >= alloc->ram_base + (alloc->total_pages * PAGE_SIZE)) {
        return -1;
    }
    return (int32_t)((p - alloc->ram_base) / PAGE_SIZE);
}

size_t palloc_free_count(const palloc_t *alloc) {
    return alloc ? alloc->free_pages : 0;
}
