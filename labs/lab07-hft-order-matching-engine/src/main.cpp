#include <iostream>
#include <string>
#include <cstring>
#include "matching_engine.h"

int run_benchmark(size_t num_orders);

static int test_pool() {
    MemoryPool<Order, 16> pool;
    if (pool.allocated_count() != 0) return 1;
    if (pool.available_count() != 16) return 2;

    std::vector<Order *> allocated;
    for (int i = 0; i < 16; ++i) {
        Order *o = pool.allocate();
        if (!o) return 3;
        allocated.push_back(o);
    }

    if (pool.allocate() != nullptr) return 4; /* Should be exhausted */

    for (Order *o : allocated) {
        pool.deallocate(o);
    }
    if (pool.allocated_count() != 0) return 5;
    return 0;
}

static int test_ring() {
    SPSCRingBuffer<int, 8> ring;
    if (!ring.empty()) return 1;

    for (int i = 1; i <= 7; ++i) {
        if (!ring.push(i)) return 2;
    }
    if (ring.size() != 7) return 3;

    int val = 0;
    for (int i = 1; i <= 7; ++i) {
        if (!ring.pop(val) || val != i) return 4;
    }
    if (!ring.empty()) return 5;
    return 0;
}

static int test_matching() {
    MatchingEngine engine;

    /* Resting sell order: ID 1, SELL, 100 shares at $10.50 (1050 ticks) */
    if (!engine.submit_order(1, Side::SELL, OrderType::LIMIT, 1050, 100)) return 1;
    if (engine.best_ask() != 1050) return 2;
    if (engine.order_count() != 1) return 3;

    /* Resting sell order: ID 2, SELL, 50 shares at $10.50 (FIFO queue behind ID 1) */
    if (!engine.submit_order(2, Side::SELL, OrderType::LIMIT, 1050, 50)) return 4;

    /* Incoming buy order: ID 3, BUY, 120 shares at $10.50 */
    /* Should fully fill ID 1 (100 shares), partially fill ID 2 (20 shares), leave ID 2 with 30 shares */
    if (!engine.submit_order(3, Side::BUY, OrderType::LIMIT, 1050, 120)) return 5;

    auto execs = engine.drain_executions();
    if (execs.size() != 2) return 6;

    if (execs[0].maker_order_id != 1 || execs[0].trade_quantity != 100) return 7;
    if (execs[1].maker_order_id != 2 || execs[1].trade_quantity != 20) return 8;

    /* ID 2 should still be in the book with remaining 30 shares */
    if (engine.order_count() != 1) return 9;

    /* Cancel remaining order ID 2 */
    if (!engine.cancel_order(2)) return 10;
    if (engine.order_count() != 0) return 11;

    return 0;
}

int main(int argc, char **argv) {
    if (argc < 2) {
        std::cout << "Usage: %s [--test-pool | --test-ring | --test-matching | --benchmark | --test-all]\n";
        return 0;
    }

    if (std::strcmp(argv[1], "--test-pool") == 0) {
        int r = test_pool();
        std::cout << "pool_test: " << (r == 0 ? "PASS" : "FAIL") << "\n";
        return r;
    }

    if (std::strcmp(argv[1], "--test-ring") == 0) {
        int r = test_ring();
        std::cout << "ring_test: " << (r == 0 ? "PASS" : "FAIL") << "\n";
        return r;
    }

    if (std::strcmp(argv[1], "--test-matching") == 0) {
        int r = test_matching();
        std::cout << "matching_test: " << (r == 0 ? "PASS" : "FAIL") << "\n";
        return r;
    }

    if (std::strcmp(argv[1], "--benchmark") == 0) {
        return run_benchmark(50000);
    }

    if (std::strcmp(argv[1], "--test-all") == 0) {
        int p = test_pool();
        int r = test_ring();
        int m = test_matching();
        int b = run_benchmark(50000);
        int total = p + r + m + b;
        std::cout << "{\"pool\": " << p << ", \"ring\": " << r << ", \"matching\": " << m << ", \"benchmark\": " << b << "}\n";
        return total == 0 ? 0 : 1;
    }

    return 1;
}
