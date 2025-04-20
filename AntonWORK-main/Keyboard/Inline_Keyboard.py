from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


class MenuCallBack(CallbackData, prefix="menu"):
    level: int#обязательный параметр колбека(те прокидываем его везде(даже там где он не меняется просто оставляем тем же))
    menu_name: str
    category: int | None = None
    page: int = 1
    product_id: int | None = None


def get_user_main_btns(*, level: int, sizes: tuple[int] = (2,)):#клава на основной странице
    keyboard = InlineKeyboardBuilder()
    btns = {
        "Товары 🍕": "catalog",
        "Корзина 🛒": "cart",
        "О нас ℹ️": "about",
        "Оплата 💰": "payment",
        "Доставка ⛵": "shipping",
        'Пополнение средств💲':'money',
        'Инвентарь📁':'inventory'
        }
    for text, menu_name in btns.items():
            if menu_name == 'catalog':#что передает кнопка(в нашем случае название след менюшки)
                keyboard.add(InlineKeyboardButton(text=text,
                        callback_data=MenuCallBack(level=level+1, menu_name=menu_name).pack()))#в  callback_data пакуем  большой MenuCallBack,состоящий из множества атрибутов
                        #отправяет на след уровень через колбек
            elif menu_name == 'cart':
                keyboard.add(InlineKeyboardButton(text=text,
                        callback_data=MenuCallBack(level=3, menu_name=menu_name).pack()))
                        #отправяет на 3й уровень через колбек
            elif menu_name == 'money':
                keyboard.add(InlineKeyboardButton(text=text,
                        callback_data=MenuCallBack(level=-1, menu_name= menu_name).pack()))
            elif menu_name == 'inventory':
                keyboard.add(InlineKeyboardButton(text=text,
                        callback_data=MenuCallBack(level=4, menu_name= menu_name).pack()))
            else:
                keyboard.add(InlineKeyboardButton(text=text,
                        callback_data=MenuCallBack(level=level, menu_name=menu_name).pack()))
                
    return keyboard.adjust(*sizes).as_markup()#сразу как маркап(не надо указывать в особенностях)



#Кнопки для меню после нажатия на каталог из главного меню
def get_user_catalog_btns(*, level: int, categories: list, sizes: tuple[int] = (2,)):
    keyboard = InlineKeyboardBuilder()

    keyboard.add(InlineKeyboardButton(text='Назад',
                callback_data=MenuCallBack(level=level-1, menu_name='main').pack()))
    keyboard.add(InlineKeyboardButton(text='Корзина 🛒',
                callback_data=MenuCallBack(level=3, menu_name='cart').pack()))
    #кнопки выбора категории
    for c in categories:
        keyboard.add(InlineKeyboardButton(text=c.name,
                callback_data=MenuCallBack(level=level+1, menu_name=c.name, category=c.id).pack()))
                #ведет на след уровень через колбек

    return keyboard.adjust(*sizes).as_markup()

def get_user_inventory_btns(*, level: int, categories: list, sizes: tuple[int] = (2,)):

    keyboard = InlineKeyboardBuilder()

    keyboard.add(InlineKeyboardButton(text='Выйти',
                callback_data=MenuCallBack(level=0, menu_name='main').pack()))
    
    for c in categories:
        keyboard.add(InlineKeyboardButton(text=c.name,
                callback_data=MenuCallBack(level=5, menu_name=c.name, category=c.id).pack()))#передает категорию в каталог где паджинатор работает
                #ведет на след уровень через колбек
    return keyboard.adjust(*sizes).as_markup()
#перелистывание страниц(редактировние сообщение как перелистывание)

def get_user_inventory_btns2(*, level: int,  sizes: tuple[int] = (1,),category: int,page: int,pagination_btns: dict,product_id: int):
    keyboard=InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='Назад',
                callback_data=MenuCallBack(level=level-1, menu_name='inventory').pack()))
    keyboard.add(InlineKeyboardButton(text='Удалить',
                callback_data=MenuCallBack(level=level, menu_name='delete1',product_id=product_id, page=page).pack()))
    keyboard.adjust(*sizes)
    row = []
    for text, menu_name in pagination_btns.items():#создание кнопок перелистывания страниц
        if menu_name == "next":
            row.append(InlineKeyboardButton(text=text,
                    callback_data=MenuCallBack(
                        level=level,
                        menu_name=menu_name,
                        category=category,
                        page=page + 1).pack()))#стр + 1(след)
        
        elif menu_name == "previous":
            row.append(InlineKeyboardButton(text=text,
                    callback_data=MenuCallBack(
                        level=level,
                        menu_name=menu_name,
                        category=category,
                        page=page - 1).pack()))#стр -1 (пред)

    return keyboard.row(*row).as_markup()#делает все эти  кнопки на один ряд
    #добавляет к нашим уже добавленным кнопкам еще ряд из кнопок(и возвращает это как результат функции)
    


#Кнопки для менб после выбора категории из пред уровня
def get_products_btns(
    *,
    level: int,
    category: int,
    page: int,
    pagination_btns: dict,
    product_id: int,
    sizes: tuple[int] = (2, 1)
):
    keyboard = InlineKeyboardBuilder()

    keyboard.add(InlineKeyboardButton(text='Назад',
                callback_data=MenuCallBack(level=level-1, menu_name='catalog').pack()))
                #кнопка назад ведет на пред уровень через колбек
    keyboard.add(InlineKeyboardButton(text='Корзина 🛒',
                callback_data=MenuCallBack(level=3, menu_name='cart').pack()))
                #переводит на 3й уровень сразу в корзину через колбек
    keyboard.add(InlineKeyboardButton(text='Купить 💵',
                callback_data=MenuCallBack(level=level, menu_name='add_to_cart', product_id=product_id).pack()))
                

    keyboard.adjust(*sizes)
#перелистывание страниц(редактировние сообщение как перелистывание)
    row = []
    for text, menu_name in pagination_btns.items():#создание кнопок перелистывания страниц
        if menu_name == "next":
            row.append(InlineKeyboardButton(text=text,
                    callback_data=MenuCallBack(
                        level=level,
                        menu_name=menu_name,
                        category=category,
                        page=page + 1).pack()))#стр + 1(след)
        
        elif menu_name == "previous":
            row.append(InlineKeyboardButton(text=text,
                    callback_data=MenuCallBack(
                        level=level,
                        menu_name=menu_name,
                        category=category,
                        page=page - 1).pack()))#стр -1 (пред)

    return keyboard.row(*row).as_markup()#делает все эти  кнопки на один ряд
    #добавляет к нашим уже добавленным кнопкам еще ряд из кнопок(и возвращает это как результат функции)
    
def get_clicker_keyboard(level,sizes: tuple[int] = (1,)):#кортеж из размеров
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='ЖМИ',
                        callback_data=MenuCallBack(level=level, menu_name='money1').pack()))
    keyboard.add(InlineKeyboardButton(text='Выйти',
                    callback_data=MenuCallBack(level=0, menu_name='main').pack()))
    return keyboard.adjust(*sizes).as_markup()
   #Клава для корзины 
def get_user_cart(
    *,
    level: int,
    page: int | None,
    pagination_btns: dict | None,
    product_id: int | None,
    sizes: tuple[int] = (3,)
):
    keyboard = InlineKeyboardBuilder()
    if page:
        #Удаление этой корзины(там будет в меню прогрессинге) (в функции)и уже из него вызов орм запроса с удалением))
        keyboard.add(InlineKeyboardButton(text='Удалить',
                    callback_data=MenuCallBack(level=level, menu_name='delete', product_id=product_id, page=page).pack()))
         #Уменьшение колва товар на 1 (отправка так же через колбек)
        keyboard.add(InlineKeyboardButton(text='-1',
                    callback_data=MenuCallBack(level=level, menu_name='decrement', product_id=product_id, page=page).pack()))
        #Увеличение колва товар на 1 (отправка так же через колбек)
        keyboard.add(InlineKeyboardButton(text='+1',
                    callback_data=MenuCallBack(level=level, menu_name='increment', product_id=product_id, page=page).pack()))

        keyboard.adjust(*sizes)
        # корзина показывается так же перелистыванием
        row = []
        for text, menu_name in pagination_btns.items():
            if menu_name == "next":
                row.append(InlineKeyboardButton(text=text,
                        callback_data=MenuCallBack(level=level, menu_name=menu_name, page=page + 1).pack()))
            elif menu_name == "previous":
                row.append(InlineKeyboardButton(text=text,
                        callback_data=MenuCallBack(level=level, menu_name=menu_name, page=page - 1).pack()))

        keyboard.row(*row)
        #еще один ряд кнопок с классич функциями
        row2 = [
        InlineKeyboardButton(text='На главную 🏠',
                    callback_data=MenuCallBack(level=0, menu_name='main').pack()),#отправляет на гл меню(0уровень)
        InlineKeyboardButton(text='Заказать',
                    callback_data=MenuCallBack(level=level, menu_name='order',product_id=product_id).pack()),#отправляет на гл меню(0уровень) ТК НЕ ДОРАБОТАНО
        ]
        return keyboard.row(*row2).as_markup()
    else:#корзин нет
        keyboard.add(
            InlineKeyboardButton(text='На главную 🏠',
                    callback_data=MenuCallBack(level=0, menu_name='main').pack()))
        
        return keyboard.adjust(*sizes).as_markup()







def get_callback_btns(
    *,
    btns: dict[str, str],
    sizes: tuple[int] = (2,)):

    keyboard = InlineKeyboardBuilder()

    for text, data in btns.items():
        
        keyboard.add(InlineKeyboardButton(text=text, callback_data=data))

    return keyboard.adjust(*sizes).as_markup()

    
    
def auto_inline_keyboard_builder_url(*,buttons: dict[str, str],sizes: tuple[int] = (2,)):

    keyboard = InlineKeyboardBuilder()

    for text, url in buttons.items():
        
        keyboard.add(InlineKeyboardButton(text=text, url=url))

    return keyboard.adjust(*sizes).as_markup()
    





def auto_Inline_keyboard_builder_mixed(*,
    btns: dict[str, str],
    sizes: tuple[int] = (2,)):

    keyboard = InlineKeyboardBuilder()

    for text, value in btns.items():
        if '://' in value:#проверка на юрл адрес
            keyboard.add(InlineKeyboardButton(text=text, url=value))
        else:
            keyboard.add(InlineKeyboardButton(text=text, callback_data=value))

    return keyboard.adjust(*sizes).as_markup()

