from models import User

USER_DATA = [
    User(**{"username": "user1", "password": "pass1"}),
    User(**{"username": "user2", "password": "pass2"})
]

def get_user_from_db(username: str):
    for user in USER_DATA:
        if user.username == username:
            return user
    return None