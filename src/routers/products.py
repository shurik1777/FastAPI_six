from fastapi import APIRouter, HTTPException
from src.models.schemas import ProductOut, ProductIn
from src.models.store_models import database, products
from typing import List

# Передаю приложение через декоратор router с префиксом и тагом
router = APIRouter(prefix="/products", tags=["products"])


# Product CRUD operations
# Создание продукта
@router.post("/", response_model=ProductOut)
async def create_product(product: ProductIn):
    query = products.insert().values(**product.model_dump())
    record_id = await database.execute(query)
    return {**product.model_dump(), "id": record_id}


# Получение конкретного продукта
@router.get("/{product_id}", response_model=ProductOut)
async def read_product(product_id: int):
    query = products.select().where(products.c.id == product_id)
    product = await database.fetch_one(query)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


# Получение всех продуктов с условием от 0 до 10
@router.get("/", response_model=List[ProductOut])
async def read_products(skip: int = 0, limit: int = 10):
    query = products.select().offset(skip).limit(limit)
    return await database.fetch_all(query)


# Изменить данные продукта по его id
@router.put("/{product_id}", response_model=ProductOut)
async def update_product(product_id: int, new_product: ProductIn):
    query = products.update().where(products.c.id == product_id).values(**new_product.model_dump())
    await database.execute(query)
    return {**new_product.model_dump(), "id": product_id}


# Удалить продукт из бд
@router.delete("/{product_id}", response_model=ProductOut)
async def delete_user(product_id: int):
    query = products.select().where(products.c.id == product_id)
    product = await database.fetch_one(query)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    delete_query = products.delete().where(products.c.id == product_id)
    await database.execute(delete_query)
    return product
