from customtkinter import *
from utilities import Concur
from time import sleep

class Panel(CTkFrame):
    def __init__(self, root, **kwargs):
        super().__init__(root, **kwargs)

        self.error_message_label = CTkLabel(self, text_color="firebrick1")
        self.success_message_label = CTkLabel(self, text_color="green")
    
    
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
    