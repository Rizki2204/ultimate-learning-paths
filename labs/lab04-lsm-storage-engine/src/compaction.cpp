#include <map>
#include <fstream>
#include <cstdio>
#include "compaction.h"
#include "memtable.h"

bool Compactor::compact_sstables(const std::vector<std::shared_ptr<SSTable>> &tables,
                                 const std::string &output_filepath,
                                 bool is_bottommost_level) {
    if (tables.empty()) return false;

    std::map<std::string, MemEntry> merged;

    /* Read all SSTables from oldest to newest so newer versions overwrite older ones */
    for (const auto &table : tables) {
        auto entries = table->read_all_entries();
        for (auto &pair : entries) {
            merged[pair.first] = std::move(pair.second);
        }
    }

    /* Purge tombstones if at bottommost level */
    if (is_bottommost_level) {
        for (auto it = merged.begin(); it != merged.end(); ) {
            if (it->second.is_tombstone) {
                it = merged.erase(it);
            } else {
                ++it;
            }
        }
    }

    if (!SSTable::create_from_map(output_filepath, merged)) {
        return false;
    }

    /* Delete compacted files */
    for (const auto &table : tables) {
        std::remove(table->filepath().c_str());
    }

    return true;
}
