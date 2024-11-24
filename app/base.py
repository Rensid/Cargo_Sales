from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData
from sqlalchemy_utils import create_database, database_exists
from app.config import settings


class DataBaseManager():
    def __init__(self, db_url: str, sync_db_url: str):
        self.db_url = db_url
        self.sync_db_url = sync_db_url
        self.metadata = MetaData()
        self.Base = declarative_base(metadata=self.metadata)
        self.engine = create_async_engine(self.db_url)
        self.async_session_maker = async_sessionmaker(
            bind=self.engine, expire_on_commit=False)
        if not database_exists(self.sync_db_url):
            create_database(self.sync_db_url)

    async def init_models(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(self.Base.metadata.create_all)

    async def get_async_session(self):
        async with self.async_session_maker() as session:
            yield session


main_database = DataBaseManager(db_url=f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}",
                                sync_db_url=f"postgresql://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")
