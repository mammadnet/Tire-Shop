from .models import User, Admin, Manager, Employee



def is_admin(user:User):
    return isinstance(user, Admin)

def is_manager(user:User):
    return isinstance(user, Manager)

def is_employee(user:User):
    return isinstance(user, Employee)