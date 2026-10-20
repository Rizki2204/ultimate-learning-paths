#include "order_book.h"

OrderBook::OrderBook() {}

void OrderBook::add_limit_order(Order *order) {
    if (!order) return;
    if (order->side == Side::BUY) {
        auto it = bids_.find(order->price);
        if (it == bids_.end()) {
            bids_.emplace(order->price, PriceLevel(order->price));
        }
        bids_[order->price].append(order);
    } else {
        auto it = asks_.find(order->price);
        if (it == asks_.end()) {
            asks_.emplace(order->price, PriceLevel(order->price));
        }
        asks_[order->price].append(order);
    }
    order_index_[order->id] = order;
}

bool OrderBook::cancel_order(OrderId id, MemoryPool<Order, 100000> &pool) {
    auto it = order_index_.find(id);
    if (it == order_index_.end()) return false;

    Order *order = it->second;
    order_index_.erase(it);

    if (order->side == Side::BUY) {
        auto level_it = bids_.find(order->price);
        if (level_it != bids_.end()) {
            level_it->second.remove(order);
            if (level_it->second.is_empty()) {
                bids_.erase(level_it);
            }
        }
    } else {
        auto level_it = asks_.find(order->price);
        if (level_it != asks_.end()) {
            level_it->second.remove(order);
            if (level_it->second.is_empty()) {
                asks_.erase(level_it);
            }
        }
    }

    pool.deallocate(order);
    return true;
}

Price OrderBook::best_bid_price() const {
    if (bids_.empty()) return 0;
    return bids_.begin()->first;
}

Price OrderBook::best_ask_price() const {
    if (asks_.empty()) return UINT64_MAX;
    return asks_.begin()->first;
}

Order *OrderBook::best_bid_order() {
    if (bids_.empty()) return nullptr;
    return bids_.begin()->second.head;
}

Order *OrderBook::best_ask_order() {
    if (asks_.empty()) return nullptr;
    return asks_.begin()->second.head;
}

void OrderBook::remove_filled_order(Order *order) {
    if (!order) return;
    order_index_.erase(order->id);

    if (order->side == Side::BUY) {
        auto it = bids_.find(order->price);
        if (it != bids_.end()) {
            it->second.remove(order);
            if (it->second.is_empty()) {
                bids_.erase(it);
            }
        }
    } else {
        auto it = asks_.find(order->price);
        if (it != asks_.end()) {
            it->second.remove(order);
            if (it->second.is_empty()) {
                asks_.erase(it);
            }
        }
    }
}

size_t OrderBook::active_order_count() const {
    return order_index_.size();
}

Order *OrderBook::find_order(OrderId id) const {
    auto it = order_index_.find(id);
    if (it == order_index_.end()) return nullptr;
    return it->second;
}
