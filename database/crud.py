from models import User,Employee,Admin,Manager,Order,Customer,Product,Size,Brand

from sqlalchemy.orm import Session, InstrumentedAttribute

from sqlalchemy import select, exists

from connection import session

def exist_chek_user(by:InstrumentedAttribute, pat):
    subq = exists(User.national_number).where(User.national_number == pat).select()
    exist_check = session.execute(subq).scalar()
    return exist_check
    


def create_new_user(session: Session, name:str, lastname:str, phone:str, national_number:str, level_type:str) -> User:
    if level_type == 'admin':
        new_user = Admin(name=name, lastname=lastname, phone=phone, national_number=national_number)
    elif level_type == 'manager':
        new_user = Manager(name=name, lastname=lastname, phone=phone, national_number=national_number)
    elif level_type == 'employee':
        new_user = Employee(name=name, lastname=lastname, phone=phone, national_number=national_number)
    else:
        return None
    
    
    
    with session as db:
        exist_check = exist_chek_user(User.national_number, national_number)
        
        if not exist_check:
            db.add(new_user)
            db.commit()
            
    # TODO rais an error that the national code already exist
    return None
        


