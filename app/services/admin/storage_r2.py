import boto3
from botocore.client import Config
from app.core.config import settings

s3 = boto3.client(
    "s3",
    endpoint_url=settings.R2_ACCOUNT_ID,
    aws_access_key_id=settings.R2_ACCESS_KEY_ID,
    aws_secret_access_key=settings.R2_SECRET_ACCESS_KEY,
    region_name="auto",
    config=Config(signature_version="s3v4"),
)
BUCKET = settings.R2_BUCKET


class StorageR2Service:
    @staticmethod
    def presign_put(key: str, content_type: str, ttl=300) -> str:
        return s3.generate_presigned_url(
            "put_object",
            Params={
                "Bucket": BUCKET,
                "Key": key,
                "ContentType": content_type,
            },
            ExpiresIn=ttl,
        )
