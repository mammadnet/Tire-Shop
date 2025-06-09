from customtkinter import *
from ..panel import Panel
from ...widgets import Item_button, Input, Btn, DropDown, render_text, create_input_fields
from database import session
from database import get_all_products_json, get_product_by_id, get_product_by_id_json
from database import get_all_customers, get_customer_by_id, create_order, get_or_create_customer
from database import ProductNotExistsException
from utilities import is_windows
from tkinter import ttk


class EmployeeSellPanel(Panel):
    def __init__(self, root):
        super().__init__(root)
        self.pack(expand=True, fill="both")
        self.configure(bg_color='transparent', fg_color='transparent')
        
        # Setup button frame
        self.btn_frame = CTkFrame(self, fg_color='transparent')
        self.btn_frame.place(relwidth=.2, relheight=.3, relx=1, rely=.1, anchor="ne")
        self.btn_frame.columnconfigure(0, weight=1)
        self.btn_frame.rowconfigure((0,1,2), weight=1)

        sell_btn = Item_button(self.btn_frame, 150, 50, rtopleft=20, rbottomleft=20, color="#393A4E", hover_color="#434357", background="#494A5F")
        sell_btn.set_text("فروش محصول", "white", 13)
        sell_btn.grid(row=0,column=0 ,sticky="e")
        sell_btn.set_action(lambda e: self.toggle_view('sell'))
        
        multi_sell_btn = Item_button(self.btn_frame, 150, 50, rtopleft=20, rbottomleft=20, color="#393A4E", hover_color="#434357", background="#494A5F")    
        multi_sell_btn.set_text("فروش چند محصول", "white", 13)
        multi_sell_btn.grid(row=1,column=0 , sticky="e")
        
        product_list_btn = Item_button(self.btn_frame, 150, 50, rtopleft=20, rbottomleft=20, color="#393A4E", hover_color="#434357", background="#494A5F")
        product_list_btn.set_text("لیست محصولات", "white", 13)
        product_list_btn.grid(row=2,column=0 , sticky="e")
        product_list_btn.set_action(lambda e: self.toggle_view('list'))
        
        self.error_message_label = CTkLabel(self, text_color="firebrick1")
        self.success_message_label = CTkLabel(self, text_color="green")
        
        # # Create table 
        self.table = self.initialize_table(self)
        
        self.sell_frame = None
        self.sell_inputs = {}
        self.sell_labels = {}
        self.sell_combobox = None
        self.sell_userinfo_combobox = None
        self.customer_sell_inputs = {}
        self.sell(self)
        

        
        # Show table by default
        self.current_view = None
        
    def toggle_view(self, view_name):
        if view_name == 'list' and self.current_view != 'list':
            if self.sell_frame:
                self.sell_frame.place_forget()
            # Show the table
            self.insert_content_to_table(self.table, get_all_products_json(session))
            self.table.place(relheight=.9, relwidth=.8, relx=.02, rely=.05)
            self.current_view = 'list'
        elif view_name == 'sell' and self.current_view != 'sell':
            if hasattr(self, 'table'):
                self.table.place_forget()
            self.sell(self)
            self.current_view = 'sell'
    #--------------------------------------------------------------------

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
            
    
    def sell(self, window):
        if self.sell_frame:
            content_frame = self.sell_frame
        else:
            content_frame = CTkFrame(window, fg_color="#5B5D76")
            self.sell_frame = content_frame
        content_frame.place(relheight=.9, relwidth=.8, relx=.02, rely=.05)
        content_frame.rowconfigure(tuple(range(0, 9)), weight=10)
        content_frame.columnconfigure(tuple(range(1,4)), weight=10, pad=20, uniform='a')
        content_frame.columnconfigure(0, weight=1, uniform='a')
        content_frame.columnconfigure(4, weight=1, uniform='a')
        # Create input fields for selling a product
        product_label = CTkLabel(content_frame, text="Product:", text_color="white", font=(None, 15))
        product_label.grid(row=0, column=1)
        products = get_all_products_json(session)
        combo_items = [f'{product["id"]}:{product["brand"]}:{product["size"]["width"]}/{product["size"]["ratio"]}/{product["size"]["rim"]}' for product in products]
        selected_product = StringVar()
        selected_product.set("Select Product")
        if self.sell_combobox:
            self.sell_combobox.grid_forget()
            self.sell_combobox.destroy() 
        self.sell_combobox = DropDown(content_frame, values=combo_items, width=250, variable=selected_product, command=self._update_sell_labels)
        self.sell_combobox.grid(row=0, column=2)
        self.create_sell_labels(content_frame, render_text("برند:"), 1, 1, 'brand')
        self.create_sell_labels(content_frame, render_text("قیمت:"), 1, 3, 'price')
        self.create_sell_labels(content_frame, render_text("سایز:"), 2, 1, 'size')
        self.create_sell_labels(content_frame, render_text("موجودی:"), 2, 3, 'quantity')

        create_input_fields(content_frame, render_text("تعداد:"), 3, 2, 'quantity', container=self.sell_inputs, just_english=True, just_number=True, show_err_callback=self.show_error_message)

        customers = get_all_customers(session)
        self.user_info_combo_items = [f'{customer.id}:{customer.name}' for customer in customers]
        selected_customer = StringVar()
        selected_customer.set("Select Customer")
        if self.sell_userinfo_combobox:
            self.sell_userinfo_combobox.grid_forget()
            self.sell_userinfo_combobox.destroy()
        self.sell_userinfo_combobox = DropDown(content_frame, values=self.user_info_combo_items, width=250, variable=selected_customer, command=self.update_customer_info_inputs)
        self.sell_userinfo_combobox.grid(row=4, column=2)
        
        create_input_fields(content_frame, render_text("نام مشتری:"), 5, 1, 'customer_name', container=self.customer_sell_inputs)
        create_input_fields(content_frame, render_text("تلفن مشتری:"), 5, 3, 'customer_phone',just_english=True, just_number=True, container=self.customer_sell_inputs, show_err_callback=self.show_error_message)
        create_input_fields(content_frame, render_text("آدرس مشتری:"), 6, 1, 'customer_address', container=self.customer_sell_inputs)
        create_input_fields(content_frame, render_text("شماره ملی:"), 6, 3, 'customer_national_number',just_english=True, just_number=True, container=self.customer_sell_inputs, show_err_callback=self.show_error_message)


        sell_btn = Btn(content_frame, 160, 45)
        sell_btn.configure(font=(None, 16))
        sell_btn.set_text(text='ثبت فروش')
        sell_btn.configure(command=lambda: self.sell_action(
            self.show_error_message,
            self.show_success_message
        ))
        sell_btn.grid(row=7, column=0, columnspan=4)
          
    def create_sell_labels(self, window, label_name, row, column, field_key, **kwargs):
        if field_key not in self.sell_labels:
            temp_frame = CTkFrame(window, fg_color="#444759", corner_radius=10)
            temp_frame.grid(row=row, column=column, sticky="ew", **kwargs)
            label = CTkLabel(temp_frame, text=label_name, text_color="white", font=(None, 13))
            label.pack(expand=True, fill="both", padx=10, pady=5, side="right")
            label_val = CTkLabel(temp_frame, text="?", text_color="white", font=(None, 13))
            label_val.pack(expand=True, fill="both", padx=10, pady=5, side="right")
            self.sell_labels[field_key] = label_val


    def update_sell_labels(self, product_info):
        # product_info is expected to be a dict with keys: 'brand', 'price', 'size'
        # 'size' itself is a dict with keys: 'width', 'ratio', 'rim'
        if not product_info:
            # Clear labels if no product_info
            self.sell_labels['brand'].configure(text="?")
            self.sell_labels['price'].configure(text="?")
            self.sell_labels['size'].configure(text="?")
            return

        brand = product_info.get('brand', '?')
        price = product_info.get('price', '?')
        size = product_info.get('size', {})
        quantity = product_info.get('quantity', '?')
        size_str = f"{size.get('width', '?')}/{size.get('ratio', '?')}/{size.get('rim', '?')}"
        self.sell_labels['brand'].configure(text=str(brand))
        self.sell_labels['price'].configure(text=str(price))
        self.sell_labels['size'].configure(text=size_str)
        self.sell_labels['quantity'].configure(text=str(quantity))
        
        
    def _update_sell_labels(self, product_info):
        # product_info is expected to be a string in the format "id:brand:width/ratio/rim"
        product_id = product_info.split(':')[0]
        product_data = get_product_by_id_json(session, product_id)
        if product_data:
            self.update_sell_labels(product_data)
        else:
            self.update_sell_labels({})
            
    def update_customer_info_inputs(self, customer_info):
        # customer_info is expected to be a string in the format "id:name"
        if not customer_info:
            self.customer_sell_inputs['customer_name'].set_placeholder_text('')
            self.customer_sell_inputs['customer_phone'].set_placeholder_text('')
            self.customer_sell_inputs['customer_address'].set_placeholder_text('')
            return
        
        customer_id, customer_name = customer_info.split(':')
        customer_data = get_customer_by_id(session, customer_id)
        
        if customer_data:
            self.customer_sell_inputs['customer_name'].set_placeholder_text(customer_data.name)
            self.customer_sell_inputs['customer_phone'].set_placeholder_text(customer_data.phone)
            self.customer_sell_inputs['customer_address'].set_placeholder_text(customer_data.address)
            self.customer_sell_inputs['customer_national_number'].set_placeholder_text(customer_data.national_number)
    def sell_action(self, show_error_callback, show_success_callback):
        try:
            product_info = self.sell_combobox.get().split(':')
            product_id = product_info[0]
            quantity = int(self.sell_inputs['quantity'].get()) if self.sell_inputs['quantity'].get() else 0
            customer_info = self.sell_userinfo_combobox.get().split(':')
            customer_id = customer_info[0]
            customer_name = self.customer_sell_inputs['customer_name'].get()
            customer_address = self.customer_sell_inputs['customer_address'].get()
            customer_phone = self.customer_sell_inputs['customer_phone'].get()
            customer_national_id = self.customer_sell_inputs['customer_national_number'].get()
            # Validate inputs
            if not product_id or not quantity or not customer_name or not customer_address or not customer_phone or not customer_national_id:
                raise ValueError("Please fill all fields.")

            self.sell_product(session, product_id, customer_name, customer_address, customer_phone, customer_national_id, quantity)
            show_success_callback(f'The product has been sold successfully.')
            self.sell(self)
            self.clear_sell_inputs()
            self.sell(self)
        except ProductNotExistsException as ve:
            show_error_callback("Please select a valid product.")
        except Exception as ve:
            show_error_callback(str(ve))
  

    def sell_product(self, session, product_id, customer_name, customer_address, customer_phone, customer_national_id, quantity):

        product = get_product_by_id(session, product_id)
        customer = get_or_create_customer(session, customer_name, customer_address, customer_phone, customer_national_id)


        create_order(session, customer, product, quantity)
        
    def clear_sell_inputs(self):
        for label in self.sell_labels.values():
            label.configure(text="?")
        for input in self.sell_inputs.values():
            input.set_placeholder_text('')
        for input in self.customer_sell_inputs.values():
            input.set_placeholder_text('')