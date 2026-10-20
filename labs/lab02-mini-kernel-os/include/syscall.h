#ifndef SYSCALL_H
#define SYSCALL_H

#include "types.h"
#include "sched.h"
#include "mmu.h"

typedef struct {
    scheduler_t *sched;
    mmu_context_t *mmu;
    char console_buffer[4096];
    size_t console_len;
} syscall_ctx_t;

void syscall_init(syscall_ctx_t *ctx, scheduler_t *sched, mmu_context_t *mmu);
int32_t syscall_dispatch(syscall_ctx_t *ctx, uint32_t sys_num, uintptr_t arg1, uintptr_t arg2, uintptr_t arg3);

#endif /* SYSCALL_H */
