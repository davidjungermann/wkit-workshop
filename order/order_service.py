from typing import List, Optional

from fastapi import HTTPException

from models.order import OrderDetail
from models.product import Product
from order.order_repository import OrderRepository
from schemas.order import OrderRequest, OrderResponse, ProductResponse


class OrderService:
    def __init__(self, repository: OrderRepository):
        self.repository = repository

    def create_order(self, request: OrderRequest) -> OrderResponse:
        new_order = self.repository.create_order()

        total_price = 0
        products_response = []
        for product_id, quantity in zip(request.products, request.quantities):
            product = self.repository.get_product_by_id(product_id)
            if not product:
                raise ValueError(f"Product with id {product_id} not found")

            total_price += product.price * quantity
            self.repository.add_order_detail(new_order.id, product.id, quantity)
            products_response.append(
                ProductResponse(
                    id=product.id,
                    name=product.name,
                    category=product.category,
                    price=product.price,
                )
            )

        self.repository.update_order_total_price(new_order.id, total_price)
        order = self.repository.get_order_by_id(new_order.id)

        if not order:
            raise HTTPException(404, "Order could not be created")

        return OrderResponse(
            id=order.id,
            timestamp=order.timestamp,
            total_price=order.total_price,
            products=order.products,
        )

    def get_all_orders(self) -> List[OrderResponse]:
        orders = self.repository.get_all_orders()
        order_responses: List[OrderResponse] = []
        for order in orders:
            order_responses.append(
                OrderResponse(
                    id=order.id,
                    timestamp=order.timestamp,
                    total_price=order.total_price,
                    products=order.products,
                )
            )
        return order_responses

    def get_order_by_id(self, order_id: int) -> Optional[OrderResponse]:
        order = self.repository.get_order_by_id(order_id)

        if not order:
            raise HTTPException(404, f"Order {order_id} not found")

        return OrderResponse(
            id=order.id,
            timestamp=order.timestamp,
            total_price=order.total_price,
            products=order.products,
        )
