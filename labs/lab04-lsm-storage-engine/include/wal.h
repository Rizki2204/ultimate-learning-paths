#ifndef WAL_H
#define WAL_H

#include <string>
#include <vector>
#include <cstdint>
#include <fstream>

enum class WalOpType : uint8_t {
    PUT = 1,
    DEL = 2
};

struct WalRecord {
    WalOpType op;
    std::string key;
    std::string value;
};

uint32_t compute_crc32(const uint8_t *data, size_t len);

class WriteAheadLog {
public:
    explicit WriteAheadLog(std::string filepath);
    ~WriteAheadLog();

    bool append_put(const std::string &key, const std::string &value);
    bool append_del(const std::string &key);
    bool sync();
    void close();

    static std::vector<WalRecord> recover(const std::string &filepath);

private:
    std::string filepath_;
    std::ofstream out_;
};

#endif /* WAL_H */
