#!/usr/bin/env python3
"""
format_pylint.py
Converts pylint raw text into a concise Markdown report (pylint_lite.md).

Usage:
    python format_pylint.py <input_file> <output_file>
"""

import re
import sys
from typing import Any, Dict, List


def write_section(out, module: str, issues: List[Dict[str, Any]]) -> None:
    """
    Writes a markdown section for the given module with any reported issues.
    """
    out.write(f"## {module}\n")
    if not issues:
        out.write("No issues found.\n\n")
        return

    for issue in issues:
        line = issue["line"]
        col = issue["col"]
        msg = issue["msg"]
        out.write(f"- Line {line}, Col {col}: {msg}\n")
    out.write("\n")


def main():
    if len(sys.argv) != 3:
        print("Usage: format_pylint.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # We'll parse the raw pylint output, grouping by module name:
    with open(input_file, "r", encoding="utf-8") as f:
        content = f.readlines()

    sections = {}  # dict: {module_name: [list of issues]}
    current_module = None

    # Regex patterns
    # Typical lines from pylint might look like:
    # "************* Module mypackage.mymodule"
    # or an error line:
    # "mypackage/mymodule.py:12:0: C0116: Missing function docstring (missing-function-docstring)"
    module_line_regex = re.compile(r"^\*{10,}\sModule\s(.*)")
    issue_line_regex = re.compile(
        r"^([^:]+):(\d+):(\d+):\s([A-Z]\d+):\s(.+)\s\(([^)]+)\)"
    )

    for line in content:
        # Check if line indicates a new module
        match_module = module_line_regex.match(line)
        if match_module:
            current_module = match_module.group(1).strip()
            if current_module not in sections:
                sections[current_module] = []
            continue

        # Check if line indicates an issue
        match_issue = issue_line_regex.match(line)
        if match_issue and current_module:
            file_path = match_issue.group(1)
            line_num = match_issue.group(2)
            col_num = match_issue.group(3)
            code = match_issue.group(4)
            message = match_issue.group(5)
            rule = match_issue.group(6)  # e.g. (missing-function-docstring)

            sections[current_module].append(
                {
                    "file": file_path,
                    "line": line_num,
                    "col": col_num,
                    "code": code,
                    "msg": message,
                    "rule": rule,
                }
            )

    # Now write the markdown output
    with open(output_file, "w", encoding="utf-8") as out:
        out.write("# File Issues:\n\n")
        if not sections:
            out.write("No modules or issues found.\n")
            return

        for module_name in sorted(sections.keys()):
            write_section(out, module_name, sections[module_name])


if __name__ == "__main__":
    main()
