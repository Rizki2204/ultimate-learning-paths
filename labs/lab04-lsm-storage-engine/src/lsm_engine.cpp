#include <iostream>
#include <sstream>
#include <cstdio>
#include "lsm_engine.h"

LSMEngine::LSMEngine(std::string db_dir, LSMOptions options)
    : db_dir_(std::move(db_dir)), options_(options), next_sstable_id_(1), sequence_num_(0) {}

LSMEngine::~LSMEngine() {
    close();
}

bool LSMEngine::open() {
    std::string wal_path = db_dir_ + "/wal.log";

    /* Recover from existing WAL if present */
    auto recovered = WriteAheadLog::recover(wal_path);
    for (const auto &rec : recovered) {
        if (rec.op == WalOpType::PUT) {
            memtable_.put(rec.key, rec.value, ++sequence_num_);
        } else if (rec.op == WalOpType::DEL) {
            memtable_.del(rec.key, ++sequence_num_);
        }
    }

    /* Open active WAL */
    wal_ = std::unique_ptr<WriteAheadLog>(new WriteAheadLog(wal_path));
    return true;
}

void LSMEngine::close() {
    if (wal_) {
        wal_->close();
        wal_ = nullptr;
    }
}

bool LSMEngine::put(const std::string &key, const std::string &value) {
    if (!wal_) return false;
    wal_->append_put(key, value);
    memtable_.put(key, value, ++sequence_num_);

    if (memtable_.approximate_size() >= options_.memtable_flush_threshold) {
        flush();
    }
    return true;
}

bool LSMEngine::del(const std::string &key) {
    if (!wal_) return false;
    wal_->append_del(key);
    memtable_.del(key, ++sequence_num_);

    if (memtable_.approximate_size() >= options_.memtable_flush_threshold) {
        flush();
    }
    return true;
}

bool LSMEngine::get(const std::string &key, std::string &value) {
    /* 1. Check MemTable */
    const auto &table = memtable_.entries();
    auto it = table.find(key);
    if (it != table.end()) {
        if (it->second.is_tombstone) {
            return false; /* Explicitly deleted */
        }
        value = it->second.value;
        return true;
    }

    /* 2. Check SSTables from newest to oldest */
    for (auto rit = sstables_.rbegin(); rit != sstables_.rend(); ++rit) {
        bool is_del = false;
        if ((*rit)->get(key, value, is_del)) {
            if (is_del) return false;
            return true;
        }
    }

    return false;
}

bool LSMEngine::flush() {
    if (memtable_.count() == 0) return true;

    std::ostringstream ss;
    ss << db_dir_ << "/table_" << next_sstable_id_++ << ".sst";
    std::string sst_path = ss.str();

    if (!SSTable::create_from_map(sst_path, memtable_.entries())) {
        return false;
    }

    auto sst = SSTable::open(sst_path);
    if (!sst) return false;
    sstables_.push_back(sst);

    memtable_.clear();

    /* Reset WAL after successful flush */
    if (wal_) {
        wal_->close();
        std::string wal_path = db_dir_ + "/wal.log";
        std::remove(wal_path.c_str());
        wal_ = std::unique_ptr<WriteAheadLog>(new WriteAheadLog(wal_path));
    }

    return true;
}

bool LSMEngine::compact() {
    if (sstables_.size() < 2) return true;

    std::ostringstream ss;
    ss << db_dir_ << "/compacted_" << next_sstable_id_++ << ".sst";
    std::string out_path = ss.str();

    if (!Compactor::compact_sstables(sstables_, out_path, true)) {
        return false;
    }

    sstables_.clear();
    auto compacted_sst = SSTable::open(out_path);
    if (compacted_sst) {
        sstables_.push_back(compacted_sst);
    }
    return true;
}

size_t LSMEngine::sstable_count() const {
    return sstables_.size();
}

size_t LSMEngine::memtable_size() const {
    return memtable_.approximate_size();
}
