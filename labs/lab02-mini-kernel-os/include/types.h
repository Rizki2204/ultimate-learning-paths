#ifndef TYPES_H
#define TYPES_H

#include <stdint.h>
#include <stddef.h>
#include <stdbool.h>

#define PAGE_SIZE       4096U
#define PAGE_SHIFT      12U
#define TOTAL_PAGES     1024U
#define RAM_SIZE_BYTES  (TOTAL_PAGES * PAGE_SIZE) /* 4 MB */

/* Page Table Entry Flags */
#define PTE_P           0x001U  /* Present */
#define PTE_W           0x002U  /* Writable */
#define PTE_U           0x004U  /* User-mode accessible */

/* Syscall numbers */
#define SYS_EXIT        0U
#define SYS_YIELD       1U
#define SYS_WRITE       2U
#define SYS_FORK        3U
#define SYS_SLEEP       4U

#endif /* TYPES_H */
