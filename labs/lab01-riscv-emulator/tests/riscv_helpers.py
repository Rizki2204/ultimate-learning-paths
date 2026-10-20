import subprocess
import json
import os
import struct

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXE_PATH = os.path.join(PROJECT_DIR, "riscv_emu.exe" if os.name == "nt" else "riscv_emu")

def ensure_compiled():
    if not os.path.exists(EXE_PATH):
        cmd = ["gcc", "-Wall", "-Wextra", "-std=c99", "-O2", "-Iinclude",
               "src/mmu.c", "src/instructions.c", "src/cpu.c", "src/main.c", "-o", EXE_PATH]
        subprocess.check_call(cmd, cwd=PROJECT_DIR)

def r_type(opcode, rd, funct3, rs1, rs2, funct7):
    val = (opcode & 0x7F) | ((rd & 0x1F) << 7) | ((funct3 & 0x07) << 12) | \
          ((rs1 & 0x1F) << 15) | ((rs2 & 0x1F) << 20) | ((funct7 & 0x7F) << 25)
    return struct.pack("<I", val)

def i_type(opcode, rd, funct3, rs1, imm):
    val = (opcode & 0x7F) | ((rd & 0x1F) << 7) | ((funct3 & 0x07) << 12) | \
          ((rs1 & 0x1F) << 15) | ((imm & 0xFFF) << 20)
    return struct.pack("<I", val)

def s_type(opcode, funct3, rs1, rs2, imm):
    imm_4_0 = imm & 0x1F
    imm_11_5 = (imm >> 5) & 0x7F
    val = (opcode & 0x7F) | (imm_4_0 << 7) | ((funct3 & 0x07) << 12) | \
          ((rs1 & 0x1F) << 15) | ((rs2 & 0x1F) << 20) | (imm_11_5 << 25)
    return struct.pack("<I", val)

def b_type(opcode, funct3, rs1, rs2, imm):
    b12 = (imm >> 12) & 1
    b11 = (imm >> 11) & 1
    b10_5 = (imm >> 5) & 0x3F
    b4_1 = (imm >> 1) & 0x0F
    val = (opcode & 0x7F) | (b11 << 7) | (b4_1 << 8) | ((funct3 & 0x07) << 12) | \
          ((rs1 & 0x1F) << 15) | ((rs2 & 0x1F) << 20) | (b10_5 << 25) | (b12 << 31)
    return struct.pack("<I", val)

def u_type(opcode, rd, imm):
    val = (opcode & 0x7F) | ((rd & 0x1F) << 7) | (imm & 0xFFFFF000)
    return struct.pack("<I", val)

def j_type(opcode, rd, imm):
    j20 = (imm >> 20) & 1
    j19_12 = (imm >> 12) & 0xFF
    j11 = (imm >> 11) & 1
    j10_1 = (imm >> 1) & 0x3FF
    val = (opcode & 0x7F) | ((rd & 0x1F) << 7) | (j19_12 << 12) | (j11 << 20) | (j10_1 << 21) | (j20 << 31)
    return struct.pack("<I", val)

def run_hex_code(code_bytes, max_cycles=1000):
    ensure_compiled()
    hex_str = code_bytes.hex()
    res = subprocess.check_output([EXE_PATH, "--exec-hex", hex_str, str(max_cycles)], cwd=PROJECT_DIR)
    return json.loads(res.decode("utf-8"))
