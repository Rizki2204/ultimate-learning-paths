import unittest
import subprocess
import os

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXE_PATH = os.path.join(PROJECT_DIR, "mini_kernel.exe" if os.name == "nt" else "mini_kernel")

class TestTwoLevelPagingMmu(unittest.TestCase):
    def test_mmu_translation_and_privileges(self):
        res = subprocess.run([EXE_PATH, "--test-mmu"], cwd=PROJECT_DIR, capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)
        self.assertIn("PASS", res.stdout)

if __name__ == "__main__":
    unittest.main()
