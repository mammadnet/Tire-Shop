from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from connection import Base, engine, session


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
class Product_size(Base):
    __tablename__ = 'product_size'
    id : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    product_id : Mapped[int] = mapped_column(ForeignKey('product.id'))
    size_id : Mapped[int] = mapped_column(ForeignKey('size.id'))
    
    product : Mapped['Product'] = relationship(back_populates='size_associations')
    size : Mapped['Size'] = relationship(back_populates='product_associations')
    

class Product(Base):
    __tablename__ = 'product'
    
    id : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    brand : Mapped[str] = mapped_column(String(20))
    size_associations : Mapped[list['Product_size']] = relationship(back_populates='product')
    sizes : Mapped[list['Size']] = relationship(secondary='product_size', back_populates='products', overlaps='size,product,size_associations')

class Size(Base):
    __tablename__ = 'size'
    
    id : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    products: Mapped[list['Product']] = relationship(secondary='product_size' ,back_populates='sizes', overlaps='product,size_associations,size')
    product_associations : Mapped[list['Product_size']] = relationship(back_populates='size', overlaps='products,sizes')
    
#----------------------------------------

# Create defined table on database
Base.metadata.create_all(engine)

