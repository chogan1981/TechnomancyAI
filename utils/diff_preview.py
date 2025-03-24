import os
import difflib

def show_diff(file_path, new_content):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            old_content = f.read()
    else:
        old_content = ""

    old_lines = old_content.splitlines()
    new_lines = new_content.splitlines()

    diff = difflib.unified_diff(
        old_lines,
        new_lines,
        fromfile=f"{file_path} (current)",
        tofile=f"{file_path} (proposed)",
        lineterm=""
    )

    print("\n--- Diff Preview ---")
    for line in diff:
        print(line)
