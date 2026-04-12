from fastapi import Depends, status, HTTPException
from fastapi.security import HTTPBasicCredentials

from models import User
from database import get_user_from_db
from security import security, verify_password, verify_docs_credentials, create_jwt_token
import config

# Task 6.1
def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
    user = get_user_from_db(credentials.username)
    if user is None or user.password != credentials.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials", headers={"WWW-Authenticate": "Basic"})
    return user

# Task 6.2
def auth_user(credentials: HTTPBasicCredentials = Depends(security)):
    user = get_user_from_db(credentials.username)
    if user is None or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid credentials", 
            headers={"WWW-Authenticate": "Basic"}
        )
    return user

# Task 6.3
def auth_docs(credentials: HTTPBasicCredentials = Depends(security)):
    if config.mode == 'PROD':
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Documentation access is restricted in production mode"
        )
    if config.mode != 'DEV':
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Undefined mode"
        )
    if not verify_docs_credentials(credentials):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid credentials", 
            headers={"WWW-Authenticate": "Basic"}
        )
    return User(username=credentials.username, password=credentials.password)

# Task 6.4
def auth_user_jwt(user: User):
    userDB = get_user_from_db(user.username)
    if userDB is None or not verify_password(user.password, userDB.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid credentials"
        )
    token = create_jwt_token({"sub": user.username})
    return token

