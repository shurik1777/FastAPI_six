from fastapi import Request, APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pandas as pd
from src.models.schemas import User, UserIn
from src.models.store_models import database, users

router = APIRouter(prefix="/users", tags=["users"])
templates = Jinja2Templates(directory='templates')


@router.post("/", response_model=User)
async def create_user(user: UserIn):
    query = users.insert().values(**user.model_dump())
    record_id = await database.execute(query)
    return {**user.model_dump(), "id": record_id}


@router.get("/", response_class=HTMLResponse)
async def read_users(request: Request):
    query = users.select()
    users_table = pd.DataFrame([user for user in await database.fetch_all(query)]).to_html(index=False)
    return templates.TemplateResponse("users.html", {"request": request, "users_table": users_table})


@router.get("/{user_id}", response_model=User)
async def read_user(request: Request, user_id: int):
    query = users.select().where(users.c.id == user_id)
    user = pd.DataFrame([u for u in await database.fetch_all(query)]).to_html(index=False)
    return templates.TemplateResponse("users.html", {"request": request, "user": user})


@router.put("/{user_id}", response_model=User)
async def update_user(user_id: int, new_user: UserIn):
    if "model_dump" not in dir(new_user):
        raise HTTPException(status_code=400, detail="Invalid request body")
    query = users.update().where(users.c.id == user_id).values(**new_user.model_dump())
    await database.execute(query)
    return {**new_user.model_dump(), "id": user_id}


@router.delete("/{user_id}", response_model=User)
async def delete_user(user_id: int):
    removed = users.select().where(users.c.id == user_id)
    query = users.delete().where(users.c.id == user_id)
    result = await database.fetch_one(removed)
    await database.execute(query)
    return result
