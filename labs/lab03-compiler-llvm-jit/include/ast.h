#ifndef AST_H
#define AST_H

#include <string>
#include <vector>
#include <memory>

class ASTNode {
public:
    virtual ~ASTNode() = default;
};

class ExprAST : public ASTNode {};

class NumberExprAST : public ExprAST {
public:
    explicit NumberExprAST(double val) : value(val) {}
    double value;
};

class VariableExprAST : public ExprAST {
public:
    explicit VariableExprAST(std::string n) : name(std::move(n)) {}
    std::string name;
};

class BinaryExprAST : public ExprAST {
public:
    BinaryExprAST(std::string op_str, std::unique_ptr<ExprAST> l, std::unique_ptr<ExprAST> r)
        : op(std::move(op_str)), lhs(std::move(l)), rhs(std::move(r)) {}
    std::string op;
    std::unique_ptr<ExprAST> lhs;
    std::unique_ptr<ExprAST> rhs;
};

class CallExprAST : public ExprAST {
public:
    CallExprAST(std::string callee_name, std::vector<std::unique_ptr<ExprAST>> arguments)
        : callee(std::move(callee_name)), args(std::move(arguments)) {}
    std::string callee;
    std::vector<std::unique_ptr<ExprAST>> args;
};

class StmtAST : public ASTNode {};

class ExprStmtAST : public StmtAST {
public:
    explicit ExprStmtAST(std::unique_ptr<ExprAST> e) : expr(std::move(e)) {}
    std::unique_ptr<ExprAST> expr;
};

class VarDeclStmtAST : public StmtAST {
public:
    VarDeclStmtAST(std::string n, std::unique_ptr<ExprAST> init_e)
        : name(std::move(n)), init(std::move(init_e)) {}
    std::string name;
    std::unique_ptr<ExprAST> init;
};

class AssignStmtAST : public StmtAST {
public:
    AssignStmtAST(std::string n, std::unique_ptr<ExprAST> v)
        : name(std::move(n)), val(std::move(v)) {}
    std::string name;
    std::unique_ptr<ExprAST> val;
};

class BlockStmtAST : public StmtAST {
public:
    explicit BlockStmtAST(std::vector<std::unique_ptr<StmtAST>> stmts)
        : statements(std::move(stmts)) {}
    std::vector<std::unique_ptr<StmtAST>> statements;
};

class IfStmtAST : public StmtAST {
public:
    IfStmtAST(std::unique_ptr<ExprAST> c, std::unique_ptr<StmtAST> t, std::unique_ptr<StmtAST> e)
        : cond(std::move(c)), then_branch(std::move(t)), else_branch(std::move(e)) {}
    std::unique_ptr<ExprAST> cond;
    std::unique_ptr<StmtAST> then_branch;
    std::unique_ptr<StmtAST> else_branch;
};

class WhileStmtAST : public StmtAST {
public:
    WhileStmtAST(std::unique_ptr<ExprAST> c, std::unique_ptr<StmtAST> b)
        : cond(std::move(c)), body(std::move(b)) {}
    std::unique_ptr<ExprAST> cond;
    std::unique_ptr<StmtAST> body;
};

class ReturnStmtAST : public StmtAST {
public:
    explicit ReturnStmtAST(std::unique_ptr<ExprAST> e) : expr(std::move(e)) {}
    std::unique_ptr<ExprAST> expr;
};

class FunctionAST : public ASTNode {
public:
    FunctionAST(std::string n, std::vector<std::string> p, std::unique_ptr<BlockStmtAST> b)
        : name(std::move(n)), params(std::move(p)), body(std::move(b)) {}
    std::string name;
    std::vector<std::string> params;
    std::unique_ptr<BlockStmtAST> body;
};

class ProgramAST : public ASTNode {
public:
    std::vector<std::unique_ptr<FunctionAST>> functions;
    std::vector<std::unique_ptr<StmtAST>> top_level_stmts;
};

#endif /* AST_H */
