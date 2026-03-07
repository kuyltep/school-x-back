from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.app.config import configs


def setup_cors(app: FastAPI):

  CORSMiddleware(app=app, allow_methods="*", allow_origins=configs.origins)
