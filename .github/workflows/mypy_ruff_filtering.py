"""
Parse Ruff and Mypy output and print them in a format that GitHub Actions can parse and display as annotations.

Ruff warnings are warnings, while Mypy warnings are merge-blocking errors.
"""
import argparse
import re
import sys


def parse_ruff(output: str) -> int:
    """
    Parse Ruff output and print it in a format that GitHub Actions can parse and display as annotations.
    """
    pattern = re.compile(
        r"^(?P<code>[A-Z]+\d+)\s+(?P<message>.+?)\n"
        r"\s*-->\s*(?P<file>.+?):(?P<line>\d+):(?P<column>\d+)$",
        re.MULTILINE | re.DOTALL,
    )
    matches = pattern.findall(output)
    for match in matches:
        code, message, file_path, line_number, column_number = match
        print(f"::warning file={file_path},line={line_number},col={column_number}::{code} {message}")

    # Ruff warnings do not block a merge
    return 0


def parse_mypy(output: str) -> int:
    """
    Parse Mypy output and print it in a format that GitHub Actions can parse and display as annotations.
    """
    return_code = 0
    for line in output.splitlines():
        match = re.match(r"(.+):(\d+): (.+)", line)
        if match:
            file_path, line_number, message = match.groups()
            print(f"::error file={file_path},line={line_number}::{message}")
            return_code = 1
    return return_code


def main() -> None:
    argument_parser = argparse.ArgumentParser(
        description="Parse Ruff and Mypy output and print them in a format that GitHub Actions can parse and display as annotations."
    )
    argument_parser.add_argument(
        "--ruff-output",
        help="Set this flag if the input is Ruff output.",
        action="store_true",
        default=False
    )
    argument_parser.add_argument(
        "--mypy-output",
        help="Set this flag if the input is Mypy output.",
        action="store_true",
        default=False
    )

    args = argument_parser.parse_args()

    if not (args.ruff_output or args.mypy_output):
        print("Error: You must specify either --ruff-output or --mypy-output.")
        sys.exit(1)

    if args.ruff_output and args.mypy_output:
        print("Error: You cannot specify both --ruff-output and --mypy-output.")
        sys.exit(1)

    stdin = sys.stdin.read()
    return_code = 0
    if args.ruff_output:
        return_code = parse_ruff(stdin)
    elif args.mypy_output:
        return_code = parse_mypy(stdin)

    sys.exit(return_code)

if __name__ == "__main__":
    main()
