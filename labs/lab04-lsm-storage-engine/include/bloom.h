#ifndef BLOOM_H
#define BLOOM_H

#include <vector>
#include <string>
#include <cstdint>

class BloomFilter {
public:
    explicit BloomFilter(size_t num_bits = 8192, size_t num_hashes = 4);

    void add(const std::string &key);
    bool may_contain(const std::string &key) const;

    const std::vector<uint8_t> &data() const;
    void set_data(const std::vector<uint8_t> &bytes);
    void clear();

private:
    uint32_t hash(const std::string &key, uint32_t seed) const;

    size_t num_bits_;
    size_t num_hashes_;
    std::vector<uint8_t> bits_;
};

#endif /* BLOOM_H */
