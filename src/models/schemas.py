import bcrypt
from pydantic import BaseModel, Field, EmailStr, validator


class UserIn(BaseModel):
    first_name: str = Field(max_length=40)
    last_name: str = Field(max_length=80)
    email: EmailStr = Field(..., max_length=50)
    password: str = Field(max_length=128)

    @validator('password')
    def hash_password(cls, value):
        return bcrypt.hashpw(value.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


class UserOut(BaseModel):
    id: int
    first_name: str
    email: EmailStr

    class Config:
        from_attributes = True


class ProductIn(BaseModel):
    title: str = Field(max_length=80)
    description: str = Field(max_length=512)
    price: float = Field(gt=0, le=999999)


class ProductOut(BaseModel):
    id: int
    title: str = Field(max_length=80)
    description: str = Field(max_length=512)
    price: float = Field(gt=0, le=999999)

    class Config:
        from_attributes = True


# модель используется только при создании и обновлении заказа
class OrderIn(BaseModel):
    status: str = Field(default="Создан")


class Order(BaseModel):
    id: int
    date: str
    status: str = Field(default="Создан")
    user_id: int = Field(foreign_key=True)
    product_id: int = Field(foreign_key=True)

    class Config:
        from_attributes = True
