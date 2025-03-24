import subprocess
import os
from dotenv import load_dotenv
from core.logger import CentralizedLogger

logger = CentralizedLogger()
load_dotenv()  # Load GitHub credentials from .env

def push_to_github(version):
    github_user = os.getenv("GITHUB_USERNAME")
    github_token = os.getenv("GITHUB_TOKEN")
    repo_name = os.getenv("GITHUB_REPO", "TechnomancyAI")

    if not github_user or not github_token:
        logger.warning("Missing GitHub credentials in .env.")
        return

    repo_url = f"https://{github_user}:{github_token}@github.com/{github_user}/{repo_name}.git"

    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", f"Version {version} update"], check=True)
        subprocess.run(["git", "push", repo_url], check=True)
        logger.info(f"✅ Version {version} pushed to GitHub.")
    except subprocess.CalledProcessError as e:
        logger.warning(f"Git push failed: {e}")
