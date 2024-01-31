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
    pass

def get_user(id: int, db: Session):
  try:
    return db.query(DbUser).filter(DbUser.id == id).first()
  except Exception as e:
    return None


def update_user(id: int, request: UserBase, db: Session):
  try:
    user = get_user(id, db)
    user.username = request.username
    user.email = request.email
    user.password = Hash.bcrypt(request.password)
    db.commit()
    return user
  except Exception as e:
    return {'result': False} 

def delete_user(id: int, db: Session):
  try:
    user = get_user(id, db)
    db.delete(user)
    db.commit()
    return {'result': True}
  except Exception as e:
    return {'result': False} 