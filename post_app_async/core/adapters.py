from adapters.storage.base import StorageAdapter
from adapters.storage.s3 import S3StorageAdapter

from core.config import settings


def get_storage() -> StorageAdapter:
    return S3StorageAdapter(
        bucket=settings.s3_bucket,
        url=settings.s3_url,
        access_key=settings.s3_access_key,
        secret_key=settings.s3_secret_key,
        region=settings.s3_region,
    )
