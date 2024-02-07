from fastapi import FastAPI
from router import user, house, person, car
from models import Base
from db.db_connector import engine
from fastapi.middleware.cors import CORSMiddleware
from auth import authentication

app = FastAPI()
app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(house.router)
app.include_router(car.router)
app.include_router(person.router)

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # You can specify specific HTTP methods if needed
    allow_headers=["*"],  # You can specify specific HTTP headers if needed
)


# If database exists - it does not create it again
Base.metadata.create_all(engine)