from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from sqlalchemy import text

from src.app.config import configs
from src.app.services.minio import MinioStorageService
from src.database.database import async_session_maker

router = APIRouter(tags=["System"])


async def check_database() -> None:
  async with async_session_maker() as session:
    await session.execute(text("SELECT 1"))


async def check_minio() -> None:
  storage = MinioStorageService.from_settings(configs)
  await storage.check_bucket_exists()


@router.get("/health")
async def health() -> JSONResponse:
  checks: dict[str, dict[str, str]] = {
    "database": {"status": "ok", "error": ""},
    "minio": {"status": "ok", "error": ""},
  }

  overall_status = "ok"

  try:
    await check_database()
  except Exception as exc:
    checks["database"] = {"status": "failed", "error": str(exc)}
    overall_status = "failed"

  try:
    await check_minio()
  except Exception as exc:
    checks["minio"] = {"status": "failed", "error": str(exc)}
    overall_status = "failed"

  status_code = status.HTTP_200_OK if overall_status == "ok" else status.HTTP_503_SERVICE_UNAVAILABLE
  return JSONResponse(
    status_code=status_code,
    content={
      "status": overall_status,
      "checks": checks,
    },
  )


@router.get("/info")
async def info() -> dict[str, str]:
  return {
    "version": configs.app_version,
    "environment": configs.app_env,
    "api_prefix": configs.api_prefix,
  }
