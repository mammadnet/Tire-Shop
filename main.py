from interface.ui import Login_page, Admin_page
from interface.widgets import Root
from customtkinter import *
from database import login_permission, session
root = Root()
def login_action(username, password, login_page:Login_page):
    res = login_permission(session, username, password)
    if res:
        login_page.destroy()

        Admin_page(root)
    else:
        # call a fucntion in side object
        login_page.login_error_message('Password or username is incorrect.')
        
l = Login_page(root, login_action)


root.mainloop()