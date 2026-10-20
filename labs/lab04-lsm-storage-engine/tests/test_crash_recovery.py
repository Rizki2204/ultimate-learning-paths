import unittest
import subprocess
from tests.test_wal import EXE_PATH, PROJECT_DIR, ensure_compiled

class TestCrashRecovery(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ensure_compiled()

    def test_wal_reconstruction(self):
        res = subprocess.run([EXE_PATH, "--test-wal"], cwd=PROJECT_DIR, capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)

if __name__ == "__main__":
    unittest.main()
