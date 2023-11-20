from sqlalchemy.orm import Session
from database import orm
from user import schema
from starlette import status
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user(db: Session, user_id: int):
    return db.query(orm.User).filter(orm.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(orm.User).filter(orm.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(orm.User).offset(skip).limit(limit).all()


def create_users(db: Session, user: schema.UserCreate):
    password = pwd_context.hash(user.password)
    db_user = orm.User(email=user.email, hashed_password=password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
