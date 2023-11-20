from datetime import timedelta, datetime

from fastapi import APIRouter, Depends, Body, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from jose import jwt

from user import repository, schema
from database import orm, connection

router = APIRouter(prefix="/users")

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
SECRET_KEY = "4ab2fce7a6bd79e1c014396315ed322dd6edb1c5d975c6b74a2904135172c03c"
ALGORITHM = "HS256"

@router.get("/")
def get_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(connection.get_db),
):
    users = repository.get_users(db, skip=skip, limit=limit)
    return users


@router.post(
    "/",
    status_code=status.HTTP_204_NO_CONTENT
)
def post_users(
    user: schema.UserCreate,
    db: Session = Depends(connection.get_db),
):
    db_user = repository.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user =  repository.create_users(db=db, user=user)

@router.post(
    "/login",
    response_model=schema.Token,
)
def login_for_access_token(
    login_user: schema.LoginUser,
    db: Session = Depends(connection.get_db)
):

    # check user and password
    user = repository.get_user_by_email(db, login_user.email)
    if not user or not repository.pwd_context.verify(login_user.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # make access token
    data = {
        "sub": user.email,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "email": user.email
    }