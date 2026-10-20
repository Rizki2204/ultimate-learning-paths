import unittest
import subprocess
import os

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXE_PATH = os.path.join(PROJECT_DIR, "hft_engine.exe" if os.name == "nt" else "hft_engine")

def ensure_compiled():
    if not os.path.exists(EXE_PATH):
        cmd = ["g++", "-Wall", "-Wextra", "-std=c++14", "-O3", "-Iinclude",
               "src/order_book.cpp", "src/matching_engine.cpp", "src/benchmark.cpp", "src/main.cpp",
               "-o", EXE_PATH]
        subprocess.check_call(cmd, cwd=PROJECT_DIR)

class TestMemoryPool(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ensure_compiled()

    def test_pool_allocation_and_free(self):
        res = subprocess.run([EXE_PATH, "--test-pool"], cwd=PROJECT_DIR, capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)
        self.assertIn("PASS", res.stdout)

if __name__ == "__main__":
    unittest.main()
