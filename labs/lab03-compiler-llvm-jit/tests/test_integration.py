import unittest
from tests.test_parser import eval_code

class TestIntegrationPrograms(unittest.TestCase):
    def test_fibonacci_loop(self):
        program = """
        let a = 0;
        let b = 1;
        let count = 1;
        while (count < 10) {
            let next = a + b;
            a = b;
            b = next;
            count = count + 1;
        }
        b;
        """
        code, out = eval_code(program)
        self.assertEqual(code, 0)
        self.assertEqual(out["result"], 55.0)

    def test_factorial_loop(self):
        program = """
        let n = 5;
        let fact = 1;
        while (n > 1) {
            fact = fact * n;
            n = n - 1;
        }
        fact;
        """
        code, out = eval_code(program)
        self.assertEqual(code, 0)
        self.assertEqual(out["result"], 120.0)

    def test_compound_nested_math(self):
        program = """
        let x = 10;
        let y = 20;
        let z = (x * 2 + y / 4) - 5;
        z;
        """
        code, out = eval_code(program)
        self.assertEqual(code, 0)
        # z = (20 + 5) - 5 = 20
        self.assertEqual(out["result"], 20.0)

if __name__ == "__main__":
    unittest.main()
