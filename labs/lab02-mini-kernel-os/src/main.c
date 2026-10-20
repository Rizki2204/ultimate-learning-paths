#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "kernel.h"

static int test_palloc(void) {
    palloc_t alloc;
    if (palloc_init(&alloc, 64) != 0) return 1;
    if (palloc_free_count(&alloc) != 64) return 2;

    int32_t f0 = palloc_alloc_frame(&alloc);
    int32_t f1 = palloc_alloc_frame(&alloc);
    if (f0 != 0 || f1 != 1) return 3;
    if (palloc_free_count(&alloc) != 62) return 4;

    if (palloc_free_frame(&alloc, (uint32_t)f0) != 0) return 5;
    if (palloc_free_count(&alloc) != 63) return 6;

    /* Double free check */
    if (palloc_free_frame(&alloc, (uint32_t)f0) != -2) return 7;

    palloc_free_pool(&alloc);
    return 0;
}

static int test_mmu(void) {
    palloc_t alloc;
    palloc_init(&alloc, 128);
    mmu_context_t ctx;
    mmu_init(&ctx, &alloc);

    uint32_t *user_dir = mmu_create_page_dir(&ctx);
    if (!user_dir) return 1;

    /* Map virtual 0x40000000 to physical frame 10 with PTE_P | PTE_W | PTE_U */
    uint32_t va = 0x40000000U;
    uint32_t pa = 10 * PAGE_SIZE;
    if (mmu_map(&ctx, user_dir, va, pa, PTE_P | PTE_W | PTE_U) != 0) return 2;

    uint32_t translated = 0;
    if (mmu_translate(&ctx, user_dir, va + 0x120, PTE_P | PTE_U, &translated) != 0) return 3;
    if (translated != pa + 0x120) return 4;

    /* User access violation test on kernel page */
    uint32_t k_va = 0x00010000U; /* kernel mapped without PTE_U */
    if (mmu_translate(&ctx, user_dir, k_va, PTE_P | PTE_U, &translated) != -2) return 5;

    mmu_destroy_page_dir(&ctx, user_dir);
    palloc_free_pool(&alloc);
    return 0;
}

static void dummy_worker(void *arg) {
    (void)arg;
}

static int test_sched(void) {
    scheduler_t sched;
    sched_init(&sched);

    int t1 = sched_create_task(&sched, dummy_worker, NULL, 1, NULL);
    int t2 = sched_create_task(&sched, dummy_worker, NULL, 1, NULL);
    if (t1 != 1 || t2 != 2) return 1;
    if (sched.active_task_count != 2) return 2;

    task_t *curr = sched_get_current(&sched);
    if (!curr || curr->pid != 1) return 3;

    /* Tick until quantum expires and context switches */
    sched_tick(&sched);
    sched_tick(&sched);
    curr = sched_get_current(&sched);
    if (!curr || curr->pid != 2) return 4;

    sched_exit_current(&sched, 0);
    if (sched.active_task_count != 1) return 5;

    return 0;
}

static int test_syscall(void) {
    kernel_t kern;
    if (kernel_init(&kern) != 0) return 1;

    int pid = sched_create_task(&kern.sched, dummy_worker, NULL, 1, kern.mmu.kernel_pgdir);
    if (pid <= 0) return 2;

    /* Test SYS_WRITE with kernel privilege string */
    const char *msg = "OS_INIT_OK\n";
    int32_t written = syscall_dispatch(&kern.syscall, SYS_WRITE, 1, (uintptr_t)msg, (uint32_t)strlen(msg));
    if (written != (int32_t)strlen(msg)) return 3;
    if (strstr(kern.syscall.console_buffer, "OS_INIT_OK") == NULL) return 4;

    /* Test SYS_YIELD */
    if (syscall_dispatch(&kern.syscall, SYS_YIELD, 0, 0, 0) != 0) return 5;

    /* Test SYS_EXIT */
    if (syscall_dispatch(&kern.syscall, SYS_EXIT, 42, 0, 0) != 0) return 6;
    if (kern.sched.active_task_count != 0) return 7;

    kernel_shutdown(&kern);
    return 0;
}

int main(int argc, char **argv) {
    if (argc < 2) {
        printf("Usage: %s [--test-palloc | --test-mmu | --test-sched | --test-syscall | --test-all]\n", argv[0]);
        return 0;
    }

    if (strcmp(argv[1], "--test-palloc") == 0) {
        int r = test_palloc();
        printf("palloc_test: %s\n", r == 0 ? "PASS" : "FAIL");
        return r;
    }
    if (strcmp(argv[1], "--test-mmu") == 0) {
        int r = test_mmu();
        printf("mmu_test: %s\n", r == 0 ? "PASS" : "FAIL");
        return r;
    }
    if (strcmp(argv[1], "--test-sched") == 0) {
        int r = test_sched();
        printf("sched_test: %s\n", r == 0 ? "PASS" : "FAIL");
        return r;
    }
    if (strcmp(argv[1], "--test-syscall") == 0) {
        int r = test_syscall();
        printf("syscall_test: %s\n", r == 0 ? "PASS" : "FAIL");
        return r;
    }
    if (strcmp(argv[1], "--test-all") == 0) {
        int p = test_palloc();
        int m = test_mmu();
        int s = test_sched();
        int y = test_syscall();
        int total_err = p + m + s + y;
        printf("{\"palloc\": %d, \"mmu\": %d, \"sched\": %d, \"syscall\": %d}\n", p, m, s, y);
        return total_err == 0 ? 0 : 1;
    }

    return 1;
}
