from customtkinter import CTk
from customtkinter import *
from widgets import *


root = Root()
mainFrame = CTkFrame(root, fg_color='red')

# Main container for contain whole widgets of page
mainFrame.pack(expand=True, fill='both')


# Left frame of login page
# This frame is for placing the image related to the login page

left_frame = CTkFrame(mainFrame, fg_color='blue')
left_frame.place(relx=0, rely=0, relwidth=0.6, relheight=1)
#-----------------------------------------------


# Right frame of login page
# This page is for placing the login entry like username and password
right_frame = CTkFrame(mainFrame, fg_color='green')
right_frame.place(relx=.6, rely=0, relwidth=0.4, relheight=1)

right_frame.rowconfigure((0, 1, 2, 3), weight=1, uniform='a')
right_frame.columnconfigure(0, weight=1, uniform='a')

# This just a container for contain login frame and place it on verticaly center
login_frame_container = CTkFrame(right_frame, fg_color='magenta')
login_frame_container.grid(row=1, column=0, rowspan=2, sticky='nsew')

login_frame_container.rowconfigure((0,2), weight=1, uniform='a')
login_frame_container.rowconfigure(1, weight=10, uniform='a')

login_frame_container.columnconfigure((0,2), weight=1, uniform='a')
login_frame_container.columnconfigure(1, weight=10, uniform='a')

# A container for contain login entries
login_frame = CTkFrame(login_frame_container, fg_color='cyan')
login_frame.grid(row=1, column=1, sticky='nswe')
#----------------------------------------------------------------------




# This part of the code is only for showing the placement of each element on the page
# **** should be removed during the UI implementation ****
CTkLabel(left_frame, text='>>> Login image placeholder <<<', fg_color='transparent', font=(None, 40)).pack(expand=True)
CTkLabel(login_frame, text='> Login widgets placeholder <', fg_color='transparent', font=(None, 30)).pack(expand=True)
#------------------------------------


# Main loop of program
root.mainloop()

