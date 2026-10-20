#ifndef HFT_ORDER_H
#define HFT_ORDER_H

#include "types.h"

struct alignas(64) Order {
    OrderId id;
    Price price;
    Quantity quantity;
    Quantity filled_quantity;
    Side side;
    OrderType type;
    Timestamp timestamp;

    /* Intrusive Doubly-Linked List Pointers for FIFO Price-Time Priority */
    Order *prev;
    Order *next;

    Quantity remaining_quantity() const {
        return quantity - filled_quantity;
    }

    bool is_filled() const {
        return filled_quantity >= quantity;
    }
};

#endif /* HFT_ORDER_H */
