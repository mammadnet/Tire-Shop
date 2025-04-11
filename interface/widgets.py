from customtkinter import *


class Btn(CTkButton):
    def __init__(self, master,text, corner_radius, width, height, **kwargs):
        super().__init__(master, **kwargs)
        
        self.configure(text=text, corner_radius = corner_radius, fg_color='#AFB3ED', hover_color='#888bba', text_color='#494A5F', border_color='#8688B0')
        self.configure(width=width, height=height)


class Input(CTkEntry):
    def __init__(self,master, corner_radius, width, height, placeholder_text,textvariable:StringVar, char_limit:int=20, show_err_callback=None, err_message=None, **kwargs):
        super().__init__(master=master,corner_radius=corner_radius, width=width, height=height, placeholder_text=placeholder_text, **kwargs)
        
        self.configure(fg_color='#646691', placeholder_text_color='#9495B8', text_color='#c5c6de', border_color='#8688B0')

        self.char_limit = char_limit
        self.textvariable = textvariable
        self.show_err_callback = show_err_callback
        self.err_message = err_message
        
        
        self._set_limit()
        
    def disable(self):
        self.configure(state='disabled')
        
    def enable(self):
        self.configure(state='normal')
    
    def set_textvariable(self, textvariable):
        self.configure(textvariable=textvariable)
        
    def _entry_update_callback(self, *k):
        val = self.textvariable.get()
        if len(val) > self.char_limit:
            self.textvariable.set(val[0:-1])
        
            if self.show_err_callback:
                if self.err_message:
                    self.show_err_callback(self.err_message)
                else:
                    message = f'Cannot be more than {self.char_limit} characters.'
                    self.show_err_callback(message)
    
    def _set_limit(self):
        self.textvariable.trace_add('write', self._entry_update_callback)
        
        
class Root(CTk):
    def __init__(self, fullscreen=True, **kwargs):
        super().__init__(**kwargs)
        
        if fullscreen:
            self.win_max()
    
    def win_max(self):
        max_width = self.winfo_screenwidth()
        max_height = self.winfo_screenheight()
        self.geometry('{}x{}+0+0'.format(max_width, max_height))
        