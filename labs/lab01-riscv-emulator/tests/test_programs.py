import unittest
from tests.riscv_helpers import r_type, i_type, b_type, u_type, s_type, j_type, run_hex_code

class TestCompletePrograms(unittest.TestCase):
    def test_fibonacci_iterative(self):
        """
        Compute 10th Fibonacci number:
        x1 = 0 (prev)
        x2 = 1 (curr)
        x3 = 1 (counter)
        x4 = 10 (target)
        loop:
          bge x3, x4, done (+16)
          add x5, x1, x2
          add x1, x0, x2
          add x2, x0, x5
          addi x3, x3, 1
          jal x0, loop (-20)
        done:
        """
        code = (
            i_type(0x13, 1, 0, 0, 0) +          # 0x00: x1 = 0
            i_type(0x13, 2, 0, 0, 1) +          # 0x04: x2 = 1
            i_type(0x13, 3, 0, 0, 1) +          # 0x08: x3 = 1
            i_type(0x13, 4, 0, 0, 10) +         # 0x0C: x4 = 10
            # loop at 0x10:
            b_type(0x63, 5, 3, 4, 24) +         # 0x10: bge x3, x4, done (target 0x28 -> +24)
            r_type(0x33, 5, 0, 1, 2, 0x00) +    # 0x14: add x5, x1, x2
            r_type(0x33, 1, 0, 2, 0, 0x00) +    # 0x18: add x1, x2, x0
            r_type(0x33, 2, 0, 5, 0, 0x00) +    # 0x1C: add x2, x5, x0
            i_type(0x13, 3, 0, 3, 1) +          # 0x20: addi x3, x3, 1
            j_type(0x6F, 0, -20) +              # 0x24: jal x0, loop (0x24 - 20 = 0x10)
            # done at 0x28:
            i_type(0x13, 6, 0, 0, 1)            # 0x28: addi x6, x0, 1 (marker)
        )
        state = run_hex_code(code, max_cycles=200)
        self.assertEqual(state["regs"][5], 55)
        self.assertEqual(state["regs"][6], 1)

    def test_euclidean_gcd(self):
        """
        Compute GCD of 48 and 18:
        x1 = 48
        x2 = 18
        loop:
          beq x2, x0, done (+28)
          blt x1, x2, swap (+12)
          sub x1, x1, x2
          jal x0, loop (-12)
        swap:
          add x3, x0, x1
          add x1, x0, x2
          add x2, x0, x3
          jal x0, loop (-24)
        done:
        """
        code = (
            i_type(0x13, 1, 0, 0, 48) +        # 0x00: x1 = 48
            i_type(0x13, 2, 0, 0, 18) +        # 0x04: x2 = 18
            # loop at 0x08:
            b_type(0x63, 0, 2, 0, 32) +        # 0x08: beq x2, x0, done (0x08 + 32 = 0x28)
            b_type(0x63, 4, 1, 2, 12) +        # 0x0C: blt x1, x2, swap (0x0C + 12 = 0x18)
            r_type(0x33, 1, 0, 1, 2, 0x20) +   # 0x10: sub x1, x1, x2
            j_type(0x6F, 0, -12) +             # 0x14: jal x0, loop (0x14 - 12 = 0x08)
            # swap at 0x18:
            r_type(0x33, 3, 0, 1, 0, 0x00) +   # 0x18: add x3, x1, x0
            r_type(0x33, 1, 0, 2, 0, 0x00) +   # 0x1C: add x1, x2, x0
            r_type(0x33, 2, 0, 3, 0, 0x00) +   # 0x20: add x2, x3, x0
            j_type(0x6F, 0, -24) +             # 0x24: jal x0, loop (0x24 - 24 = 0x08)
            # done at 0x28:
            i_type(0x13, 4, 0, 0, 1)           # 0x28: addi x4, x0, 1
        )
        state = run_hex_code(code, max_cycles=100)
        self.assertEqual(state["regs"][1], 6)

    def test_uart_banner_program(self):
        """
        Outputs 'RV32' to UART at 0x10000000.
        """
        banner = b"RV32"
        code = u_type(0x37, 1, 0x10000000)     # LUI x1, 0x10000000
        for char in banner:
            code += i_type(0x13, 2, 0, 0, char) # ADDI x2, x0, char
            code += s_type(0x23, 0, 1, 2, 0)    # SB x2, 0(x1)

        state = run_hex_code(code, max_cycles=20)
        self.assertEqual(state["uart"], "RV32")

if __name__ == "__main__":
    unittest.main()
