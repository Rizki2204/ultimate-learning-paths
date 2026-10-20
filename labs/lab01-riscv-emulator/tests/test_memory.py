import unittest
from tests.riscv_helpers import u_type, i_type, s_type, run_hex_code

class TestMemoryOperations(unittest.TestCase):
    def test_store_and_load_word(self):
        # LUI x1, 0x80002000
        # ADDI x2, x0, 1000
        # SW x2, 0(x1)
        # LW x3, 0(x1)
        code = (
            u_type(0x37, 1, 0x80002000) +
            i_type(0x13, 2, 0, 0, 1000) +
            s_type(0x23, 2, 1, 2, 0) +
            i_type(0x03, 3, 2, 1, 0)
        )
        state = run_hex_code(code, max_cycles=4)
        self.assertEqual(state["regs"][3], 1000)

    def test_halfword_signed_and_unsigned(self):
        # LUI x1, 0x80002000
        # ADDI x2, x0, -2 (0xFFFFFFFE)
        # SH x2, 0(x1)
        # LH x3, 0(x1)   -> signed 16-bit 0xFFFE is sign-extended to -2 = 0xFFFFFFFE
        # LHU x4, 0(x1)  -> unsigned 16-bit is 0x0000FFFE = 65534
        code = (
            u_type(0x37, 1, 0x80002000) +
            i_type(0x13, 2, 0, 0, -2) +
            s_type(0x23, 1, 1, 2, 0) +
            i_type(0x03, 3, 1, 1, 0) +
            i_type(0x03, 4, 5, 1, 0)
        )
        state = run_hex_code(code, max_cycles=5)
        self.assertEqual(state["regs"][3], 0xFFFFFFFE)
        self.assertEqual(state["regs"][4], 0x0000FFFE)

    def test_byte_signed_and_unsigned(self):
        # LUI x1, 0x80002000
        # ADDI x2, x0, 0xFA
        # SB x2, 4(x1)
        # LB x3, 4(x1)   -> signed 8-bit 0xFA is -6 = 0xFFFFFFFA
        # LBU x4, 4(x1)  -> unsigned 8-bit is 0xFA = 250
        code = (
            u_type(0x37, 1, 0x80002000) +
            i_type(0x13, 2, 0, 0, 0xFA) +
            s_type(0x23, 0, 1, 2, 4) +
            i_type(0x03, 3, 0, 1, 4) +
            i_type(0x03, 4, 4, 1, 4)
        )
        state = run_hex_code(code, max_cycles=5)
        self.assertEqual(state["regs"][3], 0xFFFFFFFA)
        self.assertEqual(state["regs"][4], 0xFA)

    def test_mmio_uart_output(self):
        # LUI x1, 0x10000000 (UART base)
        # ADDI x2, x0, 0x48 ('H')
        # SB x2, 0(x1)
        # ADDI x2, x0, 0x49 ('I')
        # SB x2, 0(x1)
        code = (
            u_type(0x37, 1, 0x10000000) +
            i_type(0x13, 2, 0, 0, ord('H')) +
            s_type(0x23, 0, 1, 2, 0) +
            i_type(0x13, 2, 0, 0, ord('I')) +
            s_type(0x23, 0, 1, 2, 0)
        )
        state = run_hex_code(code, max_cycles=5)
        self.assertEqual(state["uart"], "HI")

if __name__ == "__main__":
    unittest.main()
