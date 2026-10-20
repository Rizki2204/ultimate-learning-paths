import unittest
import subprocess
import os

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXE_PATH = os.path.join(PROJECT_DIR, "lsm_engine.exe" if os.name == "nt" else "lsm_engine")

def ensure_compiled():
    if not os.path.exists(EXE_PATH):
        cmd = ["g++", "-Wall", "-Wextra", "-std=c++14", "-O2", "-Iinclude",
               "src/wal.cpp", "src/memtable.cpp", "src/bloom.cpp", "src/sstable.cpp",
               "src/compaction.cpp", "src/lsm_engine.cpp", "src/main.cpp", "-o", EXE_PATH]
        subprocess.check_call(cmd, cwd=PROJECT_DIR)

class TestWriteAheadLog(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ensure_compiled()

    def test_wal_operations(self):
        res = subprocess.run([EXE_PATH, "--test-wal"], cwd=PROJECT_DIR, capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)
        self.assertIn("PASS", res.stdout)

if __name__ == "__main__":
    unittest.main()
