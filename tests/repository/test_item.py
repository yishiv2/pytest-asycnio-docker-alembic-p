import pytest
from myapp.repository import ItemRepository

@pytest.mark.parametrize("db_session", [None], indirect=True)
@pytest.mark.asyncio(loop_scope="function")
async def test_create_item(db_session):
    print(db_session)
    repo = ItemRepository(db_session)
    assert db_session.is_active  # セッションがアクティブか確認
    # アイテムを作成
    item_name = "Test Item"
    created_item = await repo.create_item(item_name)

    # 作成したアイテムのプロパティを確認
    assert created_item.name == item_name
    assert created_item.id is not None 
