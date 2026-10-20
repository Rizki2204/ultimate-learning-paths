import unittest
import sys
import os

def run_all_tests():
    lab_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(lab_dir)

    from tests.test_memory_pool import ensure_compiled
    ensure_compiled()

    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=os.path.join(lab_dir, "tests"), pattern="test_*.py")
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)

if __name__ == "__main__":
    run_all_tests()
