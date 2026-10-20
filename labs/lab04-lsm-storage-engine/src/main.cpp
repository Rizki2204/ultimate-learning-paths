#include <iostream>
#include <string>
#include <cstring>
#include "lsm_engine.h"

static int test_wal() {
    std::string test_log = "test_wal_tmp.log";
    std::remove(test_log.c_str());

    {
        WriteAheadLog wal(test_log);
        wal.append_put("user_1", "Alice");
        wal.append_put("user_2", "Bob");
        wal.append_del("user_1");
        wal.sync();
    }

    auto recovered = WriteAheadLog::recover(test_log);
    std::remove(test_log.c_str());

    if (recovered.size() != 3) return 1;
    if (recovered[0].key != "user_1" || recovered[0].value != "Alice") return 2;
    if (recovered[2].op != WalOpType::DEL || recovered[2].key != "user_1") return 3;
    return 0;
}

static int test_bloom() {
    BloomFilter filter(4096, 4);
    filter.add("alpha");
    filter.add("beta");
    filter.add("gamma");

    if (!filter.may_contain("alpha")) return 1;
    if (!filter.may_contain("beta")) return 2;
    if (!filter.may_contain("gamma")) return 3;

    /* Check false positive with non-existent keys */
    int false_positives = 0;
    int trials = 1000;
    for (int i = 0; i < trials; i++) {
        std::string non_key = "non_existent_key_" + std::to_string(i);
        if (filter.may_contain(non_key)) {
            false_positives++;
        }
    }
    double fp_rate = static_cast<double>(false_positives) / trials;
    if (fp_rate > 0.05) return 4; /* Empirical FP rate must be <= 5% with 3 keys in 4096 bits */
    return 0;
}

static int test_memtable() {
    MemTable mt;
    mt.put("k1", "v1");
    mt.put("k2", "v2");

    std::string val;
    if (!mt.get("k1", val) || val != "v1") return 1;

    mt.del("k1");
    if (mt.get("k1", val)) return 2; /* Should return false for tombstone */

    return 0;
}

static int test_sstable() {
    std::string sst_path = "test_table_tmp.sst";
    std::remove(sst_path.c_str());

    std::map<std::string, MemEntry> entries;
    entries["apple"] = {"10", false, 1};
    entries["banana"] = {"20", false, 2};
    entries["cherry"] = {"30", false, 3};

    if (!SSTable::create_from_map(sst_path, entries)) return 1;

    auto sst = SSTable::open(sst_path);
    if (!sst) return 2;

    std::string val;
    bool is_del = false;
    if (!sst->get("banana", val, is_del) || val != "20" || is_del) return 3;
    if (sst->get("dragonfruit", val, is_del)) return 4;

    std::remove(sst_path.c_str());
    return 0;
}

static int test_compaction() {
    std::string dir = ".";
    LSMOptions opts;
    opts.memtable_flush_threshold = 100; /* Flush quickly */
    LSMEngine engine(dir, opts);
    engine.open();

    engine.put("k1", "old_val");
    engine.flush();

    engine.put("k1", "new_val");
    engine.put("k2", "val2");
    engine.flush();

    std::string val;
    if (!engine.get("k1", val) || val != "new_val") return 1;

    if (!engine.compact()) return 2;
    if (!engine.get("k1", val) || val != "new_val") return 3;

    engine.close();
    return 0;
}

int main(int argc, char **argv) {
    if (argc < 2) {
        std::cout << "Usage: " << argv[0] << " [--test-wal | --test-bloom | --test-memtable | --test-sstable | --test-compaction | --test-all]\n";
        return 0;
    }

    if (std::strcmp(argv[1], "--test-wal") == 0) {
        int r = test_wal();
        std::cout << "wal_test: " << (r == 0 ? "PASS" : "FAIL") << "\n";
        return r;
    }

    if (std::strcmp(argv[1], "--test-bloom") == 0) {
        int r = test_bloom();
        std::cout << "bloom_test: " << (r == 0 ? "PASS" : "FAIL") << "\n";
        return r;
    }

    if (std::strcmp(argv[1], "--test-memtable") == 0) {
        int r = test_memtable();
        std::cout << "memtable_test: " << (r == 0 ? "PASS" : "FAIL") << "\n";
        return r;
    }

    if (std::strcmp(argv[1], "--test-sstable") == 0) {
        int r = test_sstable();
        std::cout << "sstable_test: " << (r == 0 ? "PASS" : "FAIL") << "\n";
        return r;
    }

    if (std::strcmp(argv[1], "--test-compaction") == 0) {
        int r = test_compaction();
        std::cout << "compaction_test: " << (r == 0 ? "PASS" : "FAIL") << "\n";
        return r;
    }

    if (std::strcmp(argv[1], "--test-all") == 0) {
        int w = test_wal();
        int b = test_bloom();
        int m = test_memtable();
        int s = test_sstable();
        int c = test_compaction();
        int total = w + b + m + s + c;
        std::cout << "{\"wal\": " << w << ", \"bloom\": " << b << ", \"memtable\": " << m
                  << ", \"sstable\": " << s << ", \"compaction\": " << c << "}\n";
        return total == 0 ? 0 : 1;
    }

    return 1;
}
