#ifndef LSM_ENGINE_H
#define LSM_ENGINE_H

#include <string>
#include <vector>
#include <memory>
#include "wal.h"
#include "memtable.h"
#include "sstable.h"
#include "compaction.h"

struct LSMOptions {
    size_t memtable_flush_threshold = 4096; /* 4KB threshold for testing */
    size_t bloom_bits = 8192;
};

class LSMEngine {
public:
    explicit LSMEngine(std::string db_dir, LSMOptions options = LSMOptions());
    ~LSMEngine();

    bool open();
    void close();

    bool put(const std::string &key, const std::string &value);
    bool get(const std::string &key, std::string &value);
    bool del(const std::string &key);

    bool flush();
    bool compact();

    size_t sstable_count() const;
    size_t memtable_size() const;

private:
    std::string db_dir_;
    LSMOptions options_;
    std::unique_ptr<WriteAheadLog> wal_;
    MemTable memtable_;
    std::vector<std::shared_ptr<SSTable>> sstables_;
    uint64_t next_sstable_id_;
    uint64_t sequence_num_;
};

#endif /* LSM_ENGINE_H */
