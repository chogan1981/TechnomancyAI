import os


def should_include_file(file, root):
    return (
            file.endswith(".py")
            and not file.startswith(".")
            and "venv" not in root
    )


def read_self_code():
    code = ""
    # Iterate over project files and directories
    for root, _, files in os.walk("."):
        for file in files:
            if should_include_file(file, root):
                path = os.path.join(root, file)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        code += f"\n\n# FILE: {path}\n" + f.read()
                except Exception as e:
                    print(f"⚠️ Could not read {path}: {e}")

    # Include rejection messages
    try:
        with open("memory/rejections.txt", "r", encoding="utf-8") as f:
            code += f"\n\n# FILE: memory/rejections.txt\n" + f.read()
    except Exception as e:
        print("⚠️ Could not read memory/rejections.txt:", e)

    return code.strip()
