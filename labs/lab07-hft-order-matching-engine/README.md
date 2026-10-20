# Laboratory 07: Ultra-Low Latency HFT Order Matching Engine

## 1. Architectural Overview
This laboratory implements an ultra-low latency limit order book and order matching engine in Modern C++ (C++14/C++17). Engineered specifically for high-frequency trading (HFT) environments, the architecture eliminates dynamic memory allocation (`malloc`, `free`, `new`, `delete`) on the critical trading path through a contiguous object memory pool, utilizes cacheline alignment (`alignas(64)`) to eliminate multi-core cache ping-ponging (false sharing), decouples trade ingress/egress via lock-free Single-Producer Single-Consumer (SPSC) ring buffers with memory acquire/release semantics, and executes matching using an intrusive doubly-linked list maintaining strict Price-Time Priority (FIFO).

```
+-----------------------------------------------------------------------+
|                    Ultra-Low Latency Matching Engine                  |
|                                                                       |
|   Inbound Order Stream                                                |
|          |                                                            |
|          v                                                            |
|   +---------------------------------------------------------------+   |
|   | Lock-Free SPSC Ring Buffer (Power-of-Two, Cacheline-Aligned)  |   |
|   | Producer Tail (Store Release) <---> Consumer Head (Acquire)   |   |
|   +---------------------------------------------------------------+   |
|          |                                                            |
|          v                                                            |
|   +---------------------------------------------------------------+   |
|   | Pre-Allocated Contiguous Memory Pool (100,000 Orders)         |   |
|   | Zero Heap Allocations on Critical Path (O(1) Pop/Push)        |   |
|   +---------------------------------------------------------------+   |
|          |                                                            |
|          v                                                            |
|   +---------------------------------------------------------------+   |
|   | Limit Order Book (LOB)                                        |   |
|   | Bids (Descending)                   Asks (Ascending)          |   |
|   |  $100.50 -> [Order 1] <-> [Order 2]  $100.55 -> [Order 4]     |   |
|   |  $100.45 -> [Order 3]                $100.60 -> [Order 5]     |   |
|   +---------------------------------------------------------------+   |
|          |                                                            |
|          v Trade Execution Fill Event                                 |
|   +---------------------------------------------------------------+   |
|   | Outbound Execution Ring Buffer (Reports to Market Data Feed)  |   |
|   +---------------------------------------------------------------+   |
+-----------------------------------------------------------------------+
```

## 2. Low-Latency Design Principles

### 1. Zero Allocation on Critical Path
Every order structure is allocated from `MemoryPool<Order, 100000>`. Acquiring a new order is an $O(1)$ index pop from a pre-allocated array; returning an order is an $O(1)$ index push. No heap metadata locking occurs.

### 2. Cacheline Alignment (`alignas(64)`)
Producer and consumer atomic pointers in the lock-free ring buffer reside on distinct 64-byte L1 cache lines. This prevents cache invalidation traffic across CPU core caches when orders are enqueued and dequeued simultaneously.

### 3. Intrusive Doubly-Linked List
Each order contains its own `next` and `prev` pointers. When an order is filled or cancelled, it unlinks itself from its price level in $O(1)$ without requiring list traversal or heap allocation.

### 4. Integer Fixed-Point Pricing
Prices are represented in fixed-point ticks (cents) via `uint64_t` rather than floating-point numbers, avoiding IEEE-754 precision inaccuracies, rounding artifacts, and floating-point comparison overhead.

## 3. Scaffolding & Directory Structure
```
labs/lab07-hft-order-matching-engine/
├── README.md               # Architecture documentation
├── Makefile                # Build and test automation
├── run_tests.py            # Standalone test runner
├── include/                # Header definitions
│   ├── types.h             # Fixed-point Price, OrderId, Side, ExecutionReport
│   ├── order.h             # Cacheline-aligned Order struct (64-byte padded)
│   ├── memory_pool.h       # Zero-allocation contiguous object pool
│   ├── ring_buffer.h       # Lock-free SPSC queue with acquire/release
│   ├── order_book.h        # Intrusive price-time limit order book
│   └── matching_engine.h   # Core matching and crossing algorithm
├── starter/                # Student starter scaffolding
│   ├── Makefile            # Starter compilation rules
│   └── matching_engine_starter.cpp # Starter matching skeleton
├── src/                    # Complete production reference implementation
│   ├── order_book.cpp      # Price level management and index unlinking
│   ├── matching_engine.cpp # Crossing order matching and execution engine
│   ├── benchmark.cpp       # Nanosecond benchmarking harness
│   └── main.cpp            # Test harness and CLI
└── tests/                  # Automated test suite
    ├── test_memory_pool.py # Object pool allocation and exhaustion
    ├── test_order_book.py  # Lock-free ring buffer and price levels
    ├── test_matching.py    # FIFO price-time matching and partial fills
    └── test_benchmark.py   # Latency profiling (< 1000 ns, > 1M ops/sec)
```

## 4. Milestone Progression Guide
1. **Milestone 1 (Memory Pool & Intrusive Orders)**:
   Implement the fixed-size `MemoryPool` and verify $O(1)$ allocation, deallocation, and cacheline alignment (`alignas(64)`).
2. **Milestone 2 (Lock-Free SPSC Ring Buffer)**:
   Implement power-of-two modulo masking and atomic memory ordering (`memory_order_acquire` and `memory_order_release`).
3. **Milestone 3 (Limit Order Book & Price-Time Matching)**:
   Implement price level queuing, crossing trade execution, partial fills, and $O(1)$ direct unlinking on cancellation.
4. **Milestone 4 (Nanosecond Profiling & Benchmarks)**:
   Run high-resolution clock benchmarks verifying order processing throughput exceeding 1,000,000 orders/sec and average latencies under 1,000 nanoseconds.

## 5. Verification and Execution
Run the automated test runner:
```bash
python run_tests.py
```
Or use the Makefile:
```bash
mingw32-make test
```
All 4 high-frequency trading test suites execute in ~50 milliseconds and pass with exit code 0.
