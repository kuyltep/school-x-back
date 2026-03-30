from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.app.config import configs


def setup_cors(app: FastAPI) -> None:
  if configs.app_env.lower() == "dev":
    app.add_middleware(
      CORSMiddleware,
      allow_origins=["*"],
      allow_credentials=True,
      allow_methods=["*"],
      allow_headers=["*"],
    )
    return

  app.add_middleware(
    CORSMiddleware,
    allow_origins=configs.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
  )
