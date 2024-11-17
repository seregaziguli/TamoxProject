from src.services.order_service import OrderService
from src.api.deps.order_deps import get_current_user, get_order_service
from src.api.schemas.order import OrderRequest, OrderResponse
import logging
from typing import List, Union
from src.utils.logger import logger
from fastapi.exceptions import HTTPException
from fastapi import status, APIRouter, Depends, UploadFile, File, Body
from pydantic import Json
import json

order_router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
    responses={404: {"description": "Not found"}}
)

@order_router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(
    order: Union[OrderRequest, str],
    user: dict = Depends(get_current_user),
    order_service: OrderService = Depends(get_order_service),
    image: UploadFile = File(None)
):
    if isinstance(order, str):
        try:
            order = OrderRequest.model_validate_json(order)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid input format: {str(e)}")

    return await order_service.create_order(order, user, image)

    
@order_router.get("/", response_model=List[OrderResponse], status_code=status.HTTP_200_OK)
async def get_user_orders(
    user: dict = Depends(get_current_user),
    order_service: OrderService = Depends(get_order_service)
):
    try:
        orders = await order_service.get_user_orders(user)
        return orders
    except Exception as e:
        logger.error(f"Error while retrieving orders: {e}")
        raise HTTPException(status_code=500, detail="Could not retrieve orders.")
    

@order_router.get("/all", response_model=List[OrderResponse], status_code=status.HTTP_200_OK)
async def get_all_orders(
    order_service: OrderService = Depends(get_order_service)
):
    try:
        orders = await order_service.get_all_orders()
        return orders
    except Exception as e:
        logger.error(f"Error while retrieving all orders: {e}")
        raise HTTPException(status_code=500, detail="Could not retrieve all orders.")
    
    
@order_router.get("/{order_id}", response_model=OrderResponse, status_code=status.HTTP_200_OK)
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
        logging.error(f"Error retrieving order: {e}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Coult not retrieve order.")
    

@order_router.post("/{order_id}/process", response_model=OrderResponse, status_code=status.HTTP_200_OK)
async def process_order(
    order_id: int,
    user: dict = Depends(get_current_user),
    order_service: OrderService = Depends(get_order_service)
):
    try:
        order = await order_service.process_order(order_id, user)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found or cannot be processed.")
        logger.info("In function 2")
        return order
    except HTTPException as e:
        logging.error(f"Error processing order: {e}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Could not process order.")
    
    
@order_router.put("/{order_id}", response_model=OrderResponse, status_code=status.HTTP_200_OK)
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
        logger.info("In function 3")
        return updated_order
    except HTTPException as e:
        logger.error(f"Error updating order: {e}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Could not update order.")
    
    
@order_router.post("/{order_id}/confirm_completion", status_code=status.HTTP_200_OK)
async def confirm_order_completion(
    order_id: int,
    user: dict = Depends(get_current_user),
    order_service: OrderService = Depends(get_order_service)
):
    try:
        confirmed_order = await order_service.confirm_order_completion(order_id, user)
        logger.info("In function 4")
        return confirmed_order
    except HTTPException as http_exc:
        raise http_exc
    except Exception as exc:
        logger.error(f"Error confirmed order completion: {exc}")
        raise HTTPException(status_code=500, detail="Could not confirm order completion.")