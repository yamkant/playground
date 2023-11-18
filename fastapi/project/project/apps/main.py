from fastapi import Depends, FastAPI, HTTPException, Header
from sqlalchemy.orm import Session

from .database import entity, repository
from .database.connection import SessionLocal, engine
from .database.orm import Base
from typing import Annotated

Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def read_main():
    return {"msg": "Hello World"}

@app.post("/users/", response_model=entity.User)
def create_user(user: entity.UserCreate, db: Session = Depends(get_db)):
    db_user = repository.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return repository.create_user(db=db, user=user)


@app.get("/users/", response_model=list[entity.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = repository.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=entity.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = repository.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=entity.Item)
def create_item_for_user(
    user_id: int, item: entity.ItemCreate, db: Session = Depends(get_db)
):
    return repository.create_user_item(db=db, item=item, user_id=user_id)


fake_secret_token = "coneofsilence"
fake_db = {
    "foo": {"id": "foo", "title": "Foo", "description": "There goes my hero"},
    "bar": {"id": "bar", "title": "Bar", "description": "The bartenders"},
}

@app.get("/items/{item_id}", response_model=entity.ItemBase)
async def read_main(item_id: str, x_token: Annotated[str, Header()]):
    if x_token != fake_secret_token:
        raise HTTPException(status_code=400, detail="Invalid X-Token header")
    if item_id not in fake_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return fake_db[item_id]

@app.post("/items/", response_model=entity.ItemBase)
async def create_item(item: entity.ItemCreate, x_token: Annotated[str, Header()]):
    if x_token != fake_secret_token:
        raise HTTPException(status_code=400, detail="Invalid X-Token header")
    if item.id in fake_db:
        raise HTTPException(status_code=400, detail="Item already exists")
    fake_db[item.id] = item
    return item