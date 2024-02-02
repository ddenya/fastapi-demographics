from db.db_connector import Base
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, Boolean, Double
from sqlalchemy import Column
from sqlalchemy.orm import relationship
from models.associations import people_houses
#TODO: Refactor later
from sqlalchemy.orm import Session


class DbHouse(Base):
  __tablename__ = 'houses'
  id = Column(Integer, primary_key=True, index=True)
  city = Column(String)
  street = Column(String)
  number= Column(String)
  unit = Column(String)
  zipcode = Column(String)
  acquisition_date = Column(String)
  year_built = Column(String)
  owners = relationship('DbPerson', secondary='people_houses', back_populates='houses')

  # TODO: Refactor later
  # Takes in the list of ints
  def add_owners_by_ids(self, owner_ids: list[int], session: Session):
      # Avoiding cirtular import
      from models.person import DbPerson
      self.owners = (session.query(DbPerson).filter(DbPerson.id.in_(owner_ids)).all())