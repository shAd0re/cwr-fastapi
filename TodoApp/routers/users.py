from typing import Annotated
import uvicorn
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path, Query
from starlette import status
from pydantic import BaseModel, Field
from ..models import Todos, Users
from ..database import SessionLocal
from .auth import get_current_user
from passlib.context import CryptContext


router = APIRouter(
    prefix='/users',
    tags=['users']
)


#provides a session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

@router.get('/',status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication failed.')
    user_profile = db.query(Users).filter(Users.id == user.get('id')).first()
    return user_profile

class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length= 6)

@router.put('/password',status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency, db: db_dependency,
                          user_verification: UserVerification):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication failed.')
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail= 'Old password entered is incorrect.')

    new_hashed_password = bcrypt_context.hash(user_verification.new_password)
    user_model.hashed_password = new_hashed_password
    db.add(user_model)
    db.commit()

@router.put('/phone_number/{phone_number}',status_code=status.HTTP_204_NO_CONTENT)
async def update_phone_number(user: user_dependency, db: db_dependency, phone_number: str= Path(min_length=10)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication failed.')
    user_profile = db.query(Users).filter(Users.id == user.get('id')).first()
    user_profile.phone_number = phone_number
    db.add(user_profile)
    db.commit()


# @router.put('/password',status_code=status.HTTP_204_NO_CONTENT)
# async def change_password(user: user_dependency, db: db_dependency, new_password: str= Query(min_length=7)):
#     if user is None:
#         raise HTTPException(status_code=401, detail='Authentication failed.')
#     user_profile = db.query(Users).filter(Users.id == user.get('id')).first()
#     new_hashed_password = bcrypt_context.hash(new_password)
#     # old = db.query(Users.hashed_password)
#     user_profile.hashed_password = new_hashed_password
#     db.add(user_profile)
#     db.commit()

