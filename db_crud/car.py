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
    car = get_car(id, db)
    if car is None:
      return None
    model_dump = request.dict(exclude_unset=True)
    # Update only the provided fields in the reques
    for field, value in model_dump.items():
      setattr(car, field, value)
    # Check if owner_ids are present in the request before calling the method
    if "owner_ids" in model_dump:
      car.add_owners_by_ids(request.owner_ids, session=db)
    
    setattr(car, "id", id)
    db.commit()
    return car
  except Exception as e:
    print("Exception: " + str(e))
    return None

def delete_car(id: int, db: Session):
  try:
    car = get_car(id, db)
    db.delete(car)
    db.commit()
    return True
  except Exception as e:
    return None