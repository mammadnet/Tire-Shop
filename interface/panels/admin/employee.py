from customtkinter import *
from ..panel import Panel
from ...widgets import Item_button, Input, Btn, DropDown, render_text, create_input_fields
from awesometkinter.bidirender import derender_text, isarabic
from database import session, create_new_user
from database import remove_user_by_username, update_user_by_username, user_by_username
from database import get_all_employee_and_manager_json, get_all_employee_and_manager_usernames
from utilities import is_windows
from tkinter import ttk


# This class manages the entire UI panel for employee and manager administration,
# including listing, creating, deleting, and editing users.
class AdminEmployeePanel(Panel):
    def __init__(self, root):
        super().__init__(root)
        self.pack(expand=True, fill="both")
        self.configure(bg_color='transparent', fg_color='transparent')
        
        # --- Navigation Buttons ---
        # A frame on the right side to hold the main navigation buttons for this panel.
        self.btn_frame = CTkFrame(self, fg_color='transparent')
        self.btn_frame.place(relwidth=.2, relheight=.3, relx=1, rely=.1, anchor="ne")
        self.btn_frame.columnconfigure(0, weight=1)
        self.btn_frame.rowconfigure((0,1,2,3), weight=1)

        # Button to switch to the user list view.
        employee_list_btn = Item_button(self.btn_frame, 150, 50, rtopleft=20, rbottomleft=20, color="#393A4E", hover_color="#434357", background="#494A5F")
        employee_list_btn.set_text("لیست کاربران", "white", 13)
        employee_list_btn.grid(row=0,column=0 ,sticky="e")
        employee_list_btn.set_action(lambda e: self.toggle_view('list'))
        
        # Button to switch to the "new user" form.
        employee_new_btn = Item_button(self.btn_frame, 150, 50, rtopleft=20, rbottomleft=20, color="#393A4E", hover_color="#434357", background="#494A5F")
        employee_new_btn.set_text("کاربر جدید", "white", 13)
        employee_new_btn.grid(row=1,column=0 , sticky="e")
        employee_new_btn.set_action(lambda e: self.toggle_view('new'))

        # Button to switch to the delete user view.
        employee_delete_btn = Item_button(self.btn_frame, 150, 50, rtopleft=20, rbottomleft=20, color="#393A4E", hover_color="#434357", background="#494A5F")
        employee_delete_btn.set_text( "حذف کاربر","white", 13)
        employee_delete_btn.grid(row=2,column=0 , sticky="e")
        employee_delete_btn.set_action(lambda e: self.toggle_view('delete'))

        # Button to switch to the edit user view.
        employee_update_btn = Item_button(self.btn_frame, 150, 50, rtopleft=20, rbottomleft=20, color="#393A4E", hover_color="#434357", background="#494A5F")
        employee_update_btn.set_text("تغییرات کاربر", "white", 13)
        employee_update_btn.grid(row=3,column=0 , sticky="e")
        employee_update_btn.set_action(lambda e: self.toggle_view('edit'))
        
        
        self.error_message_label = CTkLabel(self, text_color="firebrick1")
        self.success_message_label = CTkLabel(self, text_color="green")
        self.new_employee_inputs: list[Input] = []

        # --- View Initialization ---
        # All views (list, new, delete, edit) are created at the start but are hidden.
        # This prevents recreating widgets every time the view is switched.
        self.table = self.initialize_table(self)
        self.table.place_forget()
        
        # The 'new employee' form is created once and stored.
        self.employee_new(self)
        self.new_employee_frame = self.winfo_children()[-1]
        self.new_employee_frame.place_forget()
        
        # Frames for delete and edit views are created but populated later.
        self.delete_user_frame = CTkFrame(self, fg_color="#5B5D76")
        self.delete_user_comboBox = None
        self.delete_user_btn = None
        
        self.edit_user_frame = CTkFrame(self, fg_color="#5B5D76")
        self.edit_user_combobox = None
        self.edit_user_inputs = None
        
        # The panel starts by showing the user list.
        self.current_view = None
        self.toggle_view('list')

    # This method is the central controller for switching between the different views (list, new, delete, edit).
    def toggle_view(self, view_name):
        # Only switch if the requested view is not the current one.
        if view_name == 'list' and self.current_view != 'list':
            # Hide all other main view frames.
            self.new_employee_frame.place_forget()
            self.delete_user_frame.place_forget() 
            self.edit_user_frame.place_forget()
            # Show the table and refresh its content.
            self.table.place(relheight=.9, relwidth=.8, relx=.02, rely=.05)
            self.current_view = 'list'
            self.insert_content_to_table(self.table, get_all_employee_and_manager_json(session))
        elif view_name == 'new' and self.current_view != 'new':
            self.table.place_forget()
            self.delete_user_frame.place_forget()
            self.edit_user_frame.place_forget()
            self.new_employee_frame.place(relheight=.9, relwidth=.8, relx=.02, rely=.05)
            self.current_view = 'new'
        elif view_name == 'delete' and self.current_view != 'delete':
            self.table.place_forget()
            self.new_employee_frame.place_forget()
            self.edit_user_frame.place_forget()
            # Build or update the delete user UI.
            self.delete_user(self, get_all_employee_and_manager_json(session))
            self.current_view = 'delete'
        elif view_name == 'edit' and self.current_view != 'edit':
            self.table.place_forget()
            self.new_employee_frame.place_forget()
            # Build or update the edit user UI.
            self.employee_edit(self)
            self.current_view = 'edit'

    #---------------------- Setup Employee table content----------------
    # Sets up and styles the ttk.Treeview widget used for displaying the user list.
    def initialize_table(self, window):
        style = ttk.Style()
        # 'clam' theme is used on Windows for better visual compatibility.
        if is_windows():
            style.theme_use('clam')
        
        # Configure the custom style for the Treeview body.
        style.configure("Custom1.Treeview",
        background="#494A5F",
        foreground="black",
        fieldbackground="#393A4E",
        rowheight=50,
        borderwidth=0
        )
        
        # Configure the custom style for the Treeview heading.
        style.configure("Custom1.Treeview.Heading",
        background="#5B5D76",
        foreground="white",
        font=("Helvetica", 10, "bold"),
        relief='flat')
        
        # Configure the hover effect for the heading.
        style.map("Custom1.Treeview.Heading",
        background=[("active", "#6b6d87")],
        foreground=[("active", "white")])
        
        table = ttk.Treeview(window, style="Custom1.Treeview")
        table.configure(columns=("id", "name", "lastname", "username", "phone", "national", "startDate"))
        table.configure(show="headings", selectmode="none")
        
        # Define column properties.
        table.column("id", width=40, anchor="center")
        table.column("name", width=100, anchor="center")
        table.column("lastname", width=150, anchor="center")
        table.column("username", width=120, anchor="center")
        table.column("phone", width=140, anchor="center")
        table.column("national", width=150, anchor="center")
        table.column("startDate", width=200, anchor="center")
        
        # Define column headings.
        table.heading("id", text="id", anchor='center')
        table.heading("name", text="name", anchor='center')
        table.heading("lastname", text="lastname", anchor='center')
        table.heading("username", text="username", anchor='center')
        table.heading("phone", text="phone", anchor='center')
        table.heading("national", text="national", anchor='center')
        table.heading("startDate", text="startDate", anchor='center')
        
        table.place(relheight=.9, relwidth=.8, relx=.02, rely=.05)
        return table
        
    
    # Clears the existing data from the table and inserts new content.
    def insert_content_to_table(self, table:ttk.Treeview, content:list[dict]):
        # Delete all existing items in the treeview.
        table.delete(*table.get_children())
        
        # Insert new rows from the content list.
        for row in content:
            vals = (row["id"], row["name"], row["lastname"], row["username"], row["phone"], row["national_number"])
            table.insert(parent="", index=0, values=vals)
            
    #--------------------------------------------------------------------
    
    # Creates the form (widgets) for adding a new employee.
    def employee_new(self, window):
        content_frame = CTkFrame(window, fg_color="#5B5D76")
        content_frame.place(relheight=.9, relwidth=.8, relx=.02, rely=.05)
        content_frame.rowconfigure(tuple(range(0, 8)), weight=1)
        content_frame.columnconfigure((1,2,3), weight=10)
        content_frame.columnconfigure(0, weight=4)
        content_frame.columnconfigure(4, weight=4)
        
        # Dropdown to select the user's role (Employee or Manager).
        rule_label = CTkLabel(content_frame, text="Rule:", text_color="white", font=(None, 15))
        rule_label.grid(row=0, column=1)
        combo_rule_items = ['Employee', 'Manager']
        rule_comboBox = DropDown(content_frame, values=combo_rule_items)
        rule_comboBox.grid(row=0, column=2)

        # --- Input Fields ---
        name = StringVar()
        name_input = create_input_fields(content_frame, render_text("نام:"), 1, 1, "name", None,just_text=True, show_err_callback=self.show_error_message)
        name_input.set_textvariable(name)
        self.new_employee_inputs.append(name_input)

        lastname = StringVar()
        lastname_input = create_input_fields(content_frame, render_text("نام خونوادگی:"), 1, 3, "name", None,just_text=True, show_err_callback=self.show_error_message)
        lastname_input.set_textvariable(lastname)
        self.new_employee_inputs.append(lastname_input)

        national = StringVar()
        national_input =  create_input_fields(content_frame, render_text("کد ملی:"), 2, 1, "national", None,just_english=True, just_number=True, show_err_callback=self.show_error_message)
        national_input.set_textvariable(national)
        self.new_employee_inputs.append(national_input)

        phone = StringVar()
        phone_input =  create_input_fields(content_frame, render_text("شماره تلفن:"), 2, 3, "phone", None,just_english=True,just_number=True, show_err_callback=self.show_error_message)
        phone_input.set_textvariable(phone)
        self.new_employee_inputs.append(phone_input)

        username = StringVar()
        username_input =  create_input_fields(content_frame, render_text("نام کاربری:"), 3, 1, "username", None,just_english=True, show_err_callback=self.show_error_message)
        username_input.set_textvariable(username)
        self.new_employee_inputs.append(username_input)

        password = StringVar()
        password_input =  create_input_fields(content_frame, render_text("رمز:"), 3, 3, "password", None,just_english=True, char_limit=25, show_err_callback=self.show_error_message)
        password_input.set_textvariable(password)
        self.new_employee_inputs.append(password_input)

        password_repeate = StringVar()
        password_repeate_input =  create_input_fields(content_frame, render_text("تکرار رمز عبور:"), 4, 3, "repeat_password", None,just_english=True, char_limit=25, show_err_callback=self.show_error_message)
        password_repeate_input.set_textvariable(password_repeate)
        self.new_employee_inputs.append(password_repeate_input)

        # The 'Create User' button.
        btn = Btn(content_frame, 160, 45)
        # The command lambda passes all current input values to the action method.
        btn.configure(command=lambda : self.new_employee_action(
            self.show_error_message,
            name_input.get(), lastname_input.get(), national_input.get(),
            phone_input.get(), username_input.get(), password_input.get(),
            password_repeate_input.get(), rule_comboBox.get()))
        btn.configure(font=(None, 16))
        btn.set_text(text='ایجاد کاربر')
        btn.grid(row=5, column=2)
        
    
    # The logic executed when the 'Create User' button is clicked.
    def new_employee_action(self, show_err_callback, name:str=None,\
                            lastname:str=None, national:str=None, phone:str=None,\
                            username:str=None, password:str=None, repeat_password:str=None, rule:str=None):
        
        # First, validate the inputs.
        if self.check_value_inputs_in_new_imployee(show_err_callback, name, lastname, national, phone, username, password, repeat_password):
            try:
                # If validation passes, attempt to create the user in the database.
                create_new_user(session, name, lastname, phone, national, rule, username, password)
                self.show_success_message("New user was created")
                self.clear_new_employee_inputs()
            except Exception as e:
                # Show any database-level exceptions (e.g., username already exists).
                show_err_callback(e)
                
            
    # Helper method to clear all input fields in the 'new employee' form.
    def clear_new_employee_inputs(self):
        for input in self.new_employee_inputs:
            input.clear()
            
    # A helper method to perform local validation on the new employee form inputs.
    def check_value_inputs_in_new_imployee(self, show_err_callback, name:str=None, lastname:str=None, national:str=None, phone:str=None,\
                        username:str=None, password:str=None, repeat_password:str=None):
                    
        if not (name and lastname and national and phone and username and password and repeat_password):
            show_err_callback("Inputs cannot be empty.")
            return False
        
        if not (password == repeat_password):
            show_err_callback("password and repeated password should be the same")
            return False
        
        if len(password) < 8:
            show_err_callback("The minimum number of characters in the password must be 8")
            return False
        
        return True
            
    #-----------------DELETE USER PANEL-------------------------
            
    # Builds and displays the UI for deleting a user.
    def delete_user(self, window, users:list):
        # Use the existing frame if available.
        if self.delete_user_frame:
            content_frame = self.delete_user_frame
        else:
            content_frame = CTkFrame(window, fg_color="#5B5D76")
            self.delete_user_frame = content_frame
        
        content_frame.place(relheight=.9, relwidth=.8, relx=.02, rely=.05)
        content_frame.rowconfigure((0, 3), weight=1)
        content_frame.columnconfigure((0, 1), weight=1, pad=20, uniform='a')


        text = render_text("نام کاربری:")
        username_label = CTkLabel(content_frame, text=text, text_color="white", font=(None, 15))
        username_label.grid(row=0, column=1)
        # Create a list of strings for the dropdown, including name for context.
        combo_delete_items = ["{}:{} {}".format(user['username'], user['name'], user['lastname']) for user in users]
        # Recreate the dropdown to ensure the user list is always up-to-date.
        if self.delete_user_comboBox:
            self.delete_user_comboBox.destroy()
        
        self.delete_user_comboBox = DropDown(content_frame, values=combo_delete_items, width=250)
        self.delete_user_comboBox.grid(row=0, column=0)
        
        # Create the delete button only once.
        if not self.delete_user_btn:
            self.delete_user_btn = Btn(content_frame, 160, 45)
            self.delete_user_btn.configure(font=(None, 16))
            self.delete_user_btn.set_text(text='حذف کاربر')
            self.delete_user_btn.grid(row=1, column=0, columnspan=4)
        
        # Configure the button's command to pass the selected username to the action method.
        self.delete_user_btn.configure(command=lambda : self.delete_user_action(self.delete_user_comboBox.get().split(':')[0], self.show_error_message, self.show_success_message))

    # The logic executed when the 'Delete User' button is clicked.
    def delete_user_action(self, username, show_msg_callback, show_success_msg_callback):
        try:
            # Attempt to remove the user from the database.
            remove_user_by_username(session, username)
        except Exception as e:
            show_msg_callback(e)
            return # Prevent success message from showing on error.
        
        show_success_msg_callback("User was deleted")
        # Refresh the delete user UI to update the dropdown list.
        self.delete_user(self, get_all_employee_and_manager_json(session))
    
    #-----------------------------------------------------------------
    
    # Builds and displays the UI for editing a user's details.
    def employee_edit(self, window):
        
        if self.edit_user_frame:
            content_frame = self.edit_user_frame
        else:
            content_frame = CTkFrame(window, fg_color="#5B5D76")
            self.edit_user_frame = content_frame
            
        content_frame.place(relheight=.9, relwidth=.8, relx=.02, rely=.05)
        content_frame.rowconfigure(tuple(range(0, 8)), weight=1)


        content_frame.columnconfigure((1,2, 3), weight=10, pad=40, uniform='a')
        content_frame.columnconfigure(0, weight=1, pad=20, uniform='a')
        content_frame.columnconfigure(4, weight=1, pad=20, uniform='a')
        # Label and dropdown to select user by username

        select_user_label = CTkLabel(content_frame, text="Username:", text_color="white", font=(None, 15))
        select_user_label.grid(row=0, column=1)

        usernames = get_all_employee_and_manager_usernames(session)
        selected_username = StringVar()
        # Recreate the dropdown to ensure the list is fresh.
        if self.edit_user_combobox:
            self.edit_user_combobox.grid_forget()
            self.edit_user_combobox.destroy()
        # The 'command' argument links the load_user_data method to the dropdown's selection event.
        self.edit_user_combobox = DropDown(content_frame, values=usernames, variable=selected_username, command=self.load_user_data)
        self.edit_user_combobox.grid(row=0, column=2)

        # Dictionary to hold the input field widgets for easy access.
        if not self.edit_user_inputs:
            self.edit_user_inputs = {}
        

        self.create_input_field(content_frame, render_text("نام:"), 1, 1, 'name', just_text=True, show_err_callback=self.show_error_message)
        self.create_input_field(content_frame, render_text("نام خانوادگی:"), 1, 3, 'lastname', just_text=True, show_err_callback=self.show_error_message)
        self.create_input_field(content_frame, render_text("شماره ملی:"), 2, 1, 'national', just_number=True, just_english=True, show_err_callback=self.show_error_message)
        self.create_input_field(content_frame, render_text("شماره تلفن:"), 2, 3, 'phone', just_number=True,just_english=True, show_err_callback=self.show_error_message)
        self.create_input_field(content_frame, render_text("نام کاربری:"), 3, 1, 'username', show_err_callback=self.show_error_message, just_english=True)
        
        # The 'Update Information' button.
        update_btn = Btn(content_frame, 160, 45)
        update_btn.configure(command=lambda: self.update_user_action(
            self.edit_user_combobox.get(), # The user being edited.
            # The new values from the input fields.
            self.edit_user_inputs['name'].get(),
            self.edit_user_inputs['lastname'].get(),
            self.edit_user_inputs['phone'].get(),
            self.edit_user_inputs['national'].get(),
            self.edit_user_inputs['username'].get(),
            None, # Password field is not implemented in this form.
            self.show_error_message,
            self.show_success_message
        ))
        update_btn.configure(font=(None, 16))
        update_btn.set_text(text="بروزرسانی اطلاعات")
        update_btn.grid(row=6, column=0, columnspan=4)

    # Helper function to create a labeled input field within the edit form.
    def create_input_field(self, window, label_text, row, column, field_key, **kwargs):

        create_input_fields(window, label_text, row, column, field_key, container=self.edit_user_inputs, font_size=15, **kwargs)
        


    # This method is called whenever a new user is selected in the 'edit' dropdown.
    def load_user_data(self, username):
        """Fetches the selected user's data and populates the form fields with it."""
        user_data = user_by_username(session, username)
        if user_data:

            # Use set_placeholder_text to show the current data in the input fields.
             
            self.edit_user_inputs['name'].set_placeholder_text(derender_text(user_data.name) if isarabic(user_data.name) else user_data.name)
            self.edit_user_inputs['lastname'].set_placeholder_text(derender_text(user_data.lastname) if isarabic(user_data.lastname) else user_data.lastname)
            self.edit_user_inputs['national'].set_placeholder_text(derender_text(user_data.national_number) if isarabic(user_data.national_number) else user_data.national_number)
            self.edit_user_inputs['phone'].set_placeholder_text(derender_text(user_data.phone) if isarabic(user_data.phone) else user_data.phone)
            self.edit_user_inputs['username'].set_placeholder_text(derender_text(user_data.user_name) if isarabic(user_data.user_name) else user_data.user_name)
            # self.edit_user_inputs['password'].set_placeholder_text(user_data.password)

    
    # The logic executed when the 'Update Information' button is clicked.
    def update_user_action(self, username, name, lastname, phone, national, new_username, password, show_error_callback, show_success_callback):
        try:
            # Call the database update function with the new data.
            update_user_by_username(session, username, name, lastname, phone, national, new_username, password)
            show_success_callback(f'The user information has been changed.')
            # Refresh the edit panel to update the dropdown and clear fields.
            self.employee_edit(self)
            for v in list(self.edit_user_inputs.values()):
                v.textvariable.set('')

        except Exception as e:
            # Show any database-level exceptions (e.g., new username is taken).
            show_error_callback(e)
            
    # Overrides the default destroy method to ensure the panel is correctly removed from view.
    def destroy(self):
        self.pack_forget()
        super().destroy()