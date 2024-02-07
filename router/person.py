from typing import List

from fastapi.responses import JSONResponse
from models.schemas import PersonBase, PersonDisplay
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.db_connector import get_db
from db_crud import person as db_person

router = APIRouter(
    prefix='/person',
    tags=['person']
)

#Create
@router.post('/', response_model=PersonDisplay, status_code=201)
def create_person(request: PersonBase, db: Session= Depends(get_db)):
    return db_person.create_person(request, db)

# Get 
@router.get('/{id}', response_model=PersonDisplay, status_code=200)
def get_person(id: int, db: Session = Depends(get_db)):
    ret = db_person.get_person(id, db)
    if ret is None:
        return JSONResponse(
        status_code=404,
        content={"message": f'Person with id {id} not found'},
    )
    return ret

# Get all
@router.get('/', response_model=List[PersonDisplay], status_code=200)
def get_all_people(db: Session = Depends(get_db)):
    return db_person.get_all_people(db)

# Patch : 200 code https://www.rfc-editor.org/rfc/rfc5789.txt (2.1)
@router.patch('/{id}', response_model=PersonDisplay, status_code=200)
def update_person(id: int, request: PersonBase, db: Session = Depends(get_db)):
    ret = db_person.update_person(id, request, db)
    if ret is None:
        return JSONResponse(
        status_code=404,
        content={"message": f'Person with id {id} not found'},
    )
    return ret

# Delete person
@router.delete('/{id}', status_code=204)
def delete_person(id: int, db:Session=Depends(get_db)):
  ret =  db_person.delete_person(id,db)
  if ret is None:
    return JSONResponse(
      status_code=404,
      content={"message": f'Person with {id} not found'},
  )
  return ret
