from customtkinter import *
from ..panel import Panel
from ...widgets import Item_button, Input, Btn, DropDown, render_text, create_updatable_labels
from database import session, get_all_employees_json, create_new_user, create_product
from database import remove_user_by_username, update_user_by_username, user_by_username, get_all_username
from database import get_all_products_json, delete_product_by_name_and_size, get_product_by_id, get_product_by_id_json, update_product_by_id, get_all_employee_usernames
from database import get_all_employee_and_manager_json, get_all_employee_and_manager_usernames, get_all_customers, get_customer_by_id
from database import create_order, get_customer_by_national_id, get_or_create_customer, check_customer_equal, get_all_orders
from database import get_total_product_quantity, get_brands_count, get_sizes_count, get_customers_count, get_employees_count, get_monthly_sales, get_daily_sales
from database import backup_database, restore_database
from database import ProductNotExistsException
from utilities import Concur, is_windows, get_current_datetime
from tkinter import ttk, filedialog
from time import sleep

class ManagerProductPanel(Panel):
    def __init__(self, root):
        super().__init__(root)
        self.pack(expand=True, fill="both")
        self.configure(bg_color='transparent', fg_color="transparent")

        
        # Setup button frame
        self.btn_frame = CTkFrame(self, fg_color='transparent')
        self.btn_frame.place(relwidth=.2, relheight=.3, relx=1, rely=.1, anchor="ne")
        self.btn_frame.columnconfigure(0, weight=1)
        self.btn_frame.rowconfigure((0,1,2,3), weight=1)
        
        product_list_btn = Item_button(self.btn_frame, 150, 50, rtopleft=20, rbottomleft=20, color="#393A4E", hover_color="#434357", background="#494A5F")
        product_list_btn.set_text("لیست محصولات", "white", 13)
        product_list_btn.set_action(lambda e: self.toggle_view('list'))
        product_list_btn.grid(row=0,column=0 ,sticky="e")
        
        product_new_btn = Item_button(self.btn_frame, 150, 50, rtopleft=20, rbottomleft=20, color="#393A4E", hover_color="#434357", background="#494A5F")
        product_new_btn.set_text("محصول جدید", "white", 13)
        product_new_btn.set_action(lambda e: self.toggle_view('new'))
        product_new_btn.grid(row=1,column=0 , sticky="e")
        
        product_delete_btn = Item_button(self.btn_frame, 150, 50, rtopleft=20, rbottomleft=20, color="#393A4E", hover_color="#434357", background="#494A5F")
        product_delete_btn.set_text("حذف محصول", "white", 13)
        product_delete_btn.set_action(lambda e: self.toggle_view('delete'))
        product_delete_btn.grid(row=2,column=0 , sticky="e")
        
        product_update_btn = Item_button(self.btn_frame, 150, 50, rtopleft=20, rbottomleft=20, color="#393A4E", hover_color="#434357", background="#494A5F")
        product_update_btn.set_text("تغیرات محصول", "white", 13)
        product_update_btn.set_action(lambda e: self.toggle_view('update'))
        product_update_btn.grid(row=3,column=0 , sticky="e")
        
        self.edit_product_frame = None
        self.edit_product_combobox = None
        self.edit_product_inputs = {}

        # Create table and new product form but hide them initially
        self.table = self.initialize_table(self)
        self.insert_content_to_table(self.table, get_all_products_json(session))
        
        self.new_product_inputs: list[Input] = []
        
        self.new_product_frame = None
        
        
        self.delete_product_frame = None
        self.delete_product_btn = None
        self.delete_product_combobox = None
        
        self.product_new(self)
        self.delete_product(self)
        self.edit_product(self)
        self.toggle_view('list')  # Show the new product form by default

    # Toggle between different views
    def toggle_view(self, view_name):
        if view_name == 'list':
            self.table.place(relheight=.9, relwidth=.8, relx=.02, rely=.05)
            self.insert_content_to_table(self.table, get_all_products_json(session))
            self.new_product_frame.place_forget()
            self.delete_product_frame.place_forget()
            self.edit_product_frame.place_forget()
        elif view_name == 'new':
            self.product_new(self)
            self.table.place_forget()
            self.delete_product_frame.place_forget()
            self.edit_product_frame.place_forget()
        elif view_name == 'delete':
            self.table.place_forget()
            self.new_product_frame.place_forget()
            self.edit_product_frame.place_forget()
            self.delete_product(self)
        elif view_name == 'update':
            self.table.place_forget()
            self.delete_product_frame.place_forget()
            self.edit_product(self)

    def initialize_table(self, window):
        style = ttk.Style()
        if is_windows():
            style.theme_use('clam')
        
        # Configure Treeview style
        style.configure("Custom1.Treeview",
        background="#494A5F",
        foreground="black",
        fieldbackground="#393A4E",
        rowheight=50,
        borderwidth=0
        )
        
        style.configure("Custom1.Treeview.Heading",
        background="#5B5D76",     # Header background color
        foreground="white",       # Header text color
        font=("Helvetica", 10, "bold"),
        relief='flat')
        
        style.map("Custom1.Treeview.Heading",
        background=[("active", "#6b6d87")],
        foreground=[("active", "white")])
        
        table = ttk.Treeview(window, style="Custom1.Treeview")
        table.configure(columns=("id", "name", "size", "price", "quantity"))
        table.configure(show="headings", selectmode="none")
        
        
        table.column("id", width=40, anchor="center")
        table.column("name", width=150, anchor="center")
        table.column("size", width=150, anchor="center")
        table.column("price", width=100, anchor="center")
        table.column("quantity", width=100, anchor="center")
        
        table.heading("id", text="id", anchor='center')
        table.heading("name", text="name", anchor='center')
        table.heading("size", text="size", anchor='center')
        table.heading("price", text="price", anchor='center')
        table.heading("quantity", text="quantity", anchor='center')
        
        table.place(relheight=.9, relwidth=.8, relx=.02, rely=.05)
        return table
    
    
    def insert_content_to_table(self, table:ttk.Treeview, content:list[dict]):
        table.delete(*table.get_children())

        for row in content:
            vals = (row["id"], row["brand"], f"{row['size']['width']}/{row['size']['ratio']}/{row['size']['rim']}", row["price"], row["quantity"])
            table.insert(parent="", index=0, values=vals)
            
    
    
    def product_new(self, window):
        if self.new_product_frame:
            content_frame = self.new_product_frame
        else:
            content_frame = CTkFrame(window, fg_color="#5B5D76")
            self.new_product_frame = content_frame
            
        content_frame.place(relheight=.9, relwidth=.8, relx=.02, rely=.05)
        content_frame.rowconfigure(tuple(range(0, 8)), weight=1)
        content_frame.columnconfigure((0, 3), weight=1, uniform='a')

        name_label = CTkLabel(content_frame, text=render_text("برند:"), text_color="white", font=(None, 13))
        name_label.grid(row=1, column=1, sticky='e', ipadx=60)
        name = StringVar()
        name_input = Input(content_frame, 15, 150, 35, "Name", name, just_english=True, show_err_callback=self.show_error_message)
        name_input.set_textvariable(name)
        name_input.grid(row=1, column=0)
        self.new_product_inputs.append(name_input)

        
        # قیمت
        price = StringVar()
        price_label = CTkLabel(content_frame, text=render_text("قیمت:"), text_color="white", font=(None, 13))
        price_label.grid(row=2, column=1, sticky='e', ipadx=60)
        price_input = Input(content_frame, 15, 150, 35, "Price", price, just_english=True, show_err_callback=self.show_error_message)
        price_input.set_textvariable(price)
        price_input.grid(row=2, column=0)
        self.new_product_inputs.append(price_input)
        # تعداد
        quantity = StringVar()
        quantity_label = CTkLabel(content_frame, text=render_text("تعداد:"), text_color="white", font=(None, 13))
        quantity_label.grid(row=3, column=1, sticky='e', ipadx=60)
        quantity_input = Input(content_frame, 15, 150, 35, "Quantity", quantity, just_english=True, show_err_callback=self.show_error_message)
        quantity_input.set_textvariable(quantity)
        quantity_input.grid(row=3, column=0)
        self.new_product_inputs.append(quantity_input)
        # پهنا
        width = StringVar()
        width_label = CTkLabel(content_frame, text=render_text("پهنا:"), text_color="white", font=(None, 13))
        width_label.grid(row=1, column=3, sticky='e', ipadx=60)
        width_input = Input(content_frame, 15, 150, 35, "Width", width, just_english=True, show_err_callback=self.show_error_message)
        width_input.set_textvariable(width)
        width_input.grid(row=1, column=2)
        self.new_product_inputs.append(width_input)
        # نسبت
        ratio = StringVar()
        ratio_label = CTkLabel(content_frame, text=render_text("نسبت:"), text_color="white", font=(None, 13))
        ratio_label.grid(row=2, column=3, sticky='e', ipadx=60)
        ratio_input = Input(content_frame, 15, 150, 35, "Ratio", ratio, just_english=True, show_err_callback=self.show_error_message)
        ratio_input.set_textvariable(ratio)
        ratio_input.grid(row=2, column=2, sticky='e')
        self.new_product_inputs.append(ratio_input)
        # رینگ
        rim = StringVar()
        rim_label = CTkLabel(content_frame, text=render_text("رینگ:"), text_color="white", font=(None, 13))
        rim_label.grid(row=3, column=3, sticky='e', ipadx=60)
        rim_input = Input(content_frame, 15, 150, 35, "Rim", rim, just_english=True, show_err_callback=self.show_error_message)
        rim_input.set_textvariable(rim)
        rim_input.grid(row=3, column=2)
        self.new_product_inputs.append(rim_input)
        
        btn = Btn(content_frame, 160, 45)
        btn.configure(font=(None, 16))
        btn.set_text(text='ایجاد محصول')
        btn.configure(command=lambda : self.new_product_action(
            self.show_error_message,
            name_input.get(), price_input.get(), quantity_input.get(),
            width_input.get(), ratio_input.get(), rim_input.get()))
        btn.grid(row=5, column=0, columnspan=4)
        
    
    def new_product_action(self, show_err_callback, name:str=None, price:str=None, quantity:str=None, width:str=None, ratio:str=None, rim:str=None):
        if self.check_value_inputs_in_new_product(show_err_callback, name, price, quantity, width, ratio, rim):
            try:
                create_product(session, name, price, quantity, width, ratio, rim)
                self.show_success_message("New product was created")
                self.clear_new_product_inputs()
            except Exception as e:
                show_err_callback(e)
    def clear_new_product_inputs(self):
        for input in self.new_product_inputs:
            input.clear()
    def check_value_inputs_in_new_product(self, show_err_callback, name:str=None, price:str=None, quantity:str=None, width:str=None, ratio:str=None, rim:str=None):
        if not (name and price and quantity and width and ratio and rim):
            show_err_callback("Inputs cannot be empty.")
            return False
        
        if not price.isdigit() or not quantity.isdigit():
            show_err_callback("Price and Quantity must be numbers.")
            return False
        
        if not width.isdigit() or not ratio.isdigit() or not rim.isdigit():
            show_err_callback("Width, Ratio, and Rim must be numbers.")
            return False
        
        return True
    
    def delete_product(self, window):
        if self.delete_product_frame:
            content_frame = self.delete_product_frame
        else:
            content_frame = CTkFrame(window, fg_color="#5B5D76")
            self.delete_product_frame = content_frame
            
            content_frame.rowconfigure((0, 3), weight=1)
            content_frame.columnconfigure((0, 1), weight=1, pad=20, uniform='a')

            text = render_text("نام محصول:")
            product_label = CTkLabel(content_frame, text=text, text_color="white", font=(None, 15))
            product_label.grid(row=0, column=1)
        
        content_frame.place(relheight=.9, relwidth=.8, relx=.02, rely=.05)
        
        # Fetch all products and populate the dropdown
        products = get_all_products_json(session)
        combo_delete_items = ["{}:{} {}".format(product['brand'], product['size']['width'], product['size']['ratio'], product['size']['rim']) for product in products]

        if self.delete_product_combobox:
            self.delete_product_combobox.destroy()
        
        self.delete_product_combobox = DropDown(content_frame, values=combo_delete_items, width=250)
        self.delete_product_combobox.grid(row=0, column=0)

        if not self.delete_product_btn:
            self.delete_product_btn = Btn(content_frame, 160, 45)
        
            self.delete_product_btn.configure(font=(None, 16))
            self.delete_product_btn.set_text(text='حذف محصول')
            self.delete_product_btn.grid(row=1, column=0, columnspan=4)
        
        self.delete_product_btn.configure(command=lambda : self.delete_product_action(self.delete_product_combobox.get(), self.show_error_message, self.show_success_message))

    def delete_product_action(self, product_info, show_msg_callback, show_success_msg_callback):
        
        try:
            brand, size = product_info.split(':')
            width, ratio, rim = map(int, size.split('/'))
            delete_product_by_name_and_size(session, brand, width, ratio, rim)
        except Exception as e:
            show_msg_callback(e)
        
        show_success_msg_callback("Product was deleted")
        self.delete_product(self)


    def edit_product(self, window):
        if self.edit_product_frame:
            content_frame = self.edit_product_frame
        else:
            content_frame = CTkFrame(window, fg_color="#5B5D76")
            self.edit_product_frame = content_frame
            
        content_frame.place(relheight=.9, relwidth=.8, relx=.02, rely=.05)
        content_frame.rowconfigure(tuple(range(0, 8)), weight=1)
        content_frame.columnconfigure((0, 3), weight=1, pad=40, uniform='a')

        # Label and dropdown to select product by brand and size
        select_product_label = CTkLabel(content_frame, text="Product:", text_color="white", font=(None, 15))
        select_product_label.grid(row=0, column=0)

        products = get_all_products_json(session)
        combo_items = [f'{product["id"]}:{product["brand"]}:{product["size"]["width"]}/{product["size"]["ratio"]}/{product["size"]["rim"]}' for product in products]
        selected_product = StringVar()
        if self.edit_product_combobox:
            self.edit_product_combobox.grid_forget()
            self.edit_product_combobox.destroy()

        self.edit_product_combobox = DropDown(content_frame, values=combo_items, width=250, command=self.load_product_data)
        self.edit_product_combobox.grid(row=0, column=1)

        self.create_input_field(content_frame, render_text("برند:"), 1, 0, 'brand')
        self.create_input_field(content_frame, render_text("پهنا:"), 1, 2, 'width')
        self.create_input_field(content_frame, render_text("نسبت:"), 2, 0, 'ratio')
        self.create_input_field(content_frame, render_text("رینگ:"), 2, 2, 'rim')
        self.create_input_field(content_frame, render_text("قیمت:"), 3, 0, 'price')
        self.create_input_field(content_frame, render_text("تعداد:"), 3, 2, 'quantity')

        update_btn = Btn(content_frame, 160, 45, text='ویرایش محصول')
        update_btn.configure(command=lambda: self.edit_product_action(
            self.edit_product_combobox.get(),
            self.show_error_message,
            self.show_success_message
        ))
        update_btn.configure(font=(None, 16))
        update_btn.set_text(text="Update Product")
        update_btn.grid(row=6, column=0, columnspan=4)
        # Helper function to create an input field
        
        
    def create_input_field(self, window, label_text, row, column, field_key, **kwargs):
        if field_key not in self.edit_product_inputs:
            label = CTkLabel(window, text=label_text, text_color="white", font=(None, 13))
            label.grid(row=row, column=column+1, **kwargs)
            var = StringVar()
            input_widget = Input(window, 15, 150, 35, None, var, placeholder_empty=False)
            input_widget.set_textvariable(var)
            input_widget.textvariable.set('')
            input_widget.grid(row=row, column=column)
            self.edit_product_inputs[field_key] = input_widget
            
    def edit_product_action(self, product_info, show_error_callback, show_success_callback):
        try:
            product_id, _, _ = product_info.split(':')
            new_brand_name = self.edit_product_inputs['brand'].get()
            new_width = int(self.edit_product_inputs['width'].get())
            new_ratio = int(self.edit_product_inputs['ratio'].get())
            new_rim = int(self.edit_product_inputs['rim'].get())
            
            new_price = float(self.edit_product_inputs['price'].get())
            new_quantity = int(self.edit_product_inputs['quantity'].get())
            update_product_by_id(session, product_id, new_brand_name, new_width, new_ratio, new_rim, new_quantity, new_price)
            show_success_callback(f'The product information has been changed.')
            self.edit_product(self)
            for v in list(self.edit_product_inputs.values()):
                v.textvariable.set('')
        except Exception as e:
            show_error_callback(e)
            
    def load_product_data(self, product_info):
        product_id, brand_name, size = product_info.split(':')
        width, ratio, rim = map(int, size.split('/'))
        product_data = get_product_by_id_json(session, product_id)

        if product_data:
            self.edit_product_inputs['brand'].set_placeholder_text(brand_name)
            self.edit_product_inputs['width'].set_placeholder_text(str(width))
            self.edit_product_inputs['ratio'].set_placeholder_text(str(ratio))
            self.edit_product_inputs['rim'].set_placeholder_text(str(rim))
            self.edit_product_inputs['price'].set_placeholder_text(str(product_data['price']))
            self.edit_product_inputs['quantity'].set_placeholder_text(str(product_data['quantity']))
 