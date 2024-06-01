from datetime import datetime
import databases
import sqlalchemy as sa
from settings import settings

DATABASE_URL = settings.DATABASE_URL
database = databases.Database(DATABASE_URL)
metadata = sa.MetaData()

users = sa.Table(
    "users",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("first_name", sa.String(32)),
    sa.Column("last_name", sa.String(32)),
    sa.Column("email", sa.String(128)),
    sa.Column("password", sa.String(32)),
)

products = sa.Table(
    "products",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("title", sa.String(80)),
    sa.Column("description", sa.String(300)),
    sa.Column("price", sa.Float),
)

# дата и время заказа будут обновляться автоматически при изменении статуса заказа, заказ создаётся в статусе "Создан"
orders = sa.Table(
    "orders",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("date", sa.String(64), nullable=False, default=datetime.now().strftime("%d/%m/%y, %H:%M:%S"),
              onupdate=datetime.now().strftime("%d/%m/%y, %H:%M:%S")),
    sa.Column("status", sa.String(8), nullable=False, server_default="Создан"),
    sa.Column("user_id", sa.Integer, sa.ForeignKey('users.id'), nullable=False),
    sa.Column("product_id", sa.Integer, sa.ForeignKey('products.id'), nullable=False),
)

engine = sa.create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

metadata.create_all(engine)
