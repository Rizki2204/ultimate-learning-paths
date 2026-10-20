import unittest
from raft.state import RaftRole
from raft.network import SimulatedNetwork
from raft.node import RaftNode

class TestRaftLinearizability(unittest.TestCase):
    def test_sequential_state_machine_execution(self):
        net = SimulatedNetwork()
        node1 = RaftNode(1, [2, 3], net)
        node2 = RaftNode(2, [1, 3], net)
        node3 = RaftNode(3, [1, 2], net)

        node1.start_election()
        commands = [f"cmd_{i}" for i in range(10)]
        for cmd in commands:
            self.assertTrue(node1.propose(cmd))

        # Assert all 3 nodes have executed identical sequences
        self.assertEqual(node1.state_machine, commands)
        self.assertEqual(node2.state_machine, commands)
        self.assertEqual(node3.state_machine, commands)

if __name__ == "__main__":
    unittest.main()
