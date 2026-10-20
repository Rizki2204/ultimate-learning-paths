import unittest
from raft.state import RaftRole
from raft.network import SimulatedNetwork
from raft.node import RaftNode

class TestRaftPartition(unittest.TestCase):
    def test_network_partition_and_reconvergence(self):
        net = SimulatedNetwork()
        peers = {
            1: [2, 3, 4, 5],
            2: [1, 3, 4, 5],
            3: [1, 2, 4, 5],
            4: [1, 2, 3, 5],
            5: [1, 2, 3, 4],
        }
        nodes = {i: RaftNode(i, peers[i], net) for i in range(1, 6)}

        # 1. Node 1 becomes leader
        nodes[1].start_election()
        self.assertEqual(nodes[1].role, RaftRole.LEADER)
        self.assertTrue(nodes[1].propose("initial_entry"))

        # 2. Partition cluster: [1, 2] vs [3, 4, 5]
        net.partition([1, 2], [3, 4, 5])

        # Node 1 in minority attempts to commit: must fail (quorum is 3/5)
        success = nodes[1].propose("minority_entry")
        self.assertFalse(success)

        # Node 3 in majority starts election: achieves quorum (nodes 3, 4, 5)
        won = nodes[3].start_election()
        self.assertTrue(won)
        self.assertEqual(nodes[3].role, RaftRole.LEADER)

        # Node 3 commits new entries successfully
        success_majority = nodes[3].propose("majority_entry")
        self.assertTrue(success_majority)

        # 3. Heal partition
        net.heal()
        nodes[3].broadcast_heartbeat()

        # Nodes 1 and 2 must step down and synchronize with Node 3
        self.assertEqual(nodes[1].role, RaftRole.FOLLOWER)
        self.assertEqual(nodes[2].role, RaftRole.FOLLOWER)
        self.assertEqual(nodes[1].current_term, nodes[3].current_term)
        self.assertIn("majority_entry", nodes[1].state_machine)

if __name__ == "__main__":
    unittest.main()
