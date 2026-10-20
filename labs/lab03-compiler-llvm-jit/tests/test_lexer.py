import unittest
import subprocess
import os

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXE_PATH = os.path.join(PROJECT_DIR, "minilang_compiler.exe" if os.name == "nt" else "minilang_compiler")

def ensure_compiled():
    if not os.path.exists(EXE_PATH):
        cmd = ["g++", "-Wall", "-Wextra", "-std=c++14", "-O2", "-Iinclude",
               "src/lexer.cpp", "src/parser.cpp", "src/bytecode.cpp", "src/vm.cpp", "src/main.cpp",
               "-o", EXE_PATH]
        subprocess.check_call(cmd, cwd=PROJECT_DIR)

class TestLexer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ensure_compiled()

    def test_lexer_tokenization(self):
        res = subprocess.run([EXE_PATH, "--test-lexer"], cwd=PROJECT_DIR, capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)
        self.assertIn("PASS", res.stdout)

if __name__ == "__main__":
    unittest.main()
