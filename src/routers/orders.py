from datetime import datetime
from fastapi import APIRouter, HTTPException
from src.models.schemas import Order, OrderIn
from src.models.store_models import database, orders
from typing import List

# Передаю приложение через декоратор router с префиксом и тагом
router = APIRouter(prefix="/orders", tags=["orders"])


# Order CRUD operations
# Создание заказа
@router.post("/{user_id}/{product_id}", response_model=OrderIn)
async def create_order(user_id: int, product_id: int, order: OrderIn):
    query = orders.insert().values(date=datetime.now().strftime("%d/%m/%y, %H:%M:%S"), status=order.status,
                                   user_id=user_id, product_id=product_id)
    record_id = await database.execute(query)
    return {**order.model_dump(), "id": record_id}


# Получение конкретного заказа
@router.get("/orders/{order_id}", response_model=Order)
async def read_order(order_id: int):
    query = orders.select().where(orders.c.id == order_id)
    order = await database.fetch_one(query)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


# Получение всех заказов с условием от 0 до 10
@router.get("/", response_model=List[Order])
async def read_orders(skip: int = 0, limit: int = 10):
    query = orders.select().offset(skip).limit(limit)
    return await database.fetch_all(query)


# Изменить данные заказа по его id
@router.put("/{order_id}", response_model=Order)
async def update_order(order_id: int, new_order: OrderIn):
    query = orders.update().where(orders.c.id == order_id).values(date=datetime.now().strftime("%d/%m/%y, %H:%M:%S"),
                                                                  status=new_order.status)
    await database.execute(query)
    return {**new_order.model_dump(), "id": order_id}


# Удалить заказ из бд
@router.delete("/{order_id}", response_model=Order)
async def delete_order(order_id: int):
    query = orders.select().where(orders.c.id == order_id)
    order = await database.fetch_one(query)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    delete_query = orders.delete().where(orders.c.id == order_id)
    await database.execute(delete_query)
    return order
