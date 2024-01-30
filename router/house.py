from typing import List
from db.schemas import HouseDisplay, HouseBase
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.db_connector import get_db
from db_crud import house as db_house

router = APIRouter(
    prefix='/house',
    tags=['house']
)

#Create house
@router.post('/', response_model=HouseDisplay)
def create_house(request: HouseBase, db: Session= Depends(get_db)):
    return db_house.create_house(request, db)

#get specific house
@router.get('/{id}', response_model=HouseDisplay) # get this part in comment line
def get_house(id: int, db: Session = Depends(get_db)):
    return db_house.get_house(id, db)

@router.get('/', response_model=List[HouseDisplay])
def get_all_houses(db: Session=Depends(get_db)):
    return db_house.get_all_houses(db)

#update house
@router.post('/{id}', response_model=HouseDisplay)
def update_house(id: int, request: HouseBase, db: Session = Depends(get_db)):
    return db_house.update_house(id, request, db)

# Delete user