import unittest
import subprocess
import json
import os
from tests.test_lexer import EXE_PATH, PROJECT_DIR, ensure_compiled

def eval_code(code_str):
    ensure_compiled()
    res = subprocess.run([EXE_PATH, "--eval", code_str], cwd=PROJECT_DIR, capture_output=True, text=True)
    return res.returncode, json.loads(res.stdout)

class TestParser(unittest.TestCase):
    def test_precedence_multiplication_over_addition(self):
        code, out = eval_code("2 + 3 * 4;")
        self.assertEqual(code, 0)
        self.assertEqual(out["result"], 14.0)

    def test_parentheses_override_precedence(self):
        code, out = eval_code("(2 + 3) * 4;")
        self.assertEqual(code, 0)
        self.assertEqual(out["result"], 20.0)

    def test_comparisons_and_equality(self):
        code, out = eval_code("10 > 5;")
        self.assertEqual(code, 0)
        self.assertEqual(out["result"], 1.0)

        code, out = eval_code("10 == 20;")
        self.assertEqual(code, 0)
        self.assertEqual(out["result"], 0.0)

if __name__ == "__main__":
    unittest.main()
