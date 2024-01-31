from typing import List
from pydantic import BaseModel

# House inside of Person
class House(BaseModel):
  city: str
  street: str
  number: str
  unit: str
  class Config():
    orm_mode=True

# Person inside of House
class Person(BaseModel):
  name: str
  class Config():
    orm_mode=True

# Data we receive from user
class UserBase(BaseModel):
  username: str
  email: str
  password: str

# Data we display to user
class UserDisplay(BaseModel):
  username: str
  email: str
  class Config():
    orm_mode=True

class PersonBase(BaseModel):
  name: str
  age: str
  gender: str
  email: str
  nation: str

class PersonDisplay(BaseModel):
  id: int
  name: str
  age: str
  gender: str
  email: str
  nation: str
  houses : List[House] = []
  class Config():
    orm_mode=True

class HouseBase(BaseModel):
  city: str
  street: str
  number: str
  unit: str
  zipcode: int
  acquisition_date: int
  year_built : int
  # When creating a house, tying to a List[person.id]
  owner_ids : List[int]

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
