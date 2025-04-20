import math


# Простой пагинатор
class Paginator:
    def __init__(self, array: list | tuple, page: int=1, per_page: int=1):
        self.array = array#все продукты
        self.per_page = per_page
        self.page = page
        self.len = len(self.array)
        # math.ceil - округление в большую сторону до целого числа
        self.pages = math.ceil(self.len / self.per_page)#округление

    def __get_slice(self):
        start = (self.page - 1) * self.per_page
        stop = start + self.per_page#продукты на следующей странице + продукты на предыдущей
        return self.array[start:stop]# начиная с колва продуктов уже прочитанных до колва продуктов на след странице

    def get_page(self):
        page_items = self.__get_slice()
        return page_items

    def has_next(self):
        if self.page < self.pages:#ЕСЛИ СТРАНИЦА МЕНЬШЕ ЧЕМ ВСЕГО СТРАНИЦ(ЕСЛИ РАВНО ВЕРНЕТСЯ ТАК ЖЕ False ведь он за гранями условия)
            return self.page + 1
        return False

    def has_previous(self):
        if self.page > 1:
            return self.page - 1
        return False

    def get_next(self):
        if self.page < self.pages:
            self.page += 1
            return self.get_page()
        raise IndexError(f'Не существует следующей страницы.Используй has_next()  чтобы проверить это')

    def get_previous(self):
        if self.page > 1:
            self.page -= 1
            return self.__get_slice()
        raise IndexError(f'Не существует предыдущей страницы.Используй has_previous()  чтобы проверить это')