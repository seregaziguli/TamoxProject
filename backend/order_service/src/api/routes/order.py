from ...services.order_service import OrderService
from ...api.deps.order_deps import get_current_user, get_order_service, get_s3_client
from ...api.schemas.order import OrderRequestDTO, OrderResponseDTO
from fastapi.exceptions import HTTPException
from fastapi import status, APIRouter, Depends, UploadFile, File
from fastapi.responses import StreamingResponse
import io
from ...services.s3_service import S3Client
from fastapi_cache.decorator import cache
from typing import List, Union

order_router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)

@order_router.post("/", response_model=OrderResponseDTO, status_code=status.HTTP_201_CREATED)
async def create_order(
    order: Union[OrderRequestDTO, str],
    user: dict = Depends(get_current_user),
    order_service: OrderService = Depends(get_order_service),
    image: UploadFile = File(None)
):
    if isinstance(order, str):
        try:
            order = OrderRequestDTO.model_validate_json(order)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid input format: {str(e)}")

    return await order_service.create_order(order, user, image)


@order_router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(
    order_id: int,
    user: dict = Depends(get_current_user),
    order_service: OrderService = Depends(get_order_service)
):
    try:
        await order_service.delete_order(order_id, user)
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not delete order. Error: {str(e)}")


@order_router.get("/", response_model=List[OrderResponseDTO], status_code=status.HTTP_200_OK)
async def get_user_orders(
    user: dict = Depends(get_current_user),
    order_service: OrderService = Depends(get_order_service)
):
    try:
        orders = await order_service.get_user_orders(user)
        return orders
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not retrieve orders. Error: {str(e)}")


@order_router.get("/all", response_model=List[OrderResponseDTO], status_code=status.HTTP_200_OK)
@cache(expire=180)
async def get_all_orders(
    order_service: OrderService = Depends(get_order_service)
):
    try:
        orders = await order_service.get_all_orders()
        return orders
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not retrieve all orders. Error: {str(e)}")


@order_router.get("/user-notifications", status_code=status.HTTP_200_OK)
async def get_notifications(
    user: dict = Depends(get_current_user),
    order_service: OrderService = Depends(get_order_service)
):
    try:
        if not isinstance(user["id"], int):
            raise HTTPException(status_code=400, detail="Invalid user ID format.")
        user_id = int(user["id"])
        notifications = await order_service.get_user_notifications(user_id)
        return notifications
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error retrieving notifications: {str(e)}")


@order_router.get("/{order_id}", response_model=OrderResponseDTO, status_code=status.HTTP_200_OK)
async def get_order_by_id(
    order_id: int,
    user: dict = Depends(get_current_user),
    order_service: OrderService = Depends(get_order_service)
):
    try:
        order = await order_service.get_order_by_id(order_id, user)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found.")
        return order
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not retrieve order. Error: {str(e)}")


@order_router.post("/{order_id}/process", response_model=OrderResponseDTO, status_code=status.HTTP_200_OK)
async def process_order(
    order_id: int,
    user: dict = Depends(get_current_user),
    order_service: OrderService = Depends(get_order_service)
):
    try:
        order = await order_service.process_order(order_id, user)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found or cannot be processed.")
        return order
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not process order. Error: {str(e)}")


@order_router.put("/{order_id}", response_model=OrderResponseDTO, status_code=status.HTTP_200_OK)
async def update_order(
    order_id: int,
    order_data: dict,
    user: dict = Depends(get_current_user), 
    order_service: OrderService = Depends(get_order_service)
):
    try:
        updated_order = await order_service.update_order(order_id, order_data, user)
        if not updated_order:
            raise HTTPException(status_code=404, detail="Order not found.")
        return updated_order
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not update order. Error: {str(e)}")


@order_router.post("/{order_id}/confirm_completion", status_code=status.HTTP_200_OK)
async def confirm_order_completion(
    order_id: int,
    user: dict = Depends(get_current_user),
    order_service: OrderService = Depends(get_order_service)
):
    try:
        confirmed_order = await order_service.confirm_order_completion(order_id, user)
        return confirmed_order
    except HTTPException as http_exc:
        raise http_exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Could not confirm order completion. Error: {str(exc)}")


@order_router.get("/images/{object_name:path}")
async def get_image(
    object_name: str,
    s3_service: S3Client = Depends(get_s3_client),
):
    try:
        file_content = await s3_service.get_image(object_name)

        if file_content is None:
            raise HTTPException(status_code=404, detail="Image not found.")
        
        return StreamingResponse(io.BytesIO(file_content), media_type="image/jpeg")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not retrieve image. Error: {str(e)}")
