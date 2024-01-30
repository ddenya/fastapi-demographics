from typing import List
from db.schemas import PersonBase, PersonDisplay
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.db_connector import get_db
from db_crud import person as db_person

router = APIRouter(
    prefix='/person',
    tags=['person']
)

#Create
@router.post('/', response_model=PersonDisplay)
def create_person(request: PersonBase, db: Session= Depends(get_db)):
    return db_person.create_person(request, db)

# Get 
@router.get('/{id}', response_model=PersonDisplay)
def get_person(id: int, db: Session = Depends(get_db)):
    return db_person.get_person(id, db)

# Update
@router.post('/{id}', response_model=PersonDisplay)
def update_person(id: int, request: PersonBase, db: Session = Depends(get_db)):
    return db_person.update_person(id, request, db)

# Delete user
