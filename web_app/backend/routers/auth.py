from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from jose import jwt
from ..dependencies import fake_users_db, SECRET_KEY, ALGORITHM, User, get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])

class UserLogin(BaseModel):
    username: str
    password: str

class UserRegister(BaseModel):
    username: str
    password: str

@router.post("/register")
async def register(user: UserRegister):
    if user.username in fake_users_db:
        raise HTTPException(status_code=400, detail="Username exists")
    user_dict = {"id": len(fake_users_db) + 1, "username": user.username, "password": user.password}  # Prod: hash pw
    fake_users_db[user.username] = user_dict
    token = jwt.encode({"sub": user.username}, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}

@router.post("/login")
async def login(user: UserLogin):
    db_user = fake_users_db.get(user.username)
    if not db_user or db_user["password"] != user.password:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = jwt.encode({"sub": user.username}, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me")
async def me(current_user: User = Depends(get_current_user)):
    return current_user

