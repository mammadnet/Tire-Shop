# Import UI components for different user roles and base page class
from interface.ui import Login_page, Admin_page, Manager_page, Page, Employee_page
from interface.widgets import Root
from customtkinter import *
# Import database utilities for authentication and user management
from database import login_permission, session, is_admin,is_manager,is_employee, user_by_username_pass, admin_exists, create_new_user

# Initialize the main application window
root = Root()
root.title("Tire Shop")

def login_action(username, password, login_page:Login_page):
    """
    Handle user login and redirect to appropriate interface based on user role.
    Args:
        username: User's login username
        password: User's login password
        login_page: Reference to the current login page instance
    """
    user = user_by_username_pass(session, username, password)
        
    # Route user to appropriate interface based on their role
    if is_admin(user):
        Admin_page(root, user.name, user.lastname, user.type, logout_action)
    elif is_manager(user):
        Manager_page(root, user.name, user.lastname, user.type, logout_action)
    elif is_employee(user):
        Employee_page(root, user.name, user.lastname, user.type, logout_action)
    else:
        # Display error message for invalid credentials
        login_page.login_error_message('Password or username is incorrect.')
    
    # Close login page if authentication was successful
    if user:
        login_page.destroy()

def logout_action(active_page:Page):
    """
    Handle user logout by destroying current page and returning to login screen.
    Args:
        active_page: Reference to the current active page instance
    """
    active_page.destroy()
    Login_page(root, login_action)
    
# Create default admin account if no admin exists in the system
if not admin_exists(session):
    create_new_user(session, "admin", "admin", "1234", "1234", "admin", "admin", "admin")

# Start the application with the login page
Login_page(root, login_action)

# Start the main event loop
root.mainloop()