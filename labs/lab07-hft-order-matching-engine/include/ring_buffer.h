#ifndef HFT_RING_BUFFER_H
#define HFT_RING_BUFFER_H

#include <atomic>
#include <vector>
#include <cstddef>

template <typename T, size_t Capacity>
class SPSCRingBuffer {
    static_assert((Capacity & (Capacity - 1)) == 0, "Capacity must be a power of two");

public:
    SPSCRingBuffer() : head_(0), tail_(0) {
        buffer_.resize(Capacity);
    }

    bool push(const T &item) {
        const size_t current_tail = tail_.load(std::memory_order_relaxed);
        const size_t current_head = head_.load(std::memory_order_acquire);

        if ((current_tail - current_head) >= Capacity) {
            return false; /* Buffer full */
        }

        buffer_[current_tail & BUFFER_MASK] = item;
        tail_.store(current_tail + 1, std::memory_order_release);
        return true;
    }

    bool pop(T &item) {
        const size_t current_head = head_.load(std::memory_order_relaxed);
        const size_t current_tail = tail_.load(std::memory_order_acquire);

        if (current_head == current_tail) {
            return false; /* Buffer empty */
        }

        item = buffer_[current_head & BUFFER_MASK];
        head_.store(current_head + 1, std::memory_order_release);
        return true;
    }

    size_t size() const {
        size_t head = head_.load(std::memory_order_relaxed);
        size_t tail = tail_.load(std::memory_order_relaxed);
        return (tail >= head) ? (tail - head) : 0;
    }

    bool empty() const {
        return head_.load(std::memory_order_relaxed) == tail_.load(std::memory_order_relaxed);
    }

private:
    static constexpr size_t BUFFER_MASK = Capacity - 1;
    std::vector<T> buffer_;

    alignas(64) std::atomic<size_t> head_;
    alignas(64) std::atomic<size_t> tail_;
};

#endif /* HFT_RING_BUFFER_H */
