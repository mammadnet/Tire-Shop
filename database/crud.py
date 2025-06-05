from .models import User,Employee,Admin,Manager,Order,Customer,Product,Size,Brand

from sqlalchemy.orm import Session, InstrumentedAttribute

from sqlalchemy import select, exists

from .connection import session

from utilities import hashing

from .Exeptions import NationalNumberAlreadyExistsException, UsernameAlreadyExistsException, UsernameNotExistsException, ProductAlreadyExistsException, ProductNotExistsException

# Check if a user is exist
def exist_check_user(session:Session, by:InstrumentedAttribute, pat):
    subq = exists(by).where(by == pat).select()
    exist_check = session.execute(subq).scalar()
    return exist_check

def user_by_username(db:Session, username:str):
    query = select(User).where(User.user_name == username)
    user = db.execute(query).first()
    if not user or not user[0]:
        raise UsernameNotExistsException(username)
    
    return user[0]

def user_by_username_pass(session:Session, username:str, passwd:str):
    with session as db:
        
        query = select(User).where(User.user_name == username).where(User.hashed_passwd == hashing(passwd))
        user = db.execute(query).scalar()
        return user
    return None
    
    


def create_new_user(session: Session, name:str, lastname:str, phone:str, national_number:str, level_type:str, username:str, passwd:str) -> User:
    level_type = level_type.lower()
    if level_type == 'admin':
        new_user = Admin(name=name, lastname=lastname, phone=phone, national_number=national_number, user_name=username)
    elif level_type == 'manager':
        new_user = Manager(name=name, lastname=lastname, phone=phone, national_number=national_number, user_name=username)
    elif level_type == 'employee':
        new_user = Employee(name=name, lastname=lastname, phone=phone, national_number=national_number, user_name=username)
    else:
        return None
    
    
    
    with session as db:
        exist_national_id_check = exist_check_user(session, User.national_number, national_number)
        exist_username_check = exist_check_user(session, User.user_name, username)
                
        if exist_national_id_check:
            raise NationalNumberAlreadyExistsException(national_number)
        
        if exist_username_check:
            raise UsernameAlreadyExistsException(username)

        new_user.hashed_passwd = hashing(passwd)
        db.add(new_user)
        db.commit()
            
    # TODO rais an error that the national code already exist
    return None
        

def login_permission(session, username, passwd) -> bool:
    user = user_by_username_pass(session, username, passwd)
    if user:
        return True
    else:
        return False
    
    
def get_all_employees(session:Session):
    stmt = select(Employee)
    
    content = session.execute(stmt).fetchall()
    return content

def get_all_employees_json(session:Session):
    rows = get_all_employees(session)
    json = []
    
    for row in rows:
        json.append(row[0].to_dict())
    
    return json

def remove_user_by_username(db:Session, username:str):
    user = user_by_username(db, username)
    if user:
        db.delete(user)
        db.commit()
        return True
    return False


def update_user_by_username(
    session: Session,
    username: str,
    name: str = None,
    lastname: str = None,
    phone: str = None,
    national:str = None,
    new_username: str = None,
    password: str = None
) -> User:
    # Fetch the user by current username
    user = user_by_username(session, username)
    if not user:
        raise UsernameNotExistsException(f"Username '{username}' does not exist.")

    # Check if the new username is different and not taken
    if new_username and new_username != user.user_name:
        existing_user = session.query(User).filter(User.user_name == new_username).first()
        if existing_user:
            raise UsernameAlreadyExistsException(f"Username '{new_username}' is already taken.")
        user.user_name = new_username

    # Apply other updates if provided
    if name is not None:
        user.name = name
    if lastname is not None:
        user.lastname = lastname
    if phone is not None:
        user.phone = phone
    if national is not None:
        user.national_number = national
    if password is not None:
        user.hashed_passwd = hashing(password)

    # Save changes
    session.commit()
    session.refresh(user)

    return user

def get_all_username(session=Session):
    
    users = get_all_employees_json(session)
    
    return [user['username'] for user in users]


def create_product(session: Session, brand_name: str, price: float, quantity: int, width: int, ratio: int, rim: int) -> Product:
    is_new_product = False
    # Find or create brand
    brand = session.query(Brand).filter_by(name=brand_name).first()
    if not brand:
        brand = Brand(name=brand_name)
        session.add(brand)
        session.commit()  # Get the brand ID
        is_new_product = True

    # Find or create size
    size = session.query(Size).filter_by(width=width, ratio=ratio, rim=rim).first()
    if not size:
        size = Size(width=width, ratio=ratio, rim=rim)
        session.add(size)
        session.commit()  # Get the size ID
        is_new_product = True

    # Create product
    if not is_new_product:
        raise ProductAlreadyExistsException(f"Product with brand '{brand_name}' and size '{width}/{ratio}/{rim}' already exists.")
    else:
        product = Product(
            brand_id=brand.id,
            size_id=size.id,
            price=price,
            quantity=quantity
        )
        session.add(product)
        session.commit()  # Get the product ID

    return product

def search_product_by_size(session: Session, width: int = None, ratio: int = None, rim: int = None):
    query = session.query(Product).join(Size, Product.size_id == Size.id)
    if width is not None:
        query = query.filter(Size.width == width)
    if ratio is not None:
        query = query.filter(Size.ratio == ratio)
    if rim is not None:
        query = query.filter(Size.rim == rim)
    return query.all()

def search_product_by_brand(session: Session, brand_name: str):
    query = session.query(Product).join(Brand, Product.brand_id == Brand.id).filter(Brand.name == brand_name)
    return query.all()

def search_product_by_size_json(session: Session, width: int = None, ratio: int = None, rim: int = None):
    products = search_product_by_size(session, width, ratio, rim)
    result = []
    for product in products:
        result.append(product.to_dict())
    return result

def search_product_by_brand_json(session: Session, brand_name: str):
    products = search_product_by_brand(session, brand_name)
    result = []
    for product in products:
        result.append(product.to_dict())
    return result

def get_all_products(session: Session):
    return session.query(Product).all()

def get_all_products_json(session: Session):
    products = get_all_products(session)
    return [product.to_dict() for product in products]

def get_product_by_id(session: Session, product_id: int) -> Product:
    product = session.query(Product).filter_by(id=product_id).first()
    if not product:
        raise ProductNotExistsException(f"Product with id '{product_id}' does not exist.")
    return product
def get_product_by_id_json(session: Session, product_id: int) -> dict:
    product = get_product_by_id(session, product_id)
    return product.to_dict()

def delete_product_by_name_and_size(session: Session, brand_name: str, width: int, ratio: int, rim: int) -> bool:
    brand = session.query(Brand).filter_by(name=brand_name).first()
    size = session.query(Size).filter_by(width=width, ratio=ratio, rim=rim).first()
    if not brand or not size:
        return False
    product = session.query(Product).filter_by(brand_id=brand.id, size_id=size.id).first()
    if not product:
        return False
    session.delete(product)
    session.commit()
    return True

def update_product_by_id(session: Session, product_id: int, new_brand_name: str, new_width: int, new_ratio: int, new_rim: int, new_quantity: int, new_price: float) -> Product:
    # Find the product by ID
    product = session.query(Product).filter_by(id=product_id).first()
    if not product:
        raise ProductNotExistsException(f"Product with id '{product_id}' does not exist.")

    # Find or create the new brand
    brand = session.query(Brand).filter_by(name=new_brand_name).first()
    if not brand:
        brand = Brand(name=new_brand_name)
        session.add(brand)
        session.commit()

    # Find or create the new size
    size = session.query(Size).filter_by(width=new_width, ratio=new_ratio, rim=new_rim).first()
    if not size:
        size = Size(width=new_width, ratio=new_ratio, rim=new_rim)
        session.add(size)
        session.commit()

    # Update product's price and quantity
    product.price = new_price
    product.quantity = new_quantity
    
    # Update product's brand and size
    product.brand_id = brand.id
    product.size_id = size.id

    session.commit()
    session.refresh(product)
    print(product.to_dict(), new_brand_name)
    return product


def get_all_employee_usernames(session: Session):
    employees = session.query(Employee).all()
    return [employee.user_name for employee in employees]

def get_all_employee_and_manager_usernames(session: Session):
    employees = session.query(Employee).all()
    managers = session.query(Manager).all()
    usernames = [employee.user_name for employee in employees] + [manager.user_name for manager in managers]
    return usernames

def get_all_employee_and_manager(session: Session):
    employees = session.query(Employee).all()
    managers = session.query(Manager).all()
    return employees + managers

def get_all_employee_and_manager_json(session: Session):
    users = get_all_employee_and_manager(session)
    return [user.to_dict() for user in users]



def get_all_customers(session: Session):
    return session.query(Customer).all()

def get_all_customers_json(session: Session):
    customers = get_all_customers(session)
    return [customer.to_dict() for customer in customers]

def get_customer_by_id(session: Session, customer_id: int) -> Customer:
    customer = session.query(Customer).filter_by(id=customer_id).first()
    return customer

def get_customer_by_id_json(session: Session, customer_id: int) -> dict:
    customer = get_customer_by_id(session, customer_id)
    if customer:
        return customer.to_dict()
    return None