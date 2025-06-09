import datetime
from sqlalchemy import Integer, String, Date, DateTime , ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .connection import Base, engine, session


# Represents a customer in the database.
class Customer(Base):
    __tablename__ = 'customer'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(20), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    address: Mapped[str] = mapped_column(String(100), nullable=False)
    national_number: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)

    # Defines a one-to-many relationship between a Customer and their Orders.
    # 'back_populates' links this relationship to the 'customer' relationship in the Order class.
    orders: Mapped[list['Order']] = relationship('Order', back_populates='customer')


# Represents a single order made by a customer.
class Order(Base):
    __tablename__ = 'order'
    id : Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # Defines a foreign key to link the order back to a specific customer.
    customer_id : Mapped[int] = mapped_column(ForeignKey("customer.id"))
    # Defines a many-to-one relationship from Order to Customer.
    customer : Mapped['Customer'] = relationship(back_populates='orders')


    # The date the order was created, with the default value being the current date.
    date: Mapped[datetime.date] = mapped_column(Date, default=datetime.datetime.now().date(), nullable=False)
    # Defines a one-to-many relationship to the line items (ProductsOrder) within this order.
    products: Mapped[list['ProductsOrder']] = relationship('ProductsOrder', backref='order')

# Represents a line item in an order (an association between an order and product details).
# This table stores a snapshot of product details at the time of purchase.
class ProductsOrder(Base):
    __tablename__ = 'products_order'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(ForeignKey('order.id'))
    
    # Stores historical data for the ordered product.
    brand: Mapped[str] = mapped_column(String(20), nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    width: Mapped[int] = mapped_column(nullable=False)
    ratio: Mapped[int] = mapped_column(nullable=False)
    rim: Mapped[int] = mapped_column(nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, default=1)

# Represents a physical product (a tire) in the inventory.
class Product(Base):
    __tablename__ = 'product'
    id : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    # Foreign keys to link the product to its brand and size.
    brand_id : Mapped[int] = mapped_column(ForeignKey('brand.id'))
    size_id : Mapped[int] = mapped_column(ForeignKey('size.id'))
    
    price : Mapped[float] = mapped_column(nullable=False)
    quantity : Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    # --- Relationships ---
    # Defines a many-to-one relationship from Product to Brand.
    brand : Mapped['Brand'] = relationship(back_populates='products')
    # Defines a many-to-one relationship from Product to Size.
    size : Mapped['Size'] = relationship(back_populates='products')

    # A method to serialize the Product object into a dictionary.
    def to_dict(self):
        return {
            "id": self.id,
            "brand_id": self.brand_id,
            "size_id": self.size_id,
            # Includes details from related objects (Brand and Size) for convenience.
            "brand": self.brand.name if self.brand else None,
            "size": {
                "width": self.size.width if self.size else None,
                "ratio": self.size.ratio if self.size else None,
                "rim": self.size.rim if self.size else None,
            } if self.size else None,
            "price": self.price,
            "quantity": self.quantity,
        }


# Represents a product brand (e.g., Michelin, Goodyear).
class Brand(Base):
    __tablename__ = 'brand'
    
    id : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(20), unique=True)
    # Defines a one-to-many relationship from Brand to its associated Products.
    products: Mapped[list['Product']] = relationship(back_populates='brand')
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
        }

# Represents the dimensions of a tire (width, aspect ratio, rim diameter).
class Size(Base):
    __tablename__ = 'size'
    
    id : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    # Defines a one-to-many relationship from Size to its associated Products.
    products: Mapped[list['Product']] = relationship(back_populates='size')
    
    # The size of tire --> width/ratio/rim
    width :   Mapped[int] = mapped_column()
    ratio :   Mapped[int] = mapped_column()
    rim   :   Mapped[int] = mapped_column()
    def to_dict(self):
        return {
            "id": self.id,
            "width": self.width,
            "ratio": self.ratio,
            "rim": self.rim,
        }
#----------------------------------------

# --- User Hierarchy using Single Table Inheritance ---

# Represents a base user, containing common attributes for all user types (Admin, Manager, Employee).
# This class uses a single-table inheritance strategy.
class User(Base):
    __tablename__ = 'user'
    id : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name : Mapped[str] = mapped_column(String(20), nullable=False)
    lastname : Mapped[str] = mapped_column(String(20), nullable=False)
    phone : Mapped[str] = mapped_column(String(20), nullable=False)
    national_number : Mapped[str] = mapped_column(nullable=False)
    
    user_name : Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    hashed_passwd : Mapped[str] = mapped_column(String(20), nullable=False)
    
    # This is the discriminator column, which determines the specific subclass (Admin, Manager, etc.).
    type : Mapped[str]
    __mapper_args__ = {
        "polymorphic_on": "type",
        "polymorphic_identity": "user",
    }
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "lastname": self.lastname,
            "phone": self.phone,
            "national_number": self.national_number,
            "username":self.user_name
        }
    
# Represents an Administrator, inheriting from the base User class.
class Admin(User):
    
    start_date = mapped_column(Date ,default=datetime.datetime.now().date(), use_existing_column=True)
    
    # Sets the value for the 'type' column when an Admin is created.
    __mapper_args__ = {
        "polymorphic_identity": "admin",
    }
    
# Represents a Manager, inheriting from the base User class.
class Manager(User):
    start_date = mapped_column(Date, default=datetime.datetime.now().date(), use_existing_column=True)
    
    # Sets the value for the 'type' column when a Manager is created.
    __mapper_args__ = {
        "polymorphic_identity": "manager",
    }

# Represents an Employee, inheriting from the base User class.
class Employee(User):
    
    start_date = mapped_column(Date ,default=datetime.datetime.now().date(), use_existing_column=True)
    
    # Sets the value for the 'type' column when an Employee is created.
    __mapper_args__ = {
        "polymorphic_identity": "employee",
    }
        
    
# This line connects to the database and creates all the defined tables if they do not already exist.
Base.metadata.create_all(engine)