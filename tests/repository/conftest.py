import time
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import subprocess

import os
from alembic.config import Config


def run_migrations(db_url):
    # テストのルートディレクトリを取得
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', ".."))
    
    # alembic.ini のパスを作成
    alembic_ini_path = os.path.join(project_root, "alembic.ini")

    alembic_cfg = Config(alembic_ini_path)
    alembic_cfg.set_main_option("sqlalchemy.url", db_url)
    
    # Alembicマイグレーションを実行
    # subprocess.run(["alembic", "upgrade", "head"], cwd=project_root, check=True)
    result = subprocess.run(["alembic", "upgrade", "head"], cwd=project_root, check=True, capture_output=True)
    print(result.stdout.decode())
    print(result.stderr.decode())

@pytest_asyncio.fixture(scope="session",autouse=True)
async def start_mysql_container():
    """Docker ComposeでMySQLコンテナを起動し、接続情報を返す"""
    # Docker Composeを起動
    subprocess.run(["docker-compose", "-f", "tests/test_docker-compose.yml", "up", "-d"], check=True)

    # コンテナの起動を待つ
    time.sleep(30)  # 必要に応じて調整

    # MySQLの接続URLを返す
    database_url = "mysql+aiomysql://testuser:testpassword@127.0.0.1:3307/pytestdb"

    # マイグレーションを実行
    run_migrations(database_url)
    
    yield database_url

    # テストセッション後、コンテナを停止
    subprocess.run(["docker-compose", "-f", "tests/test_docker-compose.yml", "down"], check=True)


@pytest_asyncio.fixture(scope="function")
# async def db_session():
async def db_session(start_mysql_container, request):
    """テストごとに新しいDBセッションを作成する"""
    # database_url = start_mysql_container
    database_url = "mysql+aiomysql://testuser:testpassword@127.0.0.1:3307/pytestdb"
    engine = create_async_engine(database_url, future=True, echo=True)
    async_session = sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        test_data = request.param
        if test_data:
            session.add_all(test_data)
        await session.flush()
        yield session
        await session.rollback()
        await session.close()

    await engine.dispose() #RuntimeError: Event loop is closed を回避
