from raft.state import RaftRole, LogEntry
from raft.rpc import RequestVoteArgs, RequestVoteReply, AppendEntriesArgs, AppendEntriesReply

class RaftNode:
    def __init__(self, node_id, peers, network):
        self.node_id = node_id
        self.peers = list(peers)
        self.network = network
        self.network.register_node(node_id, self)

        # Persistent state
        self.current_term = 0
        self.voted_for = None
        self.log = [LogEntry(index=0, term=0, command=None)]

        # Volatile state
        self.role = RaftRole.FOLLOWER
        self.commit_index = 0
        self.last_applied = 0
        self.state_machine = []

        # Leader volatile state
        self.next_index = {}
        self.match_index = {}

    def last_log_index(self):
        return self.log[-1].index

    def last_log_term(self):
        return self.log[-1].term

    def apply_entries(self):
        while self.last_applied < self.commit_index:
            self.last_applied += 1
            cmd = self.log[self.last_applied].command
            if cmd is not None:
                self.state_machine.append(cmd)

    def start_election(self):
        self.current_term += 1
        self.role = RaftRole.CANDIDATE
        self.voted_for = self.node_id
        votes = 1

        args = RequestVoteArgs(
            term=self.current_term,
            candidate_id=self.node_id,
            last_log_index=self.last_log_index(),
            last_log_term=self.last_log_term()
        )

        for peer in self.peers:
            reply = self.network.send_request_vote(self.node_id, peer, args)
            if reply is not None:
                if reply.term > self.current_term:
                    self.current_term = reply.term
                    self.role = RaftRole.FOLLOWER
                    self.voted_for = None
                    return False
                if reply.vote_granted and self.role == RaftRole.CANDIDATE:
                    votes += 1

        quorum = (len(self.peers) + 1) // 2 + 1
        if votes >= quorum:
            self.role = RaftRole.LEADER
            self.next_index = {p: len(self.log) for p in self.peers}
            self.match_index = {p: 0 for p in self.peers}
            self.broadcast_heartbeat()
            return True

        return False

    def handle_request_vote(self, args: RequestVoteArgs) -> RequestVoteReply:
        if args.term > self.current_term:
            self.current_term = args.term
            self.role = RaftRole.FOLLOWER
            self.voted_for = None

        if args.term < self.current_term:
            return RequestVoteReply(term=self.current_term, vote_granted=False)

        # Log up-to-date check
        my_last_term = self.last_log_term()
        my_last_idx = self.last_log_index()

        candidate_up_to_date = (
            (args.last_log_term > my_last_term) or
            (args.last_log_term == my_last_term and args.last_log_index >= my_last_idx)
        )

        can_vote = (self.voted_for is None or self.voted_for == args.candidate_id) and candidate_up_to_date

        if can_vote:
            self.voted_for = args.candidate_id
            return RequestVoteReply(term=self.current_term, vote_granted=True)

        return RequestVoteReply(term=self.current_term, vote_granted=False)

    def handle_append_entries(self, args: AppendEntriesArgs) -> AppendEntriesReply:
        if args.term > self.current_term:
            self.current_term = args.term
            self.role = RaftRole.FOLLOWER
            self.voted_for = None

        if args.term < self.current_term:
            return AppendEntriesReply(term=self.current_term, success=False, match_index=0)

        if self.role == RaftRole.CANDIDATE and args.term == self.current_term:
            self.role = RaftRole.FOLLOWER

        # Log consistency check at prev_log_index
        if args.prev_log_index >= len(self.log) or self.log[args.prev_log_index].term != args.prev_log_term:
            return AppendEntriesReply(term=self.current_term, success=False, match_index=len(self.log) - 1)

        # Append new entries not already present
        insert_idx = args.prev_log_index + 1
        for entry in args.entries:
            if insert_idx < len(self.log):
                if self.log[insert_idx].term != entry.term:
                    self.log = self.log[:insert_idx]
                    self.log.append(entry)
            else:
                self.log.append(entry)
            insert_idx += 1

        # Advance commit index
        if args.leader_commit > self.commit_index:
            self.commit_index = min(args.leader_commit, len(self.log) - 1)
            self.apply_entries()

        return AppendEntriesReply(term=self.current_term, success=True, match_index=len(self.log) - 1)

    def broadcast_heartbeat(self):
        if self.role != RaftRole.LEADER:
            return
        self.replicate_log()

    def replicate_log(self):
        if self.role != RaftRole.LEADER:
            return

        for peer in self.peers:
            prev_idx = self.next_index[peer] - 1
            prev_term = self.log[prev_idx].term
            entries = self.log[self.next_index[peer]:]

            args = AppendEntriesArgs(
                term=self.current_term,
                leader_id=self.node_id,
                prev_log_index=prev_idx,
                prev_log_term=prev_term,
                entries=entries,
                leader_commit=self.commit_index
            )

            reply = self.network.send_append_entries(self.node_id, peer, args)
            if reply is not None:
                if reply.term > self.current_term:
                    self.current_term = reply.term
                    self.role = RaftRole.FOLLOWER
                    self.voted_for = None
                    return
                if reply.success:
                    self.match_index[peer] = reply.match_index
                    self.next_index[peer] = reply.match_index + 1
                else:
                    self.next_index[peer] = max(1, self.next_index[peer] - 1)

        # Check commit index advancement on majority quorum
        quorum = (len(self.peers) + 1) // 2 + 1
        old_commit = self.commit_index
        for N in range(len(self.log) - 1, self.commit_index, -1):
            if self.log[N].term == self.current_term:
                count = 1  # leader itself
                for peer in self.peers:
                    if self.match_index[peer] >= N:
                        count += 1
                if count >= quorum:
                    self.commit_index = N
                    self.apply_entries()
                    break

        if self.commit_index > old_commit:
            for peer in self.peers:
                prev_idx = self.match_index[peer]
                prev_term = self.log[prev_idx].term
                args = AppendEntriesArgs(
                    term=self.current_term,
                    leader_id=self.node_id,
                    prev_log_index=prev_idx,
                    prev_log_term=prev_term,
                    entries=[],
                    leader_commit=self.commit_index
                )
                self.network.send_append_entries(self.node_id, peer, args)

    def propose(self, command):
        """Client command proposal. Returns True if successfully committed."""
        if self.role != RaftRole.LEADER:
            return False

        entry = LogEntry(index=len(self.log), term=self.current_term, command=command)
        self.log.append(entry)
        self.replicate_log()

        return self.commit_index >= entry.index
