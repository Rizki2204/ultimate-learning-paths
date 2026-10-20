#include <iostream>
#include <string>
#include <cstring>
#include "lexer.h"
#include "parser.h"
#include "bytecode.h"
#include "vm.h"

static int test_lexer() {
    Lexer lexer("let x = 42 + 3.14 * (10 - 2);");
    auto tokens = lexer.tokenize();
    if (tokens.size() < 12) return 1;
    if (tokens[0].type != TokenType::TOKEN_LET) return 2;
    if (tokens[1].text != "x") return 3;
    if (tokens[3].number_value != 42.0) return 4;
    return 0;
}

static int test_parser() {
    Lexer lexer("2 + 3 * 4;");
    Parser parser(lexer.tokenize());
    auto prog = parser.parse_program();
    if (prog->top_level_stmts.empty()) return 1;
    return 0;
}

static int test_vm() {
    /* Test evaluating: let a = 10; let b = 20; a + b; */
    Lexer lexer("let a = 10; let b = 20; a + b;");
    Parser parser(lexer.tokenize());
    auto prog = parser.parse_program();

    Chunk chunk;
    BytecodeCompiler compiler;
    compiler.compile(*prog, chunk);

    VM vm;
    if (vm.run(chunk) != VMResult::OK) return 1;
    if (vm.get_last_result() != 30.0) return 2;
    return 0;
}

int main(int argc, char **argv) {
    if (argc < 2) {
        std::cout << "Usage: " << argv[0] << " [--eval <code> | --test-lexer | --test-parser | --test-vm | --test-all]\n";
        return 0;
    }

    if (std::strcmp(argv[1], "--test-lexer") == 0) {
        int r = test_lexer();
        std::cout << "lexer_test: " << (r == 0 ? "PASS" : "FAIL") << "\n";
        return r;
    }

    if (std::strcmp(argv[1], "--test-parser") == 0) {
        int r = test_parser();
        std::cout << "parser_test: " << (r == 0 ? "PASS" : "FAIL") << "\n";
        return r;
    }

    if (std::strcmp(argv[1], "--test-vm") == 0) {
        int r = test_vm();
        std::cout << "vm_test: " << (r == 0 ? "PASS" : "FAIL") << "\n";
        return r;
    }

    if (std::strcmp(argv[1], "--test-all") == 0) {
        int l = test_lexer();
        int p = test_parser();
        int v = test_vm();
        int total = l + p + v;
        std::cout << "{\"lexer\": " << l << ", \"parser\": " << p << ", \"vm\": " << v << "}\n";
        return total == 0 ? 0 : 1;
    }

    if (std::strcmp(argv[1], "--eval") == 0 && argc >= 3) {
        try {
            Lexer lexer(argv[2]);
            Parser parser(lexer.tokenize());
            auto prog = parser.parse_program();

            Chunk chunk;
            BytecodeCompiler compiler;
            compiler.compile(*prog, chunk);

            VM vm;
            VMResult res = vm.run(chunk);
            if (res == VMResult::OK) {
                std::cout << "{\"status\": \"OK\", \"result\": " << vm.get_last_result() << "}\n";
                return 0;
            } else {
                std::cout << "{\"status\": \"RUNTIME_ERROR\", \"result\": 0}\n";
                return 1;
            }
        } catch (const std::exception &e) {
            std::cout << "{\"status\": \"ERROR\", \"message\": \"" << e.what() << "\"}\n";
            return 1;
        }
    }

    return 1;
}
