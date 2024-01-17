from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.session import get_db_session
from order.order_repository import OrderRepository
from order.order_service import OrderService
from schemas.order import OrderRequest, OrderResponse

router = APIRouter()


@router.post("/", response_model=OrderResponse)
async def create_order(
    request: OrderRequest, db: Session = Depends(get_db_session)
) -> OrderResponse:
    order_service = OrderService(OrderRepository(db))
    return order_service.create_order(request)


@router.get("/", response_model=List[OrderResponse])
async def get_orders(db: Session = Depends(get_db_session)) -> List[OrderResponse]:
    order_service = OrderService(OrderRepository(db))
    return order_service.get_all_orders()


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: int, db: Session = Depends(get_db_session)
) -> OrderResponse | None:
    order_service = OrderService(OrderRepository(db))
    order = order_service.get_order_by_id(order_id)
    return order
