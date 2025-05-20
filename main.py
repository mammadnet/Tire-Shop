# Import necessary modules and classes from other files
from interface.ui import Login_page, Admin_page, Manager_page, Page
from interface.widgets import Root
from customtkinter import *
from database import login_permission, session, is_admin, is_manager, user_by_username_pass

# Initialize the root window for the application
root = Root()

# Define the login action function
def login_action(username, password, login_page: Login_page):
    # Retrieve user information based on username and password
    user = user_by_username_pass(session, username, password)
        
    # Check if the user is an admin and navigate to the Admin page
    if is_admin(user):
        Admin_page(root, user.name, user.lastname, user.type, logout_action)
    # Check if the user is a manager and navigate to the Manager page
    elif is_manager(user):
        Manager_page(root, user.name, user.lastname, user.type, logout_action)
    else:
        login_page.login_error_message('Password or username is incorrect.')
    
    if user:
        login_page.destroy()

# Define the logout action function
def logout_action(active_page: Page):
    active_page.destroy()
    # Redirect to the login page
    Login_page(root, login_action)

Login_page(root, login_action)

root.mainloop()