import asyncio
from contextlib import asynccontextmanager
import logging
import os
from aiobotocore.session import get_session
from botocore.exceptions import ClientError
import uuid
from src.config_env import ACCESS_KEY, SECRET_KEY, ENDPOINT_URL, BUCKET_NAME
from typing import Union
from src.utils.logger import logger

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
        logger.info(f"Uploading file: {temp_file_path} to bucket: {self.bucket_name} with key: {object_name}")
        async with self.get_client() as client:
            response = await client.put_object(
                Bucket=self.bucket_name,
                Key=object_name,
                Body=temp_file_path,
            )
        return object_name

    async def upload_image(self, file: str, object_name: str):
        async with self.get_client() as client:
            with open(file, "rb") as file:
                response = await client.put_object(
                    Bucket=self.bucket_name,
                    Key=object_name,
                    Body=file,
                )
        return object_name
    
    async def upload_image_bytes(self, file_content: bytes, object_name: str):
        logger.info(f"Uploading file to bucket: {self.bucket_name} with key: {object_name}")
        async with self.get_client() as client:
            try:
                response = await client.put_object(
                    Bucket=self.bucket_name,
                    Key=object_name,
                    Body=file_content, 
                )
                logger.info(f"Upload successful: {response}")
            except ClientError as e:
                logger.error(f"ClientError occurred: {e.response['Error']['Code']} - {e.response['Error']['Message']}")
                raise e
        return object_name

    
    async def upload_image_fixed(self, temp_file_path, object_name: str):
        logger.info(f"Uploading file: {temp_file_path} to bucket: {self.bucket_name} with key: {object_name}")
        
        async with self.get_client() as client:
            try:
                with open(temp_file_path, 'rb') as file_data:
                    file_content = file_data.read()

                response = await client.put_object(
                    Bucket=self.bucket_name,
                    Key=object_name,
                    Body=file_content,  
                )
            except ClientError as e:
                logger.error(f"ClientError occurred: {e.response['Error']['Code']} - {e.response['Error']['Message']}")
                raise e
            finally:
                if os.path.exists(temp_file_path):
                    os.remove(temp_file_path)

        return object_name

    def generate_object_name(self, prefix: str, original_filename: str):
        extension = original_filename.split('.')[-1]
        unique_name = f"{prefix}/{uuid.uuid4()}.{extension}"
        return unique_name

    async def get_permanent_url(self, object_name: str):
        url = object_name
        return url

    async def delete_file(self, object_name: str):
        try:
            async with self.get_client() as client:
                await client.delete_object(Bucket=self.bucket_name, Key=object_name)
                logger.info(f"File {object_name} deleted from {self.bucket_name}")
        except ClientError as e:
            logger.error(f"Error deleting file: {e}")

    async def get_file(self, object_name: str) -> Union[bytes, None]:
        try:
            async with self.get_client() as client:
                response = await client.get_object(Bucket=self.bucket_name, Key=object_name)
                file_content = await response["Body"].read()
                return file_content
        except ClientError as e:
            logger.error(f"Error downloading file: {e}")
            return None

    async def get_image(self, object_name: str) -> Union[bytes, None]:
        return await self.get_file(object_name)
    
    async def get_video(self, object_name: str) -> Union[bytes, None]:
        return await self.get_file(object_name)

s3_client = S3Client(
    access_key=ACCESS_KEY,
    secret_key=SECRET_KEY,
    endpoint_url=ENDPOINT_URL,
    bucket_name=BUCKET_NAME,
)
