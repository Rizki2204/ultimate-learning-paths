import unittest
import subprocess
from tests.test_memory_pool import EXE_PATH, PROJECT_DIR, ensure_compiled

class TestOrderMatching(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ensure_compiled()

    def test_fifo_price_time_priority(self):
        res = subprocess.run([EXE_PATH, "--test-matching"], cwd=PROJECT_DIR, capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)
        self.assertIn("PASS", res.stdout)

if __name__ == "__main__":
    unittest.main()
