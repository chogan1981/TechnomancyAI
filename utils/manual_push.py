import os
import subprocess
from dotenv import load_dotenv

from core.increment_version import increment_version
from core.update_goal_version import update_goal_version
from core.update_changelog import update_changelog
from core.logger import CentralizedLogger

from goals import current_goal
from utils.version_archiver import archive_version
from change import Change

# Load credentials from .env
load_dotenv()
logger = CentralizedLogger()

def manual_push():
    print("\n📦 Manual Push to GitHub")
    message = input("Enter a commit message: ").strip()
    if not message:
        print("❌ Commit message is required. Exiting.")
        return

    current_version = current_goal["version"]
    new_version = increment_version(current_version)

    # Prepare change objects for archiving all files (WRITE type)
    changes = []
    exclude_dirs = {"__pycache__", ".git", ".venv", "venv", "versions"}

    for root, _, files in os.walk("."):
        if any(part in exclude_dirs for part in root.split(os.sep)):
            continue
        for file in files:
            full_path = os.path.join(root, file)
            norm_path = os.path.normpath(full_path).lstrip("./\\")
            changes.append(Change(norm_path, "", "WRITE"))

    # Archive project into versions/vX.X.zip
    archive_version(changes, new_version)

    # Get GitHub credentials from .env
    github_user = os.getenv("GITHUB_USERNAME")
    github_token = os.getenv("GITHUB_TOKEN")
    repo_name = os.getenv("GITHUB_REPO", "TechnomancyAI")

    if not github_user or not github_token:
        logger.warning("❌ Missing GitHub credentials in .env.")
        return

    repo_url = f"https://{github_user}:{github_token}@github.com/{github_user}/{repo_name}.git"

    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", f"{message} (v{new_version})"], check=True)
        subprocess.run(["git", "push", repo_url], check=True)
        logger.info(f"✅ Manual push complete for version {new_version}.")

        # Update internal version tracking and changelog
        update_goal_version(new_version)
        update_changelog(new_version, message)

        print(f"\n✅ Project zipped, pushed, and version bumped to {new_version}.")

    except subprocess.CalledProcessError as e:
        logger.warning(f"❌ Git operation failed: {e}")
        print("❌ Git push failed. Check your terminal or credentials.")

if __name__ == "__main__":
    manual_push()
