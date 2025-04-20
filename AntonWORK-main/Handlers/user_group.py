from string import punctuation
from aiogram.filters import Command

from aiogram import F, types, Router,Bot
import time
from filters.Chat_Types import my_class
user_group_router_n1 = Router()
user_group_router_n1.message.filter(my_class(['group', 'supergroup']))
user_group_router_n1.edited_message.filter(my_class(['group', 'supergroup']))


restricted_words = {'димаизмаилов', 'хомяк', 'блять'}
def clean_text(text: str):
    return text.translate(str.maketrans('', '', punctuation))


@user_group_router_n1.message(Command('admin'))
async def admin_append(message: types.Message,bot:Bot):
    id_chat = message.chat.id
    admins_list = await bot.get_chat_administrators(id_chat)
    admins_list_Ids = [member.user.id for member in admins_list if member.status == 'creator' or 'administrator']#id
    print(admins_list_Ids)

    bot.my_admins_list = admins_list_Ids
    print('1')
    if message.from_user.id in admins_list_Ids:
        print('2')
        await message.delete()
        print(f'{bot.my_admins_list},папа')
        print('3')


#@user_group_router_n1.edited_message()
#@user_group_router_n1.message()
#async def d1(message: types.Message):
    #if restricted_words.intersection(clean_text(message.text.lower()).split()):
           # msg = await message.answer(f"{message.from_user.first_name}, соблюддайте порядок в чате!")
            #await message.delete()
            #time.sleep(5)
            #await msg.delete()
         