from fastapi import FastAPI, Depends, status, HTTPException, Response, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

from models import User, UserInDB
from database import fake_users_db, get_user_from_db
from security import security, verify_password, get_password_hash, verify_docs_credentials, create_jwt_token, get_user_from_token
import config

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

# Task 6.1
'''
def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
    user = get_user_from_db(credentials.username)
    if user is None or user.password != credentials.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials", headers={"WWW-Authenticate": "Basic"})
    return user

@app.get('/login')
def check_login(user: User = Depends(authenticate_user)):
    return ({'message' : 'You got my secret, welcome'})
'''

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

@app.post('/register')
def register(user : User):
    userindb = UserInDB(username=user.username, hashed_password=get_password_hash(user.password))
    fake_users_db.append(userindb)
    return {"message": "User successfully added"}
    
@app.get('/login')
def check_login(response : Response, user: UserInDB = Depends(auth_user)):
    response.headers["WWW-Authenticate"] = "Basic"
    return {"message": f"Welcome, {user.username}!"}
    
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

@app.get('/docs', include_in_schema=False)
def get_docs(user : User = Depends(auth_docs)):
    return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")

@app.get('/openapi.json', include_in_schema=False)
def get_openapi_schema(user : User = Depends(auth_docs)):
    return get_openapi(title=app.title, version=app.version, routes=app.routes)

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

@app.post("/login")
def post_login(token : str = Depends(auth_user_jwt)):
    try:
        return {"token": token}
    except HTTPException as error:
        return {"error": error.detail}
    
@app.get("/protected_resource")
def get_protected_resource(request: Request):
    token = request.headers.get("Authorization").split(" ")[1]
    username = get_user_from_token(token)
    user = get_user_from_db(username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid credentials"
        )
    return {"message": f"Welcome to the protected resource, {user.username}!"}

