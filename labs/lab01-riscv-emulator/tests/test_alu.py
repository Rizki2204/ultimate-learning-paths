import unittest
from tests.riscv_helpers import r_type, i_type, u_type, run_hex_code

class TestAluOperations(unittest.TestCase):
    def test_x0_is_zero(self):
        # ADDI x0, x0, 100
        code = i_type(0x13, 0, 0, 0, 100)
        state = run_hex_code(code, max_cycles=1)
        self.assertEqual(state["regs"][0], 0)

    def test_addi_and_sub(self):
        # ADDI x1, x0, 50
        # ADDI x2, x0, 20
        # SUB  x3, x1, x2 (50 - 20 = 30)
        # ADD  x4, x1, x2 (50 + 20 = 70)
        code = (
            i_type(0x13, 1, 0, 0, 50) +
            i_type(0x13, 2, 0, 0, 20) +
            r_type(0x33, 3, 0, 1, 2, 0x20) +
            r_type(0x33, 4, 0, 1, 2, 0x00)
        )
        state = run_hex_code(code, max_cycles=4)
        self.assertEqual(state["regs"][1], 50)
        self.assertEqual(state["regs"][2], 20)
        self.assertEqual(state["regs"][3], 30)
        self.assertEqual(state["regs"][4], 70)

    def test_bitwise_logic(self):
        # ADDI x1, x0, 0b1100 (12)
        # ADDI x2, x0, 0b1010 (10)
        # AND  x3, x1, x2 -> 0b1000 (8)
        # OR   x4, x1, x2 -> 0b1110 (14)
        # XOR  x5, x1, x2 -> 0b0110 (6)
        code = (
            i_type(0x13, 1, 0, 0, 12) +
            i_type(0x13, 2, 0, 0, 10) +
            r_type(0x33, 3, 7, 1, 2, 0x00) +
            r_type(0x33, 4, 6, 1, 2, 0x00) +
            r_type(0x33, 5, 4, 1, 2, 0x00)
        )
        state = run_hex_code(code, max_cycles=5)
        self.assertEqual(state["regs"][3], 8)
        self.assertEqual(state["regs"][4], 14)
        self.assertEqual(state["regs"][5], 6)

    def test_shifts_logical_and_arithmetic(self):
        # ADDI x1, x0, -16 (0xFFFFFFF0)
        # SRAI x2, x1, 2  (should maintain sign bits -> 0xFFFFFFFC = -4 = 4294967292 unsigned)
        # SRLI x3, x1, 2  (logical shift -> 0x3FFFFFFC)
        # SLLI x4, x1, 1  (shift left 1)
        code = (
            i_type(0x13, 1, 0, 0, -16) +
            i_type(0x13, 2, 5, 1, 2 | (0x20 << 5)) +
            i_type(0x13, 3, 5, 1, 2) +
            i_type(0x13, 4, 1, 1, 1)
        )
        state = run_hex_code(code, max_cycles=4)
        self.assertEqual(state["regs"][2], 0xFFFFFFFC)
        self.assertEqual(state["regs"][3], 0x3FFFFFFC)
        self.assertEqual(state["regs"][4], 0xFFFFFFE0)

    def test_slt_signed_vs_unsigned(self):
        # ADDI x1, x0, -5 (0xFFFFFFFB)
        # ADDI x2, x0, 5
        # SLT  x3, x1, x2 (signed: -5 < 5 -> 1)
        # SLTU x4, x1, x2 (unsigned: 0xFFFFFFFB < 5 -> 0)
        code = (
            i_type(0x13, 1, 0, 0, -5) +
            i_type(0x13, 2, 0, 0, 5) +
            r_type(0x33, 3, 2, 1, 2, 0x00) +
            r_type(0x33, 4, 3, 1, 2, 0x00)
        )
        state = run_hex_code(code, max_cycles=4)
        self.assertEqual(state["regs"][3], 1)
        self.assertEqual(state["regs"][4], 0)

    def test_lui_and_auipc(self):
        # LUI   x1, 0x12345000 -> x1 = 0x12345000
        # AUIPC x2, 0x00001000 -> x2 = PC + 0x00001000
        code = (
            u_type(0x37, 1, 0x12345000) +
            u_type(0x17, 2, 0x00001000)
        )
        state = run_hex_code(code, max_cycles=2)
        self.assertEqual(state["regs"][1], 0x12345000)
        self.assertEqual(state["regs"][2], 0x80000004 + 0x00001000)

if __name__ == "__main__":
    unittest.main()
