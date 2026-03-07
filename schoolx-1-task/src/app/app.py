from fastapi import FastAPI
from starlette_exporter import PrometheusMiddleware, handle_metrics

from src.api import router
from .utils.cors import setup_cors


def create_app() -> FastAPI:

  app = FastAPI()

  app.include_router(router)

  app.add_middleware(PrometheusMiddleware)
  app.add_route("/metrics", handle_metrics)

  setup_cors(app)

  return app


app = create_app()
