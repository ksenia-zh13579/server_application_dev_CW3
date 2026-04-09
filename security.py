from passlib.context import CryptContext
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from secrets import compare_digest
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