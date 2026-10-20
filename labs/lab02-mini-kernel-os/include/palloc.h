#ifndef PALLOC_H
#define PALLOC_H

#include "types.h"

typedef struct {
    uint8_t *ram_base;
    uint32_t bitmap[TOTAL_PAGES / 32];
    size_t total_pages;
    size_t free_pages;
} palloc_t;

int palloc_init(palloc_t *alloc, size_t total_pages);
void palloc_free_pool(palloc_t *alloc);
int32_t palloc_alloc_frame(palloc_t *alloc);
int palloc_free_frame(palloc_t *alloc, uint32_t frame_idx);
void *palloc_frame_to_ptr(palloc_t *alloc, uint32_t frame_idx);
int32_t palloc_ptr_to_frame(palloc_t *alloc, const void *ptr);
size_t palloc_free_count(const palloc_t *alloc);

#endif /* PALLOC_H */
