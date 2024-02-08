import traceback
from sqlalchemy.orm.session import Session
from models.house import DbHouse
from models.schemas import HouseBase

'''
This function creates object even if only part of fields is provided
It will break if fields of model are not strings!
'''
def create_house(request: HouseBase, db: Session):

  new_house = DbHouse()

  # filling values of fields with field names in case value of field is not provided
  request_dict = request.dict()
  for field, value in request_dict.items():
    if value is not None:
      setattr(new_house, field, value)
    else:
      setattr(new_house, field, field)

  if request.owner_ids:
    new_house.add_owners_by_ids(request.owner_ids, session = db)
  
  db.add(new_house)
  db.commit()
  db.refresh(new_house)

  return new_house

def get_all_houses(db: Session):
  try:
    return db.query(DbHouse).all()
  except Exception as e:
    return None

def get_house(id: int, db: Session):
  try:
    return db.query(DbHouse).filter(DbHouse.id == id).first()
  # Exception on database level
  except Exception as e:
    return None

def update_house(id: int, request: HouseBase, db: Session):
  try:
    # TODO: conversion to str if we pass int? "424242"?
    house = get_house(id, db)
    if house is None:
      return None
    model_dump = request.dict(exclude_unset=True)
    # Update only the provided fields in the reques
    for field, value in model_dump.items():
      setattr(house, field, value)
    # Check if owner_ids are present in the request before calling the method
    if "owner_ids" in model_dump:
      house.add_owners_by_ids(request.owner_ids, session=db)

    db.commit()
    return house
  except Exception as e:
    return None 

def delete_house(id: int, db: Session):
  try:
    house = get_house(id, db)
    db.delete(house)
    db.commit()
    return True
  except Exception as e:
    return None 