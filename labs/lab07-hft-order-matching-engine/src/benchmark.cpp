#include <chrono>
#include <iostream>
#include <vector>
#include "matching_engine.h"

int run_benchmark(size_t num_orders) {
    MatchingEngine engine;

    auto start = std::chrono::high_resolution_clock::now();

    for (size_t i = 1; i <= num_orders; ++i) {
        Side side = (i % 2 == 0) ? Side::BUY : Side::SELL;
        Price price = 10000 + (i % 20);
        Quantity qty = 10;
        engine.submit_order(i, side, OrderType::LIMIT, price, qty);
    }

    auto end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double, std::nano> diff = end - start;

    double total_ns = diff.count();
    double avg_latency_ns = total_ns / num_orders;
    double throughput_ops = (num_orders / (total_ns / 1e9));

    std::cout << "{\"benchmark\": {\"orders\": " << num_orders
              << ", \"total_ns\": " << total_ns
              << ", \"avg_latency_ns\": " << avg_latency_ns
              << ", \"throughput_ops\": " << throughput_ops
              << ", \"trades\": " << engine.total_trades() << "}}\n";

    return (avg_latency_ns < 10000.0) ? 0 : 1; /* Pass if under 10 microseconds per order */
}
