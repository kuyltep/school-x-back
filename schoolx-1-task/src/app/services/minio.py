import uuid
import aioboto3
from urllib.parse import quote
from src.app.config import Configs, configs

class UploadedObject:
    def __init__(self, url: str, bucket: str, object_key: str):
        self.url = url
        self.bucket = bucket
        self.object_key = object_key

class MinioStorageService:
    def __init__(
        self,
        endpoint: str,
        access_key: str,
        secret_key: str,
        bucket: str,
        public_url: str,
        secure: bool,
    ):

        endpoint_clean = endpoint.replace("http://", "").replace("https://", "")
        scheme = "https" if secure else "http"
        self.endpoint_url = f"{scheme}://{endpoint_clean}"
        
        self.access_key = access_key
        self.secret_key = secret_key
        self.bucket = bucket
        self.public_url = public_url.rstrip("/")
        self.secure = secure
        
        self.session = aioboto3.Session()

    @classmethod
    def from_settings(cls, settings: Configs | None = None) -> "MinioStorageService":
        cfg = settings or configs
        return cls(
            endpoint=cfg.minio_endpoint,
            access_key=cfg.minio_access_key.get_secret_value(),
            secret_key=cfg.minio_secret_key.get_secret_value(),
            bucket=cfg.minio_bucket,
            public_url=cfg.minio_public_url,
            secure=cfg.minio_secure,
        )

    def get_client(self):
        return self.session.client(
            "s3",
            endpoint_url=self.endpoint_url,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            use_ssl=self.secure,
            region_name="us-east-1",
        )

    async def check_bucket_exists(self) -> None:
        async with self.get_client() as client:
            await client.head_bucket(Bucket=self.bucket)

    async def ensure_bucket_exists(self) -> None:
        async with self.get_client() as client:
            try:
                await client.head_bucket(Bucket=self.bucket)
            except Exception:
                await client.create_bucket(Bucket=self.bucket)

    async def upload_avatar(
        self,
        task_id: str,
        filename: str | None,
        content: bytes,
        content_type: str,
    ) -> UploadedObject:
        
        extension = ""
        if filename and "." in filename:
            extension = "." + filename.split(".")[-1].lower()

        file_name = f"{uuid.uuid4().hex}{extension}"
        object_key = f"avatars/{task_id}/{file_name}"

        async with self.get_client() as client:
            await client.put_object(
                Bucket=self.bucket,
                Key=object_key,
                Body=content,
                ContentType=content_type,
                ContentLength=len(content),
            )

        url = f"{self.public_url}/{self.bucket}/{quote(object_key)}"
        return UploadedObject(url=url, bucket=self.bucket, object_key=object_key)
