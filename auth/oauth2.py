from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import List, Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from db.db_connector import get_db
from db_crud import user as db_user
from models.schemas import UserBase
 
 
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
 
SECRET_KEY = '77407c7339a6c00544e51af1101c4abb4aea2a31157ca5f7dfd87da02a628107'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30
 
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
  to_encode = data.copy()
  if expires_delta:
    expire = datetime.utcnow() + expires_delta
  else:
    expire = datetime.utcnow() + timedelta(minutes=15)
  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail= 'Could not validate credentials',
        headers = {"WWW-Authentication": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
       raise credentials_exception
    
    user = db_user.get_user_by_username(db, username)

    if username is None:
        raise credentials_exception
    
    return user

def check_user_types(required_user_types: list):    
    def _check_user_types(current_user: UserBase = Depends(get_current_user)):
        if current_user.user_type not in required_user_types:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='User does not have required privileges',
            )
        return current_user
    return _check_user_types