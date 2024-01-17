from contextlib import asynccontextmanager

from fastapi import FastAPI

from db.database import init_db
from order.order_controller import router as order_router
from product.product_controller import router as product_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Amalone API", lifespan=lifespan)


# Include routers from different modules
app.include_router(order_router, prefix="/orders", tags=["orders"])
app.include_router(product_router, prefix="/products", tags=["products"])

# You can add additional configurations or middleware here

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
