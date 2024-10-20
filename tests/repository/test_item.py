import pytest
from sqlalchemy import text
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


# 共通データの追加
# item1 = Item(name="Common Item 1")
# item2 = Item(name="Common Item 2")
# db_session.add_all([item1, item2])
# await db_session.commit()

# assert (
#     await db_session.execute("SELECT COUNT(*) FROM items").scalar() == 2
# )  # 共通データを追加したので2つになる


# @pytest.mark.parametrize("db_session", [[Item(name="Custom Item 1")]], indirect=True)
# @pytest.mark.asyncio
# async def test_with_custom_data(db_session):
#     # 各テスト専用の初期データを使用するテスト
#     assert (
#         await db_session.execute("SELECT COUNT(*) FROM items").scalar() == 1
#     )  # テストデータが1つだけのはず


# @pytest.mark.parametrize("db_session", [[Item(name="Combined Item 1")]], indirect=True)
# @pytest.mark.asyncio
# async def test_with_combined_data(db_session):
#     # 共通データと各テスト専用データを利用するテスト
#     item1 = Item(name="Common Item 1")
#     item2 = Item(name="Common Item 2")
#     db_session.add_all([item1, item2])
#     await db_session.commit()

#     assert (
#         await db_session.execute("SELECT COUNT(*) FROM items").scalar() == 3
#     )  # 共通データ2つ + テストデータ1つ
