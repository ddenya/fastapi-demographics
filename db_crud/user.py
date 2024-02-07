from sqlalchemy.orm.session import Session
from models.user import DbUser
from models.schemas import UserBase
from db.hash import Hash

def create_user(request: UserBase, db: Session):
  new_user = DbUser(
    username = request.username,
    email = request.email,
    password = Hash.bcrypt(request.password)
  )

  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  return new_user

def get_all_users(db: Session):
  try:
    return db.query(DbUser).all()
  except Exception as e:
    return None

def get_user(id: int, db: Session):
  try:
    return db.query(DbUser).filter(DbUser.id == id).first()
  except Exception as e:
    return None


def update_user(id: int, request: UserBase, db: Session):
  try:
    user = get_user(id, db)
    if user is None:
      return None
    model_dump = request.dict(exclude_unset=True)
    # Update only the provided fields in the reques
    for field, value in model_dump.items():
      setattr(user, field, value)
    
    setattr(user, "id", id)
    db.commit()
    return user
  except Exception as e:
    print("Exception: " + str(e))
    return None

def delete_user(id: int, db: Session):
  try:
    user = get_user(id, db)
    db.delete(user)
    db.commit()
    return True
  except Exception as e:
    return None 