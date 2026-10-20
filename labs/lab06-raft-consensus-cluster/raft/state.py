from enum import Enum
from dataclasses import dataclass
from typing import Any

class RaftRole(Enum):
    FOLLOWER = "Follower"
    CANDIDATE = "Candidate"
    LEADER = "Leader"

@dataclass
class LogEntry:
    index: int
    term: int
    command: Any
