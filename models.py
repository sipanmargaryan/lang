from sqlalchemy import String, Integer, ForeignKey, Column
from sqlalchemy.orm import declarative_base


Base = declarative_base()




class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    price = Column(Integer)


class ShoppingCard(Base):
    __tablename__ = "shopping_card"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'))