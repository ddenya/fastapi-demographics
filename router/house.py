from typing import List
from fastapi.responses import JSONResponse
from auth.oauth2 import check_assets_user_privileges, check_user_types, get_current_user
from models.person import DbPerson
from models.schemas import HouseDisplay, HouseBase, UserDisplay
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.db_connector import get_db
from db_crud import house as db_house

router = APIRouter(
    prefix='/house',
    tags=['house']
)

#Create house
@router.post('/', response_model=HouseDisplay, status_code=201, dependencies=[Depends(check_user_types(['admin', 'member']))])
def create_house(request: HouseBase, db: Session= Depends(get_db), current_user: UserDisplay = Depends(get_current_user)):
    check_assets_user_privileges(current_user, request.owner_ids, db)   
    return db_house.create_house(request, db)

#get specific house
@router.get('/{id}', response_model=HouseDisplay, dependencies=[Depends(check_user_types(['admin', 'member', 'auditor']))]) # get this part in comment line
def get_house(id: int, db: Session = Depends(get_db), current_user: UserDisplay = Depends(get_current_user)):
    house = db_house.get_house(id, db)
    if house is None:
        return JSONResponse(
        status_code=404,
        content={"message": f'House with id {id} not found'}
    )
    owners_id = []
    for owner in house.owners:
        person=db.query(DbPerson).filter(DbPerson.id == owner.id).first()
        owners_id.append(person.id)

    check_assets_user_privileges(current_user,owners_id,db)   
    return house

#get all houses
@router.get('/', response_model=List[HouseDisplay], dependencies=[Depends(check_user_types(['admin', 'member', 'auditor']))])
def get_all_houses(db: Session=Depends(get_db)):
    return db_house.get_all_houses(db)

#update house
@router.patch('/{id}', response_model=HouseDisplay, dependencies=[Depends(check_user_types(['admin', 'member']))])
def update_house(id: int, request: HouseBase, db: Session = Depends(get_db), current_user: UserDisplay = Depends(get_current_user)):
    house = db_house.get_house(id, db)
    if house is None:
        return JSONResponse(
        status_code=404,
        content={"message": f'House with id {id} not found'}
    )
    check_assets_user_privileges(current_user,request.owner_ids,db)

    updated_house =  db_house.update_house(id, request, db, current_user)
    if updated_house is None:
        return JSONResponse(
        status_code=404,
        content={"message": f'House with id {id} not found'},
    )
    return updated_house

# Delete house
@router.delete('/{id}', status_code=204, dependencies=[Depends(check_user_types('admin'))])
def delete_house(id: int, db:Session=Depends(get_db)):
  ret =  db_house.delete_house(id,db)
  if ret is None:
    return JSONResponse(
      status_code=404,
      content={"message": f'House with {id} not found'},
  )
  return ret

@router.post("/auto_add_houses")
def auto_add_houses(db: Session = Depends(get_db)):
    """
    THIS IS ONLY TO BE USED FOR TESTING PURPOSES
    """
    import json
 
    with open("Jsonfiles/housesexample.json", "r") as file:
        houses = json.load(file)
 
    for house in houses:
        db_house.create_house(db=db, request=HouseBase(**house))
    return {"message": "Houses added successfully"}