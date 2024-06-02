import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager
from src.models.store_models import database
from src.routers import users
from src.routers import products
from src.routers import orders


#  Использую lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()

app = FastAPI(lifespan=lifespan)


app.include_router(users.router, tags=["users"])
app.include_router(products.router, tags=["products"])
app.include_router(orders.router, tags=["orders"])


@app.get("/", response_class=HTMLResponse)
async def root():
    return "<h1>Добро пожаловать в наш интернет-магазин!</h1>"

if __name__ == "__main__":
    uvicorn.run("main:app",
                host="localhost",
                port=8000,
                reload=True)
