from customtkinter import *
from math import cos, pi, sin
from typing import Iterator

class Btn(CTkButton):
    def __init__(self, master,text, corner_radius, width, height, **kwargs):
        super().__init__(master, **kwargs)
        
        self.configure(text=text, corner_radius = corner_radius, fg_color='#AFB3ED', hover_color='#888bba', text_color='#494A5F', border_color='#8688B0')
        self.configure(width=width, height=height)


class Input(CTkEntry):
    def __init__(self,master, corner_radius, width, height, placeholder_text,textvariable:StringVar, show=None, char_limit:int=20, show_err_callback=None, err_message=None, **kwargs):
        super().__init__(master=master,corner_radius=corner_radius, width=width, height=height, placeholder_text=placeholder_text,show=show, **kwargs)
        
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
    
class Item_button(CTkCanvas):
    def __init__(self, root, width:int=0, height:int=0, color='#AFB3ED',hover_color="#4e4e61",background="#5B5D76", raduis:int=None, rtopleft:int=0, rtopright:int=0, rbottomleft:int=0, rbottomtright:int=0, **kwargs):
        super().__init__(root,width=width, height=height, background=background, highlightthickness=0)
        self.color=color
        if raduis:
            rtopleft, rtopright, rbottomleft, rbottomtright = (raduis, raduis, raduis, raduis)
        
        self.rtopleft = rtopleft
        self.rtopright = rtopright
        self.rbottomleft = rbottomleft
        self.rbottomtright = rbottomtright
        
        self.width = width
        self.height = height
        self.hover_color = hover_color
        self.polygon_id = self.create_rounded_box(0, 0, width, height)
        self._set_hover()
    
    @staticmethod
    def get_cos_sin(radius: int) -> Iterator[tuple[float, float]]:
        steps = max(radius, 10)
        for i in range(steps + 1):
            angle = pi * (i / steps) * 0.5
            yield (cos(angle) - 1) * radius, (sin(angle) - 1) * radius

        
    def create_rounded_box(self, x1: int, y1: int, x2: int, y2: int) -> int:
        points = []
        TR_angle_point = tuple(Item_button.get_cos_sin(self.rtopright))
        BR_angle_point = tuple(Item_button.get_cos_sin(self.rbottomtright))
        BL_angle_point = tuple(Item_button.get_cos_sin(self.rbottomleft))
        TL_angle_point = tuple(Item_button.get_cos_sin(self.rtopleft))
        
        
        for cos_r, sin_r in TR_angle_point:
            points.append((x2 + sin_r, y1 - cos_r))         # Top right
        for cos_r, sin_r in BR_angle_point:
            points.append((x2 + cos_r, y2 + sin_r))         # Botton right
        for cos_r, sin_r in BL_angle_point:
            points.append((x1 - sin_r, y2 + cos_r))         # Botton left
        for cos_r, sin_r in TL_angle_point:
            points.append((x1 - cos_r, y1 - sin_r))         # Top left
        
        
        return self.create_polygon(points, fill=self.color, smooth=True, joinstyle='round')

    def set_text(self, text:str, fill, font_size):
        x = self.width / 2
        y = self.height / 2
        self.create_text(x, y, text = text, fill=fill, font=(None, font_size))
    
    def _set_hover(self):
        self.bind("<Enter>", lambda _: self.itemconfig(self.polygon_id, fill=self.hover_color))
        self.bind("<Leave>", lambda _: self.itemconfig(self.polygon_id, fill=self.color))
        
    
    def set_action(self, action):
        self.bind("<Button-1>", action)
        