from filters.Chat_Types import my_class,test_mat2
from aiogram import types,Router,F

from string import punctuation 
import asyncio
import time
from aiogram.enums import ParseMode
restricted_words = {'димаизмаилов', 'хомяк', 'блять','cука','eбaть'}
user_router_n2 = Router()  
user_router_n2.message.filter(test_mat2(restricted_words))
@user_router_n2.message(F.text)
async def test_answer(message:types.Message):
    await message.answer('Это плохое слово')
    await message.delete()