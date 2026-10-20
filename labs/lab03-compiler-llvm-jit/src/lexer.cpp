#include <cctype>
#include <cstdlib>
#include "lexer.h"

Lexer::Lexer(std::string source)
    : src_(std::move(source)), cursor_(0), line_(1), col_(1) {}

char Lexer::peek() const {
    if (is_at_end()) return '\0';
    return src_[cursor_];
}

char Lexer::advance() {
    if (is_at_end()) return '\0';
    char c = src_[cursor_++];
    col_++;
    return c;
}

bool Lexer::match(char expected) {
    if (is_at_end() || src_[cursor_] != expected) return false;
    cursor_++;
    col_++;
    return true;
}

bool Lexer::is_at_end() const {
    return cursor_ >= src_.size();
}

void Lexer::skip_whitespace() {
    while (!is_at_end()) {
        char c = peek();
        if (c == ' ' || c == '\t' || c == '\r') {
            advance();
        } else if (c == '\n') {
            line_++;
            col_ = 1;
            advance();
        } else if (c == '/' && cursor_ + 1 < src_.size() && src_[cursor_ + 1] == '/') {
            /* Single line comment: skip until newline */
            while (!is_at_end() && peek() != '\n') advance();
        } else {
            break;
        }
    }
}

Token Lexer::scan_token() {
    skip_whitespace();
    if (is_at_end()) {
        return Token(TokenType::TOKEN_EOF, "", 0.0, line_, col_);
    }

    int start_col = col_;
    char c = advance();

    if (std::isdigit(c)) {
        cursor_--;
        col_--;
        return scan_number();
    }

    if (std::isalpha(c) || c == '_') {
        cursor_--;
        col_--;
        return scan_identifier();
    }

    switch (c) {
        case '+': return Token(TokenType::TOKEN_PLUS, "+", 0.0, line_, start_col);
        case '-': return Token(TokenType::TOKEN_MINUS, "-", 0.0, line_, start_col);
        case '*': return Token(TokenType::TOKEN_STAR, "*", 0.0, line_, start_col);
        case '/': return Token(TokenType::TOKEN_SLASH, "/", 0.0, line_, start_col);
        case '%': return Token(TokenType::TOKEN_PERCENT, "%", 0.0, line_, start_col);
        case '(': return Token(TokenType::TOKEN_LPAREN, "(", 0.0, line_, start_col);
        case ')': return Token(TokenType::TOKEN_RPAREN, ")", 0.0, line_, start_col);
        case '{': return Token(TokenType::TOKEN_LBRACE, "{", 0.0, line_, start_col);
        case '}': return Token(TokenType::TOKEN_RBRACE, "}", 0.0, line_, start_col);
        case ',': return Token(TokenType::TOKEN_COMMA, ",", 0.0, line_, start_col);
        case ';': return Token(TokenType::TOKEN_SEMICOLON, ";", 0.0, line_, start_col);
        case '=':
            if (match('=')) return Token(TokenType::TOKEN_EQ_EQ, "==", 0.0, line_, start_col);
            return Token(TokenType::TOKEN_ASSIGN, "=", 0.0, line_, start_col);
        case '!':
            if (match('=')) return Token(TokenType::TOKEN_BANG_EQ, "!=", 0.0, line_, start_col);
            break;
        case '<':
            if (match('=')) return Token(TokenType::TOKEN_LT_EQ, "<=", 0.0, line_, start_col);
            return Token(TokenType::TOKEN_LT, "<", 0.0, line_, start_col);
        case '>':
            if (match('=')) return Token(TokenType::TOKEN_GT_EQ, ">=", 0.0, line_, start_col);
            return Token(TokenType::TOKEN_GT, ">", 0.0, line_, start_col);
        default:
            break;
    }

    return Token(TokenType::TOKEN_EOF, "", 0.0, line_, start_col);
}

Token Lexer::scan_number() {
    int start_col = col_;
    size_t start_pos = cursor_;
    bool is_float = false;

    while (!is_at_end() && std::isdigit(peek())) advance();
    if (!is_at_end() && peek() == '.' && cursor_ + 1 < src_.size() && std::isdigit(src_[cursor_ + 1])) {
        is_float = true;
        advance(); /* Consume '.' */
        while (!is_at_end() && std::isdigit(peek())) advance();
    }

    std::string text = src_.substr(start_pos, cursor_ - start_pos);
    double val = std::strtod(text.c_str(), nullptr);
    TokenType type = is_float ? TokenType::TOKEN_FLOAT : TokenType::TOKEN_INT;
    return Token(type, text, val, line_, start_col);
}

Token Lexer::scan_identifier() {
    int start_col = col_;
    size_t start_pos = cursor_;

    while (!is_at_end() && (std::isalnum(peek()) || peek() == '_')) advance();

    std::string text = src_.substr(start_pos, cursor_ - start_pos);
    TokenType type = TokenType::TOKEN_IDENT;

    if (text == "let") type = TokenType::TOKEN_LET;
    else if (text == "fn") type = TokenType::TOKEN_FN;
    else if (text == "if") type = TokenType::TOKEN_IF;
    else if (text == "else") type = TokenType::TOKEN_ELSE;
    else if (text == "while") type = TokenType::TOKEN_WHILE;
    else if (text == "return") type = TokenType::TOKEN_RETURN;

    return Token(type, text, 0.0, line_, start_col);
}

std::vector<Token> Lexer::tokenize() {
    std::vector<Token> tokens;
    while (true) {
        Token tok = scan_token();
        tokens.push_back(tok);
        if (tok.type == TokenType::TOKEN_EOF) break;
    }
    return tokens;
}
