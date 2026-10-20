import unittest
from tests.test_parser import eval_code

class TestVirtualMachine(unittest.TestCase):
    def test_variable_declaration_and_math(self):
        code, out = eval_code("let a = 15; let b = 4; a - b;")
        self.assertEqual(code, 0)
        self.assertEqual(out["result"], 11.0)

    def test_if_else_branches(self):
        code, out = eval_code("let x = 7; if (x > 5) 100; else 200;")
        self.assertEqual(code, 0)
        self.assertEqual(out["result"], 100.0)

        code, out = eval_code("let x = 3; if (x > 5) 100; else 200;")
        self.assertEqual(code, 0)
        self.assertEqual(out["result"], 200.0)

    def test_division_by_zero_error(self):
        code, out = eval_code("10 / 0;")
        self.assertNotEqual(code, 0)
        self.assertEqual(out["status"], "RUNTIME_ERROR")

if __name__ == "__main__":
    unittest.main()
