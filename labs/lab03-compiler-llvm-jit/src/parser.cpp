#include <stdexcept>
#include "parser.h"

Parser::Parser(std::vector<Token> tokens)
    : tokens_(std::move(tokens)), cursor_(0) {}

const Token &Parser::peek() const {
    if (cursor_ >= tokens_.size()) return tokens_.back();
    return tokens_[cursor_];
}

const Token &Parser::previous() const {
    if (cursor_ == 0) return tokens_[0];
    return tokens_[cursor_ - 1];
}

bool Parser::is_at_end() const {
    return peek().type == TokenType::TOKEN_EOF;
}

const Token &Parser::advance() {
    if (!is_at_end()) cursor_++;
    return previous();
}

bool Parser::check(TokenType type) const {
    if (is_at_end()) return false;
    return peek().type == type;
}

bool Parser::match(TokenType type) {
    if (check(type)) {
        advance();
        return true;
    }
    return false;
}

const Token &Parser::consume(TokenType type, const std::string &err_msg) {
    if (check(type)) return advance();
    throw std::runtime_error("Parser Error: " + err_msg);
}

int Parser::get_precedence(TokenType type) const {
    switch (type) {
        case TokenType::TOKEN_EQ_EQ:
        case TokenType::TOKEN_BANG_EQ:
            return 1;
        case TokenType::TOKEN_LT:
        case TokenType::TOKEN_LT_EQ:
        case TokenType::TOKEN_GT:
        case TokenType::TOKEN_GT_EQ:
            return 2;
        case TokenType::TOKEN_PLUS:
        case TokenType::TOKEN_MINUS:
            return 3;
        case TokenType::TOKEN_STAR:
        case TokenType::TOKEN_SLASH:
        case TokenType::TOKEN_PERCENT:
            return 4;
        default:
            return 0;
    }
}

std::unique_ptr<ExprAST> Parser::parse_primary() {
    if (match(TokenType::TOKEN_INT) || match(TokenType::TOKEN_FLOAT)) {
        return std::unique_ptr<ExprAST>(new NumberExprAST(previous().number_value));
    }
    if (match(TokenType::TOKEN_IDENT)) {
        std::string name = previous().text;
        if (match(TokenType::TOKEN_LPAREN)) {
            /* Function call */
            std::vector<std::unique_ptr<ExprAST>> args;
            if (!check(TokenType::TOKEN_RPAREN)) {
                do {
                    args.push_back(parse_expression());
                } while (match(TokenType::TOKEN_COMMA));
            }
            consume(TokenType::TOKEN_RPAREN, "Expected ')' after argument list");
            return std::unique_ptr<ExprAST>(new CallExprAST(name, std::move(args)));
        }
        return std::unique_ptr<ExprAST>(new VariableExprAST(name));
    }
    if (match(TokenType::TOKEN_LPAREN)) {
        auto expr = parse_expression();
        consume(TokenType::TOKEN_RPAREN, "Expected ')' after grouped expression");
        return expr;
    }
    if (match(TokenType::TOKEN_MINUS)) {
        /* Unary negation: 0 - primary */
        auto zero = std::unique_ptr<ExprAST>(new NumberExprAST(0.0));
        auto rhs = parse_primary();
        return std::unique_ptr<ExprAST>(new BinaryExprAST("-", std::move(zero), std::move(rhs)));
    }
    throw std::runtime_error("Parser Error: Unexpected token " + peek().text);
}

std::unique_ptr<ExprAST> Parser::parse_pratt_expr(int min_prec) {
    auto lhs = parse_primary();

    while (true) {
        TokenType op_type = peek().type;
        int prec = get_precedence(op_type);
        if (prec < min_prec || prec == 0) break;

        advance(); /* consume operator */
        std::string op_text = previous().text;

        /* Left-associative: recurse with prec + 1 */
        auto rhs = parse_pratt_expr(prec + 1);
        lhs = std::unique_ptr<ExprAST>(new BinaryExprAST(op_text, std::move(lhs), std::move(rhs)));
    }

    return lhs;
}

std::unique_ptr<ExprAST> Parser::parse_expression() {
    return parse_pratt_expr(1);
}

std::unique_ptr<StmtAST> Parser::parse_let_statement() {
    const Token &name_tok = consume(TokenType::TOKEN_IDENT, "Expected variable name after 'let'");
    consume(TokenType::TOKEN_ASSIGN, "Expected '=' in variable declaration");
    auto init_val = parse_expression();
    consume(TokenType::TOKEN_SEMICOLON, "Expected ';' after let statement");
    return std::unique_ptr<StmtAST>(new VarDeclStmtAST(name_tok.text, std::move(init_val)));
}

std::unique_ptr<StmtAST> Parser::parse_if_statement() {
    consume(TokenType::TOKEN_LPAREN, "Expected '(' after 'if'");
    auto cond = parse_expression();
    consume(TokenType::TOKEN_RPAREN, "Expected ')' after if condition");
    auto then_branch = parse_statement();
    std::unique_ptr<StmtAST> else_branch = nullptr;
    if (match(TokenType::TOKEN_ELSE)) {
        else_branch = parse_statement();
    }
    return std::unique_ptr<StmtAST>(new IfStmtAST(std::move(cond), std::move(then_branch), std::move(else_branch)));
}

std::unique_ptr<StmtAST> Parser::parse_while_statement() {
    consume(TokenType::TOKEN_LPAREN, "Expected '(' after 'while'");
    auto cond = parse_expression();
    consume(TokenType::TOKEN_RPAREN, "Expected ')' after while condition");
    auto body = parse_statement();
    return std::unique_ptr<StmtAST>(new WhileStmtAST(std::move(cond), std::move(body)));
}

std::unique_ptr<StmtAST> Parser::parse_return_statement() {
    std::unique_ptr<ExprAST> expr = nullptr;
    if (!check(TokenType::TOKEN_SEMICOLON)) {
        expr = parse_expression();
    }
    consume(TokenType::TOKEN_SEMICOLON, "Expected ';' after return");
    return std::unique_ptr<StmtAST>(new ReturnStmtAST(std::move(expr)));
}

std::unique_ptr<BlockStmtAST> Parser::parse_block() {
    consume(TokenType::TOKEN_LBRACE, "Expected '{'");
    std::vector<std::unique_ptr<StmtAST>> stmts;
    while (!check(TokenType::TOKEN_RBRACE) && !is_at_end()) {
        stmts.push_back(parse_statement());
    }
    consume(TokenType::TOKEN_RBRACE, "Expected '}'");
    return std::unique_ptr<BlockStmtAST>(new BlockStmtAST(std::move(stmts)));
}

std::unique_ptr<StmtAST> Parser::parse_statement() {
    if (match(TokenType::TOKEN_LET)) return parse_let_statement();
    if (match(TokenType::TOKEN_IF)) return parse_if_statement();
    if (match(TokenType::TOKEN_WHILE)) return parse_while_statement();
    if (match(TokenType::TOKEN_RETURN)) return parse_return_statement();
    if (check(TokenType::TOKEN_LBRACE)) return parse_block();

    if (check(TokenType::TOKEN_IDENT) && cursor_ + 1 < tokens_.size() && tokens_[cursor_ + 1].type == TokenType::TOKEN_ASSIGN) {
        std::string name = advance().text;
        advance(); /* consume '=' */
        auto val = parse_expression();
        consume(TokenType::TOKEN_SEMICOLON, "Expected ';' after assignment");
        return std::unique_ptr<StmtAST>(new AssignStmtAST(name, std::move(val)));
    }

    auto expr = parse_expression();
    consume(TokenType::TOKEN_SEMICOLON, "Expected ';' after expression statement");
    return std::unique_ptr<StmtAST>(new ExprStmtAST(std::move(expr)));
}

std::unique_ptr<FunctionAST> Parser::parse_function() {
    consume(TokenType::TOKEN_FN, "Expected 'fn'");
    const Token &name_tok = consume(TokenType::TOKEN_IDENT, "Expected function name");
    consume(TokenType::TOKEN_LPAREN, "Expected '('");
    std::vector<std::string> params;
    if (!check(TokenType::TOKEN_RPAREN)) {
        do {
            const Token &p = consume(TokenType::TOKEN_IDENT, "Expected parameter name");
            params.push_back(p.text);
        } while (match(TokenType::TOKEN_COMMA));
    }
    consume(TokenType::TOKEN_RPAREN, "Expected ')'");
    auto body = parse_block();
    return std::unique_ptr<FunctionAST>(new FunctionAST(name_tok.text, std::move(params), std::move(body)));
}

std::unique_ptr<ProgramAST> Parser::parse_program() {
    auto prog = std::unique_ptr<ProgramAST>(new ProgramAST());
    while (!is_at_end()) {
        if (check(TokenType::TOKEN_FN)) {
            prog->functions.push_back(parse_function());
        } else {
            prog->top_level_stmts.push_back(parse_statement());
        }
    }
    return prog;
}
