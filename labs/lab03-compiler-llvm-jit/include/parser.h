#ifndef PARSER_H
#define PARSER_H

#include <vector>
#include <memory>
#include "token.h"
#include "ast.h"

class Parser {
public:
    explicit Parser(std::vector<Token> tokens);
    std::unique_ptr<ProgramAST> parse_program();
    std::unique_ptr<ExprAST> parse_expression();

private:
    const Token &peek() const;
    const Token &previous() const;
    bool is_at_end() const;
    const Token &advance();
    bool check(TokenType type) const;
    bool match(TokenType type);
    const Token &consume(TokenType type, const std::string &err_msg);

    std::unique_ptr<FunctionAST> parse_function();
    std::unique_ptr<StmtAST> parse_statement();
    std::unique_ptr<StmtAST> parse_let_statement();
    std::unique_ptr<StmtAST> parse_if_statement();
    std::unique_ptr<StmtAST> parse_while_statement();
    std::unique_ptr<StmtAST> parse_return_statement();
    std::unique_ptr<BlockStmtAST> parse_block();

    std::unique_ptr<ExprAST> parse_pratt_expr(int min_prec);
    std::unique_ptr<ExprAST> parse_primary();
    int get_precedence(TokenType type) const;

    std::vector<Token> tokens_;
    size_t cursor_;
};

#endif /* PARSER_H */
