"""
Hack Assembler for nand2tetris Project 6
Converts .asm files to .hack binary files
"""

import os
import sys


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

def translate_a_instruction(line, symbol_table):
    """
    Translate an A-instruction (e.g. @21) into a 16-bit binary string.
    For now, handle only numeric constants.
    """
    symbol = line[1:]  # strip '@'
    if symbol.isdigit():
        address = int(symbol)
    else:
        # Symbolic A-instruction (@LOOP, @i) will be handled later
        address = 0  # temporary placeholder

    return format(address, "016b")



def second_pass_translate(clean_lines_list, symbol_table):
    """
    Perform the second pass: translate A- and C-instructions to binary.
    Label declarations are skipped.

    Args:
        clean_lines_list: list of cleaned assembly lines
        symbol_table: dictionary of symbols to addresses

    Returns:
        List of 16-bit binary instruction strings
    """
    binary_instructions = []

    for line in clean_lines_list:
        # Skip label declarations like (LOOP)
        if line.startswith("(") and line.endswith(")"):
            continue

        if line.startswith("@"):
            # A-instruction: will handle translation in a later step
            # Placeholder for now
            binary = translate_a_instruction(line, symbol_table)
        else:
            # C-instruction: will handle translation in a later step
            binary = "1" * 16

        binary_instructions.append(binary)

    return binary_instructions


if __name__ == "__main__":
    main()
