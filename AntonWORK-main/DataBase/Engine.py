
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker,create_async_engine
from DataBase.Models_for_DataBase import Base
from DataBase.orm_query import orm_add_banner_description, orm_create_categories
from Texts.Welcome import categories, description_for_info_pages
engine = create_async_engine(url="postgresql+asyncpg://bot:bot@localhost:5432/bot",echo = True)#эхо дублирует запросы  в терминал
session1 = async_sessionmaker(bind=engine,class_=AsyncSession,expire_on_commit=False)#чтобы можно было делать не один запрос


async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    async with session1() as session:
        await orm_create_categories(session, categories)
        await orm_add_banner_description(session, description_for_info_pages)
async def delete_db():
    async with engine.begin() as engine_start:
        await engine_start.run_sync(Base.metadata.drop_all)
        