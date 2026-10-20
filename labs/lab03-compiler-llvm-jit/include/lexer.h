#ifndef LEXER_H
#define LEXER_H

#include <string>
#include <vector>
#include "token.h"

class Lexer {
public:
    explicit Lexer(std::string source);
    std::vector<Token> tokenize();

private:
    char peek() const;
    char advance();
    bool match(char expected);
    bool is_at_end() const;
    void skip_whitespace();

    Token scan_token();
    Token scan_number();
    Token scan_identifier();

    std::string src_;
    size_t cursor_;
    int line_;
    int col_;
};

#endif /* LEXER_H */
