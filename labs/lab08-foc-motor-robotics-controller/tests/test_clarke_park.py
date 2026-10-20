import unittest
import subprocess
import os

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXE_PATH = os.path.join(PROJECT_DIR, "foc_controller.exe" if os.name == "nt" else "foc_controller")

def ensure_compiled():
    if not os.path.exists(EXE_PATH):
        cmd = ["gcc", "-Wall", "-Wextra", "-std=c99", "-O2", "-Iinclude",
               "src/foc_math.c", "src/pi_controller.c", "src/svpwm.c", "src/kinematics.c",
               "src/simulation.c", "src/main.c", "-o", EXE_PATH, "-lm"]
        subprocess.check_call(cmd, cwd=PROJECT_DIR)

class TestClarkePark(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ensure_compiled()

    def test_clarke_and_park_transforms(self):
        res = subprocess.run([EXE_PATH, "--test-clarke-park"], cwd=PROJECT_DIR, capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)
        self.assertIn("PASS", res.stdout)

if __name__ == "__main__":
    unittest.main()
