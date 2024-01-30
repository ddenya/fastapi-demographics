from db.db_connector import Base
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, Boolean, Double
from sqlalchemy import Column
from sqlalchemy.orm import relationship

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