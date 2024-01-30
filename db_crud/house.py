import traceback
from sqlalchemy.orm.session import Session
from models.house import DbHouse
from db.schemas import HouseBase
from db.hash import Hash

def create_house(request: HouseBase, db: Session):
  # print(request)
  new_house = DbHouse(
    city = request.city,
    street = request.street,
    number = request.number,
    unit = request.unit,
    zipcode = request.zipcode,
    acquisition_date = request.acquisition_date,
    year_built = request.year_built
  )

  db.add(new_house)
  db.commit()
  db.refresh(new_house)
  return new_house

def get_all_houses(db: Session):
  try:
    return db.query(DbHouse).all()
  except Exception as e:
    print(e)
    return {}

def get_house(id: int, db: Session):
  try:
    return db.query(DbHouse).filter(DbHouse.id == id).first()
  except Exception as e:
    print(e)
    return {}

def update_house(id: int, request: HouseBase, db: Session):
  print(request)
  try:
    # TODO: conversion to str if we pass int? "424242"?
    house = get_house(id, db)
    house.city = request.city
    house.street = request.street
    house.number = request.number
    house.unit = request.unit
    db.commit()
    return house
  except Exception as e:
    traceback.print_exception(e)
    return {'result': False} 

def delete_user(id: int, db: Session):
  # TODO
  return False