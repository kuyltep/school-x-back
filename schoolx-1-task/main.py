import uvicorn

from src.app.config import configs

if __name__ == "__main__":
  uvicorn.run("src.app.app:app", port=configs.port)
