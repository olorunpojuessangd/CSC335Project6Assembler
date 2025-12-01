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
    input_filename = "Add.asm"
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


if __name__ == "__main__":
    main()
