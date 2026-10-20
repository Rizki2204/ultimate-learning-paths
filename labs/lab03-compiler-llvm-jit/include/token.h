#ifndef TOKEN_H
#define TOKEN_H

#include <string>

enum class TokenType {
    TOKEN_EOF = 0,
    TOKEN_INT,
    TOKEN_FLOAT,
    TOKEN_IDENT,
    /* Keywords */
    TOKEN_LET,
    TOKEN_FN,
    TOKEN_IF,
    TOKEN_ELSE,
    TOKEN_WHILE,
    TOKEN_RETURN,
    /* Operators */
    TOKEN_PLUS,
    TOKEN_MINUS,
    TOKEN_STAR,
    TOKEN_SLASH,
    TOKEN_PERCENT,
    TOKEN_ASSIGN,
    TOKEN_EQ_EQ,
    TOKEN_BANG_EQ,
    TOKEN_LT,
    TOKEN_LT_EQ,
    TOKEN_GT,
    TOKEN_GT_EQ,
    /* Delimiters */
    TOKEN_LPAREN,
    TOKEN_RPAREN,
    TOKEN_LBRACE,
    TOKEN_RBRACE,
    TOKEN_COMMA,
    TOKEN_SEMICOLON
};

struct Token {
    TokenType type;
    std::string text;
    double number_value;
    int line;
    int col;

    Token() : type(TokenType::TOKEN_EOF), number_value(0.0), line(1), col(1) {}
    Token(TokenType t, std::string txt, double val, int l, int c)
        : type(t), text(std::move(txt)), number_value(val), line(l), col(c) {}
};

#endif /* TOKEN_H */
