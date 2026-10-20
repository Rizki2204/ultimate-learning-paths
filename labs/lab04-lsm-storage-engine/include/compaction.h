#ifndef COMPACTION_H
#define COMPACTION_H

#include <vector>
#include <string>
#include <memory>
#include "sstable.h"

class Compactor {
public:
    static bool compact_sstables(const std::vector<std::shared_ptr<SSTable>> &tables,
                                 const std::string &output_filepath,
                                 bool is_bottommost_level = true);
};

#endif /* COMPACTION_H */
