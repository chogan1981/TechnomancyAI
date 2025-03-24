import os
from core.logger import CentralizedLogger

class FileManager:
    def __init__(self):
        self.logger = CentralizedLogger()

    def create_file(self, filename, content):
        if os.path.exists(filename):
            self.logger.warning(f"CREATE skipped: '{filename}' already exists.")
            return
        with open(filename, 'x') as file:
            file.write(content)
        self.logger.info(f"File created: {filename}")

    def write_file(self, filename, content):
        with open(filename, 'w') as file:
            file.write(content)

    def delete_file(self, filename):
        if not os.path.exists(filename):
            self.logger.warning(f"DELETE skipped: '{filename}' does not exist.")
            return
        os.remove(filename)
        self.logger.info(f"File deleted: {filename}")