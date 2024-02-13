from fastapi import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm.session import Session
from db.hash import Hash
from models.person import DbPerson
from models.schemas import PersonBase
from models.user import DbUser

def create_person(request: PersonBase, db: Session):
    try:
        # person = db.query(DbPerson).filter(DbPerson.user_id == request.user_id).first()
        # if person is not None:
        #      return JSONResponse(
        #         status_code=409,
        #         content={"message": f'Person with user id {request.user_id} has already existed.'}
        #     )
        
        new_user = DbUser(
          username=request.name,
          email=request.name + "@mail.com",
          # need to hash the password
          password = Hash.bcrypt(request.name),
          user_type = "member"
          #person = new_person
        )    
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        new_person = DbPerson(
            name=request.name,
            age=request.age,
            gender=request.gender,
            email=request.email,
            nation=request.nation,
            user_id=new_user.id
        )

        new_person.add_houses_by_ids(request.houses_ids, session=db)
        db.add(new_person)
        
        db.commit()
        db.refresh(new_person)
        return new_person
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f'Internal Server Error okan: {str(e)}'
        )

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