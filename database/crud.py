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

# create_new_user(session, 'admin', 'admin', '234', '1234', 'admin', 'admin', 'admin')