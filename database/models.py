import datetime
from sqlalchemy import Integer, String, Date, DateTime , ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .connection import Base, engine, session


class Customer(Base):
    __tablename__ = 'customer'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(20), nullable=False)
    lastName: Mapped[str] = mapped_column(String(20), nullable=False)
    orders: Mapped[list['Order']] = relationship('Order')


class Order(Base):
    __tablename__ = 'order'
    
    id : Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    customer_id : Mapped[int] = mapped_column(ForeignKey("customer.id"))
    customer : Mapped['Customer'] = relationship(back_populates='orders')
    name : Mapped[str] = mapped_column(String)
    
# Many to Many relationship between tire sizes and brands
class Product(Base):
    __tablename__ = 'product'
    id : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    brand_id : Mapped[int] = mapped_column(ForeignKey('brand.id'))
    size_id : Mapped[int] = mapped_column(ForeignKey('size.id'))
    
    brand : Mapped['Brand'] = relationship(back_populates='products')
    size : Mapped['Size'] = relationship(back_populates='products')

class Brand(Base):
    __tablename__ = 'brand'
    
    id : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(20), unique=True)
    products: Mapped[list['Product']] = relationship(back_populates='brand')

class Size(Base):
    __tablename__ = 'size'
    
    id : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    products: Mapped[list['Product']] = relationship(back_populates='size')
    
    # The size of tire --> width/ratio/rim
    width :   Mapped[int] = mapped_column()
    ratio :   Mapped[int] = mapped_column()
    rim   :   Mapped[int] = mapped_column()
#----------------------------------------


class User(Base):
    __tablename__ = 'user'
    id : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name : Mapped[str] = mapped_column(String(20), nullable=False)
    lastname : Mapped[str] = mapped_column(String(20), nullable=False)
    phone : Mapped[str] = mapped_column(String(20), nullable=False)
    national_number : Mapped[str] = mapped_column(nullable=False)
    
    user_name : Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    hashed_passwd : Mapped[str] = mapped_column(String(20), nullable=False)
    
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
    
class Admin(User):
    
    start_date = mapped_column(Date ,default=datetime.datetime.now().date(), use_existing_column=True)
    
    __mapper_args__ = {
        "polymorphic_identity": "admin",
    }
    
class Manager(User):
    start_date = mapped_column(Date, default=datetime.datetime.now().date(), use_existing_column=True)
    
    __mapper_args__ = {
        "polymorphic_identity": "manager",
    }

class Employee(User):
    
    start_date = mapped_column(Date ,default=datetime.datetime.now().date(), use_existing_column=True)
    
    __mapper_args__ = {
        "polymorphic_identity": "employee",
    }
        
    
# Create defined table on database
Base.metadata.create_all(engine)

