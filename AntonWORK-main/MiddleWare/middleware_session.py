from typing import Any,Awaitable,Callable,Dict
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import async_sessionmaker
class DataBaseSession(BaseMiddleware):
    def __init__(self,session_pool:async_sessionmaker):#аннотация типов в тип сешн мейкер
        self.session_pool =  session_pool
    async def __call__(self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]], event: TelegramObject, data: Dict[str, Any]):
        async with self.session_pool() as session:
            data['session'] = session#словарь:под ключевым знамением словаря data по его ключу(заменяет индексы списка) будет находится сессия(data = {'session':session})
            #тут можно добавить еще информацию в словарь дикт для передачи в каждый хендлер
            return await handler(event,data)
        