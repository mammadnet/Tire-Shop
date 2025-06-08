from customtkinter import *
from utilities import Concur
from time import sleep

# A base class for content panels that provides a standardized system 
# for displaying temporary success and error messages.
class Panel(CTkFrame):
    def __init__(self, root, **kwargs):
        super().__init__(root, **kwargs)

        # Initialize labels for displaying error and success messages.
        # They are not placed on the screen until their respective `show` methods are called.
        self.error_message_label = CTkLabel(self, text_color="firebrick1")
        self.success_message_label = CTkLabel(self, text_color="green")
    
    
    # Displays an error message at the top of the panel for a few seconds.
    def show_error_message(self, message:str | Exception=None):
            if message:
                # Ensure only one message (error or success) is visible at a time.
                self.clear_success_message()
                message = str(message)
                # Place the error label at a fixed position.
                self.error_message_label.place(relx=.03, rely=.01)
                self.error_message_label.configure(text=message)
                # Use Concur to run the clearing function in a separate thread,
                # so the message disappears automatically without freezing the UI.
                Concur(lambda : self._clear_login_error(5)).start()
            
    # Private helper method used by the timer to clear the error message.
    def _clear_login_error(self, sec):
        sleep(sec)
        self.clear_error_message()
        
    # Immediately hides the error message label.
    def clear_error_message(self):
        self.error_message_label.place_forget()
        
        
    
    # Displays a success message at the top of the panel for a few seconds.
    def show_success_message(self, message:str=None):
        if message:
            # Ensure only one message is visible.
            self.clear_error_message()
            message = str(message)
            self.success_message_label.place(relx=.03, rely=.01)
            self.success_message_label.configure(text=message)
            # Start a timer to automatically hide the message.
            Concur(lambda : self._clear_success_message(5)).start()
            
    # Private helper method used by the timer to clear the success message.
    def _clear_success_message(self, sec):
        sleep(sec)
        self.clear_success_message()
    
    # Immediately hides the success message label.
    def clear_success_message(self):
        self.success_message_label.place_forget()