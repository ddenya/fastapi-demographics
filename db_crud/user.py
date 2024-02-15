from fastapi import HTTPException,status
from sqlalchemy.orm.session import Session
from models.user import DbUser
from models.schemas import UserBase
from db.hash import Hash
from fastapi.responses import JSONResponse

def create_user(request: UserBase, db: Session):
    try:
        user = db.query(DbUser).filter(DbUser.username == request.username).first()
        if user is not None:
            return JSONResponse(
                status_code=409,
                content={"message": f'User with username {request.username} already exists. Try an unique username!!!'}
            )
        new_user = DbUser(
            username=request.username,
            email=request.email,
            password=Hash.bcrypt(request.password),
            user_type=request.user_type
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f'Internal Server Error okan: {str(e)}'
        ) 

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
  

def get_user_by_username(db: Session, username: str):
  user = db.query(DbUser).filter(DbUser.username == username).first()
  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
      detail=f'User with username {username} not found')
  return user


def update_user(id: int, request: UserBase, db: Session):
  try:
    user = get_user(id, db)
    if user is None:
      return None
    
    model_dump = request.dict(exclude_unset=True)
    # Update only the provided fields in the reques

    if 'password' in model_dump:
      model_dump['password'] = Hash.bcrypt(model_dump['password'])

    # Check if the new username already exists in the database
    if 'username' in model_dump:
        existing_user = db.query(DbUser).filter(DbUser.username == model_dump['username']).first()
        if existing_user and existing_user.id != id:
            print("test")
            return JSONResponse(
                status_code=409,
                content={"message": f'User with username {request.username} already exists. Try an unique username'}
            )
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