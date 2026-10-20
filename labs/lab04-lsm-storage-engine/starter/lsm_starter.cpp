#include <iostream>
#include <string>
#include <map>
#include <vector>

/*
 * Log-Structured Merge Tree (LSM) Storage Engine Starter Scaffolding
 *
 * Exercise Instructions:
 * Implement in-memory MemTable updates, tombstone marking, and
 * CRC32 checksum calculation following LSM architecture principles.
 */

struct StarterEntry {
    std::string value;
    bool is_deleted;
};

class StarterMemTable {
public:
    void put(const std::string &key, const std::string &val) {
        table_[key] = {val, false};
    }

    void del(const std::string &key) {
        table_[key] = {"", true};
    }

    bool get(const std::string &key, std::string &val) const {
        auto it = table_.find(key);
        if (it == table_.end() || it->second.is_deleted) return false;
        val = it->second.value;
        return true;
    }

    size_t count() const { return table_.size(); }

private:
    std::map<std::string, StarterEntry> table_;
};

int main() {
    StarterMemTable mt;
    mt.put("user_100", "Profile Data");
    std::string val;
    if (mt.get("user_100", val)) {
        std::cout << "Retrieved key user_100: " << val << std::endl;
    }
    mt.del("user_100");
    std::cout << "After deletion, found: " << (mt.get("user_100", val) ? "YES" : "NO") << std::endl;
    return 0;
}
