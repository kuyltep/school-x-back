from fastapi import FastAPI
from api.router import common_router

from core.handlers import register_exception_handlers
from core.database import Base, engine

app = FastAPI()
app.include_router(common_router)
register_exception_handlers(app)

Base.metadata.create_all(bind=engine)