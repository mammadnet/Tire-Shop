from customtkinter import CTk
from customtkinter import *
from tkinter import ttk
from .widgets import *
from utilities import Concur, is_windows
from time import sleep

from database import get_all_employees,get_all_employees_json, session

from PIL import Image
import os

# Initialize the Login_page class
class Login_page:
    def __init__(self, root, login_action):
        # Store the login action callback function
        self.login_action = login_action
        
        # Create the main frame for the login page
        self.main_frame = CTkFrame(root, fg_color='#494A5F')

        # Main container to hold all widgets of the page
        self.main_frame.pack(expand=True, fill='both')

        # Bind the "Enter" key to trigger the login button command
        root.bind('<Return>', lambda event: self.btn_command())

        # Left frame of the login page for displaying an image
        left_frame = CTkFrame(self.main_frame, fg_color='#494A5F')
        left_frame.place(relx=0, rely=0, relwidth=0.6, relheight=1)

        # Load and display the background image
        currentpath = os.path.dirname(os.path.realpath(__file__))
        back = Image.open(currentpath + '/assets/login-background.png')
        image = CTkImage(back, size=(back.width*.715, back.height*.715))
        image_lable = CTkLabel(left_frame, image=image, text='', fg_color='transparent')
        image_lable.place(relx=0, rely=0, anchor='nw')
        #-----------------------------------------------

        # Right frame of the login page for login entries (username and password)
        right_frame = CTkFrame(self.main_frame, fg_color='transparent')
        right_frame.place(relx=.6, rely=0, relwidth=0.4, relheight=1)

        # Configure grid layout for the right frame
        right_frame.rowconfigure((0, 1, 2, 3), weight=1, uniform='a')
        right_frame.columnconfigure(0, weight=1, uniform='a')
        
        # Load and display the login logo
        p = os.path.dirname(os.path.realpath(__file__))
        img = Image.open(p + "/assets/login-logo.png")
        self.logoimage = CTkLabel(right_frame, image=CTkImage(img, size=(230, 230)), text='', bg_color='transparent')
        self.logoimage.grid(row=0, sticky='nswe')

        # Container to vertically center the login frame
        login_frame_container = CTkFrame(right_frame, fg_color='#494A5F')
        login_frame_container.grid(row=1, column=0, rowspan=2, sticky='nsew')

        # Configure grid layout for the login frame container
        login_frame_container.rowconfigure((0,2), weight=1, uniform='a')
        login_frame_container.rowconfigure(1, weight=10, uniform='a')
        login_frame_container.columnconfigure((0,2), weight=1, uniform='a')
        login_frame_container.columnconfigure(1, weight=10, uniform='a')

        # Create a container for login entries
        login_frame = CTkFrame(login_frame_container, bg_color='transparent', fg_color='transparent')
        login_frame.grid(row=1, column=1)

        # Configure grid layout for the login frame
        login_frame.rowconfigure((0, 1, 2), weight=1, pad=30)
        login_frame.columnconfigure(0, weight=1)

        # Label to display error messages
        self.error_massage_lable = CTkLabel(login_frame, text_color='firebrick1')
        
        # Variables to store username and password
        self.username = StringVar()
        self.password = StringVar()
        

        # Create and configure the username entry field
        username_entry = Input(login_frame, 30, 300, 50, 'نام کاربری', self.username, show_err_callback=self.login_error_message)
        username_entry.configure(font=(None, 18))
        username_entry.set_placeholder_text("نام کاربری")
        username_entry.grid(row=0, column=0)

        # Create and configure the password entry field
        password_entry = Input(login_frame, 30, 300, 50, 'رمز', self.password, show='*', show_err_callback = self.login_error_message)
        password_entry.configure(font=(None, 18))
        password_entry.set_placeholder_text("رمز")
        password_entry.grid(row=1, column=0)

        # Link the entry fields to their respective variables
        username_entry.set_textvariable(self.username)
        password_entry.set_textvariable(self.password)
            
        # Create and configure the login button
        login_button = Btn(login_frame, 250, 50, 30, "ورود")
        login_button.grid(row=2, column=0)
        login_button.configure(font=(None, 18))
        login_button.configure(command=self.btn_command)
        

    
    # Method to get the main frame of the login page
    def get_frame(self):
        return self.main_frame
    
    # Method to handle the login button command
    def btn_command(self):
        # Trigger the login action with the provided username and password
        self.login_action(self.username.get(), self.password.get(), self)
        
    # Method to display an error message on the login page
    def login_error_message(self, message: str = None):
        if message:
            # Place the error message label on the page
            self.error_massage_lable.place(relx=.05, rely=.61)
            self.error_massage_lable.configure(text=message)
            # Start a concurrent task to clear the error message after 5 seconds
            Concur(lambda: self._clear_login_error(5)).start()
    
    # Private method to clear the error message after a delay
    def _clear_login_error(self, sec):
        sleep(sec)  # Wait for the specified number of seconds
        self.error_massage_lable.place_forget()  # Remove the error message label

    # Method to destroy the login page and its components
    def destroy(self):
        self.main_frame.pack_forget()  # Remove the main frame from the layout
        self.main_frame.destroy()  # Destroy the main frame and its children

# Initialize the Page class
class Page:
    def __init__(self, root, name: str, lastname: str, rule: str, logout_callback=None):
        # Create the main frame for the page
        self.main_frame = CTkFrame(root)
        self.main_frame.pack(expand=True, fill='both')
        
        # Store the logout callback function
        self.logout_callback = logout_callback
        
        # Create a frame for user profile and control buttons
        self.items_frame = CTkFrame(self.main_frame)
        self.items_frame.configure(fg_color='#5B5D76')
        self.items_frame.place(relwidth=0.3, relheight=1, relx=0.7, rely=0, anchor='nw')
        
        # Create a frame for the main content of the page
        self.control_frame = CTkFrame(self.main_frame)
        self.control_frame.configure(fg_color='#494A5F')
        self.control_frame.place(relwidth=0.7, relheight=1, relx=0, rely=0)
        
        # Create a container for user profile information
        self.user_profile_container = CTkFrame(self.items_frame)
        self.user_profile_container.configure(fg_color='transparent')
        self.user_profile_container.place(x=0, y=0, relwidth=1, relheight=0.15)
        
        # Create a frame for user profile details
        self.user_profile_frame = CTkFrame(self.user_profile_container)
        self.user_profile_frame.configure(fg_color='#393A4E', corner_radius=18)
        self.user_profile_frame.place(relx=0.5, rely=0.5, relwidth=0.75, relheight=0.6, anchor='center')
        
        # Set the user profile details
        self.set_profile(name, lastname, rule)
        
        # Add a logout button to the user profile
        self._set_logout_btn()

    # Method to set user profile details
    def set_profile(self, name: str, lastname: str, rule: str):
        # Capitalize the name, lastname, and rule for display
        name = name.capitalize()
        lastname = lastname.capitalize()
        rule = rule.capitalize()
         
        # Display the user's name and lastname
        self.user_name_lastname = CTkLabel(self.user_profile_frame, text=f'{name} {lastname}')
        self.user_name_lastname.configure(text_color="white", height=5)
        self.user_name_lastname.place(relx=0.25, rely=0.23)
        
        # Display the user's rule
        self.rule = CTkLabel(self.user_profile_frame, text=rule)
        self.rule.configure(text_color="white", height=20)
        self.rule.place(relx=0.25, rely=0.47)
        
    # Private method to set the logout button
    def _set_logout_btn(self):
        # Load the logout icon image
        p = os.path.dirname(os.path.realpath(__file__))
        img = Image.open(p + "/assets/logout.png")
        logoutImage = CTkImage(img)
        
        # Create the logout button
        self.btn_logout = Btn(self.user_profile_frame, image=logoutImage, height=0, width=0, border_spacing=0, corner_radius=5, anchor='center')
        self.btn_logout.configure(fg_color='transparent')
        
        # Place the logout button in the user profile frame
        self.btn_logout.place(relx=0.9, rely=0.5, anchor='center')
        
        # Set the logout action if a callback is provided
        if self.logout_callback:
            self.btn_logout.configure(command=lambda: self.logout_callback(self))

    # Method to destroy the page and its components
    def destroy(self):
        self.main_frame.pack_forget()  # Remove the main frame from the layout
        self.main_frame.destroy()  # Destroy the main frame and its children
    
    # Method to hide the page without destroying it
    def hide(self):
        self.main_frame.pack_forget()  # Remove the main frame from the layout
        

# Initialize the Admin_page class, inheriting from Page
class Admin_page(Page):
    def __init__(self, root, name: str, lastname: str, rule: str, logout_callback=None):
        # Call the parent class constructor
        super().__init__(root, name, lastname, rule, logout_callback)
        
        # Create a frame for admin-specific buttons
        self.buttons_frame = CTkFrame(self.items_frame)
        self.buttons_frame.configure(fg_color='transparent')
        self.buttons_frame.place(relx=0, rely=.15, relwidth=1, relheight=.85)
        
        # Configure the grid layout for the buttons frame
        self.buttons_frame.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8), weight=1)
        self.buttons_frame.columnconfigure(0, weight=1)
        
        # Define button styles
        self.button_font_size = 14
        self.button_color = "#393A4E"
        self.button_hover_color = "#434357"
        
        # Create and configure the "Products" button
        products_btn = Item_button(self.buttons_frame, 290, 64, rtopleft=15, rbottomleft=15, color=self.button_color, hover_color=self.button_hover_color, background="#5B5D76")
        products_btn.grid(row=0, column=0, sticky='e')
        products_btn.set_text('محصولات', fill='#FFFFFF', font_size=self.button_font_size)

        # Create and configure the "Manager" button
        backup_btn = Item_button(self.buttons_frame, 290, 64, rtopleft=15, rbottomleft=15, color=self.button_color, hover_color=self.button_hover_color, background="#5B5D76")
        backup_btn.grid(row=1, column=0, sticky='e')
        backup_btn.set_text('مدیر', fill='#FFFFFF', font_size=self.button_font_size)
        
        # Create and configure the "Employee" button
        employee_btn = Item_button(self.buttons_frame, 290, 64, rtopleft=15, rbottomleft=15, color=self.button_color, hover_color=self.button_hover_color, background="#5B5D76")
        employee_btn.grid(row=2, column=0, sticky='e')
        employee_btn.set_text('کارمند', fill='#FFFFFF', font_size=self.button_font_size)
        employee_btn.set_action(self._employee_panel_callback)
        
        # Create and configure the "Reports" button
        reports_btn = Item_button(self.buttons_frame, 290, 64, rtopleft=15, rbottomleft=15, color=self.button_color, hover_color=self.button_hover_color, background="#5B5D76")
        reports_btn.grid(row=3, column=0, sticky='e')
        reports_btn.set_text('گزارش', fill='#FFFFFF', font_size=self.button_font_size)
        
        # Create and configure the "Backup" button
        backup_btn = Item_button(self.buttons_frame, 290, 64, rtopleft=15, rbottomleft=15, color=self.button_color, hover_color=self.button_hover_color, background="#5B5D76")
        backup_btn.grid(row=4, column=0, sticky='e')
        backup_btn.set_text('بازیابی', fill='#FFFFFF', font_size=self.button_font_size)
        
        # Initialize the employee panel for development purposes
        self.employee_panel(self.control_frame)

    # Nested class for the employee panel
    class employee_panel(CTkFrame):
        def __init__(self, root):
            # Call the parent class constructor
            super().__init__(root)
            self.pack(expand=True, fill="both")
            self.configure(bg_color='transparent', fg_color='transparent')
            
            # Create a frame for employee-related buttons
            self.btn_frame = CTkFrame(self, fg_color='transparent')
            self.btn_frame.place(relwidth=.2, relheight=.3, relx=1, rely=.1, anchor="ne")
            self.btn_frame.columnconfigure(0, weight=1)
            self.btn_frame.rowconfigure((0, 1, 2), weight=1)
            
            # Create and configure the "Employee List" button
            employee_list_btn = Item_button(self.btn_frame, 150, 50, rtopleft=20, rbottomleft=20, color="#393A4E", hover_color="#434357", background="#494A5F")
            employee_list_btn.set_text("لیست کارمندان", "white", 13)
            employee_list_btn.grid(row=0, column=0, sticky="e")
            
            # Create and configure the "New Employee" button
            employee_new_btn = Item_button(self.btn_frame, 150, 50, rtopleft=20, rbottomleft=20, color="#393A4E", hover_color="#434357", background="#494A5F")
            employee_new_btn.set_text("کارمند جدید", "white", 13)
            employee_new_btn.grid(row=1, column=0, sticky="e")

            # Create and configure the "Delete Employee" button
            employee_delete_btn = Item_button(self.btn_frame, 150, 50, rtopleft=20, rbottomleft=20, color="#393A4E", hover_color="#434357", background="#494A5F")
            employee_delete_btn.set_text("کارمند جدید", "white", 13)
            employee_delete_btn.grid(row=2, column=0, sticky="e")
            
            # Initialize the content table
            self.content_table = self.initialize_table(self)
            self.insert_content_to_table(self.content_table, get_all_employees_json(session))
            
        # Method to initialize the content table
        def initialize_table(self, window):
            style = ttk.Style()
            if is_windows():
                style.theme_use('clam')
            
            # Configure Treeview style
            style.configure("Custom1.Treeview",
            background="#494A5F",
            foreground="black",
            fieldbackground="#393A4E",
            rowheight=50,
            borderwidth=0
            )
            
            style.configure("Custom1.Treeview.Heading",
            background="#5B5D76",     # Header background color
            foreground="white",       # Header text color
            font=("Helvetica", 10, "bold"),
            relief='flat')
            
            style.map("Custom1.Treeview.Heading",
            background=[("active", "#6b6d87")],
            foreground=[("active", "white")])
            
            table = ttk.Treeview(window, style="Custom1.Treeview")
            table.configure(columns=("id", "name", "lastname", "username", "phone", "national", "startDate"))
            table.configure(show="headings", selectmode="none")
            
            # Configure table columns
            table.column("id", width=40, anchor="center")
            table.column("name", width=100, anchor="center")
            table.column("lastname", width=150, anchor="center")
            table.column("username", width=120, anchor="center")
            table.column("phone", width=140, anchor="center")
            table.column("national", width=150, anchor="center")
            table.column("startDate", width=200, anchor="center")
            
            # Configure table headings
            table.heading("id", text="id", anchor='center')
            table.heading("name", text="name", anchor='center')
            table.heading("lastname", text="lastname", anchor='center')
            table.heading("username", text="username", anchor='center')
            table.heading("phone", text="phone", anchor='center')
            table.heading("national", text="national", anchor='center')
            table.heading("startDate", text="startDate", anchor='center')
            
            table.place(relheight=.9, relwidth=.8, relx=.02, rely=.05)
            return table
            
        # Method to insert content into the table
        def insert_content_to_table(self, table: ttk.Treeview, content: list[dict]):
            for row in content:
                vals = (row["id"], row["name"], row["lastname"], row["username"], row["phone"], row["national_number"])
                table.insert(parent="", index=0, values=vals)

    # Callback method for the employee panel
    def _employee_panel_callback(self, *k):
        print("Employee panel callback triggered")
        
    def _set_semple_lable(self, message):
        self.loggedin_lable = CTkLabel(self.main_frame, text_color='blue', text=message)
        self.loggedin_lable.pack(expand=True, fill='both')
        
    
    def destroy(self):
        self.main_frame.pack_forget()
        self.main_frame.destroy()



# Initialize the Manager_page class, inheriting from Page
class Manager_page(Page):
    def __init__(self, root, name, lastname, rule, logout_callback=None):
        # Call the parent class constructor
        super().__init__(root, name, lastname, rule, logout_callback)
        
        # Create a frame for manager-specific buttons
        self.buttons_frame = CTkFrame(self.items_frame)
        self.buttons_frame.configure(fg_color='transparent')
        self.buttons_frame.place(relx=0, rely=.15, relwidth=1, relheight=.85)
        
        # Configure the grid layout for the buttons frame
        self.buttons_frame.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8), weight=1)
        self.buttons_frame.columnconfigure(0, weight=1)
        
        # Define button styles
        self.button_font_size = 14
        self.button_color = "#393A4E"
        self.button_hover_color = "#434357"
        
        # Create and configure the "Dashboard" button
        dashboard_btn = Item_button(self.buttons_frame, 290, 64, rtopleft=15, rbottomleft=15, color=self.button_color, hover_color=self.button_hover_color, background="#5B5D76")
        dashboard_btn.grid(row=0, column=0, sticky='e')
        dashboard_btn.set_text('داشبورد', fill='#FFFFFF', font_size=self.button_font_size)
        
        # Create and configure the "Products" button
        products_btn = Item_button(self.buttons_frame, 290, 64, rtopleft=15, rbottomleft=15, color=self.button_color, hover_color=self.button_hover_color, background="#5B5D76")
        products_btn.grid(row=1, column=0, sticky='e')
        products_btn.set_text('محصولات', fill='#FFFFFF', font_size=self.button_font_size)
        
        # Create and configure the "Employee" button
        employee_btn = Item_button(self.buttons_frame, 290, 64, rtopleft=15, rbottomleft=15, color=self.button_color, hover_color=self.button_hover_color, background="#5B5D76")
        employee_btn.grid(row=2, column=0, sticky='e')
        employee_btn.set_text('کارمند', fill='#FFFFFF', font_size=self.button_font_size)
        
        # Create and configure the "Reports" button
        reports_btn = Item_button(self.buttons_frame, 290, 64, rtopleft=15, rbottomleft=15, color=self.button_color, hover_color=self.button_hover_color, background="#5B5D76")
        reports_btn.grid(row=3, column=0, sticky='e')
        reports_btn.set_text('گزارش', fill='#FFFFFF', font_size=self.button_font_size)
        
        # Create and configure the "Backup" button
        backup_btn = Item_button(self.buttons_frame, 290, 64, rtopleft=15, rbottomleft=15, color=self.button_color, hover_color=self.button_hover_color, background="#5B5D76")
        backup_btn.grid(row=4, column=0, sticky='e')
        backup_btn.set_text('بازیابی', fill='#FFFFFF', font_size=self.button_font_size)

    # Method to destroy the manager page and its components
    def destroy(self):
        self.main_frame.pack_forget()  # Remove the main frame from the layout
        self.main_frame.destroy()  # Destroy the main frame and its children