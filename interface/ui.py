from customtkinter import CTk
from customtkinter import *
from tkinter import ttk
from .widgets import *
from utilities import Concur, is_windows, get_current_datetime
from time import sleep

from database import get_all_employees,get_all_employees_json, session, create_new_user, remove_user_by_username, update_user_by_username, get_all_username, user_by_username
from database import UsernameAlreadyExistsException, NationalNumberAlreadyExistsException

from .panels import AdminEmployeePanel, AdminBackupPanel, ManagerProductPanel, ManagerEmployeePanel

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
        user_btn.set_action(lambda _: self.toggle_panel('users'))
        
        reports_btn = Item_button(self.buttons_frame, 290, 64, rtopleft=15, rbottomleft=15, color=self.button_color,hover_color=self.button_hover_color,background="#5B5D76")
        reports_btn.grid(row=3, column=0, sticky='e')
        reports_btn.set_action(lambda _: self.toggle_panel('backup'))
        reports_btn.set_text('بکاپ', fill='#FFFFFF', font_size=self.button_font_size)
        
        backup_btn = Item_button(self.buttons_frame, 290, 64, rtopleft=15, rbottomleft=15, color=self.button_color,hover_color=self.button_hover_color,background="#5B5D76")
        backup_btn.grid(row=4, column=0, sticky='e')
        backup_btn.set_action(lambda _: self.toggle_panel('backup'))
        backup_btn.set_text('بازیابی', fill='#FFFFFF', font_size=self.button_font_size)
        
        self.current_panel = None
        
        #----------------DELETE THIS LINES AFTER FINISH THE ADMIN PANEL DEVELOPMENT-----------
        # self.employee_panel(self.control_frame)
        self.employee_frame = None
        self.backup_frame = None
        self.toggle_panel('users')
    
    def toggle_panel(self, panel:str):
        if panel == 'users' and self.current_panel != 'users':
            if self.backup_frame:
                self.backup_frame.destroy()
            self.employee_frame = AdminEmployeePanel(self.control_frame)
            self.current_panel = 'users'
        elif panel == 'backup' and self.current_panel != 'backup':
            if self.employee_frame:
                self.employee_frame.destroy()
            self.backup_frame = AdminBackupPanel(self.control_frame)
            self.current_panel = 'backup'


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
        products_btn.set_action(lambda _: self.toggle_panel('products'))
        products_btn.set_text('محصولات', fill='#FFFFFF', font_size=self.button_font_size)
        
        employee_btn = Item_button(self.buttons_frame, 290, 64, rtopleft=15, rbottomleft=15, color=self.button_color,hover_color=self.button_hover_color,background="#5B5D76")
        employee_btn.grid(row=2, column=0, sticky='e')
        employee_btn.set_action(lambda _: self.toggle_panel('employee'))
        employee_btn.set_text('کارمند', fill='#FFFFFF', font_size=self.button_font_size)
        
        reports_btn = Item_button(self.buttons_frame, 290, 64, rtopleft=15, rbottomleft=15, color=self.button_color,hover_color=self.button_hover_color,background="#5B5D76")
        reports_btn.grid(row=3, column=0, sticky='e')
        reports_btn.set_text('گزارش', fill='#FFFFFF', font_size=self.button_font_size)

        self.current_panel = None
        self.product_frame = None
        self.employee_frame = None
        self.toggle_panel('products')
        
    def toggle_panel(self, panel:str):
        if panel == 'products' and self.current_panel != 'products':
            self.product_frame = ManagerProductPanel(self.control_frame)
            self.current_panel = 'products'
            if self.employee_frame:
                self.employee_frame.destroy()
        elif panel == 'employee' and self.current_panel != 'employee':
            self.employee_frame = ManagerEmployeePanel(self.control_frame)
            self.current_panel = 'employee'
            if self.product_frame:
                self.product_frame.destroy()
        else:
            print("Panel not found")

    def destroy(self):
        self.main_frame.pack_forget()
        self.main_frame.destroy()
        
        
        
class Employee_page(Page):
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
        
        sell_btn = Item_button(self.buttons_frame, 290, 64, rtopleft=15, rbottomleft=15, color=self.button_color,hover_color=self.button_hover_color,background="#5B5D76")
        sell_btn.grid(row=0, column=0, sticky='e')
        sell_btn.set_text('فروش', fill='#FFFFFF', font_size=self.button_font_size)
        
        products_btn = Item_button(self.buttons_frame, 290, 64, rtopleft=15, rbottomleft=15, color=self.button_color,hover_color=self.button_hover_color,background="#5B5D76")
        products_btn.grid(row=1, column=0, sticky='e')
        products_btn.set_text('محصولات', fill='#FFFFFF', font_size=self.button_font_size)
        
        reports_btn = Item_button(self.buttons_frame, 290, 64, rtopleft=15, rbottomleft=15, color=self.button_color,hover_color=self.button_hover_color,background="#5B5D76")
        reports_btn.grid(row=2, column=0, sticky='e')
        reports_btn.set_text('گزارش', fill='#FFFFFF', font_size=self.button_font_size)

    def destroy(self):
        self.main_frame.pack_forget()
        self.main_frame.destroy()
        
