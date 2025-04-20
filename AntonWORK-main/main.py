
import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
import aiohttp
from dotenv import load_dotenv, find_dotenv

from DataBase.Engine import session1, delete_db, create_db
from MiddleWare.middleware_session import DataBaseSession
from Handlers.user import user_router_n1
from Handlers.user_group import user_group_router_n1
from Handlers.admin_private import admin_router_n1
from Handlers.user2 import user_router_n2

# Загрузка переменных окружения
load_dotenv(find_dotenv())

# Создание бота и диспетчера
bot = Bot(token=os.getenv('TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
bot.my_admins_list = [7594226139]
DP = Dispatcher()
DP.include_router(user_router_n1)
DP.include_router(user_router_n2)
DP.include_router(user_group_router_n1)
DP.include_router(admin_router_n1)

# Переменная для хранения сессии aiohttp
session = None

async def on_startup(dispatcher: Dispatcher):#к чему относится эта функция(к началу раюоты диспетчера(а точнее его подметода polling))
    global session
    session = aiohttp.ClientSession()  # Создание aiohttp сессии (Открываем свою сессию (aiohttp.ClientSession))
    await create_db()  # Подключение к базе данных, если требуется создание

async def on_shutdown(dispatcher: Dispatcher):
    await session.close()  # Закрытие aiohttp сессии(А тута закрываем ее) если ее не закрыть вылезет ошибка ол сессия клиентская не закрыта
    await delete_db()  # Отключение от базы данных (если требуется удаление)

async def main():
    DP.update.middleware(DataBaseSession(session_pool=session1))# Те у нас сначала начинает работать engine and sessionmaker собствно сесия сразу пробрасывается везде,чтоб когда начался поллинг хендлеры УЖЕ ИМЕЛИ сессию
    #В проивном случае начнется поллинг,и сесия пробросится только тогда когда поллинг закончится(on_shutdown) ,тк это продолжительное действие сначала выполнится оно а пото начнет выполняться след идущее
    await create_db()
    await DP.start_polling(bot, on_startup=on_startup, on_shutdown=on_shutdown)
    
if __name__ == '__main__':
    asyncio.run(main())