from db.db_connector import Base
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, Boolean
from sqlalchemy import Column
from sqlalchemy.orm import relationship

class DbPerson(Base):
  __tablename__ = 'person'
  id = Column(Integer, primary_key=True, index=True)
  name = Column(String)
  age = Column(String)
  gender = Column(String)
  email = Column(String)
  nation = Column(String)
  houses = relationship('DbHouse', secondary='people_houses', back_populates='owners')