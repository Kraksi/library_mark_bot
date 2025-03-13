import os
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine 


engine = create_async_engine(os.getenv('DB_MARIA'), echo = True)
session_maker = async_sessionmaker(bind = engine, class_= AsyncSession, expire_on_commit=False)

#async def con():

