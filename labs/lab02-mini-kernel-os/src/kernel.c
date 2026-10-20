#include <stdlib.h>
#include <string.h>
#include "kernel.h"

int kernel_init(kernel_t *kern) {
    if (!kern) return -1;
    memset(kern, 0, sizeof(*kern));

    if (palloc_init(&kern->palloc, TOTAL_PAGES) != 0) {
        return -1;
    }

    if (mmu_init(&kern->mmu, &kern->palloc) != 0) {
        palloc_free_pool(&kern->palloc);
        return -1;
    }

    sched_init(&kern->sched);
    syscall_init(&kern->syscall, &kern->sched, &kern->mmu);
    kern->is_running = 1;
    return 0;
}

void kernel_shutdown(kernel_t *kern) {
    if (!kern) return;
    for (int i = 0; i < MAX_TASKS; i++) {
        if (kern->sched.tasks[i].stack) {
            free(kern->sched.tasks[i].stack);
            kern->sched.tasks[i].stack = NULL;
        }
    }
    palloc_free_pool(&kern->palloc);
    kern->is_running = 0;
}

int kernel_run_ticks(kernel_t *kern, uint32_t ticks) {
    if (!kern || !kern->is_running) return -1;
    for (uint32_t i = 0; i < ticks; i++) {
        if (kern->sched.active_task_count == 0) break;
        sched_tick(&kern->sched);
    }
    return (int)kern->sched.tick_count;
}
