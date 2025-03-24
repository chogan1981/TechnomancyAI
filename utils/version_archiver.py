import os
import shutil
import zipfile
import subprocess

from core.logger import CentralizedLogger

logger = CentralizedLogger()

def archive_version(changes, version):
    folder_name = f"v{version}"
    archive_dir = os.path.join("versions", folder_name)
    archive_zip = os.path.join("versions", f"{folder_name}.zip")

    os.makedirs(archive_dir, exist_ok=True)

    for change in changes:
        if change.action_type in ("CREATE", "WRITE"):
            try:
                destination = os.path.join(archive_dir, os.path.basename(change.file_name))
                shutil.copy2(change.file_name, destination)
                logger.info(f"Archived {change.file_name} → {destination}")
            except Exception as e:
                logger.warning(f"Failed to archive {change.file_name}: {e}")

    # Zip the entire version folder
    try:
        with zipfile.ZipFile(archive_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(archive_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, archive_dir)
                    zipf.write(file_path, arcname)
        logger.info(f"Created version archive: {archive_zip}")
    except Exception as e:
        logger.warning(f"Failed to zip archive {archive_dir}: {e}")
        return

    # Delete the uncompressed folder
    try:
        shutil.rmtree(archive_dir)
        logger.info(f"Removed temporary archive folder: {archive_dir}")
    except Exception as e:
        logger.warning(f"Failed to remove folder {archive_dir}: {e}")
