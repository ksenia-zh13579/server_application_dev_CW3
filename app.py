from fastapi import FastAPI, Depends, status, HTTPException, Response, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from pyrate_limiter import Duration, Limiter, Rate
from fastapi_limiter.depends import RateLimiter

from models import User, UserInDB, UserWRoles, UserRegister, Permissions, Product
from database import fake_users_db, get_user_from_db, get_user, USERS_DATA, PRODUCTS_DATA, get_product, get_user_from_token
from security import security, verify_password, get_password_hash, verify_docs_credentials, create_jwt_token, get_username_from_token
from auth import authenticate_user, auth_user, auth_docs, auth_user_jwt
from rbac import PermissionChecker

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

# Task 6.1
'''
@app.get('/login')
def check_login(user: User = Depends(authenticate_user)):
    return ({'message' : 'You got my secret, welcome'})
'''

# Task 6.2
'''
@app.post('/register')
def register(user : User):
    userindb = UserInDB(username=user.username, hashed_password=get_password_hash(user.password))
    fake_users_db.append(userindb)
    return {"message": "User successfully added"} 

@app.get('/login')
def check_login(response : Response, user: UserInDB = Depends(auth_user)):
    response.headers["WWW-Authenticate"] = "Basic"
    return {"message": f"Welcome, {user.username}!"}
'''

# Task 6.3
@app.get('/docs', include_in_schema=False)
def get_docs(user : User = Depends(auth_docs)):
    return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")

@app.get('/openapi.json', include_in_schema=False)
def get_openapi_schema(user : User = Depends(auth_docs)):
    return get_openapi(title=app.title, version=app.version, routes=app.routes)

# Task 6.4
'''
@app.post("/login")
def post_login(token : str = Depends(auth_user_jwt)):
    try:
        return {"access_token": token}
    except HTTPException as error:
        return {"error": error.detail}
    
@app.get("/protected_resource")
def get_protected_resource(request: Request):
    token = request.headers.get("Authorization").split(" ")[1]
    username = get_username_from_token(token)
    user = get_user_from_db(username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid credentials"
        )
    return {"message": f"Welcome to the protected resource, {user.username}!"}
'''

# Task 6.5
'''
@app.post(
    '/register',
    dependencies=[Depends(RateLimiter(limiter=Limiter(Rate(1, Duration.MINUTE))))]
)
def register(response : Response, user : User):
    if get_user_from_db(user.username) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail="User already exists"
        )
    userindb = UserInDB(username=user.username, hashed_password=get_password_hash(user.password))
    fake_users_db.append(userindb)
    response.status_code = 201
    return {"message": "New user created"}

@app.post(
    "/login",
    dependencies=[Depends(RateLimiter(limiter=Limiter(Rate(5, Duration.MINUTE))))]
)
def post_login(data: User):
    user = get_user_from_db(data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )
    if not verify_password(data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Authorization failed"
        )
    access_token = create_jwt_token({"sub": user.username})
    return {"access_token": access_token}
'''

# Task 7.1
@app.post('/register')
def post_register(response : Response, user : UserRegister):
    if get_user(user.username) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail="User already exists"
        )
    userwroles = UserWRoles(username=user.username, hashed_password=get_password_hash(user.password), roles=user.roles)
    USERS_DATA.append(userwroles)
    response.status_code = 201
    return {"message": "New user created"}

@app.post("/login")
def post_login(data: User):
    user = get_user(data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )
    if not verify_password(data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Authorization failed"
        )
    access_token = create_jwt_token({"sub": user.username})
    return {"access_token": access_token}

@app.get("/protected_resource")
@PermissionChecker([Permissions.GET_PROTECTED_RESOURCE])
def get_protected_resource(current_user: UserWRoles = Depends(get_user_from_token)):
    return {"message": f"Hello, {current_user.username}! This is a protected resource only for admins."}

@app.get("/products")
@PermissionChecker([Permissions.READ_PRODUCTS])
def get_products(current_user: UserWRoles = Depends(get_user_from_token)):
    return {"products": [product.model_dump_json() for product in PRODUCTS_DATA]}

@app.post("/products")
@PermissionChecker([Permissions.WRITE_PRODUCTS])
def post_products(response : Response, new_product: Product, current_user: UserWRoles = Depends(get_user_from_token)):
    existing_product = get_product(new_product.name)
    if existing_product is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail="Product already exists"
        )
    PRODUCTS_DATA.append(new_product)
    response.status_code = 201
    return {"message": "New product successfully added"}

@app.delete("/products/{product_name}")
@PermissionChecker([Permissions.DELETE_PRODUCTS])
def delete_product(product_name: str, current_user: UserWRoles = Depends(get_user_from_token)):
    deleted_product = get_product(product_name)
    if deleted_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Product Not Found"
        )
    PRODUCTS_DATA[:] = [product for product in PRODUCTS_DATA if product.name != product_name]
    return {"deleted product": deleted_product.model_dump_json()}

