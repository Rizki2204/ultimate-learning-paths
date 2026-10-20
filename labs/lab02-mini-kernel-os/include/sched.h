#ifndef SCHED_H
#define SCHED_H

#include "types.h"

#define MAX_TASKS       16
#define STACK_SIZE      4096

typedef enum {
    TASK_UNUSED = 0,
    TASK_READY,
    TASK_RUNNING,
    TASK_BLOCKED,
    TASK_TERMINATED
} task_state_t;

typedef struct {
    uint32_t sp;
    uint32_t regs[8]; /* callee-saved registers r4-r11 simulation */
} cpu_context_t;

typedef struct task {
    uint32_t pid;
    task_state_t state;
    int priority;
    int quantum_ticks;
    int ticks_left;
    uint32_t *page_dir;
    uint8_t *stack;
    cpu_context_t context;
    void (*entry)(void *);
    void *arg;
    int exit_code;
} task_t;

typedef struct {
    task_t tasks[MAX_TASKS];
    int current_idx;
    uint32_t tick_count;
    int active_task_count;
} scheduler_t;

void sched_init(scheduler_t *sched);
int sched_create_task(scheduler_t *sched, void (*entry)(void *), void *arg, int priority, uint32_t *pgdir);
void sched_yield(scheduler_t *sched);
void sched_tick(scheduler_t *sched);
void sched_exit_current(scheduler_t *sched, int exit_code);
task_t *sched_get_current(scheduler_t *sched);

#endif /* SCHED_H */
