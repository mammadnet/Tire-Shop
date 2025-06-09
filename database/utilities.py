from .models import User, Admin, Manager, Employee, Product, Order
import os
import csv
from sqlalchemy.orm import Session
from sqlalchemy import select


# --- User Type Checking Utilities ---

def is_admin(user:User):
    """Checks if the given User object is an instance of the Admin subclass."""
    return isinstance(user, Admin)

def is_manager(user:User):
    """Checks if the given User object is an instance of the Manager subclass."""
    return isinstance(user, Manager)

def is_employee(user:User):
    """Checks if the given User object is an instance of the Employee subclass."""
    return isinstance(user, Employee)


# --- Data Export Functions ---

def export_table_to_file(session: Session, path: str, file_name: str, table):
    """
    Exports all data from a given SQLAlchemy table model to a CSV file.

    Args:
        session: The SQLAlchemy session object for database interaction.
        path: The directory path where the file will be saved.
        file_name: The name of the output CSV file.
        table: The SQLAlchemy model class representing the table to export.
    """
    # Create the destination directory if it does not already exist.
    # 'exist_ok=True' prevents an error if the directory is already there.
    os.makedirs(path, exist_ok=True)

    # Create the full, platform-independent path for the output file.
    full_path = os.path.join(path, file_name)

    # Create a query to select all records from the specified table.
    stmt = select(table)
    results = session.execute(stmt).all()

    # Gracefully handle cases where the table is empty.
    if not results:
        print("No data found in the table.")
        return

    # Open the file for writing. 'newline=""' is important to prevent extra blank rows in the CSV.
    with open(full_path, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)

        # Dynamically get the column names from the first result row.
        # '_mapping.keys()' provides the names of the columns in the result set.
        column_names = results[0]._mapping.keys()
        # Write the column names as the header row of the CSV.
        writer.writerow(column_names)

        # Write all data rows to the CSV file.
        for row in results:
            writer.writerow(row)

    print(f"Data exported to {full_path}")

def export_user_table_to_file(session: Session, path: str, file_name: str):
    """
    Intended as a convenience wrapper to export the User table.
    NOTE: This function is currently implemented with infinite recursion
    and will cause a RecursionError. It should call 'export_table_to_file' instead.
    """
    export_user_table_to_file(session, path, file_name, User)

def export_product_table_to_file(session: Session, path: str, file_name: str):
    """
    Intended as a convenience wrapper to export the Product table.
    NOTE: This function is currently implemented with infinite recursion
    and will cause a RecursionError. It should call 'export_table_to_file' instead.
    """
    export_product_table_to_file(session, path, file_name, Product)
    
def export_order_table_to_file(session: Session, path: str, file_name: str):
    """
    Intended as a convenience wrapper to export the Order table.
    NOTE: This function is currently implemented with infinite recursion
    and will cause a RecursionError. It should call 'export_table_to_file' instead.
    """
    export_order_table_to_file(session, path, file_name, Order)