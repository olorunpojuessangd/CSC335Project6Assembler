"""
Hack Assembler for nand2tetris Project 6
Converts .asm files to .hack binary files
"""

import os
import sys


def main():
    """
    Main entry point for the assembler.
    Reads .asm from test_cases/, writes .hack to output/.
    """
    # Currently using a hard coded test file
    input_filename = "Max1.asm"
    input_path = os.path.join("test_cases", input_filename)

    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found. Please add test files to test_cases/")
        sys.exit(1)

    # Setup for the output path
    output_filename = input_filename.replace(".asm", ".hack")
    output_path = os.path.join("output", output_filename)

    # Read input file
    with open(input_path, "r") as f:
        raw_lines = f.readlines()

    # Process the assembly code
        cleaned = clean_lines(raw_lines)
        print(f"Cleaned {len(raw_lines)} lines to {len(cleaned)} instructions")

    # TODO: Next commits will add symbol table and translation

    # Write output (empty for now)
        os.makedirs("output", exist_ok=True)
        with open(output_path, "w") as f:
            f.write("")  # Placeholder - will fill with binary later

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


if __name__ == "__main__":
    main()
