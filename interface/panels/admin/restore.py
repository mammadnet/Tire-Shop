from customtkinter import *
from ..panel import Panel
from ...widgets import Btn, render_text
from database import restore_database, session # Added session import
from utilities import is_windows
from tkinter import filedialog
import os # Added os import


# This class defines the UI panel for the database restore functionality,
# available to the administrator.
class AdminRestorePanel(Panel):
    def __init__(self, root):
        # Initialize the parent Panel, which provides message display capabilities.
        super().__init__(root)
        self.pack(expand=True, fill="both")
        self.configure(bg_color='transparent', fg_color="#5B5D76")
        self.place(relheight=.9, relwidth=.8, relx=.02, rely=.05)
        self.rowconfigure(tuple(range(0, 8)), weight=1)
        self.columnconfigure((0, 2), weight=1, pad=20, uniform='a')
        
        # A frame for buttons, though it appears unused in this specific layout.
        self.btn_frame = CTkFrame(self, fg_color='transparent')
        self.btn_frame.place(relwidth=.2, relheight=.3, relx=1, rely=.1, anchor="ne")
        self.btn_frame.columnconfigure(0, weight=1)
        self.btn_frame.rowconfigure((0,1,2,3), weight=1)

        
        
        # A button that opens a file dialog for the user to select a backup file.
        self.path_label = Btn(self, 150, 60, 20, "مسیر فایل", text_color='white', font=(None, 15), command=lambda: self.set_path())
        self.path_label.grid(row=0, column=2, columnspan=2)
        
        # A static label for the filename display.
        self.path_label = CTkLabel(self, text=render_text('نام فایل'), text_color='white', font=(None, 15))
        self.path_label.grid(row=1, column=2, columnspan=2)
        
        # A label that will be updated to show the name of the selected backup file.
        self.path_label = CTkLabel(self, text='?', text_color='#c5c6de', font=(None, 15))
        self.path_label.grid(row=1, column=0, columnspan=2)
        
        # This instance variable will store the full path to the selected backup file.
        self.file_path = None

        
        # The main button that triggers the restore process.
        self.operation_btn = Btn(self, text="بازیابی",width=160, height=45, command=self.handle_restore)
        self.operation_btn.grid(row=3, column=0, columnspan=4)
    

    # This method is executed when the 'Select File' (مسیر فایل) button is clicked.
    def set_path(self):
        """Opens a system file dialog to allow the user to select a .db backup file."""
        # 'askopenfile' opens the dialog and returns a file object if successful.
        selected_file_object = filedialog.askopenfile(title="انتخاب فایل", filetypes=[("database", '*.db')], initialdir=self.home_path())
        
        # Check if the user selected a file (if they cancel, it will be None).
        if selected_file_object:
            # Extract the file path string from the file object.
            self.file_path = selected_file_object.name
            # Update the label to show the name of the selected file.
            # The split logic handles both Windows ('\') and Unix-like ('/') path separators.
            if is_windows():
                self.path_label.configure(text=self.file_path.split('\\')[-1])
            else:
                self.path_label.configure(text = self.file_path.split('/')[-1])
            
    # A helper method to determine a sensible default directory for the file dialog.
    def home_path(self):
        """Returns the user's Desktop path on Windows, or home directory on other OSes."""
        home_path = os.path.expanduser("~")
        
        if is_windows():
            desktop_path = os.path.join(home_path, "Desktop")
            if os.path.isdir(desktop_path):
                return desktop_path
            else:
                return home_path # Fallback to home directory if Desktop isn't found.
        else: # For macOS, Linux, etc.
            return home_path
            
    # This method is executed when the 'Restore' (بازیابی) button is clicked.
    def handle_restore(self):
        """
        Handles the logic for restoring the database from the selected backup file.
        """
        path = self.file_path
        # Check if a backup file has been selected first.
        if not path:
            self.show_error_message(render_text("فایل بکاپ را انتخات کنید"))
            return
        
        # Determine the path to the current application database.
        dbPath = os.path.join(os.getcwd(), str(session.bind.url).split('///')[-1])
        try:
            # Call the core restore function.
            restore_database(self.file_path, dbPath)
            self.show_success_message("عملیات بازیابی با موفقیت انجام شد")
        except Exception as e:
            # Display any errors that occur during the process.
            self.show_error_message(self.file_path + str(e))