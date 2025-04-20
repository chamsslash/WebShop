from sqlalchemy import DateTime, Float, ForeignKey, Numeric, String, Text, BigInteger, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())


class Banner(Base):
    __tablename__ = 'banner'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(15), unique=True)
    image: Mapped[str] = mapped_column(String(150), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)


class Category(Base):
    __tablename__ = 'category'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)


class Product(Base):
    __tablename__ = 'product'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str] = mapped_column(Text)
    price: Mapped[float] = mapped_column(Numeric(38,2), nullable=False)
    image: Mapped[str] = mapped_column(String(150))
    category_id: Mapped[int] = mapped_column(ForeignKey('category.id', ondelete='CASCADE'), nullable=False)

    category: Mapped['Category'] = relationship(backref='product',lazy='joined')#куда будет автоматически построена вторая связь(\к обьекту таблицы product)


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, unique=True)#так у айди в тг тип бигинтенджер(поэтому тут ставим тот же)
    first_name: Mapped[str] = mapped_column(String(150), nullable=True)
    last_name: Mapped[str]  = mapped_column(String(150), nullable=True)
    money:Mapped[int] =  mapped_column(Numeric(5,2), nullable=True)# precision количество цифр
    phone: Mapped[str]  = mapped_column(String(13), nullable=True)


class Cart(Base):
    __tablename__ = 'cart'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)
    #елси удалится айди продукта из таблицы продуктс то удалится этот фореин кей(автоудаление(в режиме каскад(хз че это)))
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id', ondelete='CASCADE'), nullable=False)#даннные отсюда будут каскадом удалятся если удалится первоисточник этого первичного ключа
    quantity: Mapped[int]

    user: Mapped['User'] = relationship(backref='cart',lazy='selectin')#бекреф автоматом делает такок же отношение у связанного обьекта( и способ загрузки будет идентичен)
    product: Mapped['Product'] = relationship(backref='cart',lazy='selectin')# это у нас отношение(связь с др таблицей)
class Inventory(Base):
    __tablename__ = 'inventory'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id', ondelete='CASCADE'), nullable=False)
    quantity: Mapped[int]
    category_id: Mapped[int] = mapped_column(ForeignKey('category.id', ondelete='CASCADE'), nullable=False)

    category: Mapped['Category'] = relationship(backref='inventory',lazy='selectin')#куда будет автоматически построена вторая связь(\к обьекту таблицы product)
    user: Mapped['User'] = relationship(backref='inventory',lazy='selectin')#бекреф автоматом делает такок же отношение у связанного обьекта( и способ загрузки будет идентичен)
    product: Mapped['Product'] = relationship(backref='inventory',lazy='selectin')# это у нас отношение(связь с др таблицей)
    #в бекрефе показываем в какую таблицу втоматичеки простроить обратную связь