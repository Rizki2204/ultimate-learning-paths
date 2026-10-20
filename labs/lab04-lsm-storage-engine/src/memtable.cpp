#include "memtable.h"

MemTable::MemTable() : size_bytes_(0) {}

void MemTable::put(const std::string &key, const std::string &value, uint64_t seq) {
    auto it = table_.find(key);
    if (it != table_.end()) {
        size_bytes_ -= it->first.size() + it->second.value.size() + sizeof(MemEntry);
    }
    table_[key] = {value, false, seq};
    size_bytes_ += key.size() + value.size() + sizeof(MemEntry);
}

void MemTable::del(const std::string &key, uint64_t seq) {
    auto it = table_.find(key);
    if (it != table_.end()) {
        size_bytes_ -= it->first.size() + it->second.value.size() + sizeof(MemEntry);
    }
    table_[key] = {"", true, seq};
    size_bytes_ += key.size() + sizeof(MemEntry);
}

bool MemTable::get(const std::string &key, std::string &value) const {
    auto it = table_.find(key);
    if (it == table_.end()) return false;
    if (it->second.is_tombstone) return false;
    value = it->second.value;
    return true;
}

size_t MemTable::approximate_size() const {
    return size_bytes_;
}

size_t MemTable::count() const {
    return table_.size();
}

void MemTable::clear() {
    table_.clear();
    size_bytes_ = 0;
}

const std::map<std::string, MemEntry> &MemTable::entries() const {
    return table_;
}
