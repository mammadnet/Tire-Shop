from customtkinter import CTk
from customtkinter import *
from tkinter import ttk
from .widgets import *
from utilities import Concur, is_windows
from time import sleep

from database import get_all_employees,get_all_employees_json, session

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

        self.title = CTkLabel(right_frame, text="Tire Shop", font=(None, 50))
        self.title.grid(row=0, column=0, sticky='s')

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
            
        login_button = Btn(login_frame, 'ورود', 30, 250, 50)
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
    def __init__(self, root):
        self.main_frame = CTkFrame(root)
        self.main_frame.pack(expand=True, fill='both')
        
        
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
        
        
         
    
    
    def destroy(self):
        self.main_frame.pack_forget()
        self.main_frame.destroy()
        
    def hide(self):
        self.main_frame.pack_forget()
        
        

class Admin_page(Page):
    def __init__(self, root):
        super().__init__(root)
        
        self.buttons_frame = CTkFrame(self.items_frame)
        self.buttons_frame.configure(fg_color='transparent')
        self.buttons_frame.place(relx=0, rely=.15, relwidth=1, relheight=.85)
        
        
        self.buttons_frame.rowconfigure((0,1,2,3,4,5,6,7,8), weight=1)
        self.buttons_frame.columnconfigure(0, weight=1)
        
        self.button_font_size = 14
        self.button_color = "#393A4E"
        self.button_hover_color = "#434357"
        
        products_btn = Item_button(self.buttons_frame, 290, 64, rtopleft=15, rbottomleft=15, color=self.button_color,hover_color=self.button_hover_color,background="#5B5D76")
        products_btn.grid(row=0, column=0, sticky='e')
        products_btn.set_text('محصولات', fill='#FFFFFF', font_size=self.button_font_size)

        backup_btn = Item_button(self.buttons_frame, 290, 64, rtopleft=15, rbottomleft=15, color=self.button_color,hover_color=self.button_hover_color,background="#5B5D76")
        backup_btn.grid(row=1, column=0, sticky='e')
        backup_btn.set_text('مدیر', fill='#FFFFFF', font_size=self.button_font_size)
        
        employee_btn = Item_button(self.buttons_frame, 290, 64, rtopleft=15, rbottomleft=15, color=self.button_color,hover_color=self.button_hover_color,background="#5B5D76")
        employee_btn.grid(row=2, column=0, sticky='e')
        employee_btn.set_text('کارمند', fill='#FFFFFF', font_size=self.button_font_size)
        employee_btn.set_action(self._employee_panel_callback)
        
        reports_btn = Item_button(self.buttons_frame, 290, 64, rtopleft=15, rbottomleft=15, color=self.button_color,hover_color=self.button_hover_color,background="#5B5D76")
        reports_btn.grid(row=3, column=0, sticky='e')
        reports_btn.set_text('گزارش', fill='#FFFFFF', font_size=self.button_font_size)
        
        backup_btn = Item_button(self.buttons_frame, 290, 64, rtopleft=15, rbottomleft=15, color=self.button_color,hover_color=self.button_hover_color,background="#5B5D76")
        backup_btn.grid(row=4, column=0, sticky='e')
        backup_btn.set_text('بازیابی', fill='#FFFFFF', font_size=self.button_font_size)
        
        
        #----------------DELETE THIS LINES AFTER FINISH THE ADMIN PANEL DEVELOPMENT-----------
        self.employee_panel(self.control_frame)
        
    class employee_panel(CTkFrame):
        def __init__(self, root):
            super().__init__(root)
            self.pack(expand=True, fill="both")
            self.configure(bg_color='transparent', fg_color='transparent')
            
            self.btn_frame = CTkFrame(self, fg_color='transparent')
            self.btn_frame.place(relwidth =.2, relheight=.3, relx=1, rely=.1, anchor="ne")
            self.btn_frame.columnconfigure(0, weight=1)
            self.btn_frame.rowconfigure((0,1,2), weight=1)
            
            employee_list_btn = Item_button(self.btn_frame, 150, 50, rtopleft=20, rbottomleft=20, color="#393A4E", hover_color="#434357", background="#494A5F")
            employee_list_btn.set_text("لیست کارمندان", "white", 13)
            employee_list_btn.grid(row=0,column=0 ,sticky="e")
            
            employee_new_btn = Item_button(self.btn_frame, 150, 50, rtopleft=20, rbottomleft=20, color="#393A4E", hover_color="#434357", background="#494A5F")
            employee_new_btn.set_text("کارمند جدید", "white", 13)
            employee_new_btn.grid(row=1,column=0 , sticky="e")
    
            employee_delete_btn = Item_button(self.btn_frame, 150, 50, rtopleft=20, rbottomleft=20, color="#393A4E", hover_color="#434357", background="#494A5F")
            employee_delete_btn.set_text("کارمند جدید", "white", 13)
            employee_delete_btn.grid(row=2,column=0 , sticky="e")
            
            
            self.content_table = self.initialize_table(self)
            self.insert_content_to_table(self.content_table, get_all_employees_json(session))
            
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
            
            for row in content:
                vals = (row["id"], row["name"], row["lastname"], row["username"], row["phone"], row["national_number"])
                
                table.insert(parent="", index=0, values=vals)
            
            
            
            
            
                
    
    
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
    def __init__(self, root):
        super().__init__(root)
        
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