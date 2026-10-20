#ifndef MEMTABLE_H
#define MEMTABLE_H

#include <string>
#include <map>
#include <cstdint>

struct MemEntry {
    std::string value;
    bool is_tombstone;
    uint64_t sequence;
};

class MemTable {
public:
    MemTable();

    void put(const std::string &key, const std::string &value, uint64_t seq = 0);
    void del(const std::string &key, uint64_t seq = 0);
    bool get(const std::string &key, std::string &value) const;

    size_t approximate_size() const;
    size_t count() const;
    void clear();

    const std::map<std::string, MemEntry> &entries() const;

private:
    std::map<std::string, MemEntry> table_;
    size_t size_bytes_;
};

#endif /* MEMTABLE_H */
