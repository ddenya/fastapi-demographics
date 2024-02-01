from db.db_connector import Base
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, Boolean
from sqlalchemy import Column
from sqlalchemy.orm import relationship
from models.associations import people_houses, people_cars
# TODO refactor later?
from sqlalchemy.orm import Session

class DbPerson(Base):
  __tablename__ = 'person'
  id = Column(Integer, primary_key=True, index=True)
  name = Column(String)
  age = Column(String)
  gender = Column(String)
  email = Column(String)
  nation = Column(String)
  houses = relationship('DbHouse', secondary='people_houses', back_populates='owners')
  cars = relationship('DbCar', secondary='people_cars', back_populates='owners')

# TODO refactor later?
  def add_houses_by_ids(self, houses_ids: list[int], session: Session):
    # Avoiding cirtular import
    from models.house import DbHouse
    self.houses.extend(session.query(DbHouse).filter(DbHouse.id.in_(houses_ids)).all())

  def add_cars_by_ids(self, cars_ids: list[int], session: Session):
    # Avoiding cirtular import
    from models.house import DbHouse
    self.cars.extend(session.query(DbHouse).filter(DbHouse.id.in_(cars_ids)).all())