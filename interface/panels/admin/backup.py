from customtkinter import *
from ..panel import Panel
from ...widgets import Input, Btn, render_text
from database import session
from database import backup_database
from utilities import is_windows, get_current_datetime
import os


# This class defines the UI panel for the database backup functionality,
# available to the administrator.
class AdminBackupPanel(Panel):
    def __init__(self, root):
        # Initialize the parent Panel class, which provides message display capabilities.
        super().__init__(root)
        self.pack(expand=True, fill="both")
        self.configure(bg_color='transparent', fg_color="#5B5D76")
        self.place(relheight=.9, relwidth=.8, relx=.02, rely=.05)
        self.rowconfigure(tuple(range(0, 8)), weight=1)
        self.columnconfigure((0, 2), weight=1, pad=20, uniform='a')
        
        # --- UI Widget Setup ---
        # A frame for buttons, though it appears unused in the provided code.
        self.btn_frame = CTkFrame(self, fg_color='transparent')
        self.btn_frame.place(relwidth=.2, relheight=.3, relx=1, rely=.1, anchor="ne")
        self.btn_frame.columnconfigure(0, weight=1)
        self.btn_frame.rowconfigure((0,1,2,3), weight=1)

        
        # An input field for the user to specify or change the backup path.
        default_path = self.default_path()
        path = StringVar()
        self.path_input = Input(self, 15, 280, 35, None, path, placeholder_empty=False, just_english=True, char_limit=40)
        self.path_input.grid(row=0, column=0, columnspan=2)
        self.path_input.set_textvariable(path)
        # Set the input field's initial value to the OS-specific default path.
        path.set(default_path)
        
        # A label for the path input field.
        self.path_label = CTkLabel(self, text=render_text("مسیر ذخیره فایل"), text_color='white', font=(None, 15))
        self.path_label.grid(row=0, column=2, columnspan=2)
        
        # A label for the generated filename.
        self.path_label = CTkLabel(self, text=render_text('نام فایل'), text_color='white', font=(None, 15))
        self.path_label.grid(row=1, column=2, columnspan=2)
        
        # A label to display the actual backup filename that will be used.
        self.path_label = CTkLabel(self, text=self.get_backupfile_name(), text_color='#c5c6de', font=(None, 15))
        self.path_label.grid(row=1, column=0, columnspan=2)
        

        
        # The main button that triggers the backup process.
        self.operation_btn = Btn(self, text="ذخیره",width=160, height=45, command=self.handle_backup)
        self.operation_btn.grid(row=3, column=0, columnspan=4)
    

    # This method is executed when the 'Save' (ذخیره) button is clicked.
    def handle_backup(self):
        """
        Handles the logic for creating the database backup file.
        """
        path = self.path_input.get()
        if not path:
            self.show_error_message("Path cannot be empty.")
            return

        # Ensure the specified backup directory exists, creating it if necessary.
        os.makedirs(path, exist_ok=True)
        
        filename = self.get_backupfile_name() + '.db'
        fullpath = os.path.join(path, filename)

        # Get the path to the current database file from the SQLAlchemy session.
        dbPath = os.path.join(os.getcwd(), str(session.bind.url).split('///')[-1])
        # This block seems intended to ensure the target file exists before copying,
        # but the `backup_database` function handles the copy.
        with open(fullpath, 'wb') as f:
            f.write(b'')
            f.close()
        try:
            print(dbPath, os.getcwd())
            # Call the core backup function to perform the file copy.
            backup_database(dbPath, fullpath)
            self.show_success_message(f"Backup saved to {fullpath}")
        except Exception as e:
            # Display any errors that occur during the backup process.
            self.show_error_message(e)
            
    # Determines a default backup directory based on the user's operating system.
    def default_path(self):
        """
        Returns a default backup path, typically a folder on the user's Desktop or home directory.
        """
        folder_name = "TSBackup"
        if is_windows():
            desktop_path = os.path.join(os.environ["USERPROFILE"], "Desktop")
            folder_path = os.path.join(desktop_path, folder_name)
            return folder_path
        else: # For macOS, Linux, etc.
            home_path = os.path.expanduser("~")
            folder_path = os.path.join(home_path, folder_name)
            return folder_path
                    
                    
    # Generates a unique filename for the backup based on the current date and time.
    def get_backupfile_name(self):
        """
        Creates a filename string using the current timestamp to ensure uniqueness.
        """
        now = get_current_datetime()
        return 'TS_' + now