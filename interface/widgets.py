from customtkinter import *
from math import cos, pi, sin
from typing import Iterator
from awesometkinter.bidirender import add_bidi_support_for_entry, isarabic, derender_text, render_text

# A customized CTkButton with a predefined style and bidi text support.
class Btn(CTkButton):
    def __init__(self, master, width, height, corner_radius=20, text='', **kwargs):
        super().__init__(master, **kwargs)
        # If the text is Arabic, render it correctly for right-to-left display.
        if isarabic(text):
            text = render_text(text)
        # Apply a consistent style for buttons across the application.
        self.configure(text=text, corner_radius = corner_radius, fg_color='#AFB3ED', hover_color='#888bba', text_color='#494A5F', border_color='#8688B0')
        self.configure(width=width, height=height)
        
    def disable_hover(self):
        self.configure(hover=False)
        
    def set_text(self, text):
        if isarabic(text):
            text = render_text(text)
        self.configure(text=text)


# A customized CTkEntry with advanced features like character limits,
# bidi text support, and placeholder handling.
class Input(CTkEntry):
    def __init__(self,master, corner_radius, width, height, placeholder_text,textvariable:StringVar, show=None, char_limit:int=20, show_err_callback=None, err_message=None, placeholder_empty=True,just_english:bool=False, **kwargs):
        super().__init__(master=master,corner_radius=corner_radius, width=width, height=height, placeholder_text=placeholder_text,show=show, **kwargs)
        # Enable bidi support for right-to-left languages within the entry widget.
        add_bidi_support_for_entry(self._entry)
        
        # Apply a consistent style for input fields.
        self.configure(fg_color='#646691', placeholder_text_color='#9495B8', text_color='#c5c6de', border_color='#8688B0')

        self.char_limit = char_limit
        self.textvariable = textvariable
        self.show_err_callback = show_err_callback # A callback function to display validation errors in the UI.
        self.err_message = err_message
        self.placeholder_text = placeholder_text
        self.placeholder_empty = placeholder_empty # If True, get() returns "" when the placeholder is visible.
        self.just_english = just_english
        
        # Set up the validation and behavior by binding callbacks to the textvariable.
        self._set_limit()
        self._set_just_english()
        self._set_justify()
        
    def disable(self):
        self.configure(state='disabled')
        
    def enable(self):
        self.configure(state='normal')
    
    def set_textvariable(self, textvariable):
        self.textvariable = textvariable
        self.configure(textvariable=textvariable)
        
        # Display the placeholder text initially if it exists.
        if self.placeholder_text:
            self.textvariable.set(self.placeholder_text)
            
        
    # This callback is triggered by trace_add whenever the entry's text is changed.
    def _entry_update_callback(self, *k):
        val = self.textvariable.get()
        # Enforces the character limit by trimming the string if it's too long.
        if len(val) > self.char_limit:
            self.textvariable.set(val[0:-1])
        
            # If an error callback is provided, call it to notify the user.
            if self.show_err_callback:
                if self.err_message:
                    self.show_err_callback(self.err_message)
                else:
                    message = f'Cannot be more than {self.char_limit} characters.'
                    self.show_err_callback(message)
    
    # Binds the character limit validation to the textvariable's 'write' event.
    def _set_limit(self):
        self.textvariable.trace_add('write', self._entry_update_callback)
    
    # Callback to automatically adjust text justification based on the first character's language.
    def _add_justify_for_arabic(self, *k):
        val = self.textvariable.get()
        if len(val) == 1:
            if isarabic(val):
                self.configure(justify=RIGHT)
            else:
                self.configure(justify=LEFT)
                
    # Binds the justification callback if multilingual input is allowed.
    def _set_justify(self):
        if not self.just_english:
            self.textvariable.trace_add('write', self._add_justify_for_arabic)
        
    # Callback to enforce that only English characters can be entered.
    def _set_english_only(self, *k):
        val = self.textvariable.get()
        # Ignore the callback if the text is just the initial placeholder.
        if val == self.placeholder_text:
            return

        arabic = False
        if val:
            # Check if an Arabic character was just added at the beginning or end.
            if isarabic(val[0]):
                self.textvariable.set(val[1:]) # Remove the invalid character.
                arabic = True
            
            elif isarabic(val[-1]):
                self.textvariable.set(val[:-1]) # Remove the invalid character.
                arabic = True
                
            # If an invalid character was removed, show an error message.
            if arabic and self.show_err_callback:
                message = 'Only English characters are allowed.'
                self.show_err_callback(message)
    
    # Binds the English-only validation callback if the 'just_english' flag is set.
    def _set_just_english(self):
        if self.just_english:
            self.textvariable.trace_add('write', self._set_english_only)
    
    def set_placeholder_text(self, text:str):
        if isarabic(text):
            text = render_text(text)
        self.placeholder_text = text
        self.textvariable.set(text)
            
    
    # Custom get() method to handle cases where the placeholder text is still visible.
    def get(self):
        val = self.textvariable.get()
        # If the current text is the placeholder, return an empty string instead.
        if self.placeholder_empty and val == self.placeholder_text:
            return ""
        else:
            return val
    
    def clear(self):
        self.textvariable.set('')
        
        
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
        if isarabic(text):
            text = render_text(text)
        x = self.width / 2
        y = self.height / 2
        self.create_text(x, y, text = text, fill=fill, font=(None, font_size))
    
    def _set_hover(self):
        self.bind("<Enter>", lambda _: self.itemconfig(self.polygon_id, fill=self.hover_color))
        self.bind("<Leave>", lambda _: self.itemconfig(self.polygon_id, fill=self.color))
        
    
    def set_action(self, action):
        self.bind("<Button-1>", action)
        
class DropDown(CTkComboBox):
    def __init__(self, window, width=140, height=28, dropdown_fg_color='#393A4E', dropdown_text_color="white",button_color="#8889a6", fg_color="#393A4E",text_color="white", border_color="#8889a6", **kwargs):
        
        super().__init__(window, width=width, height=height, dropdown_fg_color=dropdown_fg_color,\
                        dropdown_text_color=dropdown_text_color, text_color=text_color, fg_color=fg_color,\
                        button_color=button_color, corner_radius=15, border_color=border_color, **kwargs)
        
        

def create_updatable_labels(window, label_name, row, column, field_key, container:dict,font_size=13, **kwargs):
    if field_key not in container:
        temp_frame = CTkFrame(window, fg_color="#444759", corner_radius=10)
        temp_frame.grid(row=row, column=column, sticky="ew", **kwargs)
        label = CTkLabel(temp_frame, text=label_name, text_color="white", font=(None, font_size))
        label.pack(expand=True, fill="both", padx=10, pady=5, side="right")
        label_val = CTkLabel(temp_frame, text="?", text_color="white", font=(None, font_size))
        label_val.pack(expand=True, fill="both", padx=10, pady=5, side="right")
        if container is not None:
            container[field_key] = label_val
        return label_val
    return container[field_key]

def create_input_fields(window, label_text, row, column, field_key, container:dict,font_size=13, **kwargs):
    if (container is None) or field_key not in container:
        frame = CTkFrame(window, fg_color="transparent", bg_color="transparent")
        frame.grid(row=row, column=column, sticky="ew", **kwargs)
        label = CTkLabel(frame, text=label_text, text_color="white", font=(None, font_size))
        label.pack(expand=True, fill="both", padx=10, pady=5, side="right")
        var = StringVar()
        input_widget = Input(frame, 15, 150, 35, None, var, placeholder_empty=False)
        input_widget.set_textvariable(var)
        input_widget.textvariable.set('')
        input_widget.pack(expand=True, fill="both", padx=10, pady=5, side="right")
        if container is not None:
            container[field_key] = input_widget
        return input_widget
    return container[field_key]