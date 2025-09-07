from typing import IO, Dict, Optional, Tuple, Any
import io

import boto3
from botocore.client import Config
from botocore.exceptions import ClientError

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

    @staticmethod
    async def file_exists(file_key: str) -> bool:
        try:
            s3.head_object(Bucket=BUCKET, Key=file_key)
            return True
        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                return False

            print(f"Ошибка при проверке файла в R2: {e}")

            return False

    @staticmethod
    async def get_file_metadata(file_key: str) -> Optional[Dict[str, Any]]:
        try:
            response = s3.head_object(Bucket=BUCKET, Key=file_key)
            return {
                "content_type": response.get("ContentType"),
                "content_length": response.get("ContentLength", 0),
                "last_modified": response.get("LastModified"),
                "metadata": response.get("Metadata", {}),
            }
        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                return None

            print(f"Ошибка при получении метаданных файла из R2: {e}")
            return None

    @staticmethod
    async def get_file(file_key: str) -> Optional[Tuple[bytes, str]]:
        try:
            response = s3.get_object(Bucket=BUCKET, Key=file_key)

            file_content = response["Body"].read()
            content_type = response.get("ContentType", "application/octet-stream")

            return file_content, content_type
        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                print(f"Файл {file_key} не найден в R2")
                return None

            print(f"Ошибка при получении файла из R2: {e}")
            return None

    @staticmethod
    async def upload_file(file_key: str, file_obj: IO, content_type: str) -> bool:
        try:
            s3.upload_fileobj(
                file_obj, BUCKET, file_key, ExtraArgs={"ContentType": content_type}
            )
            return True
        except ClientError as e:
            print(f"Ошибка при загрузке файла в R2: {e}")
            return False
