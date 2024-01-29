from fastapi import FastAPI
from router import user
from models import Base
from db.db_connector import engine

app = FastAPI()
app.include_router(user.router)

# If database exists - it does not create it again
Base.metadata.create_all(engine)