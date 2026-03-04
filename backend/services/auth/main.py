from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from backend.shared.security import create_access_token, hash_password, verify_password

app = FastAPI(title="Auth Service")
USERS = {}


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    role: str = "student"


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


@app.post("/register")
async def register(req: RegisterRequest):
    if req.email in USERS:
        raise HTTPException(status_code=409, detail="User already exists")
    USERS[req.email] = {"password_hash": hash_password(req.password), "role": req.role}
    return {"status": "created"}


@app.post("/login")
async def login(req: LoginRequest):
    user = USERS.get(req.email)
    if not user or not verify_password(req.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(req.email)
    return {"access_token": token, "token_type": "bearer"}
