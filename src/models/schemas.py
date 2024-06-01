from pydantic import BaseModel, Field


class UserIn(BaseModel):
    first_name: str = Field(max_length=40)
    last_name: str = Field(max_length=80)
    email: str = Field(max_length=120)
    password: str = Field(min_length=6)


class User(UserIn):
    id: int


class ProductIn(BaseModel):
    title: str = Field(max_length=80)
    description: str = Field(max_length=512)
    price: float = Field(gt=0, le=999999)


class Product(BaseModel):
    id: int
    title: str = Field(max_length=80)
    description: str = Field(max_length=512)
    price: float = Field(gt=0, le=999999)


# модель используется только при создании и обновлении заказа
class OrderIn(BaseModel):
    status: str = Field(default="Создан")


class Order(BaseModel):
    id: int
    date: str
    status: str = Field(default="Создан")
    user_id: int = Field(foreign_key=True)
    product_id: int = Field(foreign_key=True)
