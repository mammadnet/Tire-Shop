from .models import User,Employee,Admin,Manager,Order,Customer,Product,Size,Brand

from sqlalchemy.orm import Session, InstrumentedAttribute

from sqlalchemy import select, exists

from .connection import session

from utilities import hashing

from .Exeptions import NationalNumberAlreadyExistsException, UsernameAlreadyExistsException, UsernameNotExistsException

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


def create_product(session: Session, brand_name: str, width: int, ratio: int, rim: int) -> Product:

    # Find or create brand
    brand = session.query(Brand).filter_by(name=brand_name).first()
    if not brand:
        brand = Brand(name=brand_name)
        session.add(brand)
        session.commit()  # Get the brand ID

    # Find or create size
    size = session.query(Size).filter_by(width=width, ratio=ratio, rim=rim).first()
    if not size:
        size = Size(width=width, ratio=ratio, rim=rim)
        session.add(size)
        session.commit()  # Get the size ID

    # Create product
    product = Product(
        product_id=brand.id,
        size_id=size.id
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
# create_new_user(session, 'admin', 'admin', '234', '1234', 'admin', 'admin', 'admin')