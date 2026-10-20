# Laboratory 02: Preemptive Multi-Tasking Mini-Kernel OS

## 1. Architectural Overview
This laboratory implements a preemptive multitasking operating system kernel in ANSI C (C99/C11). The kernel simulates fundamental OS subsystems: a physical page frame bitmap allocator, a hardware-accurate two-level paging Memory Management Unit (MMU), Task Control Block (TCB) management, round-robin time-slice scheduling, and a privilege-enforced system call boundary.

```
+-----------------------------------------------------------------------+
|                              User Space                               |
|   +-----------------------+               +-----------------------+   |
|   | Task 1 (PID 1)        |               | Task 2 (PID 2)        |   |
|   | User Virtual Memory   |               | User Virtual Memory   |   |
|   +-----------------------+               +-----------------------+   |
|               |                                       |               |
|               +-------------------+-------------------+               |
|                                   v                                   |
|                        System Call Boundary (TRAP)                    |
|                        SYS_EXIT, SYS_YIELD, SYS_WRITE                 |
+-----------------------------------|-----------------------------------+
                                    |
+-----------------------------------|-----------------------------------+
|                              Kernel Space                             |
|                                   v                                   |
|   +---------------------------------------------------------------+   |
|   | Syscall Dispatcher & Memory Protection Enforcement (PTE_U)    |   |
|   +---------------------------------------------------------------+   |
|               |                                   |                   |
|               v                                   v                   |
|   +-----------------------+           +-----------------------+       |
|   | Round-Robin Scheduler |           | Two-Level Paging MMU  |       |
|   | TCB Queue & Time Slices<--------->| Page Dir -> Page Table|       |
|   +-----------------------+           +-----------------------+       |
|                                                   |                   |
|                                                   v                   |
|                                       +-----------------------+       |
|                                       | Page Frame Allocator  |       |
|                                       | 1024 Physical Pages   |       |
|                                       +-----------------------+       |
+-----------------------------------------------------------------------+
```

## 2. Memory Model & Paging MMU
The simulated physical memory spans 4 Megabytes divided into 1024 frames of 4096 bytes each.

### Virtual Address Translation (Two-Level Paging)
A 32-bit virtual address (`va`) is structured as:
```
+-------------------+-------------------+--------------------+
|  PDE Index (10b)  |  PTE Index (10b)  | Page Offset (12b)  |
|    Bits 31..22    |    Bits 21..12    |     Bits 11..0     |
+-------------------+-------------------+--------------------+
```
- **Page Directory Entry (PDE)**: Points to a physical page table frame.
- **Page Table Entry (PTE)**: Points to the target physical page frame.
- **Permission Flags**:
  - `PTE_P (0x001)`: Present in physical memory.
  - `PTE_W (0x002)`: Writable. Accessing with write flags on a read-only page triggers `-3`.
  - `PTE_U (0x004)`: User-mode accessible. Accessing kernel memory without `PTE_U` triggers `-2`.

## 3. Process Management & Scheduling
- **Task Control Block (TCB)**: Maintains task metadata (`pid`, `state`, `priority`, `quantum_ticks`, `ticks_left`, `sp`, `page_dir`, `stack`).
- **Round-Robin Scheduling**: Each clock interrupt (`sched_tick`) decrements `ticks_left`. When a task depletes its time quantum, the scheduler selects the next `TASK_READY` task from the circular queue.
- **Context Switch**: Callee-saved register frames are preserved on the task stack during cooperative yields or preemptive tick switches.

## 4. System Call Boundary
The kernel exposes a strict privilege boundary:
- `SYS_EXIT (0)`: Terminates current task and yields CPU.
- `SYS_YIELD (1)`: Voluntarily yields CPU quantum to the next ready task.
- `SYS_WRITE (2)`: Validates user virtual buffer access against task page directory (`PTE_U` flag). Returns `-EFAULT (-14)` if user attempts to reference kernel memory.
- `SYS_FORK (3)`: Clones current task into a new execution thread.
- `SYS_SLEEP (4)`: Suspends current task for timed interval.

## 5. Scaffolding & Directory Structure
```
labs/lab02-mini-kernel-os/
├── README.md               # Architecture documentation
├── Makefile                # Root build and test automation
├── run_tests.py            # Standalone test runner
├── include/                # Kernel headers
│   ├── types.h             # Page constants and PTE flags
│   ├── palloc.h            # Physical page frame allocator API
│   ├── mmu.h               # Two-level paging MMU definitions
│   ├── sched.h             # TCB and Round-robin scheduler API
│   ├── syscall.h           # Syscall dispatcher and privilege check
│   └── kernel.h            # Mini-kernel orchestration
├── starter/                # Student starter scaffolding
│   ├── Makefile            # Starter build
│   └── kernel_starter.c    # Page allocator starter skeleton
├── src/                    # Complete production reference implementation
│   ├── palloc.c            # Frame allocation and bitmap management
│   ├── mmu.c               # Page directory and translation logic
│   ├── sched.c             # Preemptive round-robin scheduler
│   ├── syscall.c           # System call dispatcher with protection
│   ├── kernel.c            # Kernel initialization and tick engine
│   └── main.c              # Test harness and simulation CLI
└── tests/                  # Automated test suite
    ├── test_palloc.py      # Bitmap allocation and exhaustion tests
    ├── test_mmu.py         # MMU translation and fault tests
    ├── test_sched.py       # Multi-task scheduling order tests
    └── test_syscalls.py    # Syscall protection and execution tests
```

## 6. Milestone Progression Guide
1. **Milestone 1 (Page Frame Allocator)**:
   Implement bitmap search to find contiguous free pages, handle exhaustion, and detect double-free anomalies.
2. **Milestone 2 (Two-Level MMU & Translation)**:
   Implement PDE/PTE lookup, recursive page directory mapping, and virtual-to-physical address resolution with privilege checking.
3. **Milestone 3 (Task Management & Scheduling)**:
   Build the Task Control Block lifecycle (`TASK_READY`, `TASK_RUNNING`, `TASK_TERMINATED`) and implement round-robin quantum expiration.
4. **Milestone 4 (Privilege Isolation & Syscalls)**:
   Implement the syscall interface and verify that unprivileged user code cannot write to kernel space.

## 7. Verification and Execution
Run the automated test runner:
```bash
python run_tests.py
```
Or use the Makefile:
```bash
mingw32-make test
```
All 4 kernel subsystem test suites execute in less than 50 milliseconds and exit with code 0.
