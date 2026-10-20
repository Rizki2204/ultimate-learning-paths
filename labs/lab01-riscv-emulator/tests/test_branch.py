import unittest
from tests.riscv_helpers import i_type, b_type, j_type, run_hex_code

class TestBranchAndJump(unittest.TestCase):
    def test_beq_taken_and_not_taken(self):
        # ADDI x1, x0, 10
        # ADDI x2, x0, 10
        # BEQ  x1, x2, +8 (skip next instruction)
        # ADDI x3, x0, 999 (should be skipped)
        # ADDI x4, x0, 777 (target)
        code = (
            i_type(0x13, 1, 0, 0, 10) +
            i_type(0x13, 2, 0, 0, 10) +
            b_type(0x63, 0, 1, 2, 8) +
            i_type(0x13, 3, 0, 0, 999) +
            i_type(0x13, 4, 0, 0, 777)
        )
        state = run_hex_code(code, max_cycles=4)
        self.assertEqual(state["regs"][3], 0)
        self.assertEqual(state["regs"][4], 777)

    def test_bne_not_taken(self):
        # ADDI x1, x0, 10
        # ADDI x2, x0, 10
        # BNE  x1, x2, +8 (should NOT be taken)
        # ADDI x3, x0, 999 (executed)
        code = (
            i_type(0x13, 1, 0, 0, 10) +
            i_type(0x13, 2, 0, 0, 10) +
            b_type(0x63, 1, 1, 2, 8) +
            i_type(0x13, 3, 0, 0, 999)
        )
        state = run_hex_code(code, max_cycles=4)
        self.assertEqual(state["regs"][3], 999)

    def test_blt_and_bge(self):
        # x1 = -10, x2 = 5
        # BLT x1, x2, +8 (taken because -10 < 5)
        # ADDI x3, x0, 1 (skipped)
        # ADDI x4, x0, 1 (target)
        code = (
            i_type(0x13, 1, 0, 0, -10) +
            i_type(0x13, 2, 0, 0, 5) +
            b_type(0x63, 4, 1, 2, 8) +
            i_type(0x13, 3, 0, 0, 1) +
            i_type(0x13, 4, 0, 0, 1)
        )
        state = run_hex_code(code, max_cycles=4)
        self.assertEqual(state["regs"][3], 0)
        self.assertEqual(state["regs"][4], 1)

    def test_jal_and_jalr(self):
        # JAL x1, +8 (x1 = PC + 4 = 0x80000004; jump to PC + 8 = 0x80000008)
        # ADDI x2, x0, 111 (skipped)
        # ADDI x3, x0, 222 (at 0x80000008)
        code = (
            j_type(0x6F, 1, 8) +
            i_type(0x13, 2, 0, 0, 111) +
            i_type(0x13, 3, 0, 0, 222)
        )
        state = run_hex_code(code, max_cycles=3)
        self.assertEqual(state["regs"][1], 0x80000004)
        self.assertEqual(state["regs"][2], 0)
        self.assertEqual(state["regs"][3], 222)

if __name__ == "__main__":
    unittest.main()
