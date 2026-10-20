"""
Starter Scaffolding: Raft Distributed Consensus Node

Exercise Instructions:
Implement Raft state transitions, election timer handling,
and RequestVote RPC logic.
"""

from enum import Enum

class StarterRole(Enum):
    FOLLOWER = "Follower"
    CANDIDATE = "Candidate"
    LEADER = "Leader"

class StarterRaftNode:
    def __init__(self, node_id, peers):
        self.node_id = node_id
        self.peers = list(peers)
        self.current_term = 0
        self.voted_for = None
        self.role = StarterRole.FOLLOWER
        self.votes = 0

    def start_election(self):
        """
        Exercise: Candidate Transition and Vote Solicitation
        Increment term, become candidate, vote for self.
        """
        self.current_term += 1
        self.role = StarterRole.CANDIDATE
        self.voted_for = self.node_id
        self.votes = 1

    def receive_vote(self):
        self.votes += 1
        quorum = (len(self.peers) + 1) // 2 + 1
        if self.votes >= quorum:
            self.role = StarterRole.LEADER
            return True
        return False

if __name__ == "__main__":
    node = StarterRaftNode(1, [2, 3])
    node.start_election()
    print(f"Node {node.node_id} started election in term {node.current_term} as {node.role.value}")
    if node.receive_vote():
        print(f"Node {node.node_id} achieved quorum and became {node.role.value}")
