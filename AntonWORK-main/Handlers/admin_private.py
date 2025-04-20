from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter,or_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from filters import Chat_Types
from filters.Chat_Types import my_class,isaAdmin
from Keyboard import REPLY_KEYBOARD
from Handlers.user import restricted_words
from string import punctuation
from Handlers.user import Avalaible_Types_for_private
from DataBase.orm_query import orm_change_banner_image, orm_get_all_products,orm_add_product, orm_get_categories, orm_get_info_pages,orm_update_product,orm_delete_product,orm_get_product
from Keyboard.Inline_Keyboard import get_callback_btns
from sqlalchemy.ext.asyncio import AsyncSession
################


from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.fsm.state import State, StatesGroup
#######################



ADMIN_KB = REPLY_KEYBOARD.get_keyboard(
    "Добавить товар",
    "Ассортимент",
    "Добавить/Изменить баннер",
    placeholder="Выберите действие",
    sizes=(2,),
)




admin_router_n1 = Router()
admin_router_n1.message.filter(my_class(Avalaible_Types_for_private),isaAdmin())

#класс для машины состояний
class Addmeme(StatesGroup):        
    name = State()#состояние
    description = State()
    price = State()
    image = State()
    category = State()
    texts = {
        'Addmeme:name': 'Введите название заново:',#потому что statesgroup делает словарь из наших состояний
        'Addmeme:description': 'Введите описание заново:',
        'Addmeme:price': 'Введите стоимость заново:',
        'Addmeme:image': 'Этот стейт последний, поэтому...',
    }
    
    product_for_change = None

def clean_text(text: str):
    return text.translate(str.maketrans('', '', punctuation))


@admin_router_n1.message(Command('admin'))
async def admin_stage(message: types.Message):
    await message.answer("Чего желаете?",reply_markup=ADMIN_KB)


@admin_router_n1.message(F.text == 'Ассортимент')
async def admin_features(message: types.Message, session: AsyncSession):
    categories = await orm_get_categories(session)
    btns = {category.name : f'category_{category.id}' for category in categories}
    await message.answer("Выберите категорию", reply_markup=get_callback_btns(btns=btns))

@admin_router_n1.callback_query(F.data.startswith('category_'))
async def starring_at_product(callback: types.CallbackQuery, session: AsyncSession):
    category_id = callback.data.split('_')[-1]
    for product in await orm_get_all_products(session, int(category_id)):
        await callback.message.answer_photo(
            product.image,
            caption=f"<strong>{product.name}\
                    </strong>\n{product.description}\nСтоимость: {round(product.price, 2)}",
            reply_markup=get_callback_btns(
                btns={
                    "Удалить": f"delete_{product.id}",
                    "Изменить": f"change_{product.id}",
                },
                sizes=(2,)
            ),
        )
    await callback.answer()
    await callback.message.answer("ОК, вот список товаров ⏫")



@admin_router_n1.callback_query(F.data.startswith('delete_'))#начало обработки callbackquery,появилась загрузка на инлайн кнопке,тк асинхронн
async def delete_product(callback:types.CallbackQuery,session:AsyncSession):
    product_id = callback.data.split('_')[-1]# последный элемент списка разделенного по ниж.подчеркиванию (delete_(project.id))
    await orm_delete_product(session=session,product_id=int(product_id))
    await callback.answer()#снимает загрузуку с инлайн кнопки
    await callback.message.answer('удалено')




@admin_router_n1.callback_query(StateFilter(None), F.data.startswith("change_"))
async def change_product_callback(
    callback: types.CallbackQuery, state: FSMContext, session: AsyncSession
):
    product_id = callback.data.split("_")[-1]

    product_for_change = await orm_get_product(session, int(product_id))

    Addmeme.product_for_change = product_for_change

    await callback.answer()
    await callback.message.answer(
        "Введите название товара", reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(Addmeme.name)




class AddBanner(StatesGroup):
    image = State()

# Отправляем перечень информационных страниц бота и становимся в состояние отправки photo
@admin_router_n1.message(StateFilter(None), F.text == 'Добавить/Изменить баннер')
async def add_image2(message: types.Message, state: FSMContext, session: AsyncSession):
    pages_names = [page.name for page in await orm_get_info_pages(session)]
    await message.answer(f"Отправьте фото баннера.\nВ описании укажите для какой страницы:\
                         \n{', '.join(pages_names)}")
    await state.set_state(AddBanner.image)

# Добавляем/изменяем изображение в таблице (там уже есть записанные страницы по именам:
# main, catalog, cart(для пустой корзины), about, payment, shipping
@admin_router_n1.message(AddBanner.image, F.photo)
async def add_banner(message: types.Message, state: FSMContext, session: AsyncSession):
    image_id = message.photo[-1].file_id
    for_page = message.caption.strip()
    pages_names = [page.name for page in await orm_get_info_pages(session)]
    if for_page not in pages_names:
        await message.answer(f"Введите нормальное название страницы, например:\
                         \n{', '.join(pages_names)}")
        return
    await orm_change_banner_image(session, for_page, image_id,)
    await message.answer("Баннер добавлен/изменен.")
    await state.clear()



















@admin_router_n1.message(StateFilter(None),F.text.lower() == 'добавить товар')
async def first_fsm_stage(message:types.Message,state:FSMContext):
    await message.answer('Имя:',reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(Addmeme.name)















@admin_router_n1.message(StateFilter('*'),Command('назад'))
@admin_router_n1.message(StateFilter('*'), F.text.casefold() == "назад")          #+-lower()
async def back_step_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    print(current_state)
    if current_state == Addmeme.name:
        await message.answer('Предидущего шага нет, или введите название товара или напишите "отмена"')
        return

    previous = None
    for step in Addmeme.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer(f"Ок, вы вернулись к прошлому шагу \n {Addmeme.texts[previous]}")
            return
        previous = step.state
        print(previous)















@admin_router_n1.message(StateFilter('*'), Command("отмена"))
@admin_router_n1.message(StateFilter('*'), F.text.casefold() == "отмена")#любой но хоть какой то но не none
async def cancel_handler(message: types.Message, state: FSMContext) -> None:

    current_state = await state.get_state()
    if current_state is None:
        return
    if Addmeme.product_for_change:#те он не none значит пользователь хотел изменить
        Addmeme.product_for_change = None
    await state.clear()
    await message.answer("Действия отменены", reply_markup=REPLY_KEYBOARD.kb_admin.as_markup("Чего желаете?",reply_markup=REPLY_KEYBOARD.kb_admin.as_markup(resize_keyboard=True,input_field_placeholder='Что Вас интересует?')))




@admin_router_n1.message(StateFilter(Addmeme.name),or_f(F.text, F.text == "skip"))
async def proverka_na_opisanie(message:types.Message,state:FSMContext):
    if message.text == 'skip':
        await state.update_data(name = Addmeme.product_for_change.name)
    else:
        if restricted_words.intersection(clean_text(message.text.lower()).split()):
            await message.answer('Имя не может содержать нецензурную лексику!')
            return
        await state.update_data(name = message.text)
    await message.answer('Описание:')
        
    await state.set_state(Addmeme.description)

@admin_router_n1.message(Addmeme.name) #если не сработает условие,выйдя из хендлера по состоянию придеь сюда
async def add_name2(message: types.Message, state: FSMContext):
    await message.answer("Вы ввели не допустимые данные, введите текст названия товара")


@admin_router_n1.message(StateFilter(Addmeme.description), or_f(F.text, F.text == "skip"))
async def add_description(message: types.Message, state: FSMContext,session:AsyncSession):
    if message.text == 'skip':
        await state.update_data(description=Addmeme.product_for_change.description)
    else:
        if restricted_words.intersection(clean_text(message.text.lower()).split()):
            await message.answer('Описание не может содержать нецензурную лексику!')
            return
        await state.update_data(description=message.text)
    categories = await orm_get_categories(session)
    btns = {category.name : str(category.id) for category in categories}
    await message.answer("Выберите категорию", reply_markup=get_callback_btns(btns=btns))
    await state.set_state(Addmeme.category)

@admin_router_n1.callback_query(Addmeme.category)
async def category_choice(callback: types.CallbackQuery, state: FSMContext , session: AsyncSession):
    if int(callback.data) in [category.id for category in await orm_get_categories(session)]:
        await callback.answer()#убрать звгрузку с кнопки(она беленькая во время загрузки)
        await state.update_data(category=callback.data)
        await callback.message.answer('Теперь введите цену товара.')
        await state.set_state(Addmeme.price)
    else:
        await callback.message.answer('Выберите катеорию из кнопок.')
        await callback.answer()

#Ловим любые некорректные действия, кроме нажатия на кнопку выбора категории
@admin_router_n1.message(Addmeme.category)
async def category_choice2(message: types.Message, state: FSMContext):
    await message.answer("'Выберите катеорию из кнопок.'") 
@admin_router_n1.message(StateFilter(Addmeme.price), or_f(F.text, F.text == "skip"))
async def add_price(message: types.Message, state: FSMContext):
    if message.text == 'skip':
        await state.update_data(price=Addmeme.product_for_change.price)
    else:
        try:
            float(message.text)
        except ValueError:
            await message.answer("Введите корректное значение цены")
            return
        await state.update_data(price=message.text)
    await message.answer("Загрузите изображение товара")
    await state.set_state(Addmeme.image)


@admin_router_n1.message(Addmeme.price)        #так же
async def add_price2(message: types.Message, state: FSMContext):
    await message.answer("Вы ввели не допустимые данные, введите стоимость товара")


@admin_router_n1.message(Addmeme.image,or_f(F.photo, F.text == "skip"))
async def add_image(message: types.Message,session:AsyncSession,state: FSMContext):
    if message.text == 'skip':
        await state.update_data(image=Addmeme.product_for_change.image)
    else:
        await state.update_data(image=message.photo[-1].file_id)#.file_id  айди файла лучшего качества(те -1 элеента)
    data = await state.get_data()
    try:
        if Addmeme.product_for_change:
            await orm_update_product(session=session,product_id=Addmeme.product_for_change.id, data=data)
            
        else:
            await orm_add_product(session=session,data=data)
        await message.answer("Товар добавлен/изменен")
        await state.clear()
    except Exception as error:    
        await message.answer(f'\n{str(error)}\n Дима накосячил',reply_markup=REPLY_KEYBOARD.kb_admin.as_markup(resize_keyboard=True,input_field_placeholder='Что Вас интересует?'))
        await state.clear()
    
        












@admin_router_n1.message(Addmeme.image)
async def add_image2(message:types.Message, state:FSMContext,session:AsyncSession):
    message.answer("Отправьте именно фото!!!")