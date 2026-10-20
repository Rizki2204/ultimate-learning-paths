#include "bloom.h"

BloomFilter::BloomFilter(size_t num_bits, size_t num_hashes)
    : num_bits_(num_bits), num_hashes_(num_hashes) {
    bits_.resize((num_bits_ + 7) / 8, 0);
}

uint32_t BloomFilter::hash(const std::string &key, uint32_t seed) const {
    uint32_t h = seed ^ 2166136261U;
    for (char c : key) {
        h ^= static_cast<uint8_t>(c);
        h *= 16777619U;
    }
    return h;
}

void BloomFilter::add(const std::string &key) {
    for (size_t i = 0; i < num_hashes_; i++) {
        uint32_t h = hash(key, static_cast<uint32_t>(i * 0x9e3779b9U + 1));
        size_t bit_idx = h % num_bits_;
        bits_[bit_idx / 8] |= (1U << (bit_idx % 8));
    }
}

bool BloomFilter::may_contain(const std::string &key) const {
    for (size_t i = 0; i < num_hashes_; i++) {
        uint32_t h = hash(key, static_cast<uint32_t>(i * 0x9e3779b9U + 1));
        size_t bit_idx = h % num_bits_;
        if (!(bits_[bit_idx / 8] & (1U << (bit_idx % 8)))) {
            return false;
        }
    }
    return true;
}

const std::vector<uint8_t> &BloomFilter::data() const {
    return bits_;
}

void BloomFilter::set_data(const std::vector<uint8_t> &bytes) {
    bits_ = bytes;
    num_bits_ = bits_.size() * 8;
}

void BloomFilter::clear() {
    std::fill(bits_.begin(), bits_.end(), 0);
}
