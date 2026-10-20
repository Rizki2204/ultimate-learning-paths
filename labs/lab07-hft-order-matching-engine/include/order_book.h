#ifndef HFT_ORDER_BOOK_H
#define HFT_ORDER_BOOK_H

#include <map>
#include <unordered_map>
#include <functional>
#include "order.h"
#include "memory_pool.h"

struct PriceLevel {
    Price price;
    Quantity total_volume;
    Order *head;
    Order *tail;

    PriceLevel() : price(0), total_volume(0), head(nullptr), tail(nullptr) {}
    explicit PriceLevel(Price p) : price(p), total_volume(0), head(nullptr), tail(nullptr) {}

    void append(Order *o) {
        o->prev = tail;
        o->next = nullptr;
        if (tail) {
            tail->next = o;
        } else {
            head = o;
        }
        tail = o;
        total_volume += o->remaining_quantity();
    }

    void remove(Order *o) {
        if (o->prev) {
            o->prev->next = o->next;
        } else {
            head = o->next;
        }
        if (o->next) {
            o->next->prev = o->prev;
        } else {
            tail = o->prev;
        }
        total_volume -= o->remaining_quantity();
        o->prev = nullptr;
        o->next = nullptr;
    }

    bool is_empty() const {
        return head == nullptr;
    }
};

class OrderBook {
public:
    OrderBook();

    void add_limit_order(Order *order);
    bool cancel_order(OrderId id, MemoryPool<Order, 100000> &pool);

    Price best_bid_price() const;
    Price best_ask_price() const;

    Order *best_bid_order();
    Order *best_ask_order();

    void remove_filled_order(Order *order);

    size_t active_order_count() const;
    Order *find_order(OrderId id) const;

private:
    /* Bids sorted in descending order (highest price has priority) */
    std::map<Price, PriceLevel, std::greater<Price>> bids_;

    /* Asks sorted in ascending order (lowest price has priority) */
    std::map<Price, PriceLevel, std::less<Price>> asks_;

    /* Direct hash index for O(1) cancel / pointer unlinking */
    std::unordered_map<OrderId, Order *> order_index_;
};

#endif /* HFT_ORDER_BOOK_H */
