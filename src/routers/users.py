from fastapi import APIRouter, HTTPException
from src.models.schemas import UserIn, UserOut
from src.models.store_models import database, users
from typing import List

# Передаю приложение через декоратор router с префиксом и тагом
router = APIRouter(prefix="/users", tags=["users"])


# User CRUD operations
# Создание пользователя
@router.post("/", response_model=UserOut)
async def create_user(user: UserIn):
    query = users.insert().values(**user.model_dump())
    record_id = await database.execute(query)
    return {**user.model_dump(), "id": record_id}


# Получение конкретного пользователя
@router.get("/{user_id}", response_model=UserOut)
async def read_user(user_id: int):
    query = users.select().where(users.c.id == user_id)
    user = await database.fetch_one(query)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# Получение всех пользователей с условием от 0 до 10
@router.get("/", response_model=List[UserOut])
async def read_users(skip: int = 0, limit: int = 10):
    query = users.select().offset(skip).limit(limit)
    return await database.fetch_all(query)


# Изменить данные пользователя по его id
@router.put("/{user_id}", response_model=UserOut)
async def update_user(user_id: int, new_user: UserIn):
    if "model_dump" not in dir(new_user):
        raise HTTPException(status_code=400, detail="Invalid request body")
    query = users.update().where(users.c.id == user_id).values(**new_user.model_dump())
    await database.execute(query)
    return {**new_user.model_dump(), "id": user_id}


# Удаление пользователя из бд
@router.delete("/{user_id}", response_model=UserOut)
async def delete_user(user_id: int):
    query = users.select().where(users.c.id == user_id)
    user = await database.fetch_one(query)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    delete_query = users.delete().where(users.c.id == user_id)
    await database.execute(delete_query)
    return user
