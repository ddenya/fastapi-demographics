import traceback
from sqlalchemy.orm.session import Session
from models.house import DbHouse
from models.schemas import HouseBase, UserDisplay

def create_house(request: HouseBase, db: Session):
  new_house = DbHouse(
    city = request.city,
    street = request.street,
    number = request.number,
    unit = request.unit,
    zipcode = request.zipcode,
    acquisition_date = request.acquisition_date,
    year_built = request.year_built  
    )
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

def update_house(id: int, request: HouseBase, db: Session, current_user: UserDisplay):
  try:
    # TODO: conversion to str if we pass int? "424242"?
    house = get_house(id, db)
    if house is None:
      return None
     # If the user type is not "admin" and owner_ids is provided
    if current_user.user_type == "member" and len(house.owners) > 1:
        # Don't update the owners of the house
        if hasattr(house, "owners"):
          # Extract IDs from the list of DBPerson objects
          request.owner_ids = [owner.id for owner in house.owners]
  
    model_dump = request.dict(exclude_unset=True)
    # Update only the provided fields in the request
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