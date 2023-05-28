import datetime

from sqlalchemy import Column
from sqlalchemy import String, event

from app.helpers.database import BaseDBModel




class Product(BaseDBModel):
    __tablename__ = "products"

    name = Column(String)
    description = Column(String)
    price = Column(String)


@event.listens_for(Product, 'before_update')
def receive_before_update(mapper, connection, target):
    target.updated_at = datetime.datetime.utcnow()