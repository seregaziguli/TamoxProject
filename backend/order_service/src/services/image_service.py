import base64
from fastapi import UploadFile
from ..services.s3_service import S3Client
from ..utils.background_tasks.tasks import upload_image_task

class ImageService:
    def __init__(self, s3_client: S3Client):
        self.s3_client = s3_client

    async def upload_image(self, image: UploadFile) -> str:
        object_name = self.s3_client.generate_object_name("orders/images", image.filename)
        image_content = await image.read()
        encoded_image_content = base64.b64encode(image_content).decode('utf-8')
        await upload_image_task.kiq(encoded_image_content, object_name)
        return await self.s3_client.get_permanent_url(object_name)