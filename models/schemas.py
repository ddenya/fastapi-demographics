from typing import List, Optional
from pydantic import BaseModel

# Inside classes
# ------------------------------------------------------------------
# House inside of Person
class House(BaseModel):
  city: str
  street: str
  number: str
  unit: str
  class Config():
    orm_mode=True

#Car inside of Person
class Car(BaseModel):
  brand: str
  model: str
  year: str
  class Config():
    orm_mode=True 

# Person inside of House
class Person(BaseModel):
  name: str
  class Config():
    orm_mode=True

# Person inside of Car
class Person(BaseModel):
  name: str
  class Config():
    orm_mode=True

# Base classes - Data we receive from user
# ------------------------------------------------------------------
class UserBase(BaseModel):
  username: str
  email: str
  password: str
  user_type: str

class PersonBase(BaseModel):
  name: Optional[str] = None
  age: Optional[str] = None
  gender: Optional[str] = None
  email: Optional[str] = None
  nation: Optional[str] = None
  ##During creating car and house we can give person ids there.
  ##So there is no need to put car and houses id s to person base.
  houses_ids: Optional[List[int]] = None
  cars_ids: Optional[List[int]] = None
  #user_id: Optional[int] = None
  class Config:
    use_enum_values = True

class HouseBase(BaseModel):
  city: Optional[str] = None
  street: Optional[str] = None
  number: Optional[str] = None
  unit: Optional[str] = None
  zipcode: Optional[int] = None
  acquisition_date: Optional[int] = None
  year_built : Optional[int] = None
  # When creating a house, tying to a List[person.id]
  owner_ids : Optional[List[int]] = None

class CarBase(BaseModel):
  brand: Optional[str] = None
  model: Optional[str] = None
  type: Optional[str] = None
  color: Optional[str] = None
  year: Optional[str] = None
  owner_ids : Optional[List[int]] = None

# Display classes - Data we display to user
# ------------------------------------------------------------------
class UserDisplay(BaseModel):
  id: int
  username: str
  email: str
  user_type: str
  class Config():
    orm_mode=True

class PersonDisplay(BaseModel):
  id: int
  name: str
  age: str
  gender: str
  email: str
  nation: str
  houses : List[House] = []
  cars : List[Car] = []
  user_id: Optional[int] = None
  class Config():
    orm_mode=True

class HouseDisplay(BaseModel):
  id: int
  city: str
  street: str
  number: str
  unit: str
  zipcode: int
  acquisition_date: int
  year_built : int
  owners : List[Person] = []
  class Config():
    orm_mode=True

class CarDisplay(BaseModel):
  id: int
  brand: str
  model: str
  year: str
  owners : List[Person] = []
  class Config():
    orm_mode=True