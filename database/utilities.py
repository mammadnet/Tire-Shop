from .models import User, Admin, Manager, Employee, Product, Order
import os
import csv
from sqlalchemy.orm import Session
from sqlalchemy import select



def is_admin(user:User):
    return isinstance(user, Admin)

def is_manager(user:User):
    return isinstance(user, Manager)

def is_employee(user:User):
    return isinstance(user, Employee)



def export_table_to_file(session: Session, path: str, file_name: str, table):

    os.makedirs(path, exist_ok=True)

    full_path = os.path.join(path, file_name)

    # Query all data
    stmt = select(table)
    results = session.execute(stmt).all()

    if not results:
        print("No data found in the table.")
        return

    # Open file for writing
    with open(full_path, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)

        # Get column names
        column_names = results[0]._mapping.keys()
        writer.writerow(column_names)

        # Write rows
        for row in results:
            writer.writerow(row)

    print(f"Data exported to {full_path}")

def export_user_table_to_file(session: Session, path: str, file_name: str):
    export_user_table_to_file(session, path, file_name, User)

def export_product_table_to_file(session: Session, path: str, file_name: str):
    export_product_table_to_file(session, path, file_name, Product)
    
def export_order_table_to_file(session: Session, path: str, file_name: str):
    export_order_table_to_file(session, path, file_name, Order)