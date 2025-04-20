from aiogram.types import InputMediaPhoto
from sqlalchemy.ext.asyncio import AsyncSession

from DataBase.orm_query import (
    orm_add_to_cart,
    orm_delete_from_cart,
    orm_delete_from_inventory,
    orm_get_all_inventory,
    orm_get_banner,
    orm_get_categories,
    orm_get_all_products,
    orm_get_price_of_product,
    orm_get_user_carts,
    orm_inventory_add,
    orm_money_add,
    orm_money_minus,
    orm_reduce_product_in_cart,
)
from Keyboard.Inline_Keyboard import (
    get_clicker_keyboard,
    get_products_btns,
    get_user_cart,
    get_user_catalog_btns,
    get_user_inventory_btns,
    get_user_inventory_btns2,
    get_user_main_btns,
)

from Paginator.Paginator import Paginator

# тут просто делается баннер(его внешна и клава) и возвращается
async def main_menu(session, level, menu_name,
                    ):#главное меню
    # if menu_name == 'order':
    #     price_to_pay = orm_get_price_of_product(session=session,product_id1=product_id)
    #     if orm_money_minus(session=session,count=price_to_pay) == True:
    #         await orm_inventory_add(session=session,user_id=user_id,product_id=product_id)
    #         await callback.answer("Товар добавлен в корзину.")
    #     else:
    #         callback
    banner = await orm_get_banner(session, menu_name)#мы по названию баннера из базы данных получаем описание этого баннера(за эти нам тут имя баннера main)
    image = InputMediaPhoto(media=banner.image, caption=banner.description)#внешка

    kbds = get_user_main_btns(level=level)

    return image, kbds

async def clicker(session, level, menu_name,progress_money:int):
    if  menu_name != 'money1':
        global banner,kbds
        
        banner = await orm_get_banner(session, menu_name)
        kbds = get_clicker_keyboard(level=level)
        image = InputMediaPhoto(media=banner.image, caption=banner.description + f'\nНачнем?')#внешка\
    if menu_name == 'money1':
        if progress_money==10:
            image = InputMediaPhoto(media=banner.image, caption=banner.description + f'\n                       Начислено 10 баксов')#внешка
        else:
            image = InputMediaPhoto(media=banner.image, caption=banner.description + f'\nПрогресс {progress_money} из 10')#внешка
        print(progress_money)
    
   
    return image,kbds

async def catalog(session, level, menu_name):
    banner = await orm_get_banner(session, menu_name)
    image = InputMediaPhoto(media=banner.image, caption=banner.description)
    #Прокидываем категории(из ьаблицы из базыданных) в клавиатуру
    categories = await orm_get_categories(session)
    kbds = get_user_catalog_btns(level=level, categories=categories)

    return image, kbds
async def inventory(session, level, menu_name):
    banner = await orm_get_banner(session, menu_name)
    image = InputMediaPhoto(media=banner.image, caption=banner.description)
    #Прокидываем категории(из ьаблицы из базыданных) в клавиатуру
    categories = await orm_get_categories(session)
    kbds = get_user_inventory_btns(level=level, categories=categories)

    return image, kbds





#создание кнопок после проверки из паджинатора
def pages(paginator: Paginator):
    btns = dict()
    if paginator.has_previous():
        btns["◀ Пред."] = "previous"

    if paginator.has_next():
        btns["След. ▶"] = "next"

    return btns

async def inventory1(session, level, category, page,user_id,menu_name,product_id):
    if menu_name == "delete1":
        await orm_delete_from_inventory(session=session, user_id=user_id, product_id=product_id)
        #если это первая страница то ничего не делать
        if page > 1:
            page -= 1#удалился товар ---> нас перебрасывает на пред страницу с товаром
    products = await orm_get_all_inventory(session,user_id=user_id,category_id = category)
    if not products:
        banner = await orm_get_banner(session, "inventory1")
        image = InputMediaPhoto(
            media=banner.image, caption=f"<strong>{banner.description}</strong>"
        )

        kbds = get_user_cart(
            level=level,
            page=None,
            pagination_btns=None,
            product_id=None,
        )
    else:
        paginator = Paginator(products, page=page)
        product = paginator.get_page()[0]

        image = InputMediaPhoto(
            media=product.product.image,
            caption=f"<strong>{product.product.name}\
                    </strong>\n{product.product.description}\nСтоимость: {round(product.product.price, 2)}\n\
                    <strong>Товар {paginator.page} из {paginator.pages}</strong>",
        )

        pagination_btns = pages(paginator)

        kbds = get_user_inventory_btns2(
            level=level,
            category=category,
            page=page,
            pagination_btns=pagination_btns,
            product_id=product.product_id,
        )
        #медиа и reply_markup
    return image, kbds


async def products(session, level, category, page,full_money:int):
    products = await orm_get_all_products(session, category_id=category)

    paginator = Paginator(products, page=page)
    product = paginator.get_page()[0]

    image = InputMediaPhoto(
        media=product.image,
        caption=f"<strong>{product.name}\
                </strong>\n{product.description}\nСтоимость: {round(product.price, 2)}\n\
                <strong>Товар {paginator.page} из {paginator.pages}</strong>\n <strong>                            Ваш бюджет: {full_money}</strong>")
    

    pagination_btns = pages(paginator)

    kbds = get_products_btns(
        level=level,
        category=category,
        page=page,
        pagination_btns=pagination_btns,
        product_id=product.id,
    )
    #медиа и reply_markup
    return image, kbds


async def carts(session, level, menu_name, page, user_id, product_id,full_money:int):
    if menu_name == "delete":
        await orm_delete_from_cart(session, user_id, product_id)
        #если это первая страница то ничего не делать
        if page > 1:
            page -= 1#удалился товар ---> нас перебрасывает на пред страницу с товаром
    elif menu_name == "decrement":
        is_cart = await orm_reduce_product_in_cart(session,user_id=user_id,product_id=product_id)
        if page > 1 and not is_cart:
            page -= 1
    elif menu_name == "increment":
        await orm_add_to_cart(session, user_id, product_id)

    carts = await orm_get_user_carts(session, user_id)
    #если нет товаров в корзине
    if not carts:
        banner = await orm_get_banner(session, "cart")
        image = InputMediaPhoto(
            media=banner.image, caption=f"<strong>{banner.description}</strong>\n <strong>                          Ваш бюджет: {full_money}</strong>")
        
        kbds = get_user_cart(
            level=level,
            page=None,
            pagination_btns=None,
            product_id=None,
        )

    else:
        paginator = Paginator(carts, page=page)

        cart = paginator.get_page()[0]
        #одной корзины с товаром
        cart_price = round(cart.quantity * cart.product.price, 2)
        #всех корзин где разные товары
        total_price = round(
            sum(cart.quantity * cart.product.price for cart in carts), 2#в каждой корзине( for cart in carts ) разный продукт и его цена
        )
        image = InputMediaPhoto(
            media=cart.product.image,
            caption=f"<strong>{cart.product.name}</strong>\n{cart.product.price}$ x {cart.quantity} = {cart_price}$\
                    \nТовар {paginator.page} из {paginator.pages} в корзине.\nОбщая стоимость товаров в корзине {total_price},\n <strong>                           Ваш бюджет: {full_money}</strong>"
        )

        pagination_btns = pages(paginator)

        kbds = get_user_cart(
            level=level,
            page=page,
            pagination_btns=pagination_btns,
            product_id=cart.product.id,
        )

    return image, kbds
                # MAIN(ВЫЗОВ ОПР МЕНЮШКИ (ПО Уровню))
##########################################################
async def get_menu_content(
    session: AsyncSession,
    level: int,
    menu_name: str,
    category: int | None = None,
    page: int | None = None,
    product_id: int | None = None,
    user_id: int | None = None,
    progress_money: int = 0,
    full_money: int =0
    ):
    if  level == -1:
        return await clicker(session, level, menu_name,progress_money=progress_money)
    elif level == 0:
        return await main_menu(session, level, menu_name=menu_name)
    elif level == 1:
        return await catalog(session, level, menu_name)
    elif level == 2:
        return await products(session, level, category, page,full_money = full_money)
    elif level == 3:
        return await carts(session, level, menu_name, page, user_id, product_id,full_money=full_money)
    elif level == 4:
        return await inventory(session, level, menu_name=menu_name)
    elif level == 5:
        return await inventory1(session, level, page=page, category=category,user_id=user_id,menu_name=menu_name,product_id=product_id)