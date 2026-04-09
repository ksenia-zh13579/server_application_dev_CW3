from pydantic import BaseModel

# Task 6.1 - 6.2
class UserBase(BaseModel):
    username: str

# Task 6.1
class User(UserBase):
    username: str
    password: str

class UserInDB(UserBase):
    username: str
    hashed_password: str