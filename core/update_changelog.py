from datetime import datetime

def update_changelog(version, idea_summary):
    """
    Appends a new entry to changelog.md with the version number, timestamp, and summary of the idea.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open("changelog.md", "a", encoding="utf-8") as f:
        f.write(f"\n## {version} - {timestamp}\n")
        f.write(f"- {idea_summary.strip()}\n")