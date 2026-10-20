#ifndef HFT_MATCHING_ENGINE_H
#define HFT_MATCHING_ENGINE_H

#include <vector>
#include "types.h"
#include "order.h"
#include "memory_pool.h"
#include "ring_buffer.h"
#include "order_book.h"

class MatchingEngine {
public:
    static constexpr size_t POOL_CAPACITY = 100000;
    static constexpr size_t RING_CAPACITY = 65536;

    MatchingEngine();

    bool submit_order(OrderId id, Side side, OrderType type, Price price, Quantity qty);
    bool cancel_order(OrderId id);

    size_t order_count() const;
    Price best_bid() const;
    Price best_ask() const;

    std::vector<ExecutionReport> drain_executions();
    size_t total_trades() const;

private:
    MemoryPool<Order, POOL_CAPACITY> pool_;
    OrderBook book_;
    SPSCRingBuffer<ExecutionReport, RING_CAPACITY> execution_ring_;
    size_t total_trades_;
};

#endif /* HFT_MATCHING_ENGINE_H */
