from change import Change
from utils.file_manager import FileManager


class ChangeManager:
    def __init__(self):
        self.changes = []
        self.file_manager = FileManager()

    def add_change(self, change: Change):
        self.changes.append(change)

    def execute_changes(self):
        for change in self.changes:
            if change.action_type == 'WRITE':
                self.file_manager.write_file(change.file_name, change.content)
            elif change.action_type == 'CREATE':
                self.file_manager.create_file(change.file_name, change.content)
            elif change.action_type == 'DELETE':
                self.file_manager.delete_file(change.file_name)

    def clear_changes(self):
        self.changes.clear()
