#ifndef HFT_TYPES_H
#define HFT_TYPES_H

#include <cstdint>
#include <cstddef>

using OrderId = uint64_t;
using Price = uint64_t;     /* Price in fixed-point ticks / cents (e.g. $100.50 = 10050) */
using Quantity = uint32_t;  /* Share count */
using Timestamp = uint64_t; /* Nanoseconds epoch */

enum class Side : uint8_t {
    BUY = 1,
    SELL = 2
};

enum class OrderType : uint8_t {
    LIMIT = 1,
    MARKET = 2
};

struct ExecutionReport {
    OrderId maker_order_id;
    OrderId taker_order_id;
    Side taker_side;
    Price trade_price;
    Quantity trade_quantity;
    Timestamp exec_time;
};

#endif /* HFT_TYPES_H */
