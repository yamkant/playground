from fastapi import APIRouter, HTTPException
from apps.user import repository, schema
from apps.database.connection import SessionLocal

router = APIRouter(prefix="/users")

@router.get("/")
def read_users(skip: int = 0, limit: int = 100):
    db = SessionLocal()
    users = repository.get_users(db, skip=skip, limit=limit)
    return users


@router.post("/")
def create_user(user: schema.UserCreate):
    db = SessionLocal()
    db_user = repository.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return repository.create_users(db=db, user=user)
