from passlib.context import CryptContext
from fastapi import HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from secrets import compare_digest
import jwt

import config

# Tasks 6.1 - 6.3
security = HTTPBasic()

# Task 6.2
cryptcontext = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return cryptcontext.verify(plain_password, hashed_password)

def get_password_hash(password):
    return cryptcontext.hash(password)

# Task 6.3
def verify_docs_credentials(credentials: HTTPBasicCredentials):
    return compare_digest(credentials.username, config.docs_user) and compare_digest(credentials.password, config.docs_password)

# Task 6.4
SECRET_KEY = "supermegaultrasecret"
ALGORITHM = "HS256"

def create_jwt_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def get_user_from_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Expired token"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid token"
        )