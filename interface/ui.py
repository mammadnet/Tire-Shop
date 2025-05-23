from customtkinter import CTk
from customtkinter import *
from tkinter import ttk
from .widgets import *
from utilities import Concur, is_windows, get_current_datetime
from time import sleep

from database import get_all_employees,get_all_employees_json, session, create_new_user, remove_user_by_username, update_user_by_username, get_all_username, user_by_username
from database import UsernameAlreadyExistsException, NationalNumberAlreadyExistsException

from PIL import Image
import os

class Login_page:
    def __init__(self, root, login_action):
        self.login_action = login_action
        
        self.main_frame = CTkFrame(root, fg_color='#494A5F')

        # Main container for contain whole widgets of page
        self.main_frame.pack(expand=True, fill='both')

        # Bind the "Enter" key to the login button command
        root.bind('<Return>', lambda event: self.btn_command())

        # Left frame of login page
        # This frame is for placing the image related to the login page

        left_frame = CTkFrame(self.main_frame, fg_color='#494A5F')
        left_frame.place(relx=0, rely=0, relwidth=0.6, relheight=1)

        # Load background image
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

        right_frame.rowconfigure((0, 1, 2, 3), weight=1, uniform='a')
        right_frame.columnconfigure(0, weight=1, uniform='a')
        
        p = os.path.dirname(os.path.realpath(__file__))
        img = Image.open(p + "/assets/login-logo.png")
        
        self.logoimage = CTkLabel(right_frame, image=CTkImage(img, size=(230, 230)), text='', bg_color='transparent')
        self.logoimage.grid(row=0, sticky='nswe')

        # This just a container for contain login frame and place it on verticaly center
        login_frame_container = CTkFrame(right_frame, fg_color='#494A5F')
        login_frame_container.grid(row=1, column=0, rowspan=2, sticky='nsew')

        login_frame_container.rowconfigure((0,2), weight=1, uniform='a')
        login_frame_container.rowconfigure(1, weight=10, uniform='a')

        login_frame_container.columnconfigure((0,2), weight=1, uniform='a')
        login_frame_container.columnconfigure(1, weight=10, uniform='a')

        # A container for contain login entries
        login_frame = CTkFrame(login_frame_container, bg_color='transparent', fg_color='transparent')
        login_frame.grid(row=1, column=1)

        login_frame.rowconfigure((0, 1, 2), weight=1, pad=30)
        login_frame.columnconfigure(0, weight=1)

        self.error_massage_lable = CTkLabel(login_frame, text_color='firebrick1')
        
        self.username = StringVar()
        self.password = StringVar()
        

        username_entry = Input(login_frame, 30, 300, 50, 'نام کاربری', self.username, show_err_callback=self.login_error_message)
        username_entry.configure(font=(None, 18))
        username_entry.set_placeholder_text("نام کاربری")
        username_entry.grid(row=0, column=0)

        password_entry = Input(login_frame, 30, 300, 50, 'رمز', self.password, show='*', show_err_callback = self.login_error_message)
        password_entry.configure(font=(None, 18))
        password_entry.set_placeholder_text("رمز")
        password_entry.grid(row=1, column=0)

        username_entry.set_textvariable(self.username)
        password_entry.set_textvariable(self.password)
            
        login_button = Btn(login_frame, 250, 50, 30, "ورود")
        login_button.grid(row=2, column=0)
        login_button.configure(font=(None, 18))
        login_button.configure(command=self.btn_command)
        

    
    def get_frame(self):
        return self.main_frame
    
    def btn_command(self):
        self.login_action(self.username.get(), self.password.get(), self)
        
    def login_error_message(self, message:str=None):
        if message:
            self.error_massage_lable.place(relx=.05, rely=.61)
            self.error_massage_lable.configure(text=message)
            Concur(lambda : self._clear_login_error(5)).start()
    
    def _clear_login_error(self, sec):
        sleep(sec)
        self.error_massage_lable.place_forget()
        
    def destroy(self):
        self.main_frame.pack_forget()
        self.main_frame.destroy()


class Page:
    def __init__(self, root, name:str, lastname:str, rule:str, logout_callback=None):
        self.main_frame = CTkFrame(root)
        self.main_frame.pack(expand=True, fill='both')
        
        self.logout_callback = logout_callback
        
        self.items_frame = CTkFrame(self.main_frame)
        self.items_frame.configure(fg_color='#5B5D76')
        self.items_frame.place(relwidth = .3, relheight=1, relx=.7, rely=0, anchor='nw')
        
        self.control_frame = CTkFrame(self.main_frame)
        self.control_frame.configure(fg_color='#494A5F')
        self.control_frame.place(relwidth=.7,relheight=1, relx=0, rely=0)
        
        self.user_profile_container = CTkFrame(self.items_frame)
        self.user_profile_container.configure(fg_color='transparent')
        self.user_profile_container.place(x=0, y=0, relwidth = 1, relheight=.15)
        
        self.user_profile_frame = CTkFrame(self.user_profile_container)
        self.user_profile_frame.configure(fg_color='#393A4E', corner_radius=18)
        self.user_profile_frame.place(relx=.5, rely=.5, relwidth=.75, relheight=.6, anchor='center')
        
        self.set_profile(name, lastname, rule)
        self._set_logout_btn()
        
    
    def set_profile(self, name:str, lastname:str, rule:str)   :
        name = name.capitalize()
        lastname= lastname.capitalize()
        rule = rule.capitalize()
         
        self.user_name_lastname = CTkLabel(self.user_profile_frame, text=f'{name} {lastname}')
        self.user_name_lastname.configure(text_color="white", height=5)
        self.user_name_lastname.place(relx=.25, rely=.23)
        
        self.rule = CTkLabel(self.user_profile_frame, text=rule)
        self.rule.configure(text_color="white", height=20)
        self.rule.place(relx=.25, rely=.47)
        
    def _set_logout_btn(self):
        p = os.path.dirname(os.path.realpath(__file__))
        img = Image.open(p + "/assets/logout.png")
        logoutImage = CTkImage(img)
        self.btn_logout = Btn(self.user_profile_frame, image=logoutImage, height=0, width=0,border_spacing=0,corner_radius=5, anchor='center')
        self.btn_logout.configure(fg_color='transparent')
        
        # self.btn_logout.disable_hover()
        self.btn_logout.place(relx=.9, rely=.5, anchor='center')
        
        if self.logout_callback:
            self.btn_logout.configure(command=lambda : self.logout_callback(self))
        
        
         
    
    
    def destroy(self):
        self.main_frame.pack_forget()
        self.main_frame.destroy()
        
    def hide(self):
        self.main_frame.pack_forget()
        

class Admin_page(Page):
    def __init__(self, root, name:str, lastname:str, rule:str, logout_callback=None):
        super().__init__(root, name, lastname, rule, logout_callback)
        
        self.buttons_frame = CTkFrame(self.items_frame)
        self.buttons_frame.configure(fg_color='transparent')
        self.buttons_frame.place(relx=0, rely=.15, relwidth=1, relheight=.85)
        
        
        self.buttons_frame.rowconfigure((0,1,2,3,4,5,6,7,8), weight=1)
        self.buttons_frame.columnconfigure(0, weight=1)
        
        self.button_font_size = 14
        self.button_color = "#393A4E"
        self.button_hover_color = "#434357"
        
        user_btn = Item_button(self.buttons_frame, 290, 64, rtopleft=15, rbottomleft=15, color=self.button_color,hover_color=self.button_hover_color,background="#5B5D76")
        user_btn.grid(row=2, column=0, sticky='e')
        user_btn.set_text('کاربران', fill='#FFFFFF', font_size=self.button_font_size)
        user_btn.set_action(self._employee_panel_callback)
        
        reports_btn = Item_button(self.buttons_frame, 290, 64, rtopleft=15, rbottomleft=15, color=self.button_color,hover_color=self.button_hover_color,background="#5B5D76")
        reports_btn.grid(row=3, column=0, sticky='e')
        reports_btn.set_text('بکاپ', fill='#FFFFFF', font_size=self.button_font_size)
        
        backup_btn = Item_button(self.buttons_frame, 290, 64, rtopleft=15, rbottomleft=15, color=self.button_color,hover_color=self.button_hover_color,background="#5B5D76")
        backup_btn.grid(row=4, column=0, sticky='e')
        backup_btn.set_text('بازیابی', fill='#FFFFFF', font_size=self.button_font_size)
        
        
        #----------------DELETE THIS LINES AFTER FINISH THE ADMIN PANEL DEVELOPMENT-----------
        # self.employee_panel(self.control_frame)
        self.backup(self.control_frame)
        
    class employee_panel(CTkFrame):
        def __init__(self, root):
            super().__init__(root)
            self.pack(expand=True, fill="both")
            self.configure(bg_color='transparent', fg_color='transparent')
            
            # Setup button frame
            self.btn_frame = CTkFrame(self, fg_color='transparent')
            self.btn_frame.place(relwidth=.2, relheight=.3, relx=1, rely=.1, anchor="ne")
            self.btn_frame.columnconfigure(0, weight=1)
            self.btn_frame.rowconfigure((0,1,2,3), weight=1)

            employee_list_btn = Item_button(self.btn_frame, 150, 50, rtopleft=20, rbottomleft=20, color="#393A4E", hover_color="#434357", background="#494A5F")
            employee_list_btn.set_text("لیست کارمندان", "white", 13)
            employee_list_btn.grid(row=0,column=0 ,sticky="e")
            employee_list_btn.set_action(lambda e: self.toggle_view('list'))
            
            employee_new_btn = Item_button(self.btn_frame, 150, 50, rtopleft=20, rbottomleft=20, color="#393A4E", hover_color="#434357", background="#494A5F")
            employee_new_btn.set_text("کارمند جدید", "white", 13)
            employee_new_btn.grid(row=1,column=0 , sticky="e")
            employee_new_btn.set_action(lambda e: self.toggle_view('new'))

            employee_delete_btn = Item_button(self.btn_frame, 150, 50, rtopleft=20, rbottomleft=20, color="#393A4E", hover_color="#434357", background="#494A5F")
            employee_delete_btn.set_text("حذف کارمند", "white", 13)
            employee_delete_btn.grid(row=2,column=0 , sticky="e")
            employee_delete_btn.set_action(lambda e: self.toggle_view('delete'))

            employee_update_btn = Item_button(self.btn_frame, 150, 50, rtopleft=20, rbottomleft=20, color="#393A4E", hover_color="#434357", background="#494A5F")
            employee_update_btn.set_text("تغیرات کارمند", "white", 13)
            employee_update_btn.grid(row=3,column=0 , sticky="e")
            employee_update_btn.set_action(lambda e: self.toggle_view('edit'))
            
            
            self.error_message_label = CTkLabel(self, text_color="firebrick1")
            self.success_message_label = CTkLabel(self, text_color="green")
            self.new_employee_inputs: list[Input] = []

            # Create table and new employee form but hide them initially
            self.table = self.initialize_table(self)
            self.table.place_forget()
            
            # Call employee_new once to create all widgets
            self.employee_new(self)
            # Remember the content_frame to toggle visibility
            self.new_employee_frame = self.winfo_children()[-1]
            self.new_employee_frame.place_forget()
            
            self.delete_user_frame = CTkFrame(self, fg_color="#5B5D76")
            
            self.delete_user_comboBox = None
            self.delete_user_btn = None
            
            self.edit_user_frame = CTkFrame(self, fg_color="#5B5D76")
            self.edit_user_combobox = None
            self.edit_user_inputs = None
            
            # Show table by default
            self.current_view = None
            self.toggle_view('list')

        def toggle_view(self, view_name):
            if view_name == 'list' and self.current_view != 'list':
                self.new_employee_frame.place_forget()
                self.delete_user_frame.place_forget() 
                self.edit_user_frame.place_forget()
                self.table.place(relheight=.9, relwidth=.8, relx=.02, rely=.05)
                self.current_view = 'list'
                self.insert_content_to_table(self.table, get_all_employees_json(session))
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
                self.delete_user(self, get_all_employees_json(session))
                self.current_view = 'delete'
            elif view_name == 'edit' and self.current_view != 'edit':
                self.table.place_forget()
                self.new_employee_frame.place_forget()
                self.employee_edit(self)
                self.current_view = 'edit'

        #---------------------- Setup Employee table content----------------
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
            
            
            table.column("id", width=40, anchor="center")
            table.column("name", width=100, anchor="center")
            table.column("lastname", width=150, anchor="center")
            table.column("username", width=120, anchor="center")
            table.column("phone", width=140, anchor="center")
            table.column("national", width=150, anchor="center")
            table.column("startDate", width=200, anchor="center")
            
            table.heading("id", text="id", anchor='center')
            table.heading("name", text="name", anchor='center')
            table.heading("lastname", text="lastname", anchor='center')
            table.heading("username", text="username", anchor='center')
            table.heading("phone", text="phone", anchor='center')
            table.heading("national", text="national", anchor='center')
            table.heading("startDate", text="startDate", anchor='center')
            
            table.place(relheight=.9, relwidth=.8, relx=.02, rely=.05)
            return table
            
        
        def insert_content_to_table(self, table:ttk.Treeview, content:list[dict]):
            
            
            table.delete(*table.get_children())
            
            for row in content:
                vals = (row["id"], row["name"], row["lastname"], row["username"], row["phone"], row["national_number"])
                
                table.insert(parent="", index=0, values=vals)
                
        #--------------------------------------------------------------------
        
        def employee_new(self, window):
            content_frame = CTkFrame(window, fg_color="#5B5D76")
            content_frame.place(relheight=.9, relwidth=.8, relx=.02, rely=.05)
            content_frame.rowconfigure(tuple(range(0, 8)), weight=1)
            content_frame.columnconfigure((0, 3), weight=1, pad=20, uniform='a')

            # First column
            rule_label = CTkLabel(content_frame, text="Rule:", text_color="white", font=(None, 15))
            rule_label.grid(row=0, column=1, sticky='w')
            combo_rule_items = ['Employee', 'Manager']
            rule_comboBox = DropDown(content_frame, values=combo_rule_items)
            rule_comboBox.grid(row=0, column=2)

            name_label = CTkLabel(content_frame, text="Name:", text_color="white", font=(None, 13))
            name_label.grid(row=1, column=0)
            name = StringVar()
            name_input = Input(content_frame, 15, 150, 35, "Name", name)
            name_input.set_textvariable(name)
            name_input.grid(row=1, column=1)
            self.new_employee_inputs.append(name_input)

            lastname_label = CTkLabel(content_frame, text="Lastname:", text_color="white", font=(None, 13))
            lastname_label.grid(row=1, column=2)
            lastname = StringVar()
            lastname_input = Input(content_frame, 15, 150, 35, "Lastname", lastname)
            lastname_input.set_textvariable(lastname)
            lastname_input.grid(row=1, column=3)
            self.new_employee_inputs.append(lastname_input)
            

            national_label = CTkLabel(content_frame, text="National Number:", text_color="white", font=(None, 13))
            national_label.grid(row=2, column=0)
            national = StringVar()
            national_input = Input(content_frame, 15, 150, 35, "National Number", national)
            national_input.set_textvariable(national)
            national_input.grid(row=2, column=1)
            self.new_employee_inputs.append(national_input)
            

            # Second column
            phone_label = CTkLabel(content_frame, text="Phone Number:", text_color="white", font=(None, 13))
            phone_label.grid(row=2, column=2)
            phone = StringVar()
            phone_input = Input(content_frame, 15, 150, 35, "Phone Number", phone)
            phone_input.set_textvariable(phone)
            phone_input.grid(row=2, column=3)
            self.new_employee_inputs.append(phone_input)
            

            username_label = CTkLabel(content_frame, text="Username:", text_color="white", font=(None, 13))
            username_label.grid(row=3, column=0)
            username = StringVar()
            username_input = Input(content_frame, 15, 150, 35, "Username", username)
            username_input.set_textvariable(username)
            username_input.grid(row=3, column=1)
            self.new_employee_inputs.append(username_input)
            

            password_label = CTkLabel(content_frame, text="Password:", text_color="white", font=(None, 13))
            password_label.grid(row=3, column=2)
            password = StringVar()
            password_input = Input(content_frame, 15, 150, 35, "password", password)
            password_input.set_textvariable(password)
            password_input.grid(row=3, column=3)
            self.new_employee_inputs.append(password_input)

            password_repeate_label = CTkLabel(content_frame, text="Repeat Password:", text_color="white", font=(None, 13))
            password_repeate_label.grid(row=4, column=2)
            password_repeate = StringVar()
            password_repeate_input = Input(content_frame, 15, 150, 35, "repeat password", password_repeate)
            password_repeate_input.set_textvariable(password_repeate)
            password_repeate_input.grid(row=4, column=3)
            self.new_employee_inputs.append(password_repeate_input)

            btn = Btn(content_frame, 160, 45)
            btn.configure(command=lambda : self.new_employee_action(
                self.show_error_message,
                name_input.get(), lastname_input.get(), national_input.get(),
                phone_input.get(), username_input.get(), password_input.get(),
                password_repeate_input.get(), rule_comboBox.get()))
            btn.configure(font=(None, 16))
            btn.set_text(text='ایجاد کاربر')
            btn.grid(row=5, column=0, columnspan=4)
            # if self.check_value_inputs(self.show_error_message, name.get(), lastname.get(), national.get(), phone.get(), username.get(), password.get(), password_repeate.get())
            
        
        def new_employee_action(self, show_err_callback, name:str=None,\
                                lastname:str=None, national:str=None, phone:str=None,\
                                username:str=None, password:str=None, repeat_password:str=None, rule:str=None):
            
            if self.check_value_inputs_in_new_imployee(show_err_callback, name, lastname, national, phone, username, password, repeat_password):
                try:
                    create_new_user(session, name, lastname, phone, national, rule, username, password)
                    self.show_success_message("New user was created")
                    self.clear_new_employee_inputs()
                except Exception as e:
                    show_err_callback(e)
                    
                
            
        def clear_new_employee_inputs(self):
            for input in self.new_employee_inputs:
                input.clear()
                
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
                
        def delete_user(self, window, users:list):
            
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
            combo_delete_items = [f'{user['username']}:{user['name']} {user['lastname']}' for user in users]
            if self.delete_user_comboBox:
                self.delete_user_comboBox.destroy()
            
            self.delete_user_comboBox = DropDown(content_frame, values=combo_delete_items, width=250)
            self.delete_user_comboBox.grid(row=0, column=0)
            

            if not self.delete_user_btn:
                self.delete_user_btn = Btn(content_frame, 160, 45)
            
                self.delete_user_btn.configure(font=(None, 16))
                self.delete_user_btn.set_text(text='حذف کاربر')
                self.delete_user_btn.grid(row=1, column=0, columnspan=4)
            
            self.delete_user_btn.configure(command=lambda : self.delete_user_action(self.delete_user_comboBox.get().split(':')[0], self.show_error_message, self.show_success_message))

        def delete_user_action(self, username, show_msg_callback, show_success_msg_callback):
            try:
                remove_user_by_username(session, username)
            except Exception as e:
                show_msg_callback(e)
            
            show_success_msg_callback("User was deleted")
            self.delete_user(self, get_all_employees_json(session))
        
        #-----------------------------------------------------------------
        
        def employee_edit(self, window):
            
            if self.edit_user_frame:
                content_frame = self.edit_user_frame
            else:
                content_frame = CTkFrame(window, fg_color="#5B5D76")
                self.edit_user_frame = content_frame
                
            content_frame.place(relheight=.9, relwidth=.8, relx=.02, rely=.05)
            content_frame.rowconfigure(tuple(range(0, 8)), weight=1)
            content_frame.columnconfigure((0, 3), weight=1, pad=40, uniform='a')

            # Label and dropdown to select user by username
            select_user_label = CTkLabel(content_frame, text="Username:", text_color="white", font=(None, 15))
            select_user_label.grid(row=0, column=0)

            usernames = get_all_username(session)  # Fetch list of usernames
            selected_username = StringVar()
            if self.edit_user_combobox:
                self.edit_user_combobox.grid_forget()
                self.edit_user_combobox.destroy()
            self.edit_user_combobox = DropDown(content_frame, values=usernames, variable=selected_username, command=self.load_user_data)
            self.edit_user_combobox.grid(row=0, column=1)

            # Dictionary to hold Input objects
            if not self.edit_user_inputs:
                self.edit_user_inputs = {}
            
            self.create_input_field(content_frame, "Name:", 1, 0, 'name')
            self.create_input_field(content_frame, "Lastname:", 1, 2, 'lastname')
            self.create_input_field(content_frame, "National Number:", 2, 0, 'national')
            self.create_input_field(content_frame, "Phone Number:", 2, 2, 'phone')
            self.create_input_field(content_frame, "Username:", 3, 0, 'username')
            
            
            
            update_btn = Btn(content_frame, 160, 45)
            update_btn.configure(command=lambda: self.update_user_action(
                self.edit_user_combobox.get(),
                self.edit_user_inputs['name'].get(),
                self.edit_user_inputs['lastname'].get(),
                self.edit_user_inputs['phone'].get(),
                self.edit_user_inputs['national'].get(),
                self.edit_user_inputs['username'].get(),
                None,
                self.show_error_message,
                self.show_success_message
                # self.edit_user_inputs['password'].get(),
                # self.edit_user_inputs['password_repeat'].get(),
            ))
            update_btn.configure(font=(None, 16))
            update_btn.set_text(text="بروزرسانی اطلاعات")
            update_btn.grid(row=6, column=0, columnspan=4)

        # Helper function to create an input field
        def create_input_field(self, window, label_text, row, column, field_key, **kwargs):
            if field_key not in self.edit_user_inputs:
                label = CTkLabel(window, text=label_text, text_color="white", font=(None, 13))
                label.grid(row=row, column=column, **kwargs)
                var = StringVar()
                input_widget = Input(window, 15, 150, 35, None, var, placeholder_empty=False)
                input_widget.set_textvariable(var)
                input_widget.textvariable.set('')
                input_widget.grid(row=row, column=column+1)
                self.edit_user_inputs[field_key] = input_widget


        # Load selected user's data
        def load_user_data(self, username):
            user_data = user_by_username(session, username)
            if user_data:
                self.edit_user_inputs['name'].set_placeholder_text(user_data.name)
                self.edit_user_inputs['lastname'].set_placeholder_text(user_data.lastname)
                self.edit_user_inputs['national'].set_placeholder_text(user_data.national_number)
                self.edit_user_inputs['phone'].set_placeholder_text(user_data.phone)
                self.edit_user_inputs['username'].set_placeholder_text(user_data.user_name)
                # self.edit_user_inputs['password'].set_placeholder_text(user_data.password)

        
        def update_user_action(self, username, name, lastname, phone, national, new_username, password, show_error_callback, show_success_callback):
            try:
                update_user_by_username(session, username, name, lastname, phone, national, new_username, password)
                show_success_callback(f'The user information has been changed.')
                self.employee_edit(self)
                for v in list(self.edit_user_inputs.values()):
                    v.textvariable.set('')

            except Exception as e:
                show_error_callback(e)
                
        
        #------------------------------------------------------------
        def show_error_message(self, message:str | Exception=None):
            if message:
                self.clear_success_message()
                message = str(message)
                self.error_message_label.place(relx=.03, rely=.01)
                self.error_message_label.configure(text=message)
                Concur(lambda : self._clear_login_error(5)).start()
        
        def _clear_login_error(self, sec):
            sleep(sec)
            self.clear_error_message()
            
        def clear_error_message(self):
            self.error_message_label.place_forget()
            
            
        
        def show_success_message(self, message:str=None):
            if message:
                self.clear_error_message()
                message = str(message)
                self.success_message_label.place(relx=.03, rely=.01)
                self.success_message_label.configure(text=message)
                Concur(lambda : self._clear_success_message(5)).start()
            
        def _clear_success_message(self, sec):
            sleep(sec)
            self.clear_success_message()
        
        def clear_success_message(self):
            self.success_message_label.place_forget()
            
                
    
    class backup(CTkFrame):
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
            self.path_input = Input(self, 15, 280, 35, None, path, placeholder_empty=False)
            self.path_input.grid(row=0, column=0, columnspan=2)
            self.path_input.set_textvariable(path)
            path.set(default_path)
            
            self.path_label = CTkLabel(self, text=render_text("مسیر ذخیره فایل"), text_color='white', font=(None, 15))
            self.path_label.grid(row=0, column=2, columnspan=2)
            
            self.path_label = CTkLabel(self, text=render_text('نام فایل'), text_color='white', font=(None, 15))
            self.path_label.grid(row=1, column=2, columnspan=2)
            
            self.path_label = CTkLabel(self, text=self.get_backupfile_name(), text_color='#c5c6de', font=(None, 15))
            self.path_label.grid(row=1, column=0, columnspan=2)
            
            # Add checkboxes
            self.cb_users = CTkCheckBox(self, text="Users", border_color="#a5a7c9", hover_color="#81828a")
            self.cb_users.grid(row=2, column=0)

            self.cb_products = CTkCheckBox(self, text="Products", border_color="#a5a7c9", hover_color="#81828a")
            self.cb_products.grid(row=2, column=1)

            self.cb_orders = CTkCheckBox(self, text="Orders", border_color="#a5a7c9", hover_color="#81828a")
            self.cb_orders.grid(row=2, column=2)
            
        def default_path(self):
            folder_name = "TSBackup"
            if is_windows():
                desktop_path = os.path.join(os.environ["USERPROFILE"], "Desktop")


                folder_path = os.path.join(desktop_path, folder_name)

                # Create the folder (if it doesn't already exist)
                os.makedirs(folder_path, exist_ok=True)


                return folder_path
            
            else:
                home_path = os.path.expanduser("~")

                # Step 3: Construct the full path to the folder
                folder_path = os.path.join(home_path, folder_name)

                # Step 4: Create the folder (if it doesn’t already exist)
                os.makedirs(folder_path, exist_ok=True)
                
                return folder_path
                        
                        
        def get_backupfile_name(self):
            now = get_current_datetime()
            return 'TS_' + now
            
            
    def _employee_panel_callback(self, *k):
        # self.employee_panel(self.control_frame)
        print("hellloooooooo")
        
        
        
        
        
        
        
    def _set_semple_lable(self, message):
        self.loggedin_lable = CTkLabel(self.main_frame, text_color='blue', text=message)
        self.loggedin_lable.pack(expand=True, fill='both')
        
    
    def destroy(self):
        self.main_frame.pack_forget()
        self.main_frame.destroy()



class Manager_page(Page):
    def __init__(self, root, name, lastname, rule, logout_callback=None):
        super().__init__(root, name, lastname, rule, logout_callback)
        
        self.buttons_frame = CTkFrame(self.items_frame)
        self.buttons_frame.configure(fg_color='transparent')
        self.buttons_frame.place(relx=0, rely=.15, relwidth=1, relheight=.85)
        
        
        self.buttons_frame.rowconfigure((0,1,2,3,4,5,6,7,8), weight=1)
        self.buttons_frame.columnconfigure(0, weight=1)
        
        self.button_font_size = 14
        self.button_color = "#393A4E"
        self.button_hover_color = "#434357"
        
        dashboard_btn = Item_button(self.buttons_frame, 290, 64, rtopleft=15, rbottomleft=15, color=self.button_color,hover_color=self.button_hover_color,background="#5B5D76")
        dashboard_btn.grid(row=0, column=0, sticky='e')
        dashboard_btn.set_text('داشبورد', fill='#FFFFFF', font_size=self.button_font_size)
        
        products_btn = Item_button(self.buttons_frame, 290, 64, rtopleft=15, rbottomleft=15, color=self.button_color,hover_color=self.button_hover_color,background="#5B5D76")
        products_btn.grid(row=1, column=0, sticky='e')
        products_btn.set_text('محصولات', fill='#FFFFFF', font_size=self.button_font_size)
        
        employee_btn = Item_button(self.buttons_frame, 290, 64, rtopleft=15, rbottomleft=15, color=self.button_color,hover_color=self.button_hover_color,background="#5B5D76")
        employee_btn.grid(row=2, column=0, sticky='e')
        employee_btn.set_text('کارمند', fill='#FFFFFF', font_size=self.button_font_size)
        
        reports_btn = Item_button(self.buttons_frame, 290, 64, rtopleft=15, rbottomleft=15, color=self.button_color,hover_color=self.button_hover_color,background="#5B5D76")
        reports_btn.grid(row=3, column=0, sticky='e')
        reports_btn.set_text('گزارش', fill='#FFFFFF', font_size=self.button_font_size)
        
        backup_btn = Item_button(self.buttons_frame, 290, 64, rtopleft=15, rbottomleft=15, color=self.button_color,hover_color=self.button_hover_color,background="#5B5D76")
        backup_btn.grid(row=4, column=0, sticky='e')
        backup_btn.set_text('بازیابی', fill='#FFFFFF', font_size=self.button_font_size)
        
    def destroy(self):
        self.main_frame.pack_forget()
        self.main_frame.destroy()
        
        
        
