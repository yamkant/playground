from sqlalchemy.orm import Session
from project.apps.database import orm, entity

def get_user(db: Session, user_id: int):
    return db.query(orm.User).filter(orm.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(orm.User).filter(orm.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(orm.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: entity.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = orm.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(orm.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: entity.ItemCreate, user_id: int):
    db_item = orm.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item