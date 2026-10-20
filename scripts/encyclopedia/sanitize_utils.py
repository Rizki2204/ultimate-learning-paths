# -*- coding: utf-8 -*-
"""
Sanitization utilities for KaTeX math and Markdown formatting.
Handles escaping of stray currency dollar signs, shell prompts,
and proper code block language fencing.
"""

import re

def sanitize_dollar_signs(text: str) -> str:
    """
    Escapes currency dollar signs (e.g., $600, $440, $0.023/GB) and shell prompts ($ cmd)
    without corrupting valid KaTeX math ($x$, $$\\int$$, $2^3 = 8$, etc.).
    """
    lines = text.split("\n")
    cleaned_lines = []
    
    in_code_block = False
    
    for line in lines:
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            cleaned_lines.append(line)
            continue
            
        if in_code_block:
            cleaned_lines.append(line)
            continue
            
        # 1. Inside Mermaid diagrams, replace $ with USD
        if "-->" in line or "flowchart" in line or "graph" in line or "subgraph" in line or '["' in line:
            line = re.sub(r'(?<!\\)\$(\d+)', r'USD \1', line)

        # 2. Shell prompt: $ cmd -> \$ cmd
        line = re.sub(r'(^|[\s\"\'\(])\$\s+([a-zA-Z0-9_\-\./]+)', r'\1\\$ \2', line)

        # 3. Currency with explicit units or keywords:
        # e.g. $600/kWh, $0.023/GB/bulan, $1.5 miliar, $10.000, $64 Juta
        line = re.sub(
            r'(?<![\\\$])\$(\d+(?:[.,]\d+)?\s*(?:/|kWh|GB|bulan|miliar|juta|ribu|Juta|Miliar|USD))',
            r'\\$\1',
            line
        )

        # 4. Currency preceded by context words like senilai, biaya, anggaran, sebesar, penghematan, modal, harga:
        line = re.sub(
            r'((?:senilai|biaya|anggaran|sebesar|penghematan|modal|harga|keuntungan|rugi|mencapai)\s+)(?<!\\)\$(\d+)',
            r'\1\\$\2',
            line,
            flags=re.IGNORECASE
        )

        # 5. Currency amounts in parentheses or diffs: ($100), (+$50), ($150)
        line = re.sub(r'([\(\s\+\-])(?<!\\)\$(\d{2,}(?:[.,]\d{3})*)(\b|[\),\s])', r'\1\\$\2\3', line)

        cleaned_lines.append(line)
        
    return "\n".join(cleaned_lines)


def detect_code_language(code: str) -> str:
    """
    Infers the programming language of an unfenced code block.
    """
    ld_indicators = ["ENTRY(", "MEMORY\n", "SECTIONS\n", "MEMORY {", "SECTIONS {", "linker_script"]
    c_indicators = ["#include", "int main", "typedef struct", "uint32_t", "int16_t", "int32_t", "size_t", "printf(", "/*", "void "]
    cpp_indicators = ["std::", "template<", "class ", "public:", "nullptr"]
    rust_indicators = ["fn ", "let mut ", "impl ", "match ", "println!"]
    verilog_indicators = ["module ", "always @", "wire ", "reg ", "posedge ", "endmodule"]
    sql_indicators = ["SELECT ", "CREATE TABLE ", "INSERT INTO ", "JOIN ", "GROUP BY "]
    bash_indicators = ["#!/bin/bash", "grep ", "awk ", "sed ", "echo ", "export "]
    
    if any(ind in code for ind in ld_indicators):
        return "c"
    if any(ind in code for ind in verilog_indicators):
        return "verilog"
    if any(ind in code for ind in rust_indicators):
        return "rust"
    if any(ind in code for ind in c_indicators):
        if any(ind in code for ind in cpp_indicators):
            return "cpp"
        return "c"
    if any(ind in code for ind in sql_indicators):
        return "sql"
    if any(ind in code for ind in bash_indicators):
        return "bash"
    return "python"


def fence_code_block(code: str) -> str:
    """
    Ensures a code block has valid markdown code fences.
    """
    code_stripped = code.strip()
    if code_stripped.startswith("```"):
        return code_stripped
        
    lang = detect_code_language(code_stripped)
    return f"```{lang}\n{code_stripped}\n```"
