import traceback
from sqlalchemy.orm.session import Session
from models.car import DbCar
from models.schemas import CarBase

def create_car(request: CarBase, db: Session):
  # print(request)
  new_car = DbCar(
    brand = request.brand,
    model = request.model,
    type = request.type,
    color = request.color,
    year = request.year
    )
  new_car.add_owners_by_ids(request.owner_ids, session = db)

  db.add(new_car)
  db.commit()
  db.refresh(new_car)
  return new_car

def get_all_cars(db: Session):
  try:
    return db.query(DbCar).all()
  except Exception as e:
    return None

def get_car(id: int, db: Session):
  try:
    return db.query(DbCar).filter(DbCar.id == id).first()
  # Exception on database level
  except Exception as e:
    return None

def update_car(id: int, request: CarBase, db: Session):
  try:
    # TODO: conversion to str if we pass int? "424242"?
    car = get_car(id, db)
    if car is None:
      return None
    car.brand = request.brand
    car.model = request.model
    car.type = request.type
    car.year = request.year

    car.add_owners_by_ids(request.owner_ids, session = db)

    db.commit()
    return car
  except Exception as e:
    return None

def delete_car(id: int, db: Session):
  try:
    car = get_car(id, db)
    db.delete(car)
    db.commit()
    return True
  except Exception as e:
    return None