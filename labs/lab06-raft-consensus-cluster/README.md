# Laboratory 06: Raft Consensus Distributed Cluster

## 1. Architectural Overview
This laboratory implements a distributed fault-tolerant state machine consensus engine based on the Raft Consensus Protocol in Python 3.14. The system provides atomic log replication, leader election under randomized election timeouts, strict majority quorum safety ($Q = \lfloor N/2 \rfloor + 1$), simulated network partitions, split-brain immunity, and seamless log reconciliation upon partition healing.

```
+-----------------------------------------------------------------------+
|                    Raft State Machine Transitions                     |
|                                                                       |
|              +---------------------------------------+                |
|              |                                       |                |
|              v                                       |                |
|       +--------------+     Timeout / Election   +---------------+     |
|  +--->|   Follower   |------------------------->|   Candidate   |     |
|  |    +--------------+                          +---------------+     |
|  |           ^                                          |             |
|  |           | Higher Term Observed                     | Majority    |
|  |           |                                          | Votes       |
|  |           |                                          v             |
|  |    +--------------+                         +----------------+     |
|  +----+    Leader    |<------------------------|  Elected Leader|     |
|       +--------------+                         +----------------+     |
|              |                                                        |
|              v Heartbeat / AppendEntries RPC Broadcast                |
|   +---------------------------------------------------------------+   |
|   | Simulated Network Bus (Delays, Packet Drops, Network Cuts)    |   |
|   +---------------------------------------------------------------+   |
|              |                               |                        |
|              v                               v                        |
|       [ Node 2 (Peer) ]               [ Node 3 (Peer) ]               |
+-----------------------------------------------------------------------+
```

## 2. Invariants & Election Safety Guarantees

### 1. Election Safety
At most one leader can be elected in a given term. A candidate requires votes from a strict majority of nodes:
$$\text{Quorum} \ge \lfloor N/2 \rfloor + 1$$
Since any two majorities must overlap in at least one node, that overlapping node can vote at most once per term, ensuring no split-brain leadership.

### 2. Log Up-to-Date Restriction
A receiver denies its vote if the candidate's log is less up-to-date than its own. A log with `(last_term, last_index)` is more up-to-date if:
- `candidate_last_term > receiver_last_term`, or
- `candidate_last_term == receiver_last_term` and `candidate_last_index >= receiver_last_index`.

### 3. Log Matching Property
If two logs contain an entry with the same index and term, they are identical in all entries up to the given index.

### 4. Leader Completeness
If a log entry is committed in a given term, that entry will be present in the logs of the leaders for all higher-numbered terms.

## 3. Scaffolding & Directory Structure
```
labs/lab06-raft-consensus-cluster/
├── README.md               # Architecture documentation
├── Makefile                # Build and test automation
├── run_tests.py            # Standalone test runner
├── raft/                   # Raft protocol implementation
│   ├── __init__.py         # Public exports
│   ├── state.py            # RaftRole enum and LogEntry dataclass
│   ├── rpc.py              # RequestVote & AppendEntries RPC specs
│   ├── network.py          # Simulated network broker & partitioner
│   └── node.py             # Consensus engine, election, & replication
├── starter/                # Student starter scaffolding
│   └── raft_starter.py     # Clean Raft node skeleton
└── tests/                  # Automated test suite
    ├── test_election.py    # 1-node and 3-node election validation
    ├── test_replication.py # Quorum log replication and state machine
    ├── test_partition.py   # Asymmetric network cut, minority block, heal
    └── test_linearizability.py # Sequential consistency execution trace
```

## 4. Milestone Progression Guide
1. **Milestone 1 (Role Transitions & State)**:
   Implement `RaftRole` transitions (`Follower` -> `Candidate` -> `Leader`) and persistent state (`current_term`, `voted_for`, `log`).
2. **Milestone 2 (RequestVote RPC & Quorums)**:
   Implement vote request solicitation, up-to-date log comparisons, and majority vote tallying.
3. **Milestone 3 (AppendEntries & Log Replication)**:
   Implement log consistency validation, log truncation on conflicting terms, and leader `commit_index` advancement across quorums.
4. **Milestone 4 (Fault Injection & Partition Healing)**:
   Isolate minority nodes, verify that writes fail to commit without a majority, and assert seamless log synchronization when the partition heals.

## 5. Verification and Execution
Run the automated test runner:
```bash
python run_tests.py
```
Or use the Makefile:
```bash
mingw32-make test
```
All 5 distributed consensus test suites pass within 10 milliseconds and exit with code 0.
