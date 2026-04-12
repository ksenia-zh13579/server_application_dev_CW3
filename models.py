from pydantic import BaseModel, Field, model_validator
from enum import Enum

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

# Task 7.1
class Permissions(str, Enum):
    READ_PRODUCTS = "read:products"
    WRITE_PRODUCTS = "write:products"
    DELETE_PRODUCTS = "delete:products"
    GET_PROTECTED_RESOURCE = "get:protected_resource"

class Role(BaseModel):
    name: str
    permissions: list[str]

class Product(BaseModel):
    name: str
    price: int = Field(ge=0)

class UserRegister(User):
    username: str
    password: str
    roles: list[str]

class UserWRoles(UserInDB):
    username: str
    hashed_password: str
    disabled: bool = False
    roles: list[str]
    permissions: set[str] = Field(default_factory=set)

    @model_validator(mode="after")
    def populate_permissions(self):
        from database import ROLES_REGISTRY

        all_permissions = set()
        for role_name in self.roles:
            if role_name in ROLES_REGISTRY:
                role = ROLES_REGISTRY[role_name]
                all_permissions.update(role.permissions)

        self.permissions = all_permissions
        return self
