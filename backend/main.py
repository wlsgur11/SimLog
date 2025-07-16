from fastapi import FastAPI
from controllers import auth_controller, user_controller

from database import Base, engine
from models.user import User

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth_controller.router)
app.include_router(user_controller.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}