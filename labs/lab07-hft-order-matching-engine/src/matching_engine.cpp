#include <algorithm>
#include "matching_engine.h"

MatchingEngine::MatchingEngine() : total_trades_(0) {}

bool MatchingEngine::submit_order(OrderId id, Side side, OrderType type, Price price, Quantity qty) {
    if (qty == 0) return false;

    Quantity remaining_qty = qty;

    if (side == Side::BUY) {
        /* Match against Asks */
        while (remaining_qty > 0) {
            Price best_ask = book_.best_ask_price();
            if (type == OrderType::LIMIT && best_ask > price) {
                break; /* Limit price cannot match */
            }
            if (best_ask == UINT64_MAX) {
                break; /* No asks available */
            }

            Order *maker = book_.best_ask_order();
            if (!maker) break;

            Quantity trade_qty = std::min(remaining_qty, maker->remaining_quantity());
            maker->filled_quantity += trade_qty;
            remaining_qty -= trade_qty;
            total_trades_++;

            ExecutionReport report;
            report.maker_order_id = maker->id;
            report.taker_order_id = id;
            report.taker_side = Side::BUY;
            report.trade_price = maker->price;
            report.trade_quantity = trade_qty;
            report.exec_time = 0;
            execution_ring_.push(report);

            if (maker->is_filled()) {
                book_.remove_filled_order(maker);
                pool_.deallocate(maker);
            }
        }
    } else {
        /* Match against Bids */
        while (remaining_qty > 0) {
            Price best_bid = book_.best_bid_price();
            if (type == OrderType::LIMIT && best_bid < price) {
                break; /* Limit price cannot match */
            }
            if (best_bid == 0) {
                break; /* No bids available */
            }

            Order *maker = book_.best_bid_order();
            if (!maker) break;

            Quantity trade_qty = std::min(remaining_qty, maker->remaining_quantity());
            maker->filled_quantity += trade_qty;
            remaining_qty -= trade_qty;
            total_trades_++;

            ExecutionReport report;
            report.maker_order_id = maker->id;
            report.taker_order_id = id;
            report.taker_side = Side::SELL;
            report.trade_price = maker->price;
            report.trade_quantity = trade_qty;
            report.exec_time = 0;
            execution_ring_.push(report);

            if (maker->is_filled()) {
                book_.remove_filled_order(maker);
                pool_.deallocate(maker);
            }
        }
    }

    /* Rest of limit order goes to book */
    if (remaining_qty > 0 && type == OrderType::LIMIT) {
        Order *resting = pool_.allocate();
        if (!resting) return false; /* Pool exhausted */

        resting->id = id;
        resting->price = price;
        resting->quantity = remaining_qty;
        resting->filled_quantity = 0;
        resting->side = side;
        resting->type = type;
        resting->timestamp = 0;

        book_.add_limit_order(resting);
    }

    return true;
}

bool MatchingEngine::cancel_order(OrderId id) {
    return book_.cancel_order(id, pool_);
}

size_t MatchingEngine::order_count() const {
    return book_.active_order_count();
}

Price MatchingEngine::best_bid() const {
    return book_.best_bid_price();
}

Price MatchingEngine::best_ask() const {
    return book_.best_ask_price();
}

std::vector<ExecutionReport> MatchingEngine::drain_executions() {
    std::vector<ExecutionReport> reports;
    ExecutionReport r;
    while (execution_ring_.pop(r)) {
        reports.push_back(r);
    }
    return reports;
}

size_t MatchingEngine::total_trades() const {
    return total_trades_;
}
