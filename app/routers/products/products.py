from typing import List
from fastapi import APIRouter, status

from app.helpers.database import get_db

from .schema import Product
from app.helpers.agents import get_products_list

router = APIRouter(
    prefix="/products",
    tags=["[products]"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
)


@router.get("/")
async def products_list(product: str) -> List[Product]:

    return get_products_list(product)

