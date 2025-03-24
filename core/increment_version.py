import re

def increment_version(version: str) -> str:
    """
    Increments the minor version number.
    Example: 'v0.3' -> 'v0.4'
    """
    match = re.match(r"v(\d+)\.(\d+)", version)
    if match:
        major, minor = map(int, match.groups())
        return f"v{major}.{minor + 1}"
    return version  # Return unchanged if format is unexpected
