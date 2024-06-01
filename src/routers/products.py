from fastapi import Request, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pandas as pd
from src.models.schemas import Product, ProductIn
from src.models.store_models import database, products

router = APIRouter(prefix="/products", tags=["products"])
templates = Jinja2Templates(directory='templates')


@router.post("/", response_model=Product)
async def create_product(product: ProductIn):
    query = products.insert().values(**product.model_dump())
    record_id = await database.execute(query)
    return {**product.model_dump(), "id": record_id}


@router.get("/", response_class=HTMLResponse)
async def read_products(request: Request):
    query = products.select()
    products_table = pd.DataFrame([product for product in await database.fetch_all(query)]).to_html(index=False)
    return templates.TemplateResponse("products.html", {"request": request, "products_table": products_table})


@router.get("/{product_id}", response_model=Product)
async def read_product(request: Request, product_id: int):
    query = products.select().where(products.c.id == product_id)
    product = pd.DataFrame([p for p in await database.fetch_all(query)]).to_html(index=False)
    return templates.TemplateResponse("products.html", {"request": request, "product": product})


@router.put("/{product_id}", response_model=Product)
async def update_product(product_id: int, new_product: ProductIn):
    query = products.update().where(products.c.id == product_id).values(**new_product.model_dump())
    await database.execute(query)
    return {**new_product.model_dump(), "id": product_id}


@router.delete("/{product_id}", response_model=Product)
async def delete_user(product_id: int):
    removed = products.select().where(products.c.id == product_id)
    query = products.delete().where(products.c.id == product_id)
    result = await database.fetch_one(removed)
    await database.execute(query)
    return result
