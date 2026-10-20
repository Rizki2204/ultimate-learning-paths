import unittest
from raft.state import RaftRole
from raft.network import SimulatedNetwork
from raft.node import RaftNode

class TestRaftReplication(unittest.TestCase):
    def test_log_replication_across_quorum(self):
        net = SimulatedNetwork()
        node1 = RaftNode(1, [2, 3], net)
        node2 = RaftNode(2, [1, 3], net)
        node3 = RaftNode(3, [1, 2], net)

        # Node 1 becomes leader
        node1.start_election()
        self.assertEqual(node1.role, RaftRole.LEADER)

        # Propose commands
        committed1 = node1.propose({"type": "SET", "key": "x", "val": 10})
        committed2 = node1.propose({"type": "SET", "key": "y", "val": 20})

        self.assertTrue(committed1)
        self.assertTrue(committed2)

        # Check that follower logs and state machines have caught up
        self.assertEqual(node1.commit_index, 2)
        self.assertEqual(node2.commit_index, 2)
        self.assertEqual(node3.commit_index, 2)

        self.assertEqual(node1.state_machine, [{"type": "SET", "key": "x", "val": 10},
                                               {"type": "SET", "key": "y", "val": 20}])
        self.assertEqual(node2.state_machine, node1.state_machine)
        self.assertEqual(node3.state_machine, node1.state_machine)

if __name__ == "__main__":
    unittest.main()
