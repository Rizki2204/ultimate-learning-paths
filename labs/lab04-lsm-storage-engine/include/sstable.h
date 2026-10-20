#ifndef SSTABLE_H
#define SSTABLE_H

#include <string>
#include <vector>
#include <cstdint>
#include <map>
#include <memory>
#include "bloom.h"

struct IndexEntry {
    std::string key;
    uint64_t offset;
};

struct Footer {
    uint64_t data_len;
    uint64_t index_offset;
    uint64_t index_len;
    uint64_t bloom_offset;
    uint64_t bloom_len;
    uint64_t magic;
};

class SSTable {
public:
    static const uint64_t MAGIC_NUMBER = 0x53535441424C4531ULL; /* "SSTABLE1" */

    static bool create_from_map(const std::string &filepath,
                                const std::map<std::string, struct MemEntry> &entries,
                                size_t index_interval = 1);

    static std::shared_ptr<SSTable> open(const std::string &filepath);

    bool get(const std::string &key, std::string &value, bool &is_deleted) const;
    std::map<std::string, struct MemEntry> read_all_entries() const;
    const std::string &filepath() const;
    size_t key_count() const;

private:
    std::string filepath_;
    std::vector<IndexEntry> index_;
    BloomFilter bloom_;
    Footer footer_;
    size_t count_;
};

#endif /* SSTABLE_H */
