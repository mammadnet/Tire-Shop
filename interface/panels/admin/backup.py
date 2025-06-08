from customtkinter import *
from ..panel import Panel
from ...widgets import Item_button, Input, Btn, DropDown, render_text, create_updatable_labels
from database import session, get_all_employees_json, create_new_user, create_product
from database import remove_user_by_username, update_user_by_username, user_by_username, get_all_username
from database import get_all_products_json, delete_product_by_name_and_size, get_product_by_id, get_product_by_id_json, update_product_by_id, get_all_employee_usernames
from database import get_all_employee_and_manager_json, get_all_employee_and_manager_usernames, get_all_customers, get_customer_by_id
from database import create_order, get_customer_by_national_id, get_or_create_customer, check_customer_equal, get_all_orders
from database import get_total_product_quantity, get_brands_count, get_sizes_count, get_customers_count, get_employees_count, get_monthly_sales, get_daily_sales
from database import backup_database, restore_database
from database import ProductNotExistsException
from utilities import Concur, is_windows, get_current_datetime
from tkinter import ttk, filedialog
from time import sleep


class AdminBackupPanel(Panel):
    def __init__(self, root):
        super().__init__(root)
        self.pack(expand=True, fill="both")
        self.configure(bg_color='transparent', fg_color="#5B5D76")
        self.place(relheight=.9, relwidth=.8, relx=.02, rely=.05)
        self.rowconfigure(tuple(range(0, 8)), weight=1)
        self.columnconfigure((0, 2), weight=1, pad=20, uniform='a')
        
        # Setup button frame
        self.btn_frame = CTkFrame(self, fg_color='transparent')
        self.btn_frame.place(relwidth=.2, relheight=.3, relx=1, rely=.1, anchor="ne")
        self.btn_frame.columnconfigure(0, weight=1)
        self.btn_frame.rowconfigure((0,1,2,3), weight=1)

        
        default_path = self.default_path()
        path = StringVar()
        self.path_input = Input(self, 15, 280, 35, None, path, placeholder_empty=False, just_english=True, char_limit=40)
        self.path_input.grid(row=0, column=0, columnspan=2)
        self.path_input.set_textvariable(path)
        path.set(default_path)
        
        self.path_label = CTkLabel(self, text=render_text("مسیر ذخیره فایل"), text_color='white', font=(None, 15))
        self.path_label.grid(row=0, column=2, columnspan=2)
        
        self.path_label = CTkLabel(self, text=render_text('نام فایل'), text_color='white', font=(None, 15))
        self.path_label.grid(row=1, column=2, columnspan=2)
        
        self.path_label = CTkLabel(self, text=self.get_backupfile_name(), text_color='#c5c6de', font=(None, 15))
        self.path_label.grid(row=1, column=0, columnspan=2)
        

        
        # Add operation button
        self.operation_btn = Btn(self, text="ذخیره",width=160, height=45, command=self.handle_backup)
        self.operation_btn.grid(row=3, column=0, columnspan=4)
    

    def handle_backup(self):
        path = self.path_input.get()
        if not path:
            self.show_error_message("Path cannot be empty.")
            return

        os.makedirs(path, exist_ok=True)  # Ensure the directory exists
        
        filename = self.get_backupfile_name() + '.db'
        fullpath = os.path.join(path, filename)

        dbPath = os.path.join(os.getcwd(), str(session.bind.url).split('///')[-1])
        with open(fullpath, 'wb') as f:
            f.write(b'')  # Create an empty file if it doesn't exist
            f.close()
        try:
            print(dbPath, os.getcwd())
            backup_database(dbPath, fullpath)
            self.show_success_message(f"Backup saved to {fullpath}")
        except Exception as e:
            self.show_error_message(e)
            
    def default_path(self):
        folder_name = "TSBackup"
        if is_windows():
            desktop_path = os.path.join(os.environ["USERPROFILE"], "Desktop")


            folder_path = os.path.join(desktop_path, folder_name)

            return folder_path

        else:
            home_path = os.path.expanduser("~")

            # Step 3: Construct the full path to the folder
            folder_path = os.path.join(home_path, folder_name)
            
            return folder_path
                    
                    
    def get_backupfile_name(self):
        now = get_current_datetime()
        return 'TS_' + now