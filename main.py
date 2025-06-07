from interface.ui import Login_page, Admin_page, Manager_page, Page, Employee_page
from interface.widgets import Root
from customtkinter import *
from database import login_permission, session, is_admin,is_manager,is_employee, user_by_username_pass, admin_exists, create_new_user
root = Root()
root.title("Tire Shop")

def login_action(username, password, login_page:Login_page):
    user = user_by_username_pass(session, username, password)
        
    if is_admin(user):
        Admin_page(root, user.name, user.lastname, user.type, logout_action)
    elif is_manager(user):
        Manager_page(root, user.name, user.lastname, user.type, logout_action)
    elif is_employee(user):
        Employee_page(root, user.name, user.lastname, user.type, logout_action)
    else:
        # call a fucntion in side object
        login_page.login_error_message('Password or username is incorrect.')
    if user:
        login_page.destroy()

def logout_action(active_page:Page):
    active_page.destroy()
    Login_page(root, login_action)
    
    
if not admin_exists(session):
    create_new_user(session, "admin", "admin", "1234", "1234", "admin", "admin", "admin")

Login_page(root, login_action)

root.mainloop()