#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "riscv.h"
#include "cpu.h"

static void dump_state(const cpu_t *cpu) {
    printf("{\n  \"pc\": \"0x%08X\",\n  \"halted\": %d,\n  \"cycles\": %llu,\n  \"regs\": [",
           cpu->pc, cpu->halted, (unsigned long long)cpu->cycles);
    for (int i = 0; i < 32; i++) {
        printf("%u%s", cpu->x[i], (i == 31) ? "" : ", ");
    }
    printf("],\n  \"uart\": \"%s\"\n}\n", cpu->mmu.uart_out);
}

static int run_internal_tests(void) {
    int passed = 0;
    int failed = 0;

    printf("[Lab01 RISC-V Emulator Internal Diagnostic]\n");

    /* Test 1: Register x0 immutability */
    {
        cpu_t cpu;
        cpu_init(&cpu);
        cpu_set_reg(&cpu, 0, 0xDEADBEEF);
        if (cpu_get_reg(&cpu, 0) == 0) {
            printf("  [PASS] x0 is hardwired to 0\n");
            passed++;
        } else {
            printf("  [FAIL] x0 could be modified\n");
            failed++;
        }
        cpu_free(&cpu);
    }

    /* Test 2: ADDI instruction */
    {
        cpu_t cpu;
        cpu_init(&cpu);
        /* addi x1, x0, 42 -> 0x02A00093 */
        uint32_t code[] = { 0x02A00093U };
        mmu_load_binary(&cpu.mmu, RAM_BASE, (const uint8_t *)code, sizeof(code));
        cpu_step(&cpu);
        if (cpu_get_reg(&cpu, 1) == 42 && cpu.pc == RAM_BASE + 4) {
            printf("  [PASS] ADDI instruction executed successfully\n");
            passed++;
        } else {
            printf("  [FAIL] ADDI failed: x1=%u pc=0x%08X\n", cpu_get_reg(&cpu, 1), cpu.pc);
            failed++;
        }
        cpu_free(&cpu);
    }

    /* Test 3: SUB and SLT instructions */
    {
        cpu_t cpu;
        cpu_init(&cpu);
        /* addi x1, x0, 10 -> 0x00A00093 */
        /* addi x2, x0, 3  -> 0x00300113 */
        /* sub  x3, x1, x2 -> 0x402081B3 */
        /* slt  x4, x2, x1 -> 0x00112233 */
        uint32_t code[] = {
            0x00A00093U,
            0x00300113U,
            0x402081B3U,
            0x00112233U
        };
        mmu_load_binary(&cpu.mmu, RAM_BASE, (const uint8_t *)code, sizeof(code));
        cpu_run(&cpu, 4);
        if (cpu_get_reg(&cpu, 3) == 7 && cpu_get_reg(&cpu, 4) == 1) {
            printf("  [PASS] SUB and SLT executed successfully\n");
            passed++;
        } else {
            printf("  [FAIL] SUB/SLT failed: x3=%u x4=%u\n", cpu_get_reg(&cpu, 3), cpu_get_reg(&cpu, 4));
            failed++;
        }
        cpu_free(&cpu);
    }

    /* Test 4: Memory Store & Load (SW, LW) */
    {
        cpu_t cpu;
        cpu_init(&cpu);
        /* lui x1, 0x80001 -> 0x800010B7 (x1 = 0x80001000) */
        /* addi x2, x0, 123 -> 0x07B00113 */
        /* sw x2, 0(x1) -> 0x0020A023 */
        /* lw x3, 0(x1) -> 0x0000A183 */
        uint32_t code[] = {
            0x800010B7U,
            0x07B00113U,
            0x0020A023U,
            0x0000A183U
        };
        mmu_load_binary(&cpu.mmu, RAM_BASE, (const uint8_t *)code, sizeof(code));
        cpu_run(&cpu, 4);
        if (cpu_get_reg(&cpu, 3) == 123) {
            printf("  [PASS] SW and LW executed successfully\n");
            passed++;
        } else {
            printf("  [FAIL] Memory test failed: x3=%u\n", cpu_get_reg(&cpu, 3));
            failed++;
        }
        cpu_free(&cpu);
    }

    /* Test 5: Branch BEQ loop */
    {
        cpu_t cpu;
        cpu_init(&cpu);
        /* addi x1, x0, 5    (0x00500093) */
        /* addi x2, x0, 0    (0x00000113) */
        /* loop: */
        /* addi x2, x2, 1    (0x00110113) */
        /* bne  x2, x1, -4   (0xFE111EE3) */
        uint32_t code[] = {
            0x00500093U,
            0x00000113U,
            0x00110113U,
            0xFE111EE3U
        };
        mmu_load_binary(&cpu.mmu, RAM_BASE, (const uint8_t *)code, sizeof(code));
        cpu_run(&cpu, 30);
        if (cpu_get_reg(&cpu, 2) == 5) {
            printf("  [PASS] Branch loop terminated accurately at x2=5\n");
            passed++;
        } else {
            printf("  [FAIL] Branch loop failed: x2=%u\n", cpu_get_reg(&cpu, 2));
            failed++;
        }
        cpu_free(&cpu);
    }

    printf("Total: %d passed, %d failed\n", passed, failed);
    return failed == 0 ? 0 : 1;
}

static uint8_t hex_to_byte(char c) {
    if (c >= '0' && c <= '9') return (uint8_t)(c - '0');
    if (c >= 'a' && c <= 'f') return (uint8_t)(c - 'a' + 10);
    if (c >= 'A' && c <= 'F') return (uint8_t)(c - 'A' + 10);
    return 0;
}

int main(int argc, char **argv) {
    if (argc < 2) {
        printf("Usage: %s [--test-internal | --exec-hex <hex_string> | --run-bin <bin_path>]\n", argv[0]);
        return 0;
    }

    if (strcmp(argv[1], "--test-internal") == 0) {
        return run_internal_tests();
    }

    if (strcmp(argv[1], "--exec-hex") == 0 && argc >= 3) {
        const char *hex = argv[2];
        size_t hex_len = strlen(hex);
        size_t bin_len = hex_len / 2;
        uint8_t *bin = (uint8_t *)malloc(bin_len);
        for (size_t i = 0; i < bin_len; i++) {
            bin[i] = (hex_to_byte(hex[i * 2]) << 4) | hex_to_byte(hex[i * 2 + 1]);
        }

        cpu_t cpu;
        cpu_init(&cpu);
        mmu_load_binary(&cpu.mmu, RAM_BASE, bin, bin_len);
        free(bin);

        size_t max_cycles = (argc >= 4) ? (size_t)atoi(argv[3]) : 10000;
        cpu_run(&cpu, max_cycles);
        dump_state(&cpu);
        cpu_free(&cpu);
        return 0;
    }

    if (strcmp(argv[1], "--run-bin") == 0 && argc >= 3) {
        FILE *f = fopen(argv[2], "rb");
        if (!f) {
            fprintf(stderr, "Error opening binary file %s\n", argv[2]);
            return 1;
        }
        fseek(f, 0, SEEK_END);
        long sz = ftell(f);
        fseek(f, 0, SEEK_SET);

        uint8_t *buf = (uint8_t *)malloc(sz);
        if (fread(buf, 1, sz, f) != (size_t)sz) {
            free(buf);
            fclose(f);
            return 1;
        }
        fclose(f);

        cpu_t cpu;
        cpu_init(&cpu);
        mmu_load_binary(&cpu.mmu, RAM_BASE, buf, sz);
        free(buf);

        size_t max_cycles = (argc >= 4) ? (size_t)atoi(argv[3]) : 50000;
        cpu_run(&cpu, max_cycles);
        dump_state(&cpu);
        cpu_free(&cpu);
        return 0;
    }

    fprintf(stderr, "Unknown option %s\n", argv[1]);
    return 1;
}
