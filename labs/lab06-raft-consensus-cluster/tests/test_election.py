import unittest
from raft.state import RaftRole
from raft.network import SimulatedNetwork
from raft.node import RaftNode

class TestRaftElection(unittest.TestCase):
    def test_single_node_election(self):
        net = SimulatedNetwork()
        node = RaftNode(1, [], net)
        won = node.start_election()
        self.assertTrue(won)
        self.assertEqual(node.role, RaftRole.LEADER)
        self.assertEqual(node.current_term, 1)

    def test_three_node_cluster_election(self):
        net = SimulatedNetwork()
        node1 = RaftNode(1, [2, 3], net)
        node2 = RaftNode(2, [1, 3], net)
        node3 = RaftNode(3, [1, 2], net)

        won = node1.start_election()
        self.assertTrue(won)
        self.assertEqual(node1.role, RaftRole.LEADER)
        self.assertEqual(node2.role, RaftRole.FOLLOWER)
        self.assertEqual(node3.role, RaftRole.FOLLOWER)
        self.assertEqual(node2.current_term, 1)
        self.assertEqual(node3.current_term, 1)

if __name__ == "__main__":
    unittest.main()
