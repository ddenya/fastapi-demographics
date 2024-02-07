from typing import List
from fastapi.responses import JSONResponse
from models.schemas import CarDisplay, CarBase
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.db_connector import get_db
from db_crud import car as db_car

router = APIRouter(
    prefix='/car',
    tags=['car']
)

#Create car
@router.post('/', response_model=CarDisplay, status_code=201)
def create_car(request: CarBase, db: Session= Depends(get_db)):
    return db_car.create_car(request, db)

# Get specific car
@router.get('/{id}', response_model=CarDisplay, status_code=200) # get this part in comment line
def get_car(id: int, db: Session = Depends(get_db)):
    ret = db_car.get_car(id, db)
    if ret is None:
        return JSONResponse(
        status_code=404,
        content={"message": f'Car with id {id} not found'},
    )

# Get all cars
@router.get('/', response_model=List[CarDisplay], status_code=200)
def get_all_cars(db: Session=Depends(get_db)):
    return db_car.get_all_cars(db)

# Update cars
@router.patch('/{id}', response_model=CarDisplay, status_code=200)
def update_car(id: int, request: CarBase, db: Session = Depends(get_db)):
    ret =  db_car.update_car(id, request, db)
    if ret is None:
        return JSONResponse(
        status_code=404,
        content={"message": f'Car with id {id} not found'},
    )
    return ret

# Delete car
@router.delete('/{id}', status_code=204)
def delete_car(id: int, db:Session=Depends(get_db)):
  ret =  db_car.delete_car(id,db)
  if ret is None:
    return JSONResponse(
      status_code=404,
      content={"message": f'Car with {id} not found'},
  )
  return ret