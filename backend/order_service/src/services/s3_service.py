from contextlib import asynccontextmanager
from botocore.exceptions import ClientError
from aiobotocore.session import get_session
import os
import uuid
from ..core.conifg import settings
from typing import Union
from ..utils.logger import logger
from fastapi import HTTPException

class S3Client:
    def __init__(
            self,
            access_key: str,
            secret_key: str,
            endpoint_url: str,
            bucket_name: str,
    ):
        self.config = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "endpoint_url": endpoint_url,
        }
        self.bucket_name = bucket_name
        self.session = get_session()

    @asynccontextmanager
    async def get_client(self):
        async with self.session.create_client("s3", **self.config, region_name='us-west-2') as client:
            yield client

    async def upload_file(self, temp_file_path, object_name: str):
        try:
            async with self.get_client() as client:
                await client.put_object(
                    Bucket=self.bucket_name,
                    Key=object_name,
                    Body=temp_file_path,
                )
            return object_name
        except ClientError as e:
            logger.error(f"Error uploading file: {e}")
            raise HTTPException(status_code=500, detail="Error uploading file.")

    async def upload_image(self, file: str, object_name: str):
        try:
            async with self.get_client() as client:
                with open(file, "rb") as file:
                    await client.put_object(
                        Bucket=self.bucket_name,
                        Key=object_name,
                        Body=file,
                    )
            return object_name
        except ClientError as e:
            logger.error(f"Error uploading image: {e}")
            raise HTTPException(status_code=500, detail="Error uploading image.")

    async def upload_image_bytes(self, file_content: bytes, object_name: str):
        try:
            async with self.get_client() as client:
                await client.put_object(
                    Bucket=self.bucket_name,
                    Key=object_name,
                    Body=file_content,
                )
            return object_name
        except ClientError as e:
            logger.error(f"Error uploading image bytes: {e}")
            raise HTTPException(status_code=500, detail="Error uploading image bytes.")

    async def upload_image_fixed(self, temp_file_path, object_name: str):
        try:
            async with self.get_client() as client:
                with open(temp_file_path, 'rb') as file_data:
                    file_content = file_data.read()

                await client.put_object(
                    Bucket=self.bucket_name,
                    Key=object_name,
                    Body=file_content,  
                )
        except ClientError as e:
            logger.error(f"ClientError uploading file: {e}")
            raise HTTPException(status_code=500, detail="Error uploading fixed image.")
        finally:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)

        return object_name

    def generate_object_name(self, prefix: str, original_filename: str):
        try:
            extension = original_filename.split('.')[-1]
            unique_name = f"{prefix}/{uuid.uuid4()}.{extension}"
            return unique_name
        except Exception as e:
            logger.error(f"Error generating object name: {e}")
            raise HTTPException(status_code=500, detail="Error generating object name.")

    async def get_permanent_url(self, object_name: str):
        return object_name

    async def delete_file(self, object_name: str):
        try:
            async with self.get_client() as client:
                await client.delete_object(Bucket=self.bucket_name, Key=object_name)
                logger.info(f"File {object_name} deleted from {self.bucket_name}")
        except ClientError as e:
            logger.error(f"Error deleting file: {e}")
            raise HTTPException(status_code=500, detail="Error deleting file.")

    async def get_file(self, object_name: str) -> Union[bytes, None]:
        try:
            async with self.get_client() as client:
                response = await client.get_object(Bucket=self.bucket_name, Key=object_name)
                return await response["Body"].read()
        except ClientError as e:
            logger.error(f"Error downloading file: {e}")
            raise HTTPException(status_code=500, detail="Error downloading file.")

    async def get_image(self, object_name: str) -> Union[bytes, None]:
        return await self.get_file(object_name)

    async def get_video(self, object_name: str) -> Union[bytes, None]:
        return await self.get_file(object_name)

s3_client = S3Client(
    access_key=settings().ACCESS_KEY,
    secret_key=settings().SECRET_KEY,
    endpoint_url=settings().ENDPOINT_URL,
    bucket_name=settings().BUCKET_NAME,
)
