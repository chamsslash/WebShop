from sqlalchemy import select,update,delete
from sqlalchemy.ext.asyncio import AsyncSession

from DataBase.Models_for_DataBase import Category, Inventory, Product,Banner,Cart,User
async def orm_add_product(session: AsyncSession,data: dict):

    product = Product(
        name=data["name"],
        description=data["description"],
        price=float(data["price"]),
        image=data["image"],
        category_id=int(data["category"]),
    )
    session.add(product)
   
    await session.commit()#подтвердить добавление

async def orm_get_money(session: AsyncSession,user_id1):
    query = select(User.money).where(User.user_id == user_id1)#должно выдавать TRUE тк ==
    result = await session.execute(query)
    return result.scalar()













async def orm_money_add(session:AsyncSession,user_id:int,count:int):
    now = await orm_get_money(session=session,user_id1=user_id)
    if now:
        query = update(User).where(User.user_id == user_id).values(money = now + count)
    else:
        query = update(User).where(User.user_id == user_id).values(money = count)
    await session.execute(query)#выполнение запроса тк надо асинхрона юзаем await
    await session.commit()














async def orm_money_minus(session:AsyncSession,user_id:int,count:int):
    now = await orm_get_money(session=session,user_id1=user_id)
    if now:
        if now >= count:
            query = update(User).where(User.user_id == user_id).values(money = now - count)
            await session.execute(query)#выполнение запроса тк надо асинхрона юзаем await
            await session.commit()
            return True
        else:
            return False
        














async def orm_get_price_of_product(session: AsyncSession,product_id1):
    query = select(Product.price).where(Product.id == product_id1)#должно выдавать TRUE тк ==
    result = await session.execute(query)
    return result.scalar()








 




async def orm_get_all_products(session: AsyncSession, category_id):
    query = select(Product).where(Product.category_id == int(category_id))
    result = await session.execute(query)
    return result.scalars().all()



   

async def orm_get_all_inventory(session: AsyncSession, user_id,category_id):#все корзины этого юзера(если их несколько)
    query = select(Inventory).filter(Inventory.user_id == user_id,Inventory.category_id ==category_id)
    result = await session.execute(query)
    return result.scalars().all()











async def orm_get_product(session: AsyncSession, product_id: int):
    query = select(Product).where(Product.id == product_id)
    result = await session.execute(query)
    return result.scalar()











async def orm_update_product(session:AsyncSession,product_id: int, data):
    query =  update(Product).where(Product.id == product_id).values(
        name = data['name'],#новая дата с новым именем
        description= data['description'],
        price =float(data['price']),
        image = data['image'],)
    await session.execute(query)
    await session.commit()#подтвердить изменения





async def orm_delete_product(session: AsyncSession,product_id:int):
    query = delete(Product).where(Product.id == product_id)
    await session.execute(query)
    await session.commit()#подтвердить изменение(удаление продукта в таблице по айди)        
        
        #какие значения меняем




#ORMS FOR BANNERS 
#################################
async def orm_add_banner_description(session: AsyncSession, data: dict):
    #Добавляем новый или изменяем существующий по именам
    #пунктов меню: main, about, cart, shipping, payment, catalog
    query = select(Banner)
    result = await session.execute(query)
    if result.first():
        return
    session.add_all([Banner(name=name, description=description) for name, description in data.items()]) 
    await session.commit()


async def orm_change_banner_image(session: AsyncSession, name: str, image: str):
    query = update(Banner).where(Banner.name == name).values(image=image)
    await session.execute(query)
    await session.commit()


async def orm_get_banner(session: AsyncSession, page: str):
    query = select(Banner).where(Banner.name == page)
    result = await session.execute(query)
    return result.scalar()









#ПОЛУЧАЕМ ВСЕ блять БАННЕРЫ
async def orm_get_info_pages(session: AsyncSession):
    query = select(Banner)#делает выборку из всех таблиц типа баннер(выборка из всех баннеров,существующих в таблице)
    result = await session.execute(query)
    return result.scalars().all()
















#ORMS FOR CATEGORIES
#################################
async def orm_get_categories(session: AsyncSession):#ПОЛУЧАЕМ ВСЕ КАТЕГОРИИ
    query = select(Category)
    result = await session.execute(query)
    return result.scalars().all()






async def orm_create_categories(session: AsyncSession, categories: list):
    query = select(Category)
    result = await session.execute(query)
    if result.first():
        return
    session.add_all([Category(name=name) for name in categories]) 
    await session.commit()




#ORMS FOR USERS
#################################
async def orm_add_user(
    session: AsyncSession,
    user_id: int,
    first_name: str | None = None,
    last_name: str | None = None,
    phone: str | None = None,
    money: int | None = None,
):
    query = select(User).where(User.user_id == user_id)#должно выдавать TRUE тк ==
    result = await session.execute(query)
    if result.first() is None:#Если есть первое(в нашем случае это не список где первый индекс 0) значение(есть хотябы что нибудь)
        session.add(
            User(user_id=user_id, first_name=first_name, last_name=last_name, phone=phone,money=money)
        )
        await session.commit()


















#ORMS FOR CARTS
#################################

async def orm_add_to_cart(session: AsyncSession, user_id, product_id: int):
    query = select(Cart).where(Cart.user_id ==user_id , Cart.product_id == product_id)
    cart = await session.execute(query)
    cart = cart.scalar()
    if cart:
        cart.quantity += 1
        await session.commit()
        return cart
    else:
        session.add(Cart(user_id=user_id, product_id=product_id, quantity=1))
        await session.commit()

async def orm_get_caregory_id(session: AsyncSession, product_id):#все корзины этого юзера(если их несколько)
    query = select(Product.category_id).filter(Product.id == product_id)
    result = await session.execute(query)
    return result.scalar()

async def orm_get_user_carts(session: AsyncSession, user_id):#все корзины этого юзера(если их несколько)
    query = select(Cart).filter(Cart.user_id == user_id)
    
    result = await session.execute(query)
    return result.scalars().all()



async def orm_get_carts(session: AsyncSession):#все корзины этого юзера(если их несколько)
    query = select(Cart)
    result = await session.execute(query)
    print(query)
    return result.scalars().all()


async def orm_delete_from_cart(session: AsyncSession, user_id: int, product_id: int):
    query = delete(Cart).where(Cart.user_id == user_id, Cart.product_id == product_id)
    await session.execute(query)
    await session.commit()

async def orm_delete_from_inventory(session: AsyncSession, user_id: int, product_id: int):
    query = delete(Inventory).where(Inventory.user_id == user_id, Inventory.product_id == product_id)
    await session.execute(query)
    await session.commit()


async def orm_reduce_product_in_cart(session: AsyncSession, user_id: int, product_id: int):
    query = select(Cart).where(Cart.user_id == user_id, Cart.product_id == product_id)
    cart = await session.execute(query)
    cart = cart.scalar()

    if not cart:
        return
    if cart.quantity > 1:
        cart.quantity -= 1
        await session.commit()
        return True
    else:
        await orm_delete_from_cart(session, user_id, product_id)
        await session.commit()
        return False



async def orm_inventory_add(session:AsyncSession,product_id,user_id,category):
    query = select(Inventory).where(Inventory.user_id == user_id, Inventory.product_id == product_id,Inventory.category_id == category)
    inventory = await session.execute(query)
    inventory = inventory.scalar()
    if inventory:
        inventory.quantity += 1
        await session.commit()
        return inventory#добавилось и мы выходи из этой функции отправляя список из продуктиков в инвентаре
    else:
        session.add(Inventory(user_id=user_id, product_id=product_id, quantity=1,category_id = category))
        await session.commit()



