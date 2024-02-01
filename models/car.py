from db.db_connector import Base
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, Boolean, Double
from sqlalchemy import Column
from sqlalchemy.orm import relationship
from models.associations import people_cars
#TODO: Refactor later
from sqlalchemy.orm import Session


class DbCar(Base):
  __tablename__ = 'cars'
  id = Column(Integer, primary_key=True, index=True)
  brand = Column(String)
  model = Column(String)
  type= Column(String)
  color= Column(String)
  year = Column(String)
  owners = relationship('DbPerson', secondary='people_cars', back_populates='cars')

  # TODO: Refactor later
  # Takes in the list of ints
  def add_owners_by_ids(self, owner_ids: list[int], session: Session):
      # Avoiding cirtular import
      from models.person import DbPerson
      self.owners.extend(session.query(DbPerson).filter(DbPerson.id.in_(owner_ids)).all())