"""
Hack Assembler for nand2tetris Project 6
Converts .asm files to .hack binary files
"""

import os
import sys

COMP_TABLE = {
    "0":   "0101010",
    "1":   "0111111",
    "-1":  "0111010",
    "D":   "0001100",
    "A":   "0110000",
    "M":   "1110000",
    "!D":  "0001101",
    "!A":  "0110001",
    "!M":  "1110001",
    "-D":  "0001111",
    "-A":  "0110011",
    "-M":  "1110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "M+1": "1110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "M-1": "1110010",
    "D+A": "0000010",
    "D+M": "1000010",
    "D-A": "0010011",
    "D-M": "1010011",
    "A-D": "0000111",
    "M-D": "1000111",
    "D&A": "0000000",
    "D&M": "1000000",
    "D|A": "0010101",
    "D|M": "1010101",
}

DEST_TABLE = {
    None:  "000",
    "M":   "001",
    "D":   "010",
    "MD":  "011", "DM": "011",
    "A":   "100",
    "AM":  "101", "MA": "101",
    "AD":  "110", "DA": "110",
    "AMD": "111", "ADM": "111",
}

JUMP_TABLE = {
    None:  "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111",
}


def main():
    # Hardcoded test file for now
    input_filename = "add.asm"
    input_path = os.path.join("test_cases", input_filename)

    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found. Please add test files to test_cases/")
        sys.exit(1)

    output_filename = input_filename.replace(".asm", ".hack")
    output_path = os.path.join("output", output_filename)

    with open(input_path, "r") as f:
        raw_lines = f.readlines()

    # 1) Clean lines
    cleaned = clean_lines(raw_lines)
    print(f"Cleaned {len(raw_lines)} lines to {len(cleaned)} instructions")

    # 2) First pass: build symbol table
    symbol_table = first_pass_build_symbol_table(cleaned)
    print("First pass complete. Symbols:", len(symbol_table))

    # 3) Second pass: placeholder translation
    binary_lines = second_pass_translate(cleaned, symbol_table)
    print(f"Second pass complete. Generated {len(binary_lines)} binary instructions")

    # 4) Write output
    os.makedirs("output", exist_ok=True)
    with open(output_path, "w") as f:
        for line in binary_lines:
            f.write(line + "\n")

    print(f"Assembler complete. Output written to {output_path}")




def clean_lines(raw_lines):
    """
    Remove comments, whitespace, and empty lines from assembly code.
    """
    cleaned = []
    for line in raw_lines:
        # Remove everything after // (comments)
        if "//" in line:
            line = line.split("//")[0]

        # Remove leading/trailing whitespace
        line = line.strip()

        # Only keep non-empty lines
        if line:
            cleaned.append(line)

    return cleaned


def first_pass_build_symbol_table(clean_lines_list):
    """
    Build the initial symbol table.
    Adds predefined symbols and records label definitions.

    Args:
        clean_lines_list: list of cleaned assembly lines (no comments/blank lines)

    Returns:
        Dictionary mapping symbol names to numeric addresses
    """
    symbols = {
        "SP": 0,
        "LCL": 1,
        "ARG": 2,
        "THIS": 3,
        "THAT": 4,
        "SCREEN": 16384,
        "KBD": 24576,
    }

    # General-purpose registers R0–R15
    for i in range(16):
        symbols[f"R{i}"] = i

    instruction_address = 0  # ROM address (only real instructions)

    for line in clean_lines_list:
        if line.startswith("(") and line.endswith(")"):
            # Label declaration, e.g. (LOOP)
            label_name = line[1:-1]
            # Record the address of the next instruction
            symbols[label_name] = instruction_address
        else:
            # Real instruction (A- or C-instruction)
            instruction_address += 1

    return symbols

def translate_a_instruction(line, symbol_table, next_variable_address):
    """
    Translate an A-instruction into 16-bit binary.
    Handles:
      - @number
      - @label (predefined or from first pass)
      - @variable (new symbols starting at address 16)
    """
    symbol = line[1:]  # strip '@'

    # Case 1: literal number
    if symbol.isdigit():
        address = int(symbol)

    # Case 2: in symbol table already
    elif symbol in symbol_table:
        address = symbol_table[symbol]

    # Case 3: new variable
    else:
        symbol_table[symbol] = next_variable_address[0]
        address = next_variable_address[0]
        next_variable_address[0] += 1

    return format(address, "016b")




def second_pass_translate(clean_lines_list, symbol_table):
    """
    Second pass: translate A- and C-instructions to binary.
    """
    binary_instructions = []
    next_variable_address = [16]  # next free RAM address for variables

    for line in clean_lines_list:
        if line.startswith("(") and line.endswith(")"):
            continue

        if line.startswith("@"):
            binary = translate_a_instruction(line, symbol_table, next_variable_address)
        else:
            binary = "1" * 16  # temporary C-instruction placeholder

        binary_instructions.append(binary)

    return binary_instructions



if __name__ == "__main__":
    main()
