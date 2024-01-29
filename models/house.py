from db.db_connector import Base
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, Boolean, Double
from sqlalchemy import Column
from sqlalchemy.orm import relationship

class DbUser(Base):
  __tablename__ = 'houses'
  id = Column(Integer, primary_key=True, index=True)
  address = Column(String)
  postcode = Column(String)
  area = Column(Double)