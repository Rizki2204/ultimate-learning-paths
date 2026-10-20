#include <stdlib.h>
#include <string.h>
#include "sched.h"

void sched_init(scheduler_t *sched) {
    if (!sched) return;
    memset(sched, 0, sizeof(*sched));
    sched->current_idx = -1;
    sched->tick_count = 0;
    sched->active_task_count = 0;
}

int sched_create_task(scheduler_t *sched, void (*entry)(void *), void *arg, int priority, uint32_t *pgdir) {
    if (!sched || !entry) return -1;

    int slot = -1;
    for (int i = 0; i < MAX_TASKS; i++) {
        if (sched->tasks[i].state == TASK_UNUSED || sched->tasks[i].state == TASK_TERMINATED) {
            slot = i;
            break;
        }
    }
    if (slot < 0) return -1; /* Out of task slots */

    task_t *t = &sched->tasks[slot];
    if (t->stack) {
        free(t->stack);
        t->stack = NULL;
    }

    t->pid = (uint32_t)(slot + 1);
    t->state = TASK_READY;
    t->priority = (priority <= 0) ? 1 : priority;
    t->quantum_ticks = t->priority * 2;
    t->ticks_left = t->quantum_ticks;
    t->page_dir = pgdir;
    t->entry = entry;
    t->arg = arg;
    t->exit_code = 0;

    t->stack = (uint8_t *)malloc(STACK_SIZE);
    if (!t->stack) return -1;
    t->context.sp = (uint32_t)(uintptr_t)(t->stack + STACK_SIZE);

    sched->active_task_count++;
    if (sched->current_idx < 0) {
        sched->current_idx = slot;
        t->state = TASK_RUNNING;
    }

    return (int)t->pid;
}

void sched_yield(scheduler_t *sched) {
    if (!sched || sched->active_task_count == 0) return;

    int prev_idx = sched->current_idx;
    if (prev_idx >= 0 && sched->tasks[prev_idx].state == TASK_RUNNING) {
        sched->tasks[prev_idx].state = TASK_READY;
    }

    /* Round-robin search for next ready task */
    int next_idx = -1;
    for (int step = 1; step <= MAX_TASKS; step++) {
        int candidate = (prev_idx + step) % MAX_TASKS;
        if (sched->tasks[candidate].state == TASK_READY) {
            next_idx = candidate;
            break;
        }
    }

    if (next_idx >= 0) {
        sched->current_idx = next_idx;
        sched->tasks[next_idx].state = TASK_RUNNING;
        sched->tasks[next_idx].ticks_left = sched->tasks[next_idx].quantum_ticks;
    } else if (prev_idx >= 0 && sched->tasks[prev_idx].state == TASK_READY) {
        /* No other ready task; resume previous */
        sched->tasks[prev_idx].state = TASK_RUNNING;
    }
}

void sched_tick(scheduler_t *sched) {
    if (!sched) return;
    sched->tick_count++;

    if (sched->current_idx < 0) {
        sched_yield(sched);
        return;
    }

    task_t *curr = &sched->tasks[sched->current_idx];
    if (curr->state == TASK_RUNNING) {
        curr->ticks_left--;
        if (curr->ticks_left <= 0) {
            sched_yield(sched);
        }
    } else {
        sched_yield(sched);
    }
}

void sched_exit_current(scheduler_t *sched, int exit_code) {
    if (!sched || sched->current_idx < 0) return;

    task_t *curr = &sched->tasks[sched->current_idx];
    curr->state = TASK_TERMINATED;
    curr->exit_code = exit_code;
    if (curr->stack) {
        free(curr->stack);
        curr->stack = NULL;
    }
    sched->active_task_count--;

    sched_yield(sched);
}

task_t *sched_get_current(scheduler_t *sched) {
    if (!sched || sched->current_idx < 0) return NULL;
    return &sched->tasks[sched->current_idx];
}
