"""
scripts/challenger_stress_test.py
Adversarial Stress Test Suite & Empirical Verification Harness
Author: Challenger 1 (Empirical Challenger)
Repository: ultimate-learning-paths
"""

import os
import sys
import math
import json
import time
import struct
import random
import re
import subprocess
import urllib.parse
from typing import Dict, List, Tuple, Any

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

class StressTestRunner:
    def __init__(self):
        self.results: List[Dict[str, Any]] = []
        self.passed = 0
        self.failed = 0

    def record(self, lab_id: str, test_name: str, passed: bool, details: str, duration: float):
        status = "PASS" if passed else "FAIL"
        self.results.append({
            "lab": lab_id,
            "test": test_name,
            "status": status,
            "details": details,
            "duration": duration,
        })
        if passed:
            self.passed += 1
            print(f"  [PASS] [{lab_id}] {test_name} ({duration:.4f}s): {details}")
        else:
            self.failed += 1
            print(f"  [FAIL] [{lab_id}] {test_name} ({duration:.4f}s): {details}")

    # =========================================================================
    # LAB 01: RISC-V 32-bit Emulator Stress
    # =========================================================================
    def stress_lab01_riscv(self):
        print("\n--- [LAB 01] RISC-V Emulator Adversarial Stress Tests ---")
        lab01_dir = os.path.join(BASE_DIR, "labs", "lab01-riscv-emulator")
        if lab01_dir not in sys.path:
            sys.path.insert(0, lab01_dir)

        from tests.riscv_helpers import (
            r_type, i_type, s_type, b_type, u_type, j_type, run_hex_code, ensure_compiled
        )
        ensure_compiled()

        # 1.1 x0 Immutability under all instruction families
        t0 = time.time()
        # ADDI x0, x0, 999; LUI x0, 0x12345; JAL x0, 8; SLLI x0, x0, 5
        prog = (
            i_type(0x13, 0, 0x0, 0, 999) +
            u_type(0x37, 0, 0x12345000) +
            j_type(0x6F, 0, 8) +
            i_type(0x13, 0, 0x1, 0, 5)
        )
        res = run_hex_code(prog, max_cycles=10)
        x0_val = res["regs"][0]
        dt = time.time() - t0
        self.record(
            "Lab01", "x0_immutability_adversarial",
            x0_val == 0,
            f"x0 value after aggressive writes is {x0_val}",
            dt
        )

        # 1.2 Arithmetic Corner Cases: Two's Complement Overflow, SRA vs SRL, SLT
        t0 = time.time()
        # In RV32I, to load 0x7FFFFFFF: lui x1, 0x80000000; addi x1, x1, -1
        # x2 = 1
        # x3 = x1 + x2 -> 0x80000000 (overflow to min negative)
        # x4 = SRAI x3, 4 -> 0xF8000000 (arithmetic sign extension)
        # x5 = SRLI x3, 4 -> 0x08000000 (logical zero fill)
        # x6 = SLT x3, x2 -> 1 (0x80000000 is negative < 1)
        # x7 = SLTU x3, x2 -> 0 (0x80000000 is 2147483648 > 1 unsigned)
        # x8 = SLLI x2, 36 -> should mask 36 to 4 -> x8 = 1 << 4 = 16
        prog = (
            u_type(0x37, 1, 0x80000000) +
            i_type(0x13, 1, 0x0, 1, -1) +        # x1 = 0x7FFFFFFF
            i_type(0x13, 2, 0x0, 0, 1) +         # x2 = 1
            r_type(0x33, 3, 0x0, 1, 2, 0x00) +   # x3 = x1 + x2
            r_type(0x13, 4, 0x5, 3, 0x4, 0x20) + # x4 = SRAI x3, 4
            r_type(0x13, 5, 0x5, 3, 0x4, 0x00) + # x5 = SRLI x3, 4
            r_type(0x33, 6, 0x2, 3, 2, 0x00) +   # x6 = SLT x3, x2
            r_type(0x33, 7, 0x3, 3, 2, 0x00) +   # x7 = SLTU x3, x2
            r_type(0x13, 8, 0x1, 2, 36, 0x00)    # x8 = SLLI x2, 36 -> 1 << 4 = 16
        )
        res = run_hex_code(prog, max_cycles=20)
        dt = time.time() - t0
        regs = res["regs"]
        c1 = (regs[3] == 0x80000000)
        c2 = (regs[4] == 0xF8000000)
        c3 = (regs[5] == 0x08000000)
        c4 = (regs[6] == 1)
        c5 = (regs[7] == 0)
        c6 = (regs[8] == 16)
        all_ok = c1 and c2 and c3 and c4 and c5 and c6
        self.record(
            "Lab01", "arithmetic_corner_cases_and_shifts",
            all_ok,
            f"overflow=0x{regs[3]:08X}, sra=0x{regs[4]:08X}, srl=0x{regs[5]:08X}, slt={regs[6]}, sltu={regs[7]}, sll36={regs[8]}",
            dt
        )

        # 1.3 Misaligned Memory Access & Fault Traps
        t0 = time.time()
        # x1 = RAM_BASE (0x80000000)
        # sw x1, 1(x1) -> misaligned store trap (CAUSE_MISALIGNED_STORE = 0x6)
        prog = (
            u_type(0x37, 1, 0x80000000) +
            s_type(0x23, 0x2, 1, 1, 1) # sw x1, 1(x1)
        )
        res = run_hex_code(prog, max_cycles=10)
        dt = time.time() - t0
        halted = res["halted"] == 1
        self.record(
            "Lab01", "misaligned_store_trap_protection",
            halted,
            f"halted on misaligned store: {halted}, PC: {res['pc']}",
            dt
        )

        # 1.4 High-Cycle Computation Loop (Sum of 1..500 = 125250)
        t0 = time.time()
        prog = (
            i_type(0x13, 1, 0x0, 0, 500) +      # addi x1, x0, 500
            i_type(0x13, 2, 0x0, 0, 0) +        # addi x2, x0, 0
            b_type(0x63, 0x0, 1, 0, 16) +       # beq x1, x0, +16
            r_type(0x33, 2, 0x0, 2, 1, 0x00) +  # add x2, x2, x1
            i_type(0x13, 1, 0x0, 1, -1) +       # addi x1, x1, -1
            j_type(0x6F, 0, -12) +              # jal x0, -12
            struct.pack("<I", 0x00100073)       # ebreak
        )
        res = run_hex_code(prog, max_cycles=5000)
        dt = time.time() - t0
        expected_sum = (500 * 501) // 2
        sum_ok = (res["regs"][2] == expected_sum)
        self.record(
            "Lab01", "high_cycle_loop_convergence",
            sum_ok,
            f"computed sum(1..500) = {res['regs'][2]} (expected {expected_sum}) in {res['cycles']} cycles",
            dt
        )

    # =========================================================================
    # LAB 02: Mini Kernel OS Stress
    # =========================================================================
    def stress_lab02_kernel(self):
        print("\n--- [LAB 02] Mini Kernel OS Adversarial Stress Tests ---")
        lab_dir = os.path.join(BASE_DIR, "labs", "lab02-mini-kernel-os")

        stress_src = os.path.join(lab_dir, "stress_test.c")
        stress_exe = os.path.join(lab_dir, "stress_kernel.exe" if os.name == "nt" else "stress_kernel")

        c_code = r"""
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include "kernel.h"

int test_allocator_exhaustion(void) {
    palloc_t alloc;
    palloc_init(&alloc, 32);
    int frames[32];
    for (int i = 0; i < 32; i++) {
        frames[i] = palloc_alloc_frame(&alloc);
        if (frames[i] < 0) return 1;
    }
    if (palloc_free_count(&alloc) != 0) return 2;
    /* Must return -1 gracefully when completely exhausted */
    if (palloc_alloc_frame(&alloc) != -1) return 3;

    /* Free middle frame and reallocate */
    if (palloc_free_frame(&alloc, frames[15]) != 0) return 4;
    if (palloc_free_count(&alloc) != 1) return 5;
    int new_f = palloc_alloc_frame(&alloc);
    if (new_f != frames[15]) return 6;

    /* Double free check */
    if (palloc_free_frame(&alloc, frames[15]) != 0) return 7;
    if (palloc_free_frame(&alloc, frames[15]) != -2) return 8;

    /* Out of bounds frame check */
    if (palloc_free_frame(&alloc, 9999) != -1) return 9;

    palloc_free_pool(&alloc);
    return 0;
}

static void dummy(void *arg) { (void)arg; }

int test_scheduler_stress(void) {
    scheduler_t sched;
    sched_init(&sched);

    /* Allocate up to MAX_TASKS */
    for (int i = 0; i < MAX_TASKS; i++) {
        int pid = sched_create_task(&sched, dummy, NULL, 1, NULL);
        if (pid <= 0) return 1;
    }
    if (sched.active_task_count != MAX_TASKS) return 2;

    /* 17th task must fail gracefully */
    if (sched_create_task(&sched, dummy, NULL, 1, NULL) != -1) return 3;

    /* 1,000 preemption ticks */
    for (int t = 0; t < 1000; t++) {
        sched_tick(&sched);
        task_t *curr = sched_get_current(&sched);
        if (!curr || curr->state != TASK_RUNNING) return 4;
    }

    /* Terminate all tasks cleanly */
    for (int i = 0; i < MAX_TASKS; i++) {
        sched_exit_current(&sched, 0);
    }
    if (sched.active_task_count != 0) return 5;

    return 0;
}

int test_syscall_edge_cases(void) {
    kernel_t kern;
    kernel_init(&kern);

    sched_create_task(&kern.sched, dummy, NULL, 1, kern.mmu.kernel_pgdir);

    /* Test unknown syscall -> -38 ENOSYS */
    int32_t r_unknown = syscall_dispatch(&kern.syscall, 99999, 0, 0, 0);
    if (r_unknown != -38) return 1;

    /* Test SYS_WRITE with len=0 -> 0 */
    int32_t r_zero = syscall_dispatch(&kern.syscall, SYS_WRITE, 1, 0, 0);
    if (r_zero != 0) return 2;

    /* Test SYS_WRITE with invalid fd=99 -> -1 */
    int32_t r_badfd = syscall_dispatch(&kern.syscall, SYS_WRITE, 99, 0, 10);
    if (r_badfd != -1) return 3;

    kernel_shutdown(&kern);
    return 0;
}

int main(void) {
    int r1 = test_allocator_exhaustion();
    int r2 = test_scheduler_stress();
    int r3 = test_syscall_edge_cases();
    printf("{\"alloc\": %d, \"sched\": %d, \"syscall\": %d}\n", r1, r2, r3);
    return (r1 + r2 + r3 == 0) ? 0 : 1;
}
"""
        with open(stress_src, "w", encoding="utf-8") as f:
            f.write(c_code)

        try:
            cmd = ["gcc", "-Wall", "-Wextra", "-std=c99", "-O2", "-Iinclude",
                   "src/palloc.c", "src/mmu.c", "src/sched.c", "src/syscall.c", "src/kernel.c",
                   "stress_test.c", "-o", stress_exe]
            subprocess.check_call(cmd, cwd=lab_dir)

            t0 = time.time()
            res = subprocess.run([stress_exe], cwd=lab_dir, capture_output=True, text=True)
            dt = time.time() - t0
            passed = (res.returncode == 0)
            self.record(
                "Lab02", "kernel_alloc_sched_syscall_adversarial",
                passed,
                f"returncode={res.returncode}, output={res.stdout.strip()}",
                dt
            )
        finally:
            if os.path.exists(stress_src):
                os.remove(stress_src)
            if os.path.exists(stress_exe):
                os.remove(stress_exe)

    # =========================================================================
    # LAB 03: Compiler & Bytecode VM Stress
    # =========================================================================
    def stress_lab03_compiler(self):
        print("\n--- [LAB 03] Compiler & Bytecode VM Adversarial Stress Tests ---")
        lab_dir = os.path.join(BASE_DIR, "labs", "lab03-compiler-llvm-jit")
        exe_path = os.path.join(lab_dir, "minilang_compiler.exe" if os.name == "nt" else "minilang_compiler")

        # 3.1 Precedence and deep parenthesized math
        t0 = time.time()
        code = "let a = (100 - 25 * 3 + (14 / 2)) * 2; a;"
        res = subprocess.run([exe_path, "--eval", code], cwd=lab_dir, capture_output=True, text=True)
        dt = time.time() - t0
        data = json.loads(res.stdout) if res.stdout else {}
        expected = (100 - 25 * 3 + (14 // 2)) * 2 # 64
        self.record(
            "Lab03", "pratt_parser_precedence_deep_nesting",
            data.get("result") == expected,
            f"eval: {data.get('result')} (expected {expected})",
            dt
        )

        # 3.2 Division by Zero Runtime Error Trap
        t0 = time.time()
        code = "let x = 42 / 0; x;"
        res = subprocess.run([exe_path, "--eval", code], cwd=lab_dir, capture_output=True, text=True)
        dt = time.time() - t0
        self.record(
            "Lab03", "division_by_zero_error_handling",
            res.returncode != 0,
            f"returncode={res.returncode}, caught divide-by-zero runtime error",
            dt
        )

        # 3.3 Iterative factorial calculation
        t0 = time.time()
        fact_code = "let fact = 1; let i = 1; while (i <= 6) { fact = fact * i; i = i + 1; } fact;"
        res = subprocess.run([exe_path, "--eval", fact_code], cwd=lab_dir, capture_output=True, text=True)
        dt = time.time() - t0
        data = json.loads(res.stdout) if res.stdout else {}
        self.record(
            "Lab03", "while_loop_factorial_execution",
            data.get("result") == 720.0,
            f"6! = {data.get('result')} (expected 720.0)",
            dt
        )

    # =========================================================================
    # LAB 04: LSM Storage Engine Stress
    # =========================================================================
    def stress_lab04_lsm(self):
        print("\n--- [LAB 04] LSM Storage Engine Adversarial Stress Tests ---")
        lab_dir = os.path.join(BASE_DIR, "labs", "lab04-lsm-storage-engine")
        stress_src = os.path.join(lab_dir, "stress_lsm.cpp")
        stress_exe = os.path.join(lab_dir, "stress_lsm.exe" if os.name == "nt" else "stress_lsm")

        c_code = r"""
#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <cassert>
#include "lsm_engine.h"

int test_wal_corruption_recovery(void) {
    std::string test_log = "stress_corrupt_wal.log";
    std::remove(test_log.c_str());

    {
        WriteAheadLog wal(test_log);
        for (int i = 0; i < 10; i++) {
            wal.append_put("key_" + std::to_string(i), "val_" + std::to_string(i));
        }
        wal.sync();
    }

    /* Intentionally corrupt byte at offset in record 6 */
    std::fstream f(test_log, std::ios::in | std::ios::out | std::ios::binary);
    if (!f.is_open()) return 1;
    f.seekp(150, std::ios::beg);
    char bad_byte = 0xAA;
    f.write(&bad_byte, 1);
    f.close();

    /* Recover: must stop safely at corrupted record and return records before corruption */
    auto recs = WriteAheadLog::recover(test_log);
    std::remove(test_log.c_str());

    if (recs.empty()) return 2; /* Should have recovered at least first few */
    if (recs.size() >= 10) return 3; /* Should NOT have recovered through corruption */
    if (recs[0].key != "key_0" || recs[0].value != "val_0") return 4;

    return 0;
}

int test_bloom_scale_and_fp(void) {
    BloomFilter filter(8192, 4);
    for (int i = 0; i < 100; i++) {
        filter.add("member_" + std::to_string(i));
    }

    /* 100% True Positive check */
    for (int i = 0; i < 100; i++) {
        if (!filter.may_contain("member_" + std::to_string(i))) return 1;
    }

    /* Check False Positive rate with 5000 non-members */
    int fp = 0;
    int non_members = 5000;
    for (int i = 0; i < non_members; i++) {
        if (filter.may_contain("non_member_" + std::to_string(i))) {
            fp++;
        }
    }
    double fp_rate = (double)fp / non_members;
    if (fp_rate > 0.05) return 2; /* FP rate must be <= 5% */
    return 0;
}

int main(void) {
    int r1 = test_wal_corruption_recovery();
    int r2 = test_bloom_scale_and_fp();
    std::cout << "{\"wal_corrupt\": " << r1 << ", \"bloom_fp\": " << r2 << "}\n";
    return (r1 + r2 == 0) ? 0 : 1;
}
"""
        with open(stress_src, "w", encoding="utf-8") as f:
            f.write(c_code)

        try:
            cmd = ["g++", "-Wall", "-Wextra", "-std=c++14", "-O2", "-Iinclude",
                   "src/bloom.cpp", "src/wal.cpp", "src/memtable.cpp", "src/sstable.cpp",
                   "src/compaction.cpp", "src/lsm_engine.cpp", "stress_lsm.cpp", "-o", stress_exe]
            subprocess.check_call(cmd, cwd=lab_dir)

            t0 = time.time()
            res = subprocess.run([stress_exe], cwd=lab_dir, capture_output=True, text=True)
            dt = time.time() - t0
            passed = (res.returncode == 0)
            self.record(
                "Lab04", "wal_corruption_and_bloom_fp_rate",
                passed,
                f"returncode={res.returncode}, output={res.stdout.strip()}",
                dt
            )
        finally:
            if os.path.exists(stress_src):
                os.remove(stress_src)
            if os.path.exists(stress_exe):
                os.remove(stress_exe)

    # =========================================================================
    # LAB 05: Tensor Autograd & Attention Stress
    # =========================================================================
    def stress_lab05_autograd(self):
        print("\n--- [LAB 05] Tensor Autograd & Attention Adversarial Stress Tests ---")
        lab05_dir = os.path.join(BASE_DIR, "labs", "lab05-tensor-autograd-cuda")
        if lab05_dir not in sys.path:
            sys.path.insert(0, lab05_dir)

        from autograd.tensor import Tensor
        from autograd.attention import scaled_dot_product_attention, simulated_cuda_matmul
        from autograd.ops import matmul_raw

        # 5.1 Finite Difference Numerical Gradient Check on Multi-Layer Computation
        # y = relu(x * W + b), loss = sum(y * y)
        t0 = time.time()
        eps = 1e-5

        def compute_loss(W_val, x_val, b_val):
            W = Tensor(W_val, requires_grad=True)
            x = Tensor(x_val, requires_grad=True)
            b = Tensor(b_val, requires_grad=True)
            h = x.matmul(W) + b
            y = h.relu()
            loss = (y * y).sum()
            return loss, W, x, b

        W_init = [[0.8, -0.5], [0.3, 0.9]]
        x_init = [[1.2, 0.4]]
        b_init = [[0.1, -0.2]]

        # Analytical gradients
        loss_tensor, W_node, x_node, b_node = compute_loss(W_init, x_init, b_init)
        loss_tensor.backward()
        analytical_dW = W_node.grad

        # Numerical gradient for W[0][0]
        W_plus = [[0.8 + eps, -0.5], [0.3, 0.9]]
        W_minus = [[0.8 - eps, -0.5], [0.3, 0.9]]
        loss_plus, _, _, _ = compute_loss(W_plus, x_init, b_init)
        loss_minus, _, _, _ = compute_loss(W_minus, x_init, b_init)
        numerical_dW00 = (loss_plus.data - loss_minus.data) / (2 * eps)

        ana_val = analytical_dW[0][0]
        rel_err = abs(ana_val - numerical_dW00) / (abs(ana_val) + 1e-8)
        dt = time.time() - t0
        self.record(
            "Lab05", "autograd_finite_difference_oracle_check",
            rel_err < 1e-4,
            f"analytical={ana_val:.6f}, numerical={numerical_dW00:.6f}, rel_err={rel_err:.2e}",
            dt
        )

        # 5.2 Attention Gradient Finite Difference Verification
        t0 = time.time()
        Q_data = [[1.0, 0.5], [0.2, 0.8]]
        K_data = [[0.9, 0.1], [0.4, 0.7]]
        V_data = [[2.0, 3.0], [1.0, 4.0]]

        def eval_attn_loss(Q_d, K_d, V_d):
            Q = Tensor(Q_d, requires_grad=True)
            K = Tensor(K_d, requires_grad=True)
            V = Tensor(V_d, requires_grad=True)
            out = scaled_dot_product_attention(Q, K, V)
            return out.sum(), Q, K, V

        base_loss, Q_node, K_node, V_node = eval_attn_loss(Q_data, K_data, V_data)
        base_loss.backward()
        ana_dV00 = V_node.grad[0][0]

        # Perturb V[0][0]
        V_p = [[2.0 + eps, 3.0], [1.0, 4.0]]
        V_m = [[2.0 - eps, 3.0], [1.0, 4.0]]
        loss_vp, _, _, _ = eval_attn_loss(Q_data, K_data, V_p)
        loss_vm, _, _, _ = eval_attn_loss(Q_data, K_data, V_m)
        num_dV00 = (loss_vp.data - loss_vm.data) / (2 * eps)

        rel_err_v = abs(ana_dV00 - num_dV00) / (abs(ana_dV00) + 1e-8)
        dt = time.time() - t0
        self.record(
            "Lab05", "scaled_dot_product_attention_gradient_check",
            rel_err_v < 1e-3,
            f"V[0][0]: analytical={ana_dV00:.6f}, numerical={num_dV00:.6f}, rel_err={rel_err_v:.2e}",
            dt
        )

        # 5.3 Simulated CUDA Non-Square Matrix & Odd Dimensions
        t0 = time.time()
        # 5x3 * 3x7 matrix multiplication (odd dimensions vs 4x4 tile)
        A = [[float(i * 3 + j + 1) for j in range(3)] for i in range(5)]
        B = [[float(i * 7 + j + 2) for j in range(7)] for i in range(3)]

        golden = matmul_raw(A, B)
        simulated = simulated_cuda_matmul(A, B, tile_size=4)

        max_diff = max(abs(simulated[i][j] - golden[i][j]) for i in range(5) for j in range(7))
        dt = time.time() - t0
        self.record(
            "Lab05", "cuda_matmul_odd_dimensions_and_tile_boundaries",
            max_diff < 1e-5,
            f"5x3 * 3x7 matmul max error vs golden: {max_diff:.2e}",
            dt
        )

    # =========================================================================
    # LAB 06: Raft Consensus Cluster Stress
    # =========================================================================
    def stress_lab06_raft(self):
        print("\n--- [LAB 06] Raft Consensus Cluster Adversarial Stress Tests ---")
        lab06_dir = os.path.join(BASE_DIR, "labs", "lab06-raft-consensus-cluster")
        if lab06_dir not in sys.path:
            sys.path.insert(0, lab06_dir)

        from raft.network import SimulatedNetwork
        from raft.node import RaftNode
        from raft.state import RaftRole

        # 6.1 5-Node Partition and Split-Brain Prevention
        t0 = time.time()
        net = SimulatedNetwork()
        nodes = [RaftNode(i, [j for j in range(5) if j != i], net) for i in range(5)]

        # Initial election: Node 0
        nodes[0].start_election()
        self.record(
            "Lab06", "raft_5node_cluster_initial_election",
            nodes[0].role == RaftRole.LEADER,
            f"Node 0 elected leader (role={nodes[0].role})",
            time.time() - t0
        )

        # Partition network into minority {0, 1} and majority {2, 3, 4}
        t0 = time.time()
        net.partition([0, 1], [2, 3, 4])

        # Node 0 (minority) attempts to propose: MUST NOT commit without quorum
        committed_minority = nodes[0].propose("stale_cmd_minority")
        c1 = (not committed_minority)

        # Node 2 in majority starts election and proposes entry
        nodes[2].start_election()
        c2 = (nodes[2].role == RaftRole.LEADER)
        committed_majority = nodes[2].propose("valid_cmd_majority")
        c3 = committed_majority

        # Heal network partition
        net.heal()

        # Node 2 heartbeats to cluster: Node 0 must recognize higher term and step down to FOLLOWER
        nodes[2].broadcast_heartbeat()
        c4 = (nodes[0].role == RaftRole.FOLLOWER)
        c5 = (nodes[0].current_term == nodes[2].current_term)

        # Replicate log to former minority
        nodes[2].replicate_log()
        c6 = (len(nodes[0].state_machine) == len(nodes[2].state_machine))

        dt = time.time() - t0
        all_passed = c1 and c2 and c3 and c4 and c5 and c6
        self.record(
            "Lab06", "network_partition_split_brain_and_log_reconciliation",
            all_passed,
            f"minority_blocked={c1}, majority_leader={c2}, majority_commit={c3}, stepdown={c4}, log_sync={c6}",
            dt
        )

    # =========================================================================
    # LAB 07: HFT Order Matching Engine Stress
    # =========================================================================
    def stress_lab07_hft(self):
        print("\n--- [LAB 07] HFT Order Matching Engine Adversarial Stress Tests ---")
        lab_dir = os.path.join(BASE_DIR, "labs", "lab07-hft-order-matching-engine")
        exe_path = os.path.join(lab_dir, "hft_engine.exe" if os.name == "nt" else "hft_engine")

        # 7.1 Massive Throughput Stress (100,000 orders)
        t0 = time.time()
        res = subprocess.run([exe_path, "--benchmark", "100000"], cwd=lab_dir, capture_output=True, text=True)
        dt = time.time() - t0
        data = json.loads(res.stdout) if res.stdout else {}
        bench = data.get("benchmark", {})
        throughput = bench.get("throughput_ops", 0)
        avg_lat = bench.get("avg_latency_ns", 0)
        trades = bench.get("trades", 0)
        passed = (res.returncode == 0 and throughput > 1_000_000)
        self.record(
            "Lab07", "matching_throughput_100k_orders",
            passed,
            f"throughput: {throughput:,.0f} ops/sec, avg_latency: {avg_lat:.2f} ns, trades: {trades}",
            dt
        )

        # 7.2 Cancel non-existent order ID
        stress_src = os.path.join(lab_dir, "stress_hft.cpp")
        stress_exe = os.path.join(lab_dir, "stress_hft.exe" if os.name == "nt" else "stress_hft")
        c_code = r"""
#include <iostream>
#include <cassert>
#include "matching_engine.h"

int main(void) {
    MatchingEngine engine;
    /* Cancel on empty book */
    if (engine.cancel_order(9999)) return 1;

    /* Add order and cancel non-existent */
    engine.submit_order(1, Side::BUY, OrderType::LIMIT, 1000, 50);
    if (engine.cancel_order(2)) return 2;

    /* Cancel actual order */
    if (!engine.cancel_order(1)) return 3;
    if (engine.order_count() != 0) return 4;

    /* Double cancel */
    if (engine.cancel_order(1)) return 5;

    std::cout << "OK\n";
    return 0;
}
"""
        with open(stress_src, "w", encoding="utf-8") as f:
            f.write(c_code)
        try:
            cmd = ["g++", "-Wall", "-Wextra", "-std=c++14", "-O2", "-Iinclude",
                   "src/order_book.cpp", "src/matching_engine.cpp", "stress_hft.cpp", "-o", stress_exe]
            subprocess.check_call(cmd, cwd=lab_dir)
            t0 = time.time()
            res = subprocess.run([stress_exe], cwd=lab_dir, capture_output=True, text=True)
            dt = time.time() - t0
            self.record(
                "Lab07", "cancellation_edge_cases_and_double_cancel",
                res.returncode == 0,
                f"returncode={res.returncode}, non-existent and double cancel handled safely",
                dt
            )
        finally:
            if os.path.exists(stress_src):
                os.remove(stress_src)
            if os.path.exists(stress_exe):
                os.remove(stress_exe)

    # =========================================================================
    # LAB 08: FOC Motor & Robotics Controller Stress
    # =========================================================================
    def stress_lab08_foc(self):
        print("\n--- [LAB 08] FOC Motor & Robotics Controller Adversarial Stress Tests ---")
        lab_dir = os.path.join(BASE_DIR, "labs", "lab08-foc-motor-robotics-controller")
        stress_src = os.path.join(lab_dir, "stress_foc.c")
        stress_exe = os.path.join(lab_dir, "stress_foc.exe" if os.name == "nt" else "stress_foc")

        c_code = r"""
#include <stdio.h>
#include <math.h>
#include "foc_math.h"
#include "pi_controller.h"
#include "svpwm.h"
#include "kinematics.h"

int test_clarke_park_360_sweep(void) {
    for (int deg = 0; deg < 360; deg++) {
        double theta = deg * M_PI / 180.0;
        PhaseCurrents i_abc = { 10.0 * cos(theta), 10.0 * cos(theta - 2.0*M_PI/3.0), 10.0 * cos(theta + 2.0*M_PI/3.0) };
        AlphaBeta ab = clarke_transform(i_abc);
        DQFrame dq = park_transform(ab, theta);

        /* In synchronous frame at electrical angle theta, d should be constant ~10.0, q ~0.0 */
        if (fabs(dq.d - 10.0) > 1e-4 || fabs(dq.q) > 1e-4) return 1;

        /* Round trip back */
        AlphaBeta ab_recon = inverse_park_transform(dq, theta);
        if (fabs(ab_recon.alpha - ab.alpha) > 1e-4 || fabs(ab_recon.beta - ab.beta) > 1e-4) return 2;
    }
    return 0;
}

int test_svpwm_invariants(void) {
    double v_dc = 24.0;
    double t_pwm = 0.0001;
    for (int deg = 0; deg < 360; deg += 5) {
        double theta = deg * M_PI / 180.0;
        AlphaBeta v_ab = { 8.0 * cos(theta), 8.0 * sin(theta) };
        SVPWMResult res = svpwm_generate(v_ab, v_dc, t_pwm);

        if (res.sector < 1 || res.sector > 6) return 1;
        if (fabs((res.t1 + res.t2 + res.t0) - t_pwm) > 1e-8) return 2;
        if (res.duty.a < 0.0 || res.duty.a > 1.0) return 3;
        if (res.duty.b < 0.0 || res.duty.b > 1.0) return 4;
        if (res.duty.c < 0.0 || res.duty.c > 1.0) return 5;
    }
    return 0;
}

int test_kinematics_workspace_boundary(void) {
    ArmDimensions arm = { 1.0, 0.8 };
    /* Boundary reachability: r = 1.79 */
    EndEffectorPos boundary = { 1.79, 0.0 };
    JointAngles q;
    if (!inverse_kinematics(arm, boundary, false, &q)) return 1;
    EndEffectorPos recon = forward_kinematics(arm, q);
    if (fabs(recon.x - boundary.x) > 1e-3) return 2;

    /* Outside workspace: r = sqrt(8) ~ 2.82 > 1.8 */
    EndEffectorPos outside = { 2.0, 2.0 };
    if (inverse_kinematics(arm, outside, false, &q)) return 3; /* Must reject */
    return 0;
}

int main(void) {
    int r1 = test_clarke_park_360_sweep();
    int r2 = test_svpwm_invariants();
    int r3 = test_kinematics_workspace_boundary();
    printf("{\"clarke_park\": %d, \"svpwm\": %d, \"kinematics\": %d}\n", r1, r2, r3);
    return (r1 + r2 + r3 == 0) ? 0 : 1;
}
"""
        with open(stress_src, "w", encoding="utf-8") as f:
            f.write(c_code)
        try:
            cmd = ["gcc", "-Wall", "-Wextra", "-std=c99", "-O2", "-Iinclude",
                   "src/foc_math.c", "src/pi_controller.c", "src/svpwm.c", "src/kinematics.c",
                   "stress_foc.c", "-o", stress_exe, "-lm"]
            subprocess.check_call(cmd, cwd=lab_dir)
            t0 = time.time()
            res = subprocess.run([stress_exe], cwd=lab_dir, capture_output=True, text=True)
            dt = time.time() - t0
            self.record(
                "Lab08", "foc_transforms_svpwm_and_kinematics_sweep",
                res.returncode == 0,
                f"returncode={res.returncode}, output={res.stdout.strip()}",
                dt
            )
        finally:
            if os.path.exists(stress_src):
                os.remove(stress_src)
            if os.path.exists(stress_exe):
                os.remove(stress_exe)

    # =========================================================================
    # REPO-WIDE LINK INTEGRITY & HYGIENE STRESS
    # =========================================================================
    def stress_link_integrity_and_hygiene(self):
        print("\n--- [REPO-WIDE] Exhaustive Link Integrity & Hygiene Crawler ---")
        t0 = time.time()
        broken_links = []
        total_links = 0

        target_dirs = ["tracks", "drills", "flashcards", "labs", "curriculum"]
        for tdir in target_dirs:
            full_tdir = os.path.join(BASE_DIR, tdir)
            if not os.path.isdir(full_tdir):
                continue
            for root, _, files in os.walk(full_tdir):
                for f in files:
                    if f.endswith(".md"):
                        md_path = os.path.join(root, f)
                        try:
                            with open(md_path, "r", encoding="utf-8", errors="ignore") as fh:
                                content = fh.read()
                        except Exception:
                            continue
                        
                        # Strip code fences so that Python indexing like arr[i](arg) is not parsed as markdown link
                        stripped_content = re.sub(r"```[\s\S]*?```", "", content)
                        # Also strip inline backticks `...`
                        stripped_content = re.sub(r"`[^`]*`", "", stripped_content)

                        links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", stripped_content)
                        for label, target in links:
                            target = target.strip()
                            if target.startswith(("http://", "https://", "mailto:", "ftp://", "#")):
                                continue
                            clean_target = urllib.parse.unquote(target.split("#")[0].strip())
                            if not clean_target:
                                continue
                            total_links += 1
                            resolved = os.path.normpath(os.path.join(root, clean_target))
                            if not os.path.exists(resolved):
                                broken_links.append((os.path.relpath(md_path, BASE_DIR), target, resolved))

        dt = time.time() - t0
        self.record(
            "RepoLinks", "exhaustive_markdown_link_resolution",
            len(broken_links) == 0,
            f"verified {total_links} relative links across {target_dirs}; broken links: {len(broken_links)}",
            dt
        )

    def run_all(self):
        start = time.time()
        print("================================================================================")
        print("          EMPIRICAL CHALLENGER 1 - ADVERSARIAL STRESS TEST SUITE")
        print("================================================================================")
        self.stress_lab01_riscv()
        self.stress_lab02_kernel()
        self.stress_lab03_compiler()
        self.stress_lab04_lsm()
        self.stress_lab05_autograd()
        self.stress_lab06_raft()
        self.stress_lab07_hft()
        self.stress_lab08_foc()
        self.stress_link_integrity_and_hygiene()

        total_time = time.time() - start
        print("\n================================================================================")
        print(f"ADVERSARIAL STRESS TEST SUMMARY: {self.passed} PASSED, {self.failed} FAILED")
        print(f"Total Duration: {total_time:.2f}s | Final Verdict: {'APPROVE' if self.failed == 0 else 'REQUEST_CHANGES'}")
        print("================================================================================")
        return 0 if self.failed == 0 else 1

if __name__ == "__main__":
    runner = StressTestRunner()
    sys.exit(runner.run_all())
