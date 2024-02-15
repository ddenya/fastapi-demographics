from typing import List
from fastapi.responses import JSONResponse
from models.schemas import UserBase, UserDisplay
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.db_connector import get_db
from db_crud import user as db_user
from auth.oauth2 import check_user_operations_privileges, check_user_types, get_current_user

router = APIRouter(
  prefix='/users',
  tags=['Users']
)

# Create
@router.post('/', response_model=UserDisplay, status_code=201)
def create_user(request: UserBase, db: Session=Depends(get_db)):
  return db_user.create_user(request, db)

# Read all users
@router.get('/',response_model=List[UserDisplay], status_code=200, dependencies=[Depends(check_user_types(['admin', 'auditor']))])
def get_all_users(db: Session=Depends(get_db)):
  return db_user.get_all_users(db)


# Read one user 
@router.get('/{id}', response_model=UserDisplay, status_code=200, dependencies=[Depends(check_user_types(['admin', 'member', 'auditor']))])
def get_user(id: int, db: Session=Depends(get_db),  current_user: UserDisplay = Depends(get_current_user)):

  check_user_operations_privileges(current_user, id) 

  ret = db_user.get_user(id,db)
  if ret is None:
    return JSONResponse(
        status_code=404,
        content={"message": f'User with {id} not found'},
    )
  return ret


# Update
@router.patch('/{id}', response_model=UserDisplay, status_code=200, dependencies=[Depends(check_user_types(['admin', 'member']))])
def update_user(id: int, request: UserBase, db: Session=Depends(get_db),  current_user: UserDisplay = Depends(get_current_user)):
  
  check_user_operations_privileges(current_user, id) 
 
  user = db_user.update_user(id, request, db)
  if user is None:
   return JSONResponse(
      status_code=404,
      content={"message": f'User with {id} not found'},
  )
  return user


# Delete
@router.delete('/{id}', status_code=204, dependencies=[Depends(check_user_types('admin'))])
def delete_user(id: int, db:Session=Depends(get_db)):
  ret =  db_user.delete_user(id,db)
  if ret is None:
    return JSONResponse(
      status_code=404,
      content={"message": f'User with {id} not found'},
  )
  return ret