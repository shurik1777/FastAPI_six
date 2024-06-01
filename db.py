import databases
from sqlalchemy import Column, Table, String, MetaData, Integer, ForeignKey, create_engine

from settings import settings

DATABASE_URL = settings.DATABASE_URL
database = databases.Database(DATABASE_URL)
metadata = MetaData()

users = Table("users", metadata,
              Column("id", Integer, primary_key=True),
              Column("name", String(32)),
              Column("surname", String(32)),
              Column("email", String(128)),
              Column("password", String(32)),
              )

products = Table("products", metadata,
                 Column("id", Integer, primary_key=True),
                 Column("title", String(50)),
                 Column("description", String(300)),
                 Column("price", Integer)
                 )

orders = Table("orders", metadata,
               Column("id", Integer, primary_key=True),
               Column("user_id", ForeignKey("users.id")),
               Column("prod_id", ForeignKey("products.id")),
               Column("date", String),
               Column("status", String(20))
               )

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)
