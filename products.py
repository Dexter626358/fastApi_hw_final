from random import randint
from fastapi import APIRouter, HTTPException
from typing import List
import db
import models

router = APIRouter()


@router.get("/fake_products/{count}")
async def create_note(count: int):
    for i in range(count):
        query = db.products.insert().values(title=f'product {i}', description=f'all about product {i}',
                                            price=randint(1, 100000))
        await db.database.execute(query)
    return {'message': f'{count} fake products create'}


@router.get("/products/", response_model=List[models.ProductRead])
async def read_products():
    query = db.products.select()
    return await db.database.fetch_all(query)


@router.get("/products/{product_id}", response_model=models.ProductRead)
async def read_product(product_id: int):
    query = db.products.select().where(db.products.c.id == product_id)
    product = await db.database.fetch_one(query)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.put("/products/{product_id}", response_model=models.ProductRead)
async def update_product(product_id: int, new_product: models.ProductCreate):
    query = db.products.update().where(db.products.c.id == product_id).values(**new_product.dict())
    await db.database.execute(query)
    return {**new_product.dict(), "id": product_id}


@router.put("/orders/{order_id}", response_model=models.OrderRead)
async def update_order(order_id: int, new_order: models.OrderCreate):
    query = db.orders.update().where(db.orders.c.id == order_id).values(**new_order.dict())
    await db.database.execute(query)
    return {**new_order.dict(), "id": order_id}


@router.delete("/products/{product_id}")
async def delete_product(product_id: int):
    query = db.products.delete().where(db.products.c.id == product_id)
    await db.database.execute(query)
    return {'message': 'Product deleted'}
