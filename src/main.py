import sys
import warnings
from abc import ABC, abstractmethod


class CreationLoggerMixin:
    def __init__(self, *args, **kwargs):
        print(f"Создан объект класса: {self.__class__.__name__}")
        print(f"Параметры: args={args}, kwargs={kwargs}")
        super().__init__(*args, **kwargs)


class BaseProduct(ABC):
    def __init__(self, name, description, price, quantity):
        self.name = name
        self.description = description
        self._price = price
        self.quantity = quantity

    @property
    @abstractmethod
    def price(self):
        pass

    @price.setter
    @abstractmethod
    def price(self, new_price):
        pass

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def __add__(self, other):
        pass


class Product(CreationLoggerMixin, BaseProduct):
    def __init__(self, name, description, price, quantity):
        super().__init__(name, description, price, quantity)

    def __str__(self):
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other):
        if type(self) is not type(other):
            raise TypeError("Можно складывать товары только из одинаковых классов продуктов.")
        if isinstance(other, Product):
            return (self.price * self.quantity) + \
                   (other.price * other.quantity)
        else:
            raise TypeError("Можно складывать только объекты Product "
                            "и их наследников между собой.")

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, new_price):
        if not isinstance(new_price, (int, float)):
            warnings.warn("Цена должна быть числом.", UserWarning)
            return

        if new_price <= 0:
            warnings.warn("Цена не должна быть нулевая или отрицательная.", UserWarning)
            return

        if new_price < self._price:
            while True:
                confirmation = input(
                    f"Цена товара '{self.name}' понижается с {self._price} до "
                    f"{new_price}. Подтвердите (y/n): ").lower()
                if confirmation == 'y':
                    self._price = new_price
                    print(f"Цена товара '{self.name}' успешно понижена до "
                          f"{self._price}.")
                    break
                elif confirmation == 'n':
                    print(f"Понижение цены для '{self.name}' отменено. "
                          f"Текущая цена: {self._price}.")
                    break
                else:
                    print("Некорректный ввод. Пожалуйста, введите 'y' или 'n'.")
        else:
            self._price = new_price

    @classmethod
    def new_product(cls, product_data, products_list=None):
        name = product_data.get("name")
        description = product_data.get("description")
        price = product_data.get("price")
        quantity = product_data.get("quantity")

        if not all([name, description, price, quantity is not None]):
            raise ValueError("Недостаточно данных для создания продукта.")

        if products_list:
            for existing_product in products_list:
                if existing_product.name == name:
                    print(f"Найден дубликат товара: '{name}'. "
                          f"Обновляем существующий товар.")
                    existing_product.quantity += quantity
                    if price > existing_product.price:
                        existing_product.price = price
                    return existing_product

        return cls(name, description, price, quantity)


class Smartphone(Product):
    def __init__(self, name, description, price, quantity, efficiency, model, memory, color):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color


class LawnGrass(Product):
    def __init__(self, name, description, price, quantity, country, germination_period, color):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color


class Category:
    category_count = 0
    product_count = 0

    def __init__(self, name, description, products):
        self.name = name
        self.description = description
        self.__products = []
        for product in products:
            self.add_product(product)

        Category.category_count += 1

    def __str__(self):
        total_quantity_in_category = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity_in_category} шт."

    def add_product(self, product):
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только объекты классов Product или его наследников.")
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self):
        product_info = []
        for product in self.__products:
            product_info.append(str(product))
        return product_info


if __name__ == '__main__':

    Category.category_count = 0
    Category.product_count = 0

    print("--- Создание и вывод информации о Смартфонах ---")
    smartphone1 = Smartphone("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5, 95.5,
                             "S23 Ultra", 256, "Серый")
    smartphone2 = Smartphone("Iphone 15", "512GB, Gray space", 210000.0, 8, 98.2, "15", 512, "Gray space")
    smartphone3 = Smartphone("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14, 90.3, "Note 11", 1024, "Синий")

    print(f"Смартфон 1: {smartphone1.name}, {smartphone1.description}, {smartphone1.price}, "
          f"{smartphone1.quantity}, {smartphone1.efficiency}, {smartphone1.model}, "
          f"{smartphone1.memory}, {smartphone1.color}")
    print(f"Смартфон 2: {smartphone2.name}, {smartphone2.description}, {smartphone2.price}, "
          f"{smartphone2.quantity}, {smartphone2.efficiency}, {smartphone2.model}, "
          f"{smartphone2.memory}, {smartphone2.color}")
    print(f"Смартфон 3: {smartphone3.name}, {smartphone3.description}, {smartphone3.price}, "
          f"{smartphone3.quantity}, {smartphone3.efficiency}, {smartphone3.model}, "
          f"{smartphone3.memory}, {smartphone3.color}")

    print("\n--- Создание и вывод информации о Газонной траве ---")
    grass1 = LawnGrass("Газонная трава", "Элитная трава для газона", 500.0, 20, "Россия", "7 дней", "Зеленый")
    grass2 = LawnGrass("Газонная трава 2", "Выносливая трава", 450.0, 15, "США", "5 дней", "Темно-зеленый")

    print(f"Трава 1: {grass1.name}, {grass1.description}, {grass1.price}, {grass1.quantity}, "
          f"{grass1.country}, {grass1.germination_period}, {grass1.color}")
    print(f"Трава 2: {grass2.name}, {grass2.description}, {grass2.price}, {grass2.quantity}, "
          f"{grass2.country}, {grass2.germination_period}, {grass2.color}")


    print("\n--- Проверка сложения однотипных продуктов ---")
    smartphone_sum = smartphone1 + smartphone2
    print(f"smartphone1 + smartphone2: {smartphone_sum}")

    grass_sum = grass1 + grass2
    print(f"grass1 + grass2: {grass_sum}")

    print("\n--- Проверка сложения разнотипных продуктов (ожидается TypeError) ---")
    try:
        invalid_sum = smartphone1 + grass1
    except TypeError as e:
        print(f"Возникла ожидаемая ошибка TypeError при попытке сложения: {e}")
    else:
        print("Не возникла ошибка TypeError при попытке сложения (ОШИБКА)")


    print("\n--- Проверка инициализации категорий с наследниками ---")
    category_smartphones = Category("Смартфоны", "Высокотехнологичные смартфоны", [smartphone1, smartphone2])
    print(f"Категория Смартфоны: {category_smartphones}")
    print(category_smartphones.products)

    category_grass = Category("Газонная трава", "Различные виды газонной травы", [grass1, grass2])
    print(f"Категория Газонная трава: {category_grass}")
    print(category_grass.products)


    print("\n--- Проверка добавления продуктов в категорию (add_product) ---")
    category_smartphones.add_product(smartphone3)
    print(f"Категория Смартфоны после добавления smartphone3: {category_smartphones}")
    print(category_smartphones.products)

    print(f"Общее количество продуктов во всех категориях (Category.product_count): "
          f"{Category.product_count}")

    print("\n--- Проверка добавления не-продукта в категорию (ожидается TypeError) ---")
    try:
        category_smartphones.add_product("Not a product")
    except TypeError as e:
        print(f"Возникла ожидаемая ошибка TypeError при добавлении не продукта: {e}")
    else:
        print("Не возникла ошибка TypeError при добавлении не продукта (ОШИБКА)")

    try:
        category_smartphones.add_product(123)
    except TypeError as e:
        print(f"Возникла ожидаемая ошибка TypeError при добавлении числа: {e}")
    else:
        print("Не возникла ошибка TypeError при добавлении числа (ОШИБКА)")

    print("\n--- Проверка BaseProduct (попытка создания экземпляра, ожидается TypeError) ---")
    try:
        base_prod_test = BaseProduct("Базовый", "Описание", 10.0, 1)
        print("ОШИБКА: удалось создать экземпляр BaseProduct.")
    except TypeError as e:
        print(f"УСПЕХ: Не удалось создать экземпляр BaseProduct. Ошибка: {e}")
