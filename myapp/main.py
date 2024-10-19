# myapp/main.py
from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from myapp.models import get_db

from .repository import ItemRepository

app = FastAPI()


@app.post("/items/")
async def create_item(name: str, db: AsyncSession = Depends(get_db)):
    repo = ItemRepository(db)
    return await repo.create_item(name)


@app.get("/items/{item_id}")
async def read_item(item_id: int, db: AsyncSession = Depends(get_db)):
    repo = ItemRepository(db)
    return await repo.get_item(item_id)
