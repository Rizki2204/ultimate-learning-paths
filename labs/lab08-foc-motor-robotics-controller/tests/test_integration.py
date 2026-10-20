import unittest
import subprocess
from tests.test_clarke_park import EXE_PATH, PROJECT_DIR, ensure_compiled

class TestFOCSimulation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ensure_compiled()

    def test_closed_loop_torque_convergence(self):
        res = subprocess.run([EXE_PATH, "--test-sim"], cwd=PROJECT_DIR, capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)
        self.assertIn("PASS", res.stdout)

if __name__ == "__main__":
    unittest.main()
