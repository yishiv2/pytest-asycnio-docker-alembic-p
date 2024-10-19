from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from myapp.models import Item


class ItemRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_item(self, name: str) -> Item:
        item = Item(name=name)
        self.session.add(item)
        await self.session.commit()
        await self.session.refresh(item)
        return item

    async def get_item(self, item_id: int) -> Item:
        result = await self.session.execute(select(Item).where(Item.id == item_id))
        return result.scalar_one_or_none()
