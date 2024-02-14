from typing import List
from fastapi.responses import JSONResponse
from auth.oauth2 import  check_user_types, get_current_user, check_assets_user_privileges
from models.person import DbPerson
from models.schemas import CarDisplay, CarBase, UserDisplay
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.db_connector import get_db
from db_crud import car as db_car

router = APIRouter(
    prefix='/cars',
    tags=['cars']
)

#Create car
@router.post('/', response_model=CarDisplay, status_code=201, dependencies=[Depends(check_user_types(['admin', 'member']))])
def create_car(request: CarBase, db: Session= Depends(get_db), current_user: UserDisplay = Depends(get_current_user)):
    check_assets_user_privileges(current_user, request.owner_ids, db)   
    return db_car.create_car(request, db)

# Get specific car
@router.get('/{id}', response_model=CarDisplay, status_code=200, dependencies=[Depends(check_user_types(['admin', 'member', 'auditor']))]) # get this part in comment line
def get_car(id: int, db: Session = Depends(get_db),current_user: UserDisplay = Depends(get_current_user)):    
    car = db_car.get_car(id, db)
    if car is None:
        return JSONResponse(
        status_code=404,
        content={"message": f'Car with id {id} not found'},
    )
    owners_id = []
    for owner in car.owners:
        person=db.query(DbPerson).filter(DbPerson.id == owner.id).first()
        owners_id.append(person.id)

    check_assets_user_privileges(current_user,owners_id,db)  
    return car

# Get all cars
@router.get('/', response_model=List[CarDisplay], status_code=200, dependencies=[Depends(check_user_types(['admin', 'auditor']))])
def get_all_cars(db: Session=Depends(get_db)):
    return db_car.get_all_cars(db)

# Update cars
@router.patch('/{id}', response_model=CarDisplay, status_code=200, dependencies=[Depends(check_user_types(['admin', 'member']))])
def update_car(id: int, request: CarBase, db: Session = Depends(get_db), current_user: UserDisplay = Depends(get_current_user)):
    car = db_car.get_car(id, db)
    if car is None:
        return JSONResponse(
        status_code=404,
        content={"message": f'Car with id {id} not found'}
    )
    check_assets_user_privileges(current_user,request.owner_ids,db)
    
    updated_car =  db_car.update_car(id, request, db,current_user)
    if updated_car is None:
        return JSONResponse(
        status_code=404,
        content={"message": f'Car with id {id} not found'},
    )
    return updated_car

# Delete car
@router.delete('/{id}', status_code=204, dependencies=[Depends(check_user_types('admin'))])
def delete_car(id: int, db:Session=Depends(get_db)):
  ret =  db_car.delete_car(id,db)
  if ret is None:
    return JSONResponse(
      status_code=404,
      content={"message": f'Car with {id} not found'},
  )
  return ret


@router.post("/cars/auto_add_cars")
def auto_add_cars(db: Session = Depends(get_db)):
    """
    THIS IS ONLY TO BE USED FOR TESTING PURPOSES
    """
    import json
 
    with open("Jsonfiles/carsexamplefiles.json", "r") as file:
        cars = json.load(file)
 
    for car in cars:
        db_car.create_car(db=db, request=CarBase(**car))
    
    return {"message": "Cars added successfully"}