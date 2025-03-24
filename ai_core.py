import os
import re

from core.read_self_code import read_self_code
from core.ask_for_idea import ask_for_idea
from core.ask_for_code import ask_for_code
from core.get_approval import get_approval
from core.increment_version import increment_version
from core.update_goal_version import update_goal_version
from core.update_changelog import update_changelog
from core.logger import CentralizedLogger
from core.ask_for_summary import ask_for_summary

from goals import current_goal
from change import Change
from utils.change_manager import ChangeManager
from utils.diff_preview import show_diff
from utils.version_archiver import archive_version
from utils.git_push import push_to_github

# Initialize logger
logger = CentralizedLogger()

# Regex patterns for parsing AI-generated changes
CHANGE_BLOCK_PATTERN = r'\[(CREATE|WRITE|DELETE)\]\s+([^\n]+)\n```(?:python)?\n(.*?)```'
DELETE_LINE_PATTERN = r'\[DELETE\]\s+([^\n]+)'

def main():
    code = read_self_code()
    current_version = current_goal['version']
    print(f"\nTechnomancyAI {current_version}")
    print("Step 1: Self-reflection and idea generation...\n")

    idea = ask_for_idea(code, current_goal)
    print("\n--- Proposed Improvement Idea ---\n")
    print(idea)

    if not get_approval("Do you approve this idea for code generation?"):
        reason = input("Enter reason for rejection: ")
        logger.warning(f"Rejection: {reason} - IDEA")
        print("\nIdea rejected. Exiting.\n")
        return

    acceptance_reason = input("Enter reason for acceptance: ")
    logger.info(f"Acceptance: {acceptance_reason} - IDEA")

    print("\nStep 2: Generating code for proposed improvement...\n")
    ai_code_block = ask_for_code(code, idea)
    print("\n--- Proposed Code & Actions ---\n")
    print(ai_code_block)

    if not get_approval("Do you approve this code for implementation?"):
        reason = input("Enter reason for rejection: ")
        logger.warning(f"Rejection: {reason} - CODE")
        print("\nCode rejected. Exiting.\n")
        return

    acceptance_reason = input("Enter reason for acceptance: ")
    logger.info(f"Acceptance: {acceptance_reason} - CODE")

    new_version = increment_version(current_version)
    change_manager = ChangeManager()

    matches = re.findall(CHANGE_BLOCK_PATTERN, ai_code_block, re.DOTALL)
    if not matches:
        logger.warning("No valid change blocks found in AI-generated code.")

    for action_type, file_name, content in matches:
        normalized_name = os.path.normpath(file_name.strip())
        change = Change(normalized_name, content.strip(), action_type.strip())
        change_manager.add_change(change)

    delete_matches = re.findall(DELETE_LINE_PATTERN, ai_code_block)
    for file_name in delete_matches:
        normalized_name = os.path.normpath(file_name.strip())
        if not any(c.file_name == normalized_name and c.action_type == "DELETE" for c in change_manager.changes):
            change = Change(normalized_name, "", "DELETE")
            change_manager.add_change(change)

    for change in change_manager.changes:
        if change.action_type in ("CREATE", "WRITE"):
            show_diff(change.file_name, change.content)

    if not get_approval("Do you approve all changes after reviewing the diffs?"):
        reason = input("Enter reason for rejection: ")
        logger.warning(f"Rejection: {reason} - DIFF")
        print("\nChanges rejected. Exiting.\n")
        return

    change_manager.execute_changes()

    # 🔥 Archive all written/created files into versions/vX.X/
    archive_version(change_manager.changes, new_version)
    push_to_github(new_version)

    change_manager.clear_changes()

    update_goal_version(new_version)
    summary = ask_for_summary(idea, ai_code_block)
    update_changelog(new_version, summary)

    print(f"\n✅ Code implemented and version bumped to {new_version}.")

if __name__ == "__main__":
    main()
