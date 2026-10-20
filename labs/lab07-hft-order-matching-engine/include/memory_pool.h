#ifndef HFT_MEMORY_POOL_H
#define HFT_MEMORY_POOL_H

#include <vector>
#include <cstdint>
#include <cstddef>
#include "order.h"

template <typename T, size_t Capacity>
class MemoryPool {
public:
    MemoryPool() : free_head_(0), allocated_count_(0) {
        storage_.resize(Capacity);
        free_indices_.resize(Capacity);
        for (size_t i = 0; i < Capacity; ++i) {
            free_indices_[i] = i;
        }
    }

    T *allocate() {
        if (free_head_ >= Capacity) {
            return nullptr; /* Exhausted */
        }
        size_t idx = free_indices_[free_head_++];
        allocated_count_++;
        T *obj = &storage_[idx];
        obj->prev = nullptr;
        obj->next = nullptr;
        return obj;
    }

    void deallocate(T *ptr) {
        if (!ptr) return;
        size_t idx = ptr - storage_.data();
        if (idx >= Capacity) return;
        if (free_head_ == 0) return;
        free_indices_[--free_head_] = idx;
        allocated_count_--;
    }

    size_t allocated_count() const {
        return allocated_count_;
    }

    size_t available_count() const {
        return Capacity - allocated_count_;
    }

private:
    std::vector<T> storage_;
    std::vector<size_t> free_indices_;
    size_t free_head_;
    size_t allocated_count_;
};

#endif /* HFT_MEMORY_POOL_H */
