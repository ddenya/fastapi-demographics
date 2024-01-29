from db.db_connector import Base
from sqlalchemy import Table, Column, Integer, ForeignKey

people_houses = Table(
    'people_houses',
    Base.metadata,
    Column('person_id', Integer, ForeignKey('person.id')),
    Column('house_id', Integer, ForeignKey('houses.id'))
)
