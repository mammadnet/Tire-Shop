from .models import User,Employee,Admin,Manager,Order,Customer,Product,Size,Brand

from sqlalchemy.orm import Session, InstrumentedAttribute

from sqlalchemy import select, exists

from .connection import session

from utilities import hashing

def exist_check_user(by:InstrumentedAttribute, pat):
    subq = exists(User.national_number).where(User.national_number == pat).select()
    exist_check = session.execute(subq).scalar()
    return exist_check

def user_by_username_pass(session:Session, username:str, passwd:str):
    with session as db:
        
        query = select(User).where(User.user_name == username).where(User.hashed_passwd == hashing(passwd))
        user = db.execute(query).scalar()
        return user
    return None
    
    


def create_new_user(session: Session, name:str, lastname:str, phone:str, national_number:str, level_type:str, username:str, passwd:str) -> User:
    if level_type == 'admin':
        new_user = Admin(name=name, lastname=lastname, phone=phone, national_number=national_number, user_name=username)
    elif level_type == 'manager':
        new_user = Manager(name=name, lastname=lastname, phone=phone, national_number=national_number, user_name=username)
    elif level_type == 'employee':
        new_user = Employee(name=name, lastname=lastname, phone=phone, national_number=national_number, user_name=username)
    else:
        return None
    
    
    
    with session as db:
        exist_national_id_check = exist_check_user(User.national_number, national_number)
        exist_username_check = exist_check_user(User.user_name, username)
        
        if not exist_national_id_check and not exist_username_check:
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

