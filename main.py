from fastapi import FastAPI
from router import user, house, person, car
from models import Base
from db.db_connector import engine

app = FastAPI()
app.include_router(user.router)
app.include_router(house.router)
app.include_router(car.router)
app.include_router(person.router)


# If database exists - it does not create it again
Base.metadata.create_all(engine)