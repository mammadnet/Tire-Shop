from customtkinter import *
from ..panel import Panel
from ...widgets import Item_button, DropDown, render_text, create_updatable_labels
from database import session
from database import get_all_customers, get_customer_by_id
from database import get_all_orders
from utilities import is_windows
from tkinter import ttk


class ManagerReportPanel(Panel):
    def __init__(self, root):
        super().__init__(root)
        self.pack(expand=True, fill="both")
        self.configure(bg_color='transparent', fg_color='transparent')
        
        # Setup button frame
        self.btn_frame = CTkFrame(self, fg_color='transparent')
        self.btn_frame.place(relwidth=.2, relheight=.3, relx=1, rely=.1, anchor="ne")
        self.btn_frame.columnconfigure(0, weight=1)
        self.btn_frame.rowconfigure((0,1), weight=1)

        
        report_btn = Item_button(self.btn_frame, 150, 50, rtopleft=20, rbottomleft=20, color="#393A4E", hover_color="#434357", background="#494A5F")
        report_btn.set_text("گزارش فروش", "white", 13)
        report_btn.set_action(lambda _: self.toogle_view('sell'))
        report_btn.grid(row=0,column=0 ,sticky="e")
        
        customer_report_btn = Item_button(self.btn_frame, 150, 50, rtopleft=20, rbottomleft=20, color="#393A4E", hover_color="#434357", background="#494A5F")
        customer_report_btn.set_text("گزارش مشتریان", "white", 13)
        customer_report_btn.set_action(lambda _: self.toogle_view('customer'))
        customer_report_btn.grid(row=1,column=0 , sticky="e")
        
        self.sell_report_table = None
        self.customer_report_frame = None
        
        self.initialized_customer_report = False
        self.initialized_sell_report = False
        
        self.customer_report_label_total_buy = None
        self.customer_report_label_total_orders = None
        # Create table 
        # self.initialize_report_table(self)
        # self.insert_content_to_report_table(self.sell_report_table, get_all_orders(session))
        self.customer_report_dropdown = None
        self.customer_report_table = None
        self.customer_report_labels = {}
        self.customer_report(self)
        # Show table by default
        self.current_view = 'customer'

    def toogle_view(self, view_name):
        if view_name == 'sell' and self.current_view != 'sell':
            self.initialize_report_table(self)
            self.insert_content_to_report_table(self.sell_report_table, get_all_orders(session))
            self.customer_report_frame.place_forget()
            self.current_view = 'sell'
        elif view_name == 'customer' and self.current_view != 'customer':
            
            self.sell_report_table.place_forget()
            self.customer_report(self)
            self.current_view = 'customer'
        
    
    def initialize_report_table(self, window):
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
        
        if self.sell_report_table:
            table = self.sell_report_table
        else:
            self.sell_report_table = ttk.Treeview(window, style="Custom1.Treeview")
            table = self.sell_report_table
            
        table.configure(columns=("id", "brand", "size", "price", "customer", "date"))
        table.configure(show="headings", selectmode="none")
        
        
        table.column("id", width=40, anchor="center")
        table.column("brand", width=100, anchor="center")
        table.column("size", width=150, anchor="center")
        table.column("price", width=120, anchor="center")
        table.column("customer", width=140, anchor="center")
        table.column("date", width=200, anchor="center")
        
        table.heading("id", text="id", anchor='center')
        table.heading("brand", text="brand", anchor='center')
        table.heading("size", text="size", anchor='center')
        table.heading("price", text="price", anchor='center')
        table.heading("customer", text="customer", anchor='center')
        table.heading("date", text="date", anchor='center')
        # Place the table in the window
        table.place(relheight=.9, relwidth=.8, relx=.02, rely=.05)
        
        return table

    def insert_content_to_report_table(self, table:ttk.Treeview, orders:list):
        table.delete(*table.get_children())

        for order in orders:
            for product in order.products:
                vals = (order.id, product.brand, f"{product.width}/{product.ratio}/{product.rim}", product.price, order.customer.name, order.date)
                table.insert(parent="", index=0, values=vals)
#---------------------------------------------------------------

    def customer_report(self, window):
        if not self.initialized_customer_report:
            content_frame = CTkFrame(window, fg_color="#5B5D76")
            self.customer_report_frame = content_frame
            
            content_frame.rowconfigure(tuple(range(0, 9)), weight=10)
            content_frame.columnconfigure(tuple(range(1,4)), weight=10, pad=20, uniform='a')
            content_frame.columnconfigure(0, weight=1, uniform='a')
            content_frame.columnconfigure(4, weight=1, uniform='a')
            
            dropdown_frame = CTkFrame(content_frame, fg_color="transparent")
            dropdown_frame.rowconfigure((0, 1), weight=1)
            dropdown_frame.columnconfigure((0,1,2,3), weight=1)
            dropdown_frame.place(relx=0.5, rely=0.05, relwidth=1, relheight=0.15,anchor="n")
            self.customer_report_dropdown_frame = dropdown_frame
            
            table_frame = CTkFrame(content_frame, fg_color="#45475C", corner_radius=10)
            table_frame.place(relx=0, rely=0.2, relwidth=1, relheight=0.8, anchor='nw')
            self.initialize_customer_report_table(table_frame)
        
            self.customer_report_label_total_buy = create_updatable_labels(dropdown_frame, render_text("مجموع خرید:"), 0, 2, "total_buy", container=self.customer_report_labels)
            self.customer_report_label_total_orders = create_updatable_labels(dropdown_frame, render_text("تعداد سفارشات:"), 1, 2, "total_orders", container=self.customer_report_labels)
            
            self.initialized_customer_report = True
            
        # Add dropdown for customer selection
        customers = get_all_customers(session)
        combo_items = [f'{customer.id}:{customer.name}' for customer in customers]

        if self.customer_report_dropdown:
            self.customer_report_dropdown.grid_forget()
            self.customer_report_dropdown.destroy()
    
        self.customer_report_dropdown = DropDown(self.customer_report_dropdown_frame, width=250, variable=StringVar(value=render_text("انتخاب مشتری:")), command=lambda x: self.customer_report_action(x))
        self.customer_report_dropdown.configure(values=combo_items)
        self.customer_report_dropdown.grid(row=0, column=0)

        self.clear_info(True)
        self.customer_report_frame.place(relheight=.9, relwidth=.8, relx=.02, rely=.05)
        
        
    def initialize_customer_report_table(self, window):
        style = ttk.Style()

        if is_windows():
            style.theme_use('clam')
        
        
        # Configure table style
        style.configure("Custom1.Treeview",
            background="#494A5F",
            foreground="black",
            fieldbackground="#393A4E",
            rowheight=50,
            borderwidth=0
        )
        
        style.configure("Custom1.Treeview.Heading",
            background="#5B5D76",
            foreground="white",
            font=("Helvetica", 10, "bold"),
            relief='flat'
        )
        
        style.map("Custom1.Treeview.Heading",
            background=[("active", "#6b6d87")],
            foreground=[("active", "white")]
        )
        
        # Create frame to hold dropdown and table
        if self.customer_report_table:
            table = self.customer_report_table
        else:
            self.customer_report_table = ttk.Treeview(window, style="Custom1.Treeview")
            table = self.customer_report_table
        
            
            # configure table
            table.configure(columns=("order_id", "product_id","brand", "size", "quantity", "price", "date"))
            table.configure(show="headings", selectmode="none")
            
            # Configure columns
            table.column("order_id", width=80, anchor="center")
            table.column("product_id", width=150, anchor="center")
            table.column("brand", width=150, anchor="center")
            table.column("size", width=150, anchor="center")
            table.column("quantity", width=100, anchor="center")
            table.column("price", width=120, anchor="center")
            table.column("date", width=150, anchor="center")
            
            # Configure headings
            table.heading("order_id", text="Order ID", anchor='center')
            table.heading("product_id", text="Product ID", anchor='center')
            table.heading("brand", text="Brand", anchor='center')
            table.heading("size", text="Size", anchor='center')
            table.heading("quantity", text="Quantity", anchor='center')
            table.heading("price", text="Price", anchor='center')
            table.heading("date", text="Date", anchor='center')
        
        table.pack(fill='both', expand=True, padx=5, pady=5)
        
        return table

    def insert_to_customer_table(self, orders:list):
        # Clear existing entries
        table = self.customer_report_table
        table.delete(*table.get_children())
        # Insert new entries
        for order in orders:
            for product in order.products:
                vals = (
                    order.id,
                    product.id,
                    product.brand,
                    f"{product.width}/{product.ratio}/{product.rim}",
                    product.quantity,
                    product.price,
                    order.date
                )
                table.insert(parent="", index=0, values=vals)
    
    def clear_info(self, reset=True):
        for label in self.customer_report_labels.values():
            label.configure(text="?" if reset else "0")
        self.customer_report_table.delete(*self.customer_report_table.get_children())
        

    def customer_report_action(self, customer_info:str):
        if not customer_info:
            return
            
        # Extract customer id from dropdown selection
        customer_id = customer_info.split(':')[0]
        
        # Get customer's orders
        customer = get_customer_by_id(session, customer_id)
        if customer and customer.orders:
            self.customer_report_label_total_orders.configure(text=len(customer.orders))
            total_buy = 0
            for products in customer.orders:
                total_buy += sum(product.price * product.quantity for product in products.products)
            # Update total buy label
            self.customer_report_label_total_orders.configure(text=len(customer.orders))
            self.customer_report_label_total_buy.configure(text=str(total_buy))
            # Update table with customer's orders
            self.insert_to_customer_table(customer.orders)
        else:
            # Clear table if no orders found
            self.clear_info(False)
    
    def destroy(self):
        self.pack_forget()
        return super().destroy()
