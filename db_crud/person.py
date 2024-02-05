from sqlalchemy.orm.session import Session
from models.person import DbPerson
from models.schemas import PersonBase

def create_person(request: PersonBase, db: Session):
  new_person = DbPerson(
    name = request.name,
    age = request.age,
    gender = request.gender,
    email = request.email,
    nation = request.nation,
  )
  new_person.add_houses_by_ids(request.houses_ids, session = db)
  db.add(new_person)
  db.commit()
  db.refresh(new_person)
  return new_person

def get_all_people(db: Session):
  try:
    return db.query(DbPerson).all()
  except Exception as e:
    return None

def get_person(id: int, db: Session):
  try:
    return db.query(DbPerson).filter(DbPerson.id == id).first()
  except Exception as e:
    return None

def update_person(id: int, request: PersonBase, db: Session):
  try:
    person = get_person(id, db)
    if person is None:
      return None
    model_dump = request.dict(exclude_unset=True)
    # Update only the provided fields in the reques
    for field, value in model_dump.items():
      setattr(person, field, value)
      # Check if houses_ids are present in the request before calling the method
    if "houses_ids" in model_dump:
      person.add_houses_by_ids(request.houses_ids, session=db)
        # Check if cars_ids are present in the request before calling the method
    if "cars_ids" in model_dump:
      person.add_cars_by_ids(request.cars_ids, session=db)
    
    setattr(person, "id", id)
    db.commit()
    return person
  except Exception as e:
    print("Exception: " + str(e))
    return None

def delete_person(id: int, db: Session):
  try:
    person = get_person(id, db)
    db.delete(person)
    db.commit()
    return True
  except Exception as e:
    return None 