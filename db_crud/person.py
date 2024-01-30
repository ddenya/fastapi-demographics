from sqlalchemy.orm.session import Session
from models.person import DbPerson
from db.schemas import PersonBase

def create_person(request: PersonBase, db: Session):
  new_person = DbPerson(
    name = request.name,
    age = request.age,
    gender = request.gender,
    email = request.email,
    nation = request.nation,
  )
  db.add(new_person)
  db.commit()
  db.refresh(new_person)
  return new_person

def get_all_people(db: Session):
  try:
    return db.query(DbPerson).all()
  except Exception as e:
    print(e)
    return {}

def get_person(id: int, db: Session):
  try:
    return db.query(DbPerson).filter(DbPerson.id == id).first()
  except Exception as e:
    print(e)
    return {}

def update_person(id: int, request: PersonBase, db: Session):
  try:
    person = get_person(id, db)
    person.name = request.name
    person.age = request.age
    person.gender = request.gender
    person.email = request.email
    person.nation = request.nation
    db.commit()
    return person
  except Exception as e:
    return {'result': False} 

def delete_person(id: int, db: Session):
  # TODO
  return False