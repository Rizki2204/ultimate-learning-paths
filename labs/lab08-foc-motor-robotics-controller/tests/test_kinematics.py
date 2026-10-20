import unittest
import subprocess
from tests.test_clarke_park import EXE_PATH, PROJECT_DIR, ensure_compiled

class TestKinematics(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ensure_compiled()

    def test_2dof_forward_and_inverse_kinematics(self):
        res = subprocess.run([EXE_PATH, "--test-kinematics"], cwd=PROJECT_DIR, capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)
        self.assertIn("PASS", res.stdout)

if __name__ == "__main__":
    unittest.main()
