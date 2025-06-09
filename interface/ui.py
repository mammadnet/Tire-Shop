from customtkinter import *
from .widgets import *
from utilities import Concur
from time import sleep

from .panels import AdminEmployeePanel, AdminBackupPanel, ManagerProductPanel, ManagerEmployeePanel, ManagerReportPanel, EmployeeSellPanel, EmployeeReportPanel, ManagerDashboardPanel, AdminRestorePanel

from PIL import Image
import os
# Handles the creation and management of all widgets and logic for the user login interface.
class Login_page:
    def __init__(self, root, login_action):
        self.root = root
        
        # A callback function passed from the main application to handle the login verification logic.
        self.login_action = login_action
        
        self.main_frame = CTkFrame(root, fg_color='#494A5F')

        # Main container for contain whole widgets of page
        self.main_frame.pack(expand=True, fill='both')

        # Bind the "Enter" key to the login button command for better user experience.
        root.bind('<Return>', lambda event: self.btn_command())

        # Left frame of login page
        # This frame is for placing the image related to the login page

        left_frame = CTkFrame(self.main_frame, fg_color='#494A5F')
        left_frame.place(relx=0, rely=0, relwidth=0.6, relheight=1)

        # Load background image from the assets folder.
        currentpath = os.path.dirname(os.path.realpath(__file__))
        back = Image.open(currentpath + '/assets/login-background.png')
        image = CTkImage(back, size=(back.width*.715, back.height*.715))
        image_lable = CTkLabel(left_frame, image=image, text='', fg_color='transparent', )
        image_lable.place(relx=0, rely=0, anchor='nw')
        #-----------------------------------------------

        # Right frame of login page
        # This page is for placing the login entry like username and password
        right_frame = CTkFrame(self.main_frame, fg_color='transparent')
        right_frame.place(relx=.6, rely=0, relwidth=0.4, relheight=1)

        # Configure the grid layout to make the widgets within this frame responsive.
        right_frame.rowconfigure((0, 1, 2, 3), weight=1, uniform='a')
        right_frame.columnconfigure(0, weight=1, uniform='a')
        
        p = os.path.dirname(os.path.realpath(__file__))
        img = Image.open(p + "/assets/login-logo.png")
        
        self.logoimage = CTkLabel(right_frame, image=CTkImage(img, size=(230, 230)), text='', bg_color='transparent')
        self.logoimage.grid(row=0, sticky='nswe')

        # This just a container for contain login frame and place it on verticaly center
        login_frame_container = CTkFrame(right_frame, fg_color='#494A5F')
        login_frame_container.grid(row=1, column=0, rowspan=2, sticky='nsew')

        # Configure the grid layout for the container to center the login form.
        login_frame_container.rowconfigure((0,2), weight=1, uniform='a')
        login_frame_container.rowconfigure(1, weight=10, uniform='a')

        login_frame_container.columnconfigure((0,2), weight=1, uniform='a')
        login_frame_container.columnconfigure(1, weight=10, uniform='a')

        # A container for contain login entries
        login_frame = CTkFrame(login_frame_container, bg_color='transparent', fg_color='transparent')
        login_frame.grid(row=1, column=1)

        login_frame.rowconfigure((0, 1, 2, 4), weight=1, pad=30)
        login_frame.columnconfigure(0, weight=1)

        # A label to display login error messages.
        self.error_massage_lable = CTkLabel(login_frame, text_color='firebrick1')
        
        self.username = StringVar()
        self.password = StringVar()
        
        # Custom input widget for the username.
        username_entry = Input(login_frame, 30, 300, 50, 'نام کاربری', self.username, show_err_callback=self.login_error_message, just_english=True)
        username_entry.configure(font=(None, 18))
        username_entry.set_placeholder_text("نام کاربری")
        username_entry.grid(row=1, column=0)

        # Custom input widget for the password.
        password_entry = Input(login_frame, 30, 300, 50, 'رمز', self.password, show='*', show_err_callback = self.login_error_message)
        password_entry.configure(font=(None, 18))
        password_entry.set_placeholder_text("رمز")
        password_entry.grid(row=2, column=0)

        username_entry.set_textvariable(self.username)
        password_entry.set_textvariable(self.password)
            
        login_button = Btn(login_frame, 250, 50, 30, "ورود")
        login_button.grid(row=3, column=0)
        login_button.configure(font=(None, 18))
        login_button.configure(command=self.btn_command)
        
        # Add forgot password button
        forgot_password_button = Btn(login_frame, 250, 30, 20, "فراموشی رمز عبور")
        forgot_password_button.grid(row=4, column=0, pady=(10, 0))
        forgot_password_button.configure(font=(None, 14))
        forgot_password_button.configure(command=self.show_forgot_password_dialog)
        
    def get_frame(self):
        return self.main_frame
    
    # This method is called when the login button is pressed or Enter is hit.
    def btn_command(self):
        self.root.unbind('<Return>')  # Unbind the "Enter" key to prevent multiple calls while processing.
        self.login_action(self.username.get(), self.password.get(), self)
        
    # Displays a temporary error message on the screen.
    def login_error_message(self, message:str=None):
        if message:
            self.error_massage_lable.configure(text=message)
            self.error_massage_lable.grid(row=5, column=0, pady=(10, 0))  # Move error message below forgot password button
            # Use Concur to run the clearing function in a separate thread, so it doesn't freeze the UI.
            Concur(lambda : self._clear_login_error(5)).start()
    
    # A private helper method to automatically remove the error message after a delay.
    def _clear_login_error(self, sec):
        sleep(sec)
        self.error_massage_lable.grid_remove()
        
    # Destroys the login page frame to clean up resources.
    def destroy(self):
        self.main_frame.pack_forget()
        self.main_frame.destroy()

    # Creates and displays the "Forgot Password" dialog window.
    def show_forgot_password_dialog(self):
        dialog = ForgotPasswordDialog(self.root)
        # This waits for the dialog to be closed before the main window can be interacted with again.
        self.root.wait_window(dialog)

# Creates a new Toplevel window (a dialog) for the password recovery process.
# This class handles user verification and the subsequent password reset.
class ForgotPasswordDialog(CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("فراموشی رمز عبور")
        self.geometry("480x480")  # Larger window
        # This keeps the dialog window on top of its parent window.
        self.transient(parent)
        # This makes the dialog modal, so the user cannot interact with the main window.
        self.after(10, self.grab_set)
        # Will store the user object after successful verification.
        self.verified_user = None

        # Remove black margin by using only one main frame, fill all
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Main container
        main_frame = CTkFrame(self, fg_color='#494A5F')
        main_frame.grid(row=0, column=0, sticky='nsew', padx=0, pady=0)
        main_frame.grid_rowconfigure((0, 1, 2, 3), weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        # Title
        title_label = CTkLabel(main_frame, text=render_text("بازیابی رمز عبور"), font=(None, 28, 'bold'))
        title_label.grid(row=0, column=0, pady=(30, 30))

        self.national_id = StringVar()
        self.phone = StringVar()

        # Input frame
        input_frame = CTkFrame(main_frame, fg_color='transparent')
        input_frame.grid(row=1, column=0, pady=10)
        input_frame.grid_columnconfigure(0, weight=1)

        # National ID
        national_id_label = CTkLabel(input_frame, text=render_text("کد ملی:"), font=(None, 16))
        national_id_label.grid(row=0, column=0, pady=(0, 5), sticky='w')
        national_id_entry = CTkEntry(input_frame, textvariable=self.national_id, width=340, height=44, font=(None, 15), placeholder_text=render_text("کد ملی را وارد کنید"))
        national_id_entry.grid(row=1, column=0, pady=(0, 20))

        # Phone
        phone_label = CTkLabel(input_frame, text=render_text("شماره تلفن:"), font=(None, 16))
        phone_label.grid(row=2, column=0, pady=(0, 5), sticky='w')
        phone_entry = CTkEntry(input_frame, textvariable=self.phone, width=340, height=44, font=(None, 15), placeholder_text=render_text("شماره تلفن را وارد کنید"))
        phone_entry.grid(row=3, column=0, pady=(0, 20))

        # Check info button (larger, new text)
        check_btn = Btn(main_frame, 260, 48, 24, "بررسی اطلاعات")
        check_btn.grid(row=2, column=0, pady=30)
        check_btn.configure(font=(None, 18))
        check_btn.configure(command=self.retrieve_credentials)

        # NOTE: The following password fields are initialized but seem unused in the main workflow.
        # The actual password reset happens in a new window created by `show_password_reset_window`.
        self.new_pass_var = StringVar()
        self.confirm_pass_var = StringVar()
        self.pass_frame = CTkFrame(self, fg_color='transparent')
        self.pass_frame.grid(row=1, column=0, sticky='ew')
        self.pass_frame.grid_remove() # This frame is immediately hidden and never shown.
        self.pass_frame.grid_columnconfigure(0, weight=1)

        new_pass_label = CTkLabel(self.pass_frame, text=render_text("رمز عبور جدید:"), font=(None, 16))
        new_pass_label.grid(row=0, column=0, pady=(0, 5), sticky='w')
        new_pass_entry = CTkEntry(self.pass_frame, textvariable=self.new_pass_var, width=340, height=44, font=(None, 15), show='*', placeholder_text=render_text("رمز عبور جدید را وارد کنید"))
        new_pass_entry.grid(row=1, column=0, pady=(0, 15))

        confirm_pass_label = CTkLabel(self.pass_frame, text=render_text("تکرار رمز عبور:"), font=(None, 16))
        confirm_pass_label.grid(row=2, column=0, pady=(0, 5), sticky='w')
        confirm_pass_entry = CTkEntry(self.pass_frame, textvariable=self.confirm_pass_var, width=340, height=44, font=(None, 15), show='*', placeholder_text=render_text("تکرار رمز عبور جدید"))
        confirm_pass_entry.grid(row=3, column=0, pady=(0, 15))

        self.set_pass_btn = Btn(self.pass_frame, 220, 44, 20, "ثبت رمز جدید")
        self.set_pass_btn.grid(row=4, column=0, pady=10)
        self.set_pass_btn.configure(font=(None, 16))
        self.set_pass_btn.configure(command=self.set_new_password)

        # The following lines center the dialog window on top of its parent.
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - self.winfo_width()) // 2
        y = parent.winfo_y() + (parent.winfo_height() - self.winfo_height()) // 2
        self.geometry(f"+{x}+{y}")
        # Ensures the window is properly destroyed when the 'X' button is clicked.
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        # Set focus on the first input field.
        national_id_entry.focus()

    # Fetches user credentials from the database for verification.
    def retrieve_credentials(self):
        national_id = self.national_id.get().strip()
        phone = self.phone.get().strip()
        self.pass_frame.grid_remove()
        self.verified_user = None
        if not national_id or not phone:
            self.show_message(render_text("لطفا تمام فیلدها را پر کنید"), error=True)
            return
        try:
            # Importing here locally can help prevent circular dependencies.
            from database import session
            from database.crud import user_by_national_id_phone
            user = user_by_national_id_phone(session, national_id, phone)
            if user:
                self.verified_user = user
                # If the user is found, open the next step in the process.
                self.show_password_reset_window(user)
            else:
                self.show_message(render_text("کاربری با این مشخصات یافت نشد.\nلطفا کد ملی و شماره تلفن را با دقت وارد کنید."), error=True)
        except Exception as e:
            self.show_message(render_text("خطا در جستجوی کاربر:"), error=True)

    # Opens another dialog window to allow the verified user to set a new password.
    def show_password_reset_window(self, user):
        win = CTkToplevel(self)
        win.title("تغییر رمز عبور")
        win.geometry("400x320")
        win.transient(self)
        win.after(10, win.grab_set)
        win.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1) # Corrected row count
        win.grid_columnconfigure(0, weight=1)

        title = CTkLabel(win, text=f"نام کاربری: {user.user_name}", font=(None, 18, 'bold'))
        title.grid(row=0, column=0, pady=(20, 10))
        new_pass_var = StringVar()
        confirm_pass_var = StringVar()
        new_pass_label = CTkLabel(win, text=render_text("رمز عبور جدید:"), font=(None, 15))
        new_pass_label.grid(row=1, column=0, pady=(0, 5), sticky='w', padx=40)
        new_pass_entry = CTkEntry(win, textvariable=new_pass_var, width=260, height=40, font=(None, 14), show='*', placeholder_text=render_text("رمز عبور جدید را وارد کنید"))
        new_pass_entry.grid(row=2, column=0, pady=(0, 10))
        confirm_pass_label = CTkLabel(win, text=render_text("تکرار رمز عبور:"), font=(None, 15))
        confirm_pass_label.grid(row=3, column=0, pady=(0, 5), sticky='w', padx=40)
        confirm_pass_entry = CTkEntry(win, textvariable=confirm_pass_var, width=260, height=40, font=(None, 14), show='*', placeholder_text="تکرار رمز عبور جدید")
        confirm_pass_entry.grid(row=4, column=0, pady=(0, 10))
        msg_label = CTkLabel(win, text="", text_color="firebrick1", font=(None, 14))
        msg_label.grid(row=5, column=0, pady=(0, 10))
        
        # This nested function handles the logic for resetting the password.
        def do_reset():
            new_pass = new_pass_var.get().strip()
            confirm_pass = confirm_pass_var.get().strip()
            if not new_pass or not confirm_pass:
                msg_label.configure(text=render_text("لطفا هر دو فیلد رمز عبور را پر کنید."), text_color="firebrick1")
                return
            if new_pass != confirm_pass:
                msg_label.configure(text=render_text("رمزهای عبور مطابقت ندارند!"), text_color="firebrick1")
                return
            if len(new_pass) < 4:
                msg_label.configure(text=render_text("رمز عبور باید حداقل ۴ کاراکتر باشد."), text_color="firebrick1")
                return
            try:
                from database import session
                from database.crud import update_user_by_username
                update_user_by_username(session, user.user_name, password=new_pass)
                msg_label.configure(text=render_text("رمز عبور با موفقیت تغییر کرد!"), text_color="green")
                # Automatically close the window after a short delay on success.
                win.after(1500, win.destroy)
            except Exception as e:
                msg_label.configure(text=render_text("خطا در تغییر رمز عبور:"), text_color="firebrick1")

        reset_btn = Btn(win, 180, 40, 18, "ثبت رمز جدید")
        reset_btn.grid(row=6, column=0, pady=10)
        reset_btn.configure(font=(None, 15))
        reset_btn.configure(command=do_reset)
        new_pass_entry.focus()
    
    # NOTE: This method appears to be an alternative or old way of setting the password
    # and is not called in the current primary workflow.
    def set_new_password(self):
        new_pass = self.new_pass_var.get().strip()
        confirm_pass = self.confirm_pass_var.get().strip()
        if not new_pass or not confirm_pass:
            self.show_message(render_text("لطفا هر دو فیلد رمز عبور را پر کنید."), error=True)
            return
        if new_pass != confirm_pass:
            self.show_message(render_text("رمزهای عبور مطابقت ندارند!"), error=True)
            return
        if len(new_pass) < 4:
            self.show_message(render_text("رمز عبور باید حداقل ۴ کاراکتر باشد."), error=True)
            return
        try:
            from database import session
            from database.crud import update_user_by_username
            update_user_by_username(session, self.verified_user.user_name, password=new_pass)
            self.show_message(render_text("رمز عبور با موفقیت تغییر کرد!"), error=False)
        except Exception as e:
            self.show_message(render_text("خطا در تغییر رمز عبور:"), error=True)
    
    # A helper method to display a small, temporary message in a separate popup window.
    def show_message(self, msg, error=False):
        # Show a temporary message in a popup window
        win = CTkToplevel(self)
        win.title("پیام")
        win.geometry("340x120")
        win.transient(self)
        win.after(10, win.grab_set)
        label = CTkLabel(win, text=msg, text_color="firebrick1" if error else "green", font=(None, 15), wraplength=320)
        label.pack(expand=True, fill='both', padx=20, pady=20)
        # The message window will automatically destroy itself after 2.5 seconds.
        win.after(2500, win.destroy)

# This is a base class for all main application pages (e.g., Admin, Manager, Employee).
# It establishes a common layout with a main content area and a sidebar for navigation and user info.
class Page:
    def __init__(self, root, name:str, lastname:str, rule:str, logout_callback=None):
        # The main container frame for this page.
        self.main_frame = CTkFrame(root)
        self.main_frame.pack(expand=True, fill='both')
        
        # A callback function to be executed when the logout button is clicked.
        self.logout_callback = logout_callback
        
        # The right-hand sidebar, typically used for navigation buttons and user profile.
        self.items_frame = CTkFrame(self.main_frame)
        self.items_frame.configure(fg_color='#5B5D76')
        self.items_frame.place(relwidth = .3, relheight=1, relx=.7, rely=0, anchor='nw')
        
        # The main content area on the left, where different functional panels will be displayed.
        self.control_frame = CTkFrame(self.main_frame)
        self.control_frame.configure(fg_color='#494A5F')
        self.control_frame.place(relwidth=.7,relheight=1, relx=0, rely=0)
        
        # A container at the top of the sidebar for the user profile section.
        self.user_profile_container = CTkFrame(self.items_frame)
        self.user_profile_container.configure(fg_color='transparent')
        self.user_profile_container.place(x=0, y=0, relwidth = 1, relheight=.15)
        
        # The inner frame that visually holds the user's name, role, and logout button.
        self.user_profile_frame = CTkFrame(self.user_profile_container)
        self.user_profile_frame.configure(fg_color='#393A4E', corner_radius=18)
        self.user_profile_frame.place(relx=.5, rely=.5, relwidth=.75, relheight=.6, anchor='center')
        
        # Initialize the user profile display and the logout button.
        self.set_profile(name, lastname, rule)
        self._set_logout_btn()
        
    
    # Populates the user profile frame with the logged-in user's information.
    def set_profile(self, name:str, lastname:str, rule:str)   :
        # Capitalize strings for consistent display formatting.
        name = name.capitalize()
        lastname= lastname.capitalize()
        rule = rule.capitalize()
         
        self.user_name_lastname = CTkLabel(self.user_profile_frame, text=f'{name} {lastname}')
        self.user_name_lastname.configure(text_color="white", height=5)
        self.user_name_lastname.place(relx=.25, rely=.23)
        
        self.rule = CTkLabel(self.user_profile_frame, text=rule)
        self.rule.configure(text_color="white", height=20)
        self.rule.place(relx=.25, rely=.47)
        
    # A private helper method to create and configure the logout button.
    def _set_logout_btn(self):
        # Load the logout icon from the assets directory.
        p = os.path.dirname(os.path.realpath(__file__))
        img = Image.open(p + "/assets/logout.png")
        logoutImage = CTkImage(img)
        self.btn_logout = Btn(self.user_profile_frame, image=logoutImage, height=0, width=0,border_spacing=0,corner_radius=5, anchor='center')
        self.btn_logout.configure(fg_color='transparent')
        
        # self.btn_logout.disable_hover()
        self.btn_logout.place(relx=.9, rely=.5, anchor='center')
        
        # If a logout callback function was provided, assign it to the button's command.
        if self.logout_callback:
            self.btn_logout.configure(command=lambda : self.logout_callback(self))
        
         
    
    
    # Removes the page's main frame from the window, effectively closing the page.
    def destroy(self):
        self.main_frame.pack_forget()
        self.main_frame.destroy()
        

# Defines the specific user interface for the 'Admin' user.
# It inherits the basic layout from the Page class and adds navigation
# for admin-specific functions like user management and data backup/restore.
class Admin_page(Page):
    def __init__(self, root, name:str, lastname:str, rule:str, logout_callback=None):
        # Initialize the parent Page class to set up the basic layout.
        super().__init__(root, name, lastname, rule, logout_callback)
        
        # Create a frame within the sidebar to hold the navigation buttons.
        self.buttons_frame = CTkFrame(self.items_frame)
        self.buttons_frame.configure(fg_color='transparent')
        self.buttons_frame.place(relx=0, rely=.15, relwidth=1, relheight=.85)
        
        # Configure the grid layout for the buttons frame to space buttons evenly.
        self.buttons_frame.rowconfigure((0,1,2,3,4,5,6,7,8), weight=1)
        self.buttons_frame.columnconfigure(0, weight=1)
        
        # Define common styling for the navigation buttons.
        self.button_font_size = 14
        self.button_color = "#393A4E"
        self.button_hover_color = "#434357"
        
        # --- Navigation Buttons ---
        user_btn = Item_button(self.buttons_frame, 290, 64, rtopleft=15, rbottomleft=15, color=self.button_color,hover_color=self.button_hover_color,background="#5B5D76")
        user_btn.set_text('کاربران', fill='#FFFFFF', font_size=self.button_font_size)
        user_btn.set_action(lambda _: self.toggle_panel('users'))
        user_btn.grid(row=2, column=0, sticky='e')
        
        reports_btn = Item_button(self.buttons_frame, 290, 64, rtopleft=15, rbottomleft=15, color=self.button_color,hover_color=self.button_hover_color,background="#5B5D76")
        reports_btn.set_action(lambda _: self.toggle_panel('backup'))
        reports_btn.set_text('بکاپ', fill='#FFFFFF', font_size=self.button_font_size)
        reports_btn.grid(row=3, column=0, sticky='e')
        
        backup_btn = Item_button(self.buttons_frame, 290, 64, rtopleft=15, rbottomleft=15, color=self.button_color,hover_color=self.button_hover_color,background="#5B5D76")
        backup_btn.set_action(lambda _: self.toggle_panel('restore'))
        backup_btn.set_text('بازیابی', fill='#FFFFFF', font_size=self.button_font_size)
        backup_btn.grid(row=4, column=0, sticky='e')
        
        # This variable keeps track of which panel is currently being displayed.
        self.current_panel = None
        
        #----------------DELETE THIS LINES AFTER FINISH THE ADMIN PANEL DEVELOPMENT-----------
        # self.employee_panel(self.control_frame)

        # Initialize attributes to hold the frame instances for each panel.
        self.employee_frame = None
        self.backup_frame = None
        self.restore_frame = None

        # Display the 'users' panel by default when the admin page is first loaded.
        self.toggle_panel('users')
    
    # This method acts as a controller to switch between different content panels
    # in the main content area (self.control_frame).
    def toggle_panel(self, panel:str):
        # --- Users Panel ---
        # Only switch if the requested panel is not already the current one.
        if panel == 'users' and self.current_panel != 'users':
            # Destroy other panels to free up memory and prevent overlap.
            if self.backup_frame:
                self.backup_frame.destroy()
            if self.restore_frame:
                self.restore_frame.destroy()
            # Create and display the new panel.
            self.employee_frame = AdminEmployeePanel(self.control_frame)
            # Update the state of the current panel.
            self.current_panel = 'users'

        # --- Backup Panel ---
        elif panel == 'backup' and self.current_panel != 'backup':
            if self.employee_frame:
                self.employee_frame.destroy()
            if self.restore_frame:
                self.restore_frame.destroy()
            self.backup_frame = AdminBackupPanel(self.control_frame)
            self.current_panel = 'backup'

        # --- Restore Panel ---
        elif panel == 'restore' and self.current_panel != 'restore':
            if self.employee_frame:
                self.employee_frame.destroy()
            if self.backup_frame:
                self.backup_frame.destroy()
            self.restore_frame = AdminRestorePanel(self.control_frame)
            self.current_panel = 'restore'

        
        
        
        
        
        
        
    # This seems to be an unused helper method, possibly for debugging purposes.
    def _set_semple_lable(self, message):
        self.loggedin_lable = CTkLabel(self.main_frame, text_color='blue', text=message)
        self.loggedin_lable.pack(expand=True, fill='both')
        
    
    # Destroys the main frame of the page to clean up all its widgets.
    def destroy(self):
        self.main_frame.pack_forget()
        self.main_frame.destroy()
# Defines the specific user interface for the 'Manager' user.
# It inherits from the Page class and provides navigation to panels for
# dashboard, product management, employee management, and reports.
class Manager_page(Page):
    def __init__(self, root, name, lastname, rule, logout_callback=None):
        # Initialize the parent Page class to set up the basic layout.
        super().__init__(root, name, lastname, rule, logout_callback)
        
        # Create a frame within the sidebar for the navigation buttons.
        self.buttons_frame = CTkFrame(self.items_frame)
        self.buttons_frame.configure(fg_color='transparent')
        self.buttons_frame.place(relx=0, rely=.15, relwidth=1, relheight=.85)
        
        # Configure the grid layout for the buttons frame.
        self.buttons_frame.rowconfigure((0,1,2,3,4,5,6,7,8), weight=1)
        self.buttons_frame.columnconfigure(0, weight=1)
        
        # Define common styling for the navigation buttons.
        self.button_font_size = 14
        self.button_color = "#393A4E"
        self.button_hover_color = "#434357"
        
        # --- Navigation Buttons ---
        dashboard_btn = Item_button(self.buttons_frame, 290, 64, rtopleft=15, rbottomleft=15, color=self.button_color,hover_color=self.button_hover_color,background="#5B5D76")
        dashboard_btn.set_action(lambda _: self.toggle_panel('dashboard'))
        dashboard_btn.set_text('داشبورد', fill='#FFFFFF', font_size=self.button_font_size)
        dashboard_btn.grid(row=0, column=0, sticky='e')
        
        products_btn = Item_button(self.buttons_frame, 290, 64, rtopleft=15, rbottomleft=15, color=self.button_color,hover_color=self.button_hover_color,background="#5B5D76")
        products_btn.set_action(lambda _: self.toggle_panel('products'))
        products_btn.set_text('محصولات', fill='#FFFFFF', font_size=self.button_font_size)
        products_btn.grid(row=1, column=0, sticky='e')
        
        employee_btn = Item_button(self.buttons_frame, 290, 64, rtopleft=15, rbottomleft=15, color=self.button_color,hover_color=self.button_hover_color,background="#5B5D76")
        employee_btn.set_action(lambda _: self.toggle_panel('employee'))
        employee_btn.set_text('کارمند', fill='#FFFFFF', font_size=self.button_font_size)
        employee_btn.grid(row=2, column=0, sticky='e')
        
        reports_btn = Item_button(self.buttons_frame, 290, 64, rtopleft=15, rbottomleft=15, color=self.button_color,hover_color=self.button_hover_color,background="#5B5D76")
        reports_btn.set_action(lambda _: self.toggle_panel('report'))
        reports_btn.set_text('گزارش', fill='#FFFFFF', font_size=self.button_font_size)
        reports_btn.grid(row=3, column=0, sticky='e')

        # Initialize attributes to hold the frame instance for each panel.
        self.current_panel = None
        self.product_frame = None
        self.employee_frame = None
        self.report_frame = None
        self.dashboard_frame = None
        # Set the 'dashboard' as the default panel to display.
        self.toggle_panel('dashboard')
        
    # This method manages switching between the different content panels.
    # It destroys the old panel before creating the new one to manage resources.
    def toggle_panel(self, panel:str):
        if panel == 'products' and self.current_panel != 'products':
            # Destroy all other panels before creating the new one.
            if self.dashboard_frame:
                self.dashboard_frame.destroy()
            if self.employee_frame:
                self.employee_frame.destroy()
            if self.report_frame:
                self.report_frame.destroy()
            self.product_frame = ManagerProductPanel(self.control_frame)
            self.current_panel = 'products'
        elif panel == 'employee' and self.current_panel != 'employee':
            if self.dashboard_frame:
                self.dashboard_frame.destroy()
            if self.report_frame:
                self.report_frame.destroy()
            if self.product_frame:
                self.product_frame.destroy()
            self.employee_frame = ManagerEmployeePanel(self.control_frame)
            self.current_panel = 'employee'
        elif panel == 'report' and self.current_panel != 'report':
            if self.dashboard_frame:
                self.dashboard_frame.destroy()
            if self.product_frame:
                self.product_frame.destroy()
            if self.employee_frame:
                self.employee_frame.destroy()
            self.report_frame = ManagerReportPanel(self.control_frame)
            self.current_panel = 'report'
        elif panel == 'dashboard' and self.current_panel != 'dashboard':
            if self.product_frame:
                self.product_frame.destroy()
            if self.employee_frame:
                self.employee_frame.destroy()
            if self.report_frame:
                self.report_frame.destroy()
            self.dashboard_frame = ManagerDashboardPanel(self.control_frame)
            self.current_panel = 'dashboard'
        else:
            # This case handles an invalid panel name, which can be useful for debugging.
            print("Panel not found")

    # Destroys the main frame of the page to clean up all its widgets.
    def destroy(self):
        self.main_frame.pack_forget()
        self.main_frame.destroy()
        
# Defines the specific user interface for the 'Employee' user.
# It inherits from the Page class and provides navigation for sales and reports.
class Employee_page(Page):
    def __init__(self, root, name, lastname, rule, logout_callback=None):
        # Initialize the parent Page class to set up the basic layout.
        super().__init__(root, name, lastname, rule, logout_callback)
        
        # Create a frame within the sidebar for the navigation buttons.
        self.buttons_frame = CTkFrame(self.items_frame)
        self.buttons_frame.configure(fg_color='transparent')
        self.buttons_frame.place(relx=0, rely=.15, relwidth=1, relheight=.85)
        
        
        self.buttons_frame.rowconfigure((0,1,2,3,4,5,6,7,8), weight=1)
        self.buttons_frame.columnconfigure(0, weight=1)
        
        self.button_font_size = 14
        self.button_color = "#393A4E"
        self.button_hover_color = "#434357"
        
        # --- Navigation Buttons ---
        sell_btn = Item_button(self.buttons_frame, 290, 64, rtopleft=15, rbottomleft=15, color=self.button_color,hover_color=self.button_hover_color,background="#5B5D76")
        sell_btn.set_action(lambda _: self.toggle_panel('sell'))
        sell_btn.set_text('فروش', fill='#FFFFFF', font_size=self.button_font_size)
        sell_btn.grid(row=0, column=0, sticky='e')
        
        
        reports_btn = Item_button(self.buttons_frame, 290, 64, rtopleft=15, rbottomleft=15, color=self.button_color,hover_color=self.button_hover_color,background="#5B5D76")
        reports_btn.set_action(lambda _: self.toggle_panel('report'))
        reports_btn.set_text('گزارش', fill='#FFFFFF', font_size=self.button_font_size)
        reports_btn.grid(row=2, column=0, sticky='e')
        
        # Initialize attributes to hold the frame instance for each panel.
        self.current_panel = None
        self.employee_sell_panel = None
        self.employee_report_panel = None
        
        # Set the 'sell' panel as the default view for the employee page.
        self.toggle_panel("sell")

    # This method manages switching between the 'sell' and 'report' panels.
    def toggle_panel(self, panel:str):
        if panel == 'sell' and self.current_panel != 'sell':
            # If the report panel exists, destroy it.
            if self.employee_report_panel:
                self.employee_report_panel.destroy()
            # Create the sales panel.
            self.employee_sell_panel = EmployeeSellPanel(self.control_frame)
            self.current_panel = 'sell'
        elif panel == 'report' and self.current_panel != 'report':
            # If the sales panel exists, destroy it.
            if self.employee_sell_panel:
                self.employee_sell_panel.destroy()
            # Create the report panel.
            self.employee_report_panel = EmployeeReportPanel(self.control_frame)
            self.current_panel = 'report'

    # Destroys the main frame of the page to clean up all its widgets.
    def destroy(self):
        self.main_frame.pack_forget()
        self.main_frame.destroy()