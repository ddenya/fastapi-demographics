from typing import List
from fastapi.responses import JSONResponse
from auth.oauth2 import check_user_privileges, check_user_types, get_current_user
from models.schemas import PersonBase, PersonDisplay, UserDisplay
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.db_connector import get_db
from db_crud import person as db_person

router = APIRouter(
    prefix='/person',
    tags=['person']
)

#Create
@router.post('/', response_model=PersonDisplay, status_code=201, dependencies=[Depends(check_user_types(['admin']))])
def create_person(request: PersonBase, db: Session= Depends(get_db)): #, current_user: UserDisplay = Depends(get_current_user)):
    #check_user_privileges(current_user, request.user_id)       
    return db_person.create_person(request, db)

# Get 
@router.get('/{id}', response_model=PersonDisplay, status_code=200, dependencies=[Depends(check_user_types(['admin', 'member', 'auditor']))])
def get_person(id: int, db: Session = Depends(get_db), current_user: UserDisplay = Depends(get_current_user)):
    ret = db_person.get_person(id, db)
    if ret is None:
        return JSONResponse(
        status_code=404,
        content={"message": f'Person with id {id} not found'},
    )

    check_user_privileges(current_user, ret.user_id)   
    return ret

# Get all
@router.get('/', response_model=List[PersonDisplay], status_code=200, dependencies=[Depends(check_user_types(['admin', 'auditor', 'member']))])
def get_all_people(db: Session = Depends(get_db)):
    return db_person.get_all_people(db)

# Patch : 200 code https://www.rfc-editor.org/rfc/rfc5789.txt (2.1)
@router.patch('/{id}', response_model=PersonDisplay, status_code=200, dependencies=[Depends(check_user_types(['admin', 'member']))])
def update_person(id: int, request: PersonBase, db: Session = Depends(get_db), current_user: UserDisplay = Depends(get_current_user)):
    ##Refactor: If checking privileges after if condition then it means that update operation has already finished
    ##But if checking is here then it meands that if even person doesnot exist its returns 403 prilivileges
    #print("current_user_id: " + str(current_user.id))
    #print("request.user_id: " + str(request.user_id))
    person = db_person.get_person(id, db)
    if person is None:
        return JSONResponse(
        status_code=404,
        content={"message": f'Person with id {id} not found okan'},
    )

    check_user_privileges(current_user, person.user_id) 
    ret = db_person.update_person(id, request, db)
    if ret is None:
        return JSONResponse(
        status_code=404,
        content={"message": f'Person with id {id} not found'},
    )    
    return ret

# Delete person
@router.delete('/{id}', status_code=204, dependencies=[Depends(check_user_types('admin'))])
def delete_person(id: int, db:Session=Depends(get_db)):
  ret =  db_person.delete_person(id,db)
  if ret is None:
    return JSONResponse(
      status_code=404,
      content={"message": f'Person with {id} not found'},
  )
  return ret
