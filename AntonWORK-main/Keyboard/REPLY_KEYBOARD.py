from aiogram.types import KeyboardButtonPollType, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove,InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder,InlineKeyboardBuilder

kb_start = ReplyKeyboardBuilder()
kb_start.add(KeyboardButton(text="start"))




kb_admin = ReplyKeyboardBuilder()
kb_admin.add(KeyboardButton(text='1'),
             KeyboardButton(text='2'),
             KeyboardButton(text='3'),
             KeyboardButton(text='ассортимент'),
             KeyboardButton(text='начать'))
kb_admin.adjust(2,2,1)



kb1 = ReplyKeyboardBuilder()
kb1.add(KeyboardButton(text='Меню'),
        KeyboardButton(text="Отправить локацию",request_location=True),
        KeyboardButton(text="Отправить номер",request_contact=True)
        )
kb1.adjust(1,2)
 
def get_keyboard(
    *btns: str,
    placeholder: str = None,
    request_contact: int = None,
    request_location: int = None,
    sizes: tuple[int] = (2,),
):
    '''
    Parameters request_contact and request_location must be as indexes of btns args for buttons you need.
    Example:
    get_keyboard(
            "Меню",
            "О магазине",
            "Варианты оплаты",
            "Варианты доставки",
            "Отправить номер телефона",
            placeholder="Что вас интересует?",
            request_contact=4,
            sizes=(2, 2, 1)
        )
    '''
    keyboard = ReplyKeyboardBuilder()

    for index, text in enumerate(btns, start=0):
        
        if request_contact and request_contact == index:
            keyboard.add(KeyboardButton(text=text, request_contact=True))

        elif request_location and request_location == index:
            keyboard.add(KeyboardButton(text=text, request_location=True))
        else:
            keyboard.add(KeyboardButton(text=text))

    return keyboard.adjust(*sizes).as_markup(
            resize_keyboard=True, input_field_placeholder=placeholder)