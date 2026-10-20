import unittest
import subprocess
from tests.test_memory_pool import EXE_PATH, PROJECT_DIR, ensure_compiled

class TestOrderBook(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ensure_compiled()

    def test_ring_buffer_operations(self):
        res = subprocess.run([EXE_PATH, "--test-ring"], cwd=PROJECT_DIR, capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)
        self.assertIn("PASS", res.stdout)

if __name__ == "__main__":
    unittest.main()
