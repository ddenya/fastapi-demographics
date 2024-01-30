from db.db_connector import Base
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, Boolean, Double
from sqlalchemy import Column
from sqlalchemy.orm import relationship
from models.associations import people_houses
from models.person import DbPerson

class DbHouse(Base):
  __tablename__ = 'houses'
  id = Column(Integer, primary_key=True, index=True)
  city = Column(String)
  street = Column(String)
  number= Column(Integer)
  unit = Column(String)
  zipcode = Column(Integer)
  acquisition_date = Column(Integer)
  year_built = Column(Integer)
  owners = relationship('DbPerson', secondary='people_houses', back_populates='houses')