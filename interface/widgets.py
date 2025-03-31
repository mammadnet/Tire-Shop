from customtkinter import *


class Btn(CTkButton):
    def __init__(self, master,text, corner_radius, width, height, **kwargs):
        super().__init__(master, **kwargs)
        
        self.configure(text=text, corner_radius = corner_radius, fg_color='#AFB3ED', hover_color='#888bba', text_color='#494A5F')
        self.configure(width=width, height=height)
