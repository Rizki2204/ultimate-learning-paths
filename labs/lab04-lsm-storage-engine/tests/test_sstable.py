import unittest
import subprocess
from tests.test_wal import EXE_PATH, PROJECT_DIR, ensure_compiled

class TestSSTable(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ensure_compiled()

    def test_sstable_creation_and_binary_search(self):
        res = subprocess.run([EXE_PATH, "--test-sstable"], cwd=PROJECT_DIR, capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)
        self.assertIn("PASS", res.stdout)

if __name__ == "__main__":
    unittest.main()
