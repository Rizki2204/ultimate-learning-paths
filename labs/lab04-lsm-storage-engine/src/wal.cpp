#include <iostream>
#include "wal.h"

uint32_t compute_crc32(const uint8_t *data, size_t len) {
    uint32_t crc = 0xFFFFFFFFU;
    for (size_t i = 0; i < len; i++) {
        crc ^= data[i];
        for (int k = 0; k < 8; k++) {
            crc = (crc >> 1) ^ (0xEDB88320U & (-(crc & 1U)));
        }
    }
    return ~crc;
}

WriteAheadLog::WriteAheadLog(std::string filepath)
    : filepath_(std::move(filepath)) {
    out_.open(filepath_, std::ios::binary | std::ios::app);
}

WriteAheadLog::~WriteAheadLog() {
    close();
}

void WriteAheadLog::close() {
    if (out_.is_open()) {
        out_.flush();
        out_.close();
    }
}

bool WriteAheadLog::sync() {
    if (!out_.is_open()) return false;
    out_.flush();
    return true;
}

static bool write_entry(std::ofstream &out, WalOpType op_type, const std::string &key, const std::string &value) {
    if (!out.is_open()) return false;

    uint8_t op = static_cast<uint8_t>(op_type);
    uint16_t key_len = static_cast<uint16_t>(key.size());
    uint32_t val_len = static_cast<uint32_t>(value.size());

    size_t payload_size = 1 + 2 + key_len + 4 + val_len;
    std::vector<uint8_t> payload(payload_size);

    size_t offset = 0;
    payload[offset++] = op;

    payload[offset++] = static_cast<uint8_t>(key_len & 0xFF);
    payload[offset++] = static_cast<uint8_t>((key_len >> 8) & 0xFF);

    for (char c : key) payload[offset++] = static_cast<uint8_t>(c);

    payload[offset++] = static_cast<uint8_t>(val_len & 0xFF);
    payload[offset++] = static_cast<uint8_t>((val_len >> 8) & 0xFF);
    payload[offset++] = static_cast<uint8_t>((val_len >> 16) & 0xFF);
    payload[offset++] = static_cast<uint8_t>((val_len >> 24) & 0xFF);

    for (char c : value) payload[offset++] = static_cast<uint8_t>(c);

    uint32_t crc = compute_crc32(payload.data(), payload.size());
    uint32_t record_size = static_cast<uint32_t>(payload.size());

    out.write(reinterpret_cast<const char *>(&record_size), sizeof(record_size));
    out.write(reinterpret_cast<const char *>(&crc), sizeof(crc));
    out.write(reinterpret_cast<const char *>(payload.data()), payload.size());
    out.flush();
    return out.good();
}

bool WriteAheadLog::append_put(const std::string &key, const std::string &value) {
    return write_entry(out_, WalOpType::PUT, key, value);
}

bool WriteAheadLog::append_del(const std::string &key) {
    return write_entry(out_, WalOpType::DEL, key, "");
}

std::vector<WalRecord> WriteAheadLog::recover(const std::string &filepath) {
    std::vector<WalRecord> records;
    std::ifstream in(filepath, std::ios::binary);
    if (!in.is_open()) return records;

    while (in.peek() != EOF) {
        uint32_t record_size = 0;
        uint32_t expected_crc = 0;

        in.read(reinterpret_cast<char *>(&record_size), sizeof(record_size));
        if (in.gcount() != sizeof(record_size)) break;

        in.read(reinterpret_cast<char *>(&expected_crc), sizeof(expected_crc));
        if (in.gcount() != sizeof(expected_crc)) break;

        if (record_size == 0 || record_size > 64 * 1024 * 1024) break; /* Sanity bound */

        std::vector<uint8_t> payload(record_size);
        in.read(reinterpret_cast<char *>(payload.data()), record_size);
        if (in.gcount() != static_cast<std::streamsize>(record_size)) break;

        uint32_t actual_crc = compute_crc32(payload.data(), payload.size());
        if (actual_crc != expected_crc) {
            /* Corrupted record: stop recovery at boundary */
            break;
        }

        size_t off = 0;
        WalOpType op = static_cast<WalOpType>(payload[off++]);

        uint16_t key_len = payload[off] | (payload[off + 1] << 8);
        off += 2;

        std::string key(reinterpret_cast<char *>(&payload[off]), key_len);
        off += key_len;

        uint32_t val_len = payload[off] | (payload[off + 1] << 8) |
                           (payload[off + 2] << 16) | (payload[off + 3] << 24);
        off += 4;

        std::string val(reinterpret_cast<char *>(&payload[off]), val_len);

        records.push_back({op, std::move(key), std::move(val)});
    }

    return records;
}
