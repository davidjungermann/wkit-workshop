from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException

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


# Health Check Endpoint
@app.get("/health")
async def health_check():
    try:
        return {"status": "OK"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Additional configurations or middleware can be added here

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
