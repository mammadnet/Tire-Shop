from customtkinter import *
from ..panel import Panel
from ...widgets import render_text, create_updatable_labels
from database import session
from database import get_total_product_quantity, get_brands_count, get_sizes_count, get_customers_count, get_employees_count, get_monthly_sales, get_daily_sales


class ManagerDashboardPanel(Panel):
    def __init__(self, root):
        super().__init__(root)
        self.pack(expand=True, fill="both", padx=20, pady=20)
        self.configure(bg_color="transparent", fg_color="transparent")

        # Setup button frame
        self.content_frame = CTkFrame(self, fg_color="#373849", corner_radius=20)
        self.content_frame.rowconfigure((0,1,2,3), weight=1)
        self.content_frame.columnconfigure((1,2,3), weight=10)
        self.content_frame.columnconfigure(0, weight=1)
        self.content_frame.columnconfigure(4, weight=1)
        
        
        self.content_frame.pack(fill="both", expand=True)

        self.labels = {}
        create_updatable_labels(self.content_frame, render_text("تعداد کارمندان"), 0, 1, "employee_number",font_size=16,container=self.labels)     
        create_updatable_labels(self.content_frame, render_text("فروش روزانه"), 0, 3, "daily_sell",font_size=16,container=self.labels)
        create_updatable_labels(self.content_frame, render_text("فروش ماهانه"), 1, 1, "monthly_sell",font_size=16,container=self.labels)
        create_updatable_labels(self.content_frame, render_text("تعداد مشتریان"), 1, 3, "customer_number",font_size=16,container=self.labels)
        create_updatable_labels(self.content_frame, render_text("تعداد محصولات"), 2, 1, "product_number",font_size=16,container=self.labels)
        create_updatable_labels(self.content_frame, render_text("تعداد سایزها"), 2, 3, "product_size_number",font_size=16,container=self.labels)
        create_updatable_labels(self.content_frame, render_text("تعداد برندها"), 3, 2, "product_brand_number",font_size=16,container=self.labels)

        self.update_labels()

    def update_labels(self):
        # Update the labels with the latest data
        self.labels['employee_number'].configure(text=str(get_employees_count(session)))
        self.labels['daily_sell'].configure(text=str(get_daily_sales(session)))
        self.labels['monthly_sell'].configure(text=str(get_monthly_sales(session)))
        self.labels['customer_number'].configure(text=str(get_customers_count(session)))
        self.labels['product_number'].configure(text=str(get_total_product_quantity(session)))
        self.labels['product_size_number'].configure(text=str(get_sizes_count(session)))
        self.labels['product_brand_number'].configure(text=str(get_brands_count(session)))

