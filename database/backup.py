import shutil
import os


def backup_database(source_db_path: str, backup_db_path: str) -> None:
    """
    Backs up a database file by copying it to a specified backup location.

    Args:
        source_db_path: The full path to the source database file to be backed up.
        backup_db_path: The path to the directory where the backup file will be stored.
    
    Raises:
        FileNotFoundError: If the source database path or the backup directory does not exist.
    """
    # Check if the destination directory for the backup exists.
    if not os.path.exists(backup_db_path):
        raise FileNotFoundError(f"Backup path does not exist: {backup_db_path}")
    # Check if the source database file itself exists.
    if not os.path.exists(source_db_path):
        raise FileNotFoundError(f"Source database path does not exist: {source_db_path}")
    
    # Copy the source file to the backup directory.
    shutil.copy(source_db_path, backup_db_path)
    
    
def restore_database(backup_db_path: str, target_db_path: str) -> None:
    """
    Restores a database file from a backup by copying it to a target location.

    Args:
        backup_db_path: The full path to the backup database file.
        target_db_path: The full path where the database should be restored (including the filename).

    Raises:
        FileNotFoundError: If the backup file or the target directory does not exist.
    """
    # Check if the backup file exists.
    if not os.path.exists(backup_db_path):
        raise FileNotFoundError(f"Backup path does not exist: {backup_db_path}")
    # Check if the directory where the database is to be restored exists.
    if not os.path.exists(os.path.dirname(target_db_path)):
        raise FileNotFoundError(f"Target database directory does not exist: {os.path.dirname(target_db_path)}")
    
    # Copy the backup file to the target path, overwriting if it exists.
    shutil.copy(backup_db_path, target_db_path)