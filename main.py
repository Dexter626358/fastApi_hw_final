import uvicorn
from fastapi import FastAPI, HTTPException
import db
import orders, users, products


app = FastAPI()


@app.on_event("startup")
async def startup():
    await db.database.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.database.disconnect()


app.include_router(users.router, tags=["users"])
app.include_router(orders.router, tags=["orders"])
app.include_router(products.router, tags=["products"])


@app.get("/")
def root():
    return {"Message": "Hello"}


if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
