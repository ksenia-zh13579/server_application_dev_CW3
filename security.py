from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordBearer
from secrets import compare_digest
import jwt
import datetime

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
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_jwt_token(data: dict):
    to_encode = data.copy()
    expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=config.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(data, config.secret_key, algorithm=config.algorithm)

def get_username_from_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, config.secret_key, algorithms=[config.algorithm])
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
    
