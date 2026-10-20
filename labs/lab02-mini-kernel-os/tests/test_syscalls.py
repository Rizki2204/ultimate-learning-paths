import unittest
import subprocess
import os

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXE_PATH = os.path.join(PROJECT_DIR, "mini_kernel.exe" if os.name == "nt" else "mini_kernel")

def ensure_compiled():
    if not os.path.exists(EXE_PATH):
        cmd = ["gcc", "-Wall", "-Wextra", "-std=c99", "-O2", "-Iinclude",
               "src/palloc.c", "src/mmu.c", "src/sched.c", "src/syscall.c", "src/kernel.c", "src/main.c",
               "-o", EXE_PATH]
        subprocess.check_call(cmd, cwd=PROJECT_DIR)

class TestSyscallSubsystem(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ensure_compiled()

    def test_syscall_dispatch(self):
        res = subprocess.run([EXE_PATH, "--test-syscall"], cwd=PROJECT_DIR, capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)
        self.assertIn("PASS", res.stdout)

if __name__ == "__main__":
    unittest.main()
