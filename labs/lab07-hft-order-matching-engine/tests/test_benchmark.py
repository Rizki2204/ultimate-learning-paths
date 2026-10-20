import unittest
import subprocess
import json
from tests.test_memory_pool import EXE_PATH, PROJECT_DIR, ensure_compiled

class TestBenchmark(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ensure_compiled()

    def test_latency_and_throughput(self):
        res = subprocess.run([EXE_PATH, "--benchmark"], cwd=PROJECT_DIR, capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)
        data = json.loads(res.stdout)
        stats = data["benchmark"]

        # Assert sub-microsecond average latency (< 1000 ns)
        self.assertLess(stats["avg_latency_ns"], 1000.0)
        # Assert throughput exceeding 1,000,000 orders per second
        self.assertGreater(stats["throughput_ops"], 1_000_000.0)

if __name__ == "__main__":
    unittest.main()
