#include <string.h>
#include <stdio.h>
#include "syscall.h"

void syscall_init(syscall_ctx_t *ctx, scheduler_t *sched, mmu_context_t *mmu) {
    if (!ctx) return;
    ctx->sched = sched;
    ctx->mmu = mmu;
    ctx->console_len = 0;
    memset(ctx->console_buffer, 0, sizeof(ctx->console_buffer));
}

int32_t syscall_dispatch(syscall_ctx_t *ctx, uint32_t sys_num, uintptr_t arg1, uintptr_t arg2, uintptr_t arg3) {
    if (!ctx || !ctx->sched) return -1;

    task_t *curr = sched_get_current(ctx->sched);
    if (!curr) return -1;

    switch (sys_num) {
        case SYS_EXIT:
            sched_exit_current(ctx->sched, (int)arg1);
            return 0;

        case SYS_YIELD:
            sched_yield(ctx->sched);
            return 0;

        case SYS_WRITE: {
            uint32_t fd = (uint32_t)arg1;
            uintptr_t va = arg2;
            uint32_t len = (uint32_t)arg3;

            if (fd != 1 && fd != 2) return -1; /* Only stdout/stderr supported */
            if (len == 0) return 0;

            /* Check memory permission: if user task with user page directory, buffer must be mapped with PTE_U */
            const char *src = NULL;
            if (curr->page_dir && ctx->mmu && curr->page_dir != ctx->mmu->kernel_pgdir) {
                uint32_t pa = 0;
                int tr = mmu_translate(ctx->mmu, curr->page_dir, (uint32_t)va, PTE_P | PTE_U, &pa);
                if (tr != 0) {
                    return -14; /* -EFAULT: Bad address / permission denied */
                }
                if (ctx->mmu->alloc && ctx->mmu->alloc->ram_base && pa < ctx->mmu->alloc->total_pages * PAGE_SIZE) {
                    src = (const char *)(ctx->mmu->alloc->ram_base + pa);
                }
            }

            /* Read buffer from translated physical memory or host buffer */
            if (!src) {
                src = (const char *)va;
            }
            for (uint32_t i = 0; i < len; i++) {
                if (ctx->console_len < sizeof(ctx->console_buffer) - 1) {
                    ctx->console_buffer[ctx->console_len++] = src[i];
                }
            }
            ctx->console_buffer[ctx->console_len] = '\0';
            return (int32_t)len;
        }

        case SYS_FORK: {
            /* Create duplicate child task */
            int child_pid = sched_create_task(ctx->sched, curr->entry, curr->arg, curr->priority, curr->page_dir);
            return child_pid;
        }

        case SYS_SLEEP: {
            /* Yield current task */
            sched_yield(ctx->sched);
            return 0;
        }

        default:
            return -38; /* -ENOSYS: Function not implemented */
    }
}
