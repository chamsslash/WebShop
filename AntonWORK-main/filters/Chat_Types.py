from typing import Any
from aiogram.filters import Filter
from aiogram import types
from aiogram import Bot, types
from string import punctuation
my_owner = [7594226139]
class my_class(Filter):
    def __init__(self,chat_types: list[str]):
        self.chat_types = chat_types
    async def __call__(self,message:types.Message):
        return message.chat.type in self.chat_types
class isaAdmin(Filter):
    def __init__(self):
        pass
    async def __call__(self,message: types.Message, bot: Bot):
        return message.from_user.id in bot.my_admins_list or my_owner                   #фильтры возвращают true or false\
class test_mat(Filter):
    def __init__(self,restricted_words: set[str]):
        self.restricted_words = restricted_words
    async def __call__(self,message: types.Message):
            try:
                if self.restricted_words.intersection(clean_text(message.text.lower()).split()) :#types.ContentType.Text
           
                    print(1)
                    return False
                else:
                    print(2)
                    return True
            except Exception:
                return True
class test_mat2(Filter):
    def __init__(self,restricted_words: set[str]):
        self.restricted_words = restricted_words
    async def __call__(self,message: types.Message):
        try:
            if self.restricted_words.intersection(clean_text(message.text.lower()).split()):
                print(1)
                return True
            else:
                print(2)
                return False
        except Exception:
            return True
            #except Exception:
                #return True

def clean_text(text: str):
    return text.translate(str.maketrans('', '', punctuation))     
