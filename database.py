from models import UserInDB
from security import get_password_hash
import secrets

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
    UserInDB(**{"username": "user2", "hashed_password": get_password_hash("pass2")})]

def get_user_from_db(username: str):
    for user in fake_users_db:
        if secrets.compare_digest(username, user.username):
            return user
    return None