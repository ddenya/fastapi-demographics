from typing import List
from db.schemas import HouseDisplay, HouseBase
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from db import db_house

router = APIRouter(
    prefix='/house',
    tags=['house']
)

#Create house
@router.post('/', response_model=HouseDisplay)
def create_house(request: HouseBase, db: Session= Depends(get_db)):
    return db_house.create_house(db, request)

#get specific house
@router.get('/{id}', response_model=HouseDisplay) # get this part in comment line
def get_house(id: int, db: Session = Depends(get_db)):
    return{
      'data' : db_house.get_house(db, id)
    }

#update house
@router.post('/{id}/update')
def update_house(id: int, request: HouseBase, db: Session = Depends(get_db)):
    return db_house.update_house(db,id,request)

# Delete user
