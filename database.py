import secrets
from fastapi import HTTPException, status, Depends

from models import UserInDB, Role, Permissions, Product, UserWRoles
from security import get_password_hash, get_username_from_token

# Task 6.1
'''
USER_DATA = [
    User(**{"username": "user1", "password": "pass1"}),
    User(**{"username": "user2", "password": "pass2"})
]

def get_user_from_db(username: str):
    for user in USER_DATA:
        if user.username == username:
            return user
    return None
'''

# Task 6.2
fake_users_db = [UserInDB(**{"username": "user1", "hashed_password": get_password_hash("pass1")}),
    UserInDB(**{"username": "user2", "hashed_password": get_password_hash("pass2")})
]

def get_user_from_db(username: str):
    for user in fake_users_db:
        if secrets.compare_digest(username, user.username):
            return user
    return None

# Task 7.1
ROLES_REGISTRY = {
    "admin": Role(
        name="admin",
        permissions=[
            Permissions.READ_PRODUCTS,
            Permissions.WRITE_PRODUCTS,
            Permissions.DELETE_PRODUCTS,
            Permissions.GET_PROTECTED_RESOURCE
        ]
    ),
    "user": Role(
        name="user",
        permissions=[
            Permissions.READ_PRODUCTS,
            Permissions.WRITE_PRODUCTS
        ]
    ),
    "guest": Role(
        name="guest",
        permissions=[
            Permissions.READ_PRODUCTS
        ]
    )
}

PRODUCTS_DATA = [
    Product(name="notebook", price=350), 
    Product(name="pen", price="135")
]

def get_product(product_name: str):
    for product in PRODUCTS_DATA:
        if product.name == product_name:
            return product
    return None

USERS_DATA = [
    UserWRoles(**{
        "username": "main_admin",
        "hashed_password": get_password_hash("adminpass"),
        "roles": ["admin"],
        "disabled": False,
    })
]

def get_user(username: str):
    for user in USERS_DATA:
        if secrets.compare_digest(username, user.username):
            return user
    return None

def get_user_from_token(username: str = Depends(get_username_from_token)):
    user = get_user(username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )
    return user