from dataclasses import dataclass, field
from typing import List
from raft.state import LogEntry

@dataclass
class RequestVoteArgs:
    term: int
    candidate_id: int
    last_log_index: int
    last_log_term: int

@dataclass
class RequestVoteReply:
    term: int
    vote_granted: bool

@dataclass
class AppendEntriesArgs:
    term: int
    leader_id: int
    prev_log_index: int
    prev_log_term: int
    entries: List[LogEntry] = field(default_factory=list)
    leader_commit: int = 0

@dataclass
class AppendEntriesReply:
    term: int
    success: bool
    match_index: int = 0
