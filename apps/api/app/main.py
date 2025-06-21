from fastapi import FastAPI
from app.api.routers import auth, users
from app.db.base import Base
from app.db.session import engine

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth.router)
app.include_router(users.router)