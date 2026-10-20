#include <iostream>
#include <vector>
#include <cstdint>

/*
 * High-Frequency Trading Order Matching Engine Starter Scaffolding
 *
 * Exercise Instructions:
 * Implement fixed-point order price comparison, FIFO execution matching,
 * and lock-free ring buffer index management.
 */

using OrderId = uint64_t;
using Price = uint64_t;
using Quantity = uint32_t;

struct StarterOrder {
    OrderId id;
    Price price;
    Quantity qty;
    bool is_buy;
};

class StarterEngine {
public:
    /*
     * Exercise: Basic Order Matching
     * If buy price >= sell price, execute trade and return true.
     */
    bool try_match(const StarterOrder &buy, const StarterOrder &sell, Quantity &trade_qty, Price &trade_price) {
        if (!buy.is_buy || sell.is_buy) return false;
        if (buy.price >= sell.price) {
            trade_qty = std::min(buy.qty, sell.qty);
            trade_price = sell.price; /* Maker price */
            return true;
        }
        return false;
    }
};

int main() {
    StarterEngine engine;
    StarterOrder buy{1, 1050, 100, true};
    StarterOrder sell{2, 1040, 50, false};
    Quantity traded = 0;
    Price exec_price = 0;
    if (engine.try_match(buy, sell, traded, exec_price)) {
        std::cout << "Matched " << traded << " shares at $" << (exec_price / 100.0) << std::endl;
    }
    return 0;
}
