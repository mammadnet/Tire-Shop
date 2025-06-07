import shutil
import os


def backup_database(source_db_path: str, backup_db_path: str) -> None:
    if not os.path.exists(backup_db_path):
        raise FileNotFoundError(f"Backup path does not exist: {backup_db_path}")
    if not os.path.exists(source_db_path):
        raise FileNotFoundError(f"Source database path does not exist: {source_db_path}")
    
    shutil.copy(source_db_path, backup_db_path)
    
    
def restore_database(backup_db_path: str, target_db_path: str) -> None:
    if not os.path.exists(backup_db_path):
        raise FileNotFoundError(f"Backup path does not exist: {backup_db_path}")
    if not os.path.exists(os.path.dirname(target_db_path)):
        raise FileNotFoundError(f"Target database directory does not exist: {os.path.dirname(target_db_path)}")
    
    shutil.copy(backup_db_path, target_db_path)