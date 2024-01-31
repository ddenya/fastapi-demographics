from typing import List
from fastapi.responses import JSONResponse
from models.schemas import UserBase, UserDisplay
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.db_connector import get_db
from db_crud import user as db_user

router = APIRouter(
  prefix='/user',
  tags=['user']
)

# Create
@router.post('/', response_model=UserDisplay)
def create_user(request: UserBase, db: Session=Depends(get_db)):
  return db_user.create_user(request, db)

# Read all users
@router.get('/',response_model=List[UserDisplay])
def get_all_users(db: Session=Depends(get_db)):
  return db_user.get_all_users(db)

# Read one user 
@router.get('/{id}', response_model=UserDisplay)
def get_user(id: int, db: Session=Depends(get_db)):
  ret = db_user.get_user(id,db)
  if ret is None:
    return JSONResponse(
        status_code=404,
        content={"message": f'User with {id} not found'},
    )
  return ret

# Update
@router.post('/{id}', response_model=UserDisplay)
def update_user(id: int, request: UserBase, db: Session=Depends(get_db)):
  return db_user.update_user(id, request, db)

# Delete
@router.delete('/{id}')
def delete_user(id: int, db:Session=Depends(get_db)):
  return db_user.delete_user(id,db)