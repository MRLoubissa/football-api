
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.database import get_connection
from app.security import hash_password, verify_password
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter(prefix="/auth", tags=["Auth"])

SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login-swagger")


# -------------------------
# MODELS
# -------------------------
class UserCreate(BaseModel):
    username: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


# -------------------------
# REGISTER
# -------------------------
@router.post("/register")
def register(user: UserCreate):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        hashed_pw = hash_password(user.password)

        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (user.username, hashed_pw)
        )

        conn.commit()
        return {"message": "User created successfully"}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    finally:
        conn.close()


# -------------------------
# LOGIN (JSON)
# -------------------------
@router.post("/login")
def login(user: UserLogin):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, password FROM users WHERE username = ?",
        (user.username,)
    )

    db_user = cursor.fetchone()
    conn.close()

    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    user_id, hashed_password = db_user

    if not verify_password(user.password, hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = jwt.encode(
        {"user_id": user_id},
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return {"access_token": token}


# -------------------------
# LOGIN POUR SWAGGER 
# -------------------------
@router.post("/login-swagger")
def login_swagger(form_data: OAuth2PasswordRequestForm = Depends()):
    return login(UserLogin(
        username=form_data.username,
        password=form_data.password
    ))


# -------------------------
# PROTECTION JWT
# -------------------------
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        return user_id

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    