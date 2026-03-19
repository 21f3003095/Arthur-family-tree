"""
main.py
"""

import sys
import shlex
from typing import Optional, List
from family_tree import FamilyTree
from seeder import build_arthur_family


# Command constants
CMD_ADD_CHILD        = "ADD_CHILD"
CMD_GET_RELATIONSHIP = "GET_RELATIONSHIP"


# Parser
def _parse_tokens(line: str) -> List[str]:

    try:
        return shlex.split(line)
    except ValueError:
        return line.split()


def process_command(tree: FamilyTree, line: str) -> Optional[str]:

    stripped = line.strip()
    if not stripped or stripped.startswith("#"):
        return None

    tokens = _parse_tokens(stripped)
    if not tokens:
        return None

    command = tokens[0].upper()

    if command == CMD_ADD_CHILD:
        if len(tokens) != 4:
            return "CHILD_ADDITION_FAILED"
        _, mother_name, child_name, gender_str = tokens
        return tree.add_child(mother_name, child_name, gender_str)

    if command == CMD_GET_RELATIONSHIP:
        if len(tokens) != 3:
            return "PERSON_NOT_FOUND"
        _, name, relationship = tokens
        return tree.get_relationship(name, relationship)

    # Unknown command
    return f"UNKNOWN_COMMAND: {command}"


# Main

def run(input_path: str) -> None:
    tree: FamilyTree = build_arthur_family()

    try:
        with open(input_path, "r", encoding="utf-8") as fh:
            lines = fh.readlines()
    except FileNotFoundError:
        print(f"Error: file not found — '{input_path}'", file=sys.stderr)
        sys.exit(1)
    except OSError as exc:
        print(f"Error reading file: {exc}", file=sys.stderr)
        sys.exit(1)

    for line in lines:
        result = process_command(tree, line)
        if result is not None:
            print(result)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <path_to_input_file>", file=sys.stderr)
        sys.exit(1)

    run(sys.argv[1])
