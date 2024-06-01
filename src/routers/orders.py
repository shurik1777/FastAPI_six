from datetime import datetime
from fastapi import Request, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pandas as pd
from src.models.schemas import Order, OrderIn
from src.models.store_models import database, orders

router = APIRouter(prefix="/orders", tags=["orders"])
templates = Jinja2Templates(directory='templates')


@router.post("/{user_id}/{product_id}", response_model=OrderIn)
async def create_order(user_id: int, product_id: int, order: OrderIn):
    query = orders.insert().values(date=datetime.now().strftime("%d/%m/%y, %H:%M:%S"), status=order.status,
                                   user_id=user_id, product_id=product_id)
    record_id = await database.execute(query)
    return {**order.model_dump(), "id": record_id}


@router.get("/", response_class=HTMLResponse)
async def read_order(request: Request):
    query = orders.select()
    orders_table = pd.DataFrame([order for order in await database.fetch_all(query)]).to_html(index=False)
    return templates.TemplateResponse("orders.html", {"request": request, "orders_table": orders_table})


@router.get("/{order_id}", response_model=Order)
async def update_order(request: Request, order_id: int):
    query = orders.select().where(orders.c.id == order_id)
    order = pd.DataFrame([o for o in await database.fetch_all(query)]).to_html(index=False)
    return templates.TemplateResponse("orders.html", {"request": request, "order": order})


@router.put("/{order_id}", response_model=OrderIn)
async def update_order(order_id: int, new_order: OrderIn):
    query = orders.update().where(orders.c.id == order_id).values(date=datetime.now().strftime("%d/%m/%y, %H:%M:%S"),
                                                                  status=new_order.status)
    await database.execute(query)
    return {**new_order.model_dump(), "id": order_id}


@router.delete("/{order_id}", response_model=Order)
async def delete_order(order_id: int):
    removed = orders.select().where(orders.c.id == order_id)
    query = orders.delete().where(orders.c.id == order_id)
    result = await database.fetch_one(removed)
    await database.execute(query)
    return result
