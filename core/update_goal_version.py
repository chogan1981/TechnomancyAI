def update_goal_version(new_version):
    """
    Replaces the current version string in goals.py with the new_version.
    Assumes version is stored like: "version": "v0.3",
    """
    with open("goals.py", "r", encoding="utf-8") as f:
        lines = f.readlines()

    with open("goals.py", "w", encoding="utf-8") as f:
        for line in lines:
            if '"version"' in line:
                f.write(f'    "version": "{new_version}",\n')
            else:
                f.write(line)