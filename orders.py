from datetime import datetime
from random import randint

from fastapi import APIRouter, HTTPException
from typing import List

import db
import models

router = APIRouter()


@router.get("/fake_orders/{count}")
async def create_note(count: int):
    for i in range(count):
        query = db.orders.insert().values(user_id=randint(1, 20), prod_id=randint(1, 20), status="created",
                                          date=datetime.now())
        await db.database.execute(query)
    return {'message': f'{count} fake orders create'}


@router.get("/orders/", response_model=List[models.OrderRead])
async def read_orders():
    query = db.orders.select()
    return await db.database.fetch_all(query)


@router.get("/orders/{order_id}", response_model=models.OrderRead)
async def read_order(order_id: int):
    query = db.orders.select().where(db.orders.c.id == order_id)
    order = await db.database.fetch_one(query)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.delete("/orders/{order_id}")
async def delete_order(order_id: int):
    query = db.orders.delete().where(db.orders.c.id == order_id)
    await db.database.execute(query)
    return {'message': 'Order deleted'}
