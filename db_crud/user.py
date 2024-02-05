from sqlalchemy.orm.session import Session
from models.user import DbUser
from models.schemas import UserBase
from db.hash import Hash
from fastapi import HTTPException, status


def create_user(request: UserBase, db: Session):
  new_user = DbUser(
    username = request.username,
    email = request.email,
    password = Hash.bcrypt(request.password),
    user_type = request.user_type
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

#Ask Denys if getting user by username is logical?
def get_user_by_username(db: Session, username: str):
  user = db.query(DbUser).filter(DbUser.username == username).first()
  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
      detail=f'User with username {username} not found')
  return user


def update_user(id: int, request: UserBase, db: Session):
  try:
    user = get_user(id, db)
    user.username = request.username
    user.email = request.email
    user.password = Hash.bcrypt(request.password)
    user.user_type = request.user_type
    db.commit()
    return user
  except Exception as e:
    return None 

def delete_user(id: int, db: Session):
  try:
    user = get_user(id, db)
    db.delete(user)
    db.commit()
    return True
  except Exception as e:
    return None 