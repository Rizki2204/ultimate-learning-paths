#include <fstream>
#include <algorithm>
#include <iostream>
#include "sstable.h"
#include "memtable.h"

bool SSTable::create_from_map(const std::string &filepath,
                             const std::map<std::string, MemEntry> &entries,
                             size_t index_interval) {
    std::ofstream out(filepath, std::ios::binary);
    if (!out.is_open()) return false;

    BloomFilter bloom(8192, 4);
    for (const auto &pair : entries) {
        bloom.add(pair.first);
    }

    std::vector<IndexEntry> index;
    uint64_t current_data_offset = 0;
    size_t counter = 0;

    /* 1. Write Data Block */
    for (const auto &pair : entries) {
        const std::string &k = pair.first;
        const MemEntry &entry = pair.second;

        if (counter % index_interval == 0) {
            index.push_back({k, current_data_offset});
        }
        counter++;

        uint16_t k_len = static_cast<uint16_t>(k.size());
        uint32_t v_len = static_cast<uint32_t>(entry.value.size());
        uint8_t tomb = entry.is_tombstone ? 1 : 0;

        out.write(reinterpret_cast<const char *>(&k_len), sizeof(k_len));
        out.write(k.data(), k.size());
        out.write(reinterpret_cast<const char *>(&v_len), sizeof(v_len));
        out.write(entry.value.data(), entry.value.size());
        out.write(reinterpret_cast<const char *>(&tomb), sizeof(tomb));

        current_data_offset += sizeof(k_len) + k.size() + sizeof(v_len) + entry.value.size() + sizeof(tomb);
    }
    uint64_t data_len = current_data_offset;

    /* 2. Write Index Block */
    uint64_t index_offset = out.tellp();
    for (const auto &ie : index) {
        uint16_t k_len = static_cast<uint16_t>(ie.key.size());
        uint64_t off = ie.offset;
        out.write(reinterpret_cast<const char *>(&k_len), sizeof(k_len));
        out.write(ie.key.data(), ie.key.size());
        out.write(reinterpret_cast<const char *>(&off), sizeof(off));
    }
    uint64_t index_len = static_cast<uint64_t>(out.tellp()) - index_offset;

    /* 3. Write Bloom Filter Block */
    uint64_t bloom_offset = out.tellp();
    const auto &bloom_data = bloom.data();
    out.write(reinterpret_cast<const char *>(bloom_data.data()), bloom_data.size());
    uint64_t bloom_len = static_cast<uint64_t>(out.tellp()) - bloom_offset;

    /* 4. Write Footer */
    Footer footer;
    footer.data_len = data_len;
    footer.index_offset = index_offset;
    footer.index_len = index_len;
    footer.bloom_offset = bloom_offset;
    footer.bloom_len = bloom_len;
    footer.magic = MAGIC_NUMBER;

    out.write(reinterpret_cast<const char *>(&footer), sizeof(footer));
    out.flush();
    return out.good();
}

std::shared_ptr<SSTable> SSTable::open(const std::string &filepath) {
    std::ifstream in(filepath, std::ios::binary | std::ios::ate);
    if (!in.is_open()) return nullptr;

    std::streamsize file_size = in.tellg();
    if (file_size < static_cast<std::streamsize>(sizeof(Footer))) return nullptr;

    /* Read Footer */
    in.seekg(file_size - sizeof(Footer));
    Footer footer;
    in.read(reinterpret_cast<char *>(&footer), sizeof(Footer));
    if (footer.magic != MAGIC_NUMBER) return nullptr;

    auto table = std::make_shared<SSTable>();
    table->filepath_ = filepath;
    table->footer_ = footer;

    /* Read Bloom Filter */
    in.seekg(footer.bloom_offset);
    std::vector<uint8_t> bloom_bytes(footer.bloom_len);
    in.read(reinterpret_cast<char *>(bloom_bytes.data()), footer.bloom_len);
    table->bloom_.set_data(bloom_bytes);

    /* Read Index */
    in.seekg(footer.index_offset);
    uint64_t read_bytes = 0;
    while (read_bytes < footer.index_len) {
        uint16_t k_len = 0;
        in.read(reinterpret_cast<char *>(&k_len), sizeof(k_len));
        std::string k(k_len, '\0');
        in.read(&k[0], k_len);
        uint64_t off = 0;
        in.read(reinterpret_cast<char *>(&off), sizeof(off));

        table->index_.push_back({std::move(k), off});
        read_bytes += sizeof(k_len) + k_len + sizeof(off);
    }

    table->count_ = table->index_.size();
    return table;
}

bool SSTable::get(const std::string &key, std::string &value, bool &is_deleted) const {
    /* 1. Bloom filter check */
    if (!bloom_.may_contain(key)) {
        return false;
    }

    if (index_.empty()) return false;

    /* 2. Binary search in sparse index */
    auto it = std::upper_bound(index_.begin(), index_.end(), key,
        [](const std::string &k, const IndexEntry &ie) {
            return k < ie.key;
        });

    uint64_t start_offset = 0;
    if (it != index_.begin()) {
        start_offset = (it - 1)->offset;
    }

    /* 3. Scan Data block */
    std::ifstream in(filepath_, std::ios::binary);
    if (!in.is_open()) return false;

    in.seekg(start_offset);
    while (static_cast<uint64_t>(in.tellg()) < footer_.data_len) {
        uint16_t k_len = 0;
        in.read(reinterpret_cast<char *>(&k_len), sizeof(k_len));
        if (in.gcount() != sizeof(k_len)) break;

        std::string curr_k(k_len, '\0');
        in.read(&curr_k[0], k_len);

        uint32_t v_len = 0;
        in.read(reinterpret_cast<char *>(&v_len), sizeof(v_len));

        std::string curr_v(v_len, '\0');
        in.read(&curr_v[0], v_len);

        uint8_t tomb = 0;
        in.read(reinterpret_cast<char *>(&tomb), sizeof(tomb));

        if (curr_k == key) {
            is_deleted = (tomb != 0);
            value = std::move(curr_v);
            return true;
        }

        if (curr_k > key) {
            /* Passed key: because data block is sorted, key does not exist */
            break;
        }
    }

    return false;
}

std::map<std::string, MemEntry> SSTable::read_all_entries() const {
    std::map<std::string, MemEntry> entries;
    std::ifstream in(filepath_, std::ios::binary);
    if (!in.is_open()) return entries;

    while (static_cast<uint64_t>(in.tellg()) < footer_.data_len) {
        uint16_t k_len = 0;
        in.read(reinterpret_cast<char *>(&k_len), sizeof(k_len));
        if (in.gcount() != sizeof(k_len)) break;

        std::string curr_k(k_len, '\0');
        in.read(&curr_k[0], k_len);

        uint32_t v_len = 0;
        in.read(reinterpret_cast<char *>(&v_len), sizeof(v_len));

        std::string curr_v(v_len, '\0');
        in.read(&curr_v[0], v_len);

        uint8_t tomb = 0;
        in.read(reinterpret_cast<char *>(&tomb), sizeof(tomb));

        entries[curr_k] = {std::move(curr_v), tomb != 0, 0};
    }
    return entries;
}

const std::string &SSTable::filepath() const {
    return filepath_;
}

size_t SSTable::key_count() const {
    return count_;
}
