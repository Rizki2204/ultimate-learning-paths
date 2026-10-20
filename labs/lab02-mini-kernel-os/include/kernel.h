#ifndef KERNEL_H
#define KERNEL_H

#include "types.h"
#include "palloc.h"
#include "mmu.h"
#include "sched.h"
#include "syscall.h"

typedef struct {
    palloc_t palloc;
    mmu_context_t mmu;
    scheduler_t sched;
    syscall_ctx_t syscall;
    int is_running;
} kernel_t;

int kernel_init(kernel_t *kern);
void kernel_shutdown(kernel_t *kern);
int kernel_run_ticks(kernel_t *kern, uint32_t ticks);

#endif /* KERNEL_H */
