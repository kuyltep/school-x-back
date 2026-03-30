from fastapi import FastAPI
from starlette_exporter import PrometheusMiddleware, handle_metrics

from src.api import router as api_router
from src.api.system.router import router as system_router

from .utils.cors import setup_cors


def create_app() -> FastAPI:
  app = FastAPI(version="1.0.0")

  app.include_router(system_router)
  app.include_router(api_router)

  app.add_middleware(PrometheusMiddleware)
  app.add_route("/metrics", handle_metrics)

  setup_cors(app)

  return app


app = create_app()
