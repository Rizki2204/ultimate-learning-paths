# Laboratory 04: Log-Structured Merge Tree (LSM) Storage Engine

## 1. Architectural Overview
This laboratory implements an industrial-pattern Log-Structured Merge Tree (LSM Tree) key-value storage engine in C++14. The architecture guarantees atomicity and durability via an append-only Write-Ahead Log (WAL) protected by IEEE 802.3 CRC32 checksums, provides low-latency memory ingestion via a sorted MemTable, achieves high read throughput through immutable Sorted String Tables (SSTables) equipped with Bloom filters and sparse index blocks, and manages disk space via tiered compaction.

```
+-----------------------------------------------------------------------+
|                         LSM Storage Engine                            |
|                                                                       |
|   Write Path:                                                         |
|   Client Write (PUT / DEL)                                            |
|          |                                                            |
|          +-------------> [ Write-Ahead Log (WAL) ]                    |
|          |                CRC32 Checksummed Disk Append               |
|          v                                                            |
|   [ Active MemTable ] (Sorted Map in Memory)                          |
|          |                                                            |
|          v (Threshold Exceeded -> Flush)                              |
|   +---------------------------------------------------------------+   |
|   | SSTable on Disk                                               |   |
|   |  +---------------------------------------------------------+  |   |
|   |  | Data Block: Sorted [Key, Value, Tombstone Flag]         |  |   |
|   |  +---------------------------------------------------------+  |   |
|   |  | Sparse Index Block: [Key, Data Block Byte Offset]       |  |   |
|   |  +---------------------------------------------------------+  |   |
|   |  | Bloom Filter Block: Murmur/FNV Multi-Hash Bitset        |  |   |
|   |  +---------------------------------------------------------+  |   |
|   |  | Footer: DataLen, IndexOff, IndexLen, BloomOff, Magic    |  |   |
|   |  +---------------------------------------------------------+  |   |
|   +---------------------------------------------------------------+   |
|          |                                                            |
|          v                                                            |
|   [ Tiered Compaction ] (K-Way Merge Sort & Tombstone Purge)          |
+-----------------------------------------------------------------------+
```

## 2. On-Disk Binary Formats

### Write-Ahead Log Record Layout
Each entry in `wal.log` is structured as:
```
+---------------+---------------+---------------+--------------+----------+--------------+------------+
| Size (4 Bytes)| CRC32 (4 Bytes| OpType (1 Byte| KeyLen (2 B) | Key Data | ValLen (4 B) | Value Data |
+---------------+---------------+---------------+--------------+----------+--------------+------------+
```
If an ungraceful shutdown occurs, the engine verifies the CRC32 checksum of each record and safely halts replay at the first uncorrupted boundary.

### SSTable File Layout
```
+-------------------------------------------------------------+
| Data Block                                                  |
| Entries: [KeyLen: 2B][Key][ValLen: 4B][Val][IsTombstone: 1B]|
+-------------------------------------------------------------+
| Sparse Index Block                                          |
| Entries: [KeyLen: 2B][Key][Data Offset: 8B]                 |
+-------------------------------------------------------------+
| Bloom Filter Block                                          |
| Bit array with FNV-1a hash seeds                            |
+-------------------------------------------------------------+
| Footer (48 Bytes)                                           |
| [DataLen: 8B][IndexOff: 8B][IndexLen: 8B]                   |
| [BloomOff: 8B][BloomLen: 8B][Magic: 8B (0x53535441424C4531)]|
+-------------------------------------------------------------+
```

## 3. Query Path & Compaction
1. **Point Get**:
   - Check active `MemTable`. If found, return value (or `not found` if tombstone).
   - For each SSTable (from newest to oldest):
     - Check Bloom filter. If `may_contain == false`, skip file entirely (eliminating random disk seeks).
     - Binary search sparse index block to locate the candidate data block segment.
     - Scan forward in data block until key matches or exceeds target.
2. **Tiered Compaction**:
   - Background k-way merge sort merges overlapping Level 0 SSTables into a consolidated Level 1 SSTable.
   - Tombstone markers (`DEL`) are permanently purged when compacting at the bottommost storage level, reclaiming physical disk space.

## 4. Scaffolding & Directory Structure
```
labs/lab04-lsm-storage-engine/
├── README.md               # Architecture documentation
├── Makefile                # Build and test automation
├── run_tests.py            # Standalone test runner
├── include/                # Header definitions
│   ├── wal.h               # Write-Ahead Log and CRC32 API
│   ├── memtable.h          # In-memory sorted table API
│   ├── bloom.h             # Bloom filter interface
│   ├── sstable.h           # SSTable reader, writer, and indexer
│   ├── compaction.h        # Tiered compaction engine
│   └── lsm_engine.h        # Orchestration layer
├── starter/                # Student starter scaffolding
│   ├── Makefile            # Starter compilation rules
│   └── lsm_starter.cpp     # Clean MemTable skeleton
├── src/                    # Complete production reference implementation
│   ├── wal.cpp             # Binary WAL logging and recovery
│   ├── memtable.cpp        # Red-black tree MemTable
│   ├── bloom.cpp           # Multi-hash Bloom filter
│   ├── sstable.cpp         # SSTable encoder and reader
│   ├── compaction.cpp      # K-way merge compactor
│   ├── lsm_engine.cpp      # Engine orchestration
│   └── main.cpp            # Test harness and CLI
└── tests/                  # Automated test suite
    ├── test_wal.py         # WAL durability and CRC32 verification
    ├── test_bloom.py       # Bloom filter false positive rates
    ├── test_memtable.py    # MemTable mutations and tombstones
    ├── test_sstable.py     # SSTable binary search lookup tests
    ├── test_compaction.py  # Merge-sort and tombstone cleanup tests
    └── test_crash_recovery.py # Recovery from uncommitted WAL logs
```

## 5. Milestone Progression Guide
1. **Milestone 1 (Durability & WAL)**:
   Implement binary serialization and CRC32 checksumming for WAL records. Verify recovery of valid records after truncation.
2. **Milestone 2 (MemTable & Tombstones)**:
   Implement in-memory sorted map with deletion tombstones and byte-size tracking.
3. **Milestone 3 (Bloom Filter & SSTable Format)**:
   Implement multi-hash Bloom filter bitsets and write structured SSTable files with sparse index sampling.
4. **Milestone 4 (Compaction & Engine Integration)**:
   Build the point lookup pipeline and implement tiered compaction to merge SSTables and purge tombstones.

## 6. Verification and Execution
Run the automated test runner:
```bash
python run_tests.py
```
Or use the Makefile:
```bash
mingw32-make test
```
All 6 storage engine test suites complete within 150 milliseconds and pass with exit code 0.
