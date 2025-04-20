#Импортируем все нужные нам библиотеки и фреймворки.
from aiogram import types,Router,F
from aiogram.filters import Command,CommandStart, or_f,and_f
from string import punctuation 
import asyncio
import time
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.enums import ParseMode
from aiogram.methods import send_location
from aiogram.utils.formatting import as_list, as_marked_section, Bold
from DataBase.orm_query import orm_add_to_cart, orm_add_user, orm_delete_from_cart, orm_get_caregory_id, orm_get_carts, orm_get_money, orm_get_price_of_product, orm_inventory_add, orm_money_add, orm_money_minus
from Handlers.Menu_progress import get_menu_content, main_menu
from Keyboard.Inline_Keyboard import MenuCallBack
from filters.Chat_Types import my_class,test_mat
from Keyboard import REPLY_KEYBOARD
from Base.Loc_name import Purse
restricted_words = {'димаизмаилов', 'хомяк', 'блять','cука','eбaть'}
Avalaible_Types_for_private = ['private']
user_router_n1 = Router()  
user_router_n1.message.filter(my_class(Avalaible_Types_for_private))
user_router_n1.message.filter(test_mat(restricted_words))#return true or false

class Money:
    def __init__(self):
        self.dict = {}
        try:# если не эта штука то когда второй пользователь жмет поднять бабла сбрасывается список со всеми пользователями их кликами(ДАЖЕ КОГДА ДРУГОЙ ПОЛЬЗОВАТЕЛЬ В ЭТО ВРЕМЯ КЛИКАЕТ(ЕГО СЧЕТЧИК КЛИКОВ ДО 10 ОБНУЛИТСЯ(НАЧНЕТСЯ ЗАНОВО С 0))
            if res:
                self.dict=res
                
        except Exception:
            pass
        self.clicks = 0
        self.clicks1 = 0  #await orm_get_money(session=session,user_id1=user_id)


    def __call__(self):
        pass
    async def gg(self,session,user_id):
        if user_id not in self.dict:
            print('not in')
            
            self.dict[user_id] = self.clicks
            self.dict[f'{user_id}fullmoney'] = self.clicks1
            
        self.dict[user_id]=self.dict.get(user_id)+1
        
        

        
        

        if  self.dict.get(user_id) == 10:
            await orm_money_add(count=10,session=session,user_id=user_id)
            self.dict[user_id] = 0
            self.dict[f'{user_id}fullmoney']  += 10
            return {f'{user_id}fullmoney': self.dict[f'{user_id}fullmoney'],user_id:10}
        else:
            return self.dict
    
        
@user_router_n1.message(CommandStart())
async def start_cmd(message: types.Message, session: AsyncSession):
    user = message.from_user
    await orm_add_user(
        session,
        user_id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        phone=None,
    )
    media, reply_markup = await get_menu_content(session, level=0, menu_name="main")
    
    await message.answer_photo(media.media, caption=media.caption, reply_markup=reply_markup)

#эта функция запускается через главную(в самом низу)
async def add_to_cart(callback: types.CallbackQuery, callback_data: MenuCallBack, session: AsyncSession):
    user = callback.from_user
    await orm_add_to_cart(session, user_id=user.id, product_id=callback_data.product_id)
    await callback.answer("Товар добавлен в корзину.")


    
    
        
@user_router_n1.callback_query(MenuCallBack.filter())#принимает абсолютна любой колбек(через нее(эту функцию) меняются менюшки)
async def user_menu(callback: types.CallbackQuery, callback_data: MenuCallBack, session: AsyncSession):
    full_money = 0
    progress_money =0
   
    # if callback_data.menu_name == 'money':
    #     k(callback=callback)
   
    if callback_data.menu_name ==  'money':   
        global Click 
        
        Click = Money()#ОТКРЫВАЕМ(ЗАПУСКАЕМ КЛАСС)
        
    if callback_data.menu_name ==  'money1':
        # Click = Money()
        await callback.answer()
        global res             
        res = await Click.gg(session=session,user_id=callback.from_user.id) 
        if res != None:
            progress_money = res[callback.from_user.id]
        else:
            progress_money = 0
            print('nononono try')
        
    if callback_data.menu_name == "add_to_cart":#(если колбек из MenuCallBack имеет название менюшки купить(add_to_cart))
        await add_to_cart(callback, callback_data, session)
        return
    
    if callback_data.menu_name == 'order':
        # price_to_pay = await orm_get_price_of_product(session=session,product_id1=callback_data.product_id)
        
        carts = await orm_get_carts(session)
        suma=  round(
            sum(cart.quantity * cart.product.price for cart in carts), 2#в каждой корзине( for cart in carts ) разный продукт и его цена
        )
        total = (cart.product.id for cart in carts)
        if await orm_money_minus(session=session,count=suma,user_id=callback.from_user.id) == True:
            category =await orm_get_caregory_id(session,product_id=callback_data.product_id)
            await orm_inventory_add(session=session,user_id=callback.from_user.id,product_id=callback_data.product_id,category=category)
            await callback.answer("Товар добавлен в инвентарь.")
            for i in total:
                cat_last = await orm_get_caregory_id(session=session,product_id=i)
                await orm_inventory_add(session=session,user_id=callback.from_user.id,product_id=i,category=cat_last)
                await orm_delete_from_cart(session=session,user_id=callback.from_user.id,product_id=i)
            
        else:
            await callback.answer("Недостаточно средств.")
            return 
   
    if callback_data.level == 2 or callback_data.level == 3:
        full_money = await orm_get_money(session=session,user_id1=callback.from_user.id)
                
    print(full_money,'asadadsadasdasd')
    media, reply_markup = await get_menu_content(
        session,
        level=callback_data.level,
        menu_name=callback_data.menu_name,
        category=callback_data.category,
        page=callback_data.page,
        product_id=callback_data.product_id,
        user_id=callback.from_user.id,
        full_money = full_money,
        progress_money =  progress_money
    )
    await callback.message.edit_media(media=media, reply_markup=reply_markup)#'перелистывание'
    await callback.answer()









    




@user_router_n1.message(or_f(Command('keyboard'),F.text.lower().contains("клав")))
async def klava(message:types.Message):
    await message.answer('Ок',reply_markup=REPLY_KEYBOARD.kb1.as_markup(
                            resize_keyboard=True,
                            input_field_placeholder='Что Вас интересует?'))
locations = {}
@user_router_n1.message(F.location)
async def location_handler(message: types.Message):
    latitude = message.location.latitude
    longitude = message.location.longitude
    user_name = message.from_user.id
    str_user_name = str(user_name)
    locations = {}
    locations['latitude'] = latitude
    locations['longitude'] = longitude
    locations_for_write = [locations.get('latitude'),locations.get("longitude")]
    user_name=Purse(message=message,latitude=latitude,longitude=longitude,str_username=str_user_name)
    await user_name.answer_location(message=message,locations_for_write=locations_for_write)




@user_router_n1.message((F.text.lower().contains('привет')))
async def Privet_contain(message:types.Message):
    await acc(message)
            
async def acc(message: types.Message):
    if restricted_words.intersection(clean_text(message.text.lower()).split()): 
        msg = await message.answer(f"{message.from_user.first_name}, соблюддайте порядок в чате!")
        await message.delete()
        time.sleep(5)
        await msg.delete()
    else:
        await message.answer("Привет,дружище!!!")





def clean_text(text: str):
    return text.translate(str.maketrans('', '', punctuation))   





#@user_router_n1.edited_message()
#@user_router_n1.message()
#async def d1(message: types.Message):
    #if restricted_words.intersection(clean_text(message.text.lower()).split()):
            #msg = await message.answer(f"{message.from_user.first_name}, соблюддайте порядок в чате!")
            #await message.delete()
            #time.sleep(5)
            #await msg.delete()
    
         
    




