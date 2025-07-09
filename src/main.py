class Product:

    def __init__(self, name, description, price, quantity):
        self.name = name
        self.description = description
        # Приватный атрибут для цены
        self.__price = price
        self.quantity = quantity

    @property
    def price(self):
        """Геттер для получения цены продукта."""
        return self.__price

    @price.setter
    def price(self, new_price):
        """
        Сеттер для установки цены продукта с проверками.
        Цена не должна быть <= 0.
        При понижении цены требуется подтверждение пользователя.
        """
        if not isinstance(new_price, (int, float)):
            print("Цена должна быть числом.")
            return

        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return

        # Дополнительное задание 4: Логика подтверждения понижения цены
        if new_price < self.__price:
            while True:
                confirmation = input(
                    f"Цена товара '{self.name}' понижается с {self.__price} до "
                    f"{new_price}. Подтвердите (y/n): ").lower()
                if confirmation == 'y':
                    self.__price = new_price
                    print(f"Цена товара '{self.name}' успешно понижена до "
                          f"{self.__price}.")
                    break
                elif confirmation == 'n':
                    print(f"Понижение цены для '{self.name}' отменено. "
                          f"Текущая цена: {self.__price}.")
                    break
                else:
                    print("Некорректный ввод. Пожалуйста, введите 'y' или 'n'.")
        else:
            self.__price = new_price

    @classmethod
    def new_product(cls, product_data, products_list=None):
        """
        Создает новый объект Product из словаря данных.
        Если products_list предоставлен, проверяет на дубликаты по имени.
        При дубликате складывает количество и выбирает более высокую цену.
        """
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
                        # Используем сеттер для проверки цены
                        existing_product.price = price
                    # Возвращаем обновленный существующий продукт
                    return existing_product

        # Если дубликат не найден или список не предоставлен, создаем новый продукт
        return cls(name, description, price, quantity)


class Category:
    category_count = 0
    product_count = 0

    def __init__(self, name, description, products):
        self.name = name
        self.description = description
        # Задание 1: Приватный список товаров
        self.__products = []
        # Добавляем продукты через метод add_product,
        # чтобы использовать его логику и увеличивать счетчик
        for product in products:
            self.add_product(product)

        Category.category_count += 1

    def add_product(self, product):
        """Добавляет объект Product в список товаров категории."""
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только объекты класса Product.")
        self.__products.append(product)
        Category.product_count += 1  # Увеличиваем общий счетчик товаров

    @property
    def products(self):
        """
        Возвращает список товаров категории в формате строк:
        'Название продукта, Цена руб. Остаток: N шт.'
        """
        product_info = []
        for product in self.__products:
            # Используем геттер price, чтобы получить актуальную цену
            product_info.append(f"{product.name}, {product.price} руб. "
                                f"Остаток: {product.quantity} шт.")
        return product_info


if __name__ == "__main__":
    # Сбросим счетчики перед каждым запуском main.py
    # для чистоты демонстрации
    Category.category_count = 0
    Category.product_count = 0

    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера",
                       180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    category1 = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения "
        "дополнительных функций для удобства жизни",
        [product1, product2, product3]
    )

    print("--- Проверка category1.products (геттер) ---")
    print(category1.products)

    print("\n--- Добавление продукта через add_product ---")
    product4 = Product("55\" QLED 4K", "Фоновая подсветка", 123000.0, 7)
    category1.add_product(product4)
    print(category1.products)
    print(f"Общее количество продуктов в категориях (Category.product_count): "
          f"{Category.product_count}")

    print("\n--- Использование new_product (класс-метод) ---")
    # Создаем список существующих продуктов для проверки дубликатов
    # Здесь мы будем передавать все продукты, которые уже есть, в add_product
    # и затем этот же список в new_product для проверки
    existing_products_in_system = [product1, product2, product3, product4]

    new_product_data1 = {"name": "Samsung Galaxy S23 Ultra", "description": "новая версия",
                         "price": 190000.0, "quantity": 3}
    # new_product будет обновлять product1, так как имя совпадает
    new_product1 = Product.new_product(new_product_data1,
                                       products_list=existing_products_in_system)
    print(f"\nРезультат new_product (дубликат):")
    print(f"Имя: {new_product1.name}, Описание: {new_product1.description}, "
          f"Цена: {new_product1.price}, Количество: {new_product1.quantity}")
    # Должно быть 5 + 3 = 8
    print(f"Исходный product1.quantity после обновления: {product1.quantity}")
    # Должно быть 190000.0 (более высокая цена)
    print(f"Исходный product1.price после обновления: {product1.price}")

    new_product_data2 = {"name": "Новый Супер Товар", "description": "абсолютно новый",
                         "price": 50000.0, "quantity": 10}
    # new_product создаст новый продукт, так как нет дубликата
    new_product2 = Product.new_product(new_product_data2,
                                       products_list=existing_products_in_system)
    print(f"\nРезультат new_product (новый товар):")
    print(f"Имя: {new_product2.name}, Описание: {new_product2.description}, "
          f"Цена: {new_product2.price}, Количество: {new_product2.quantity}")

    print("\n--- Проверка сеттера цены ---")
    print(f"Исходная цена product2: {product2.price}")

    print("Попытка установить цену 800:")
    product2.price = 800
    print(f"Новая цена product2: {product2.price}")

    print("Попытка установить цену -100:")
    product2.price = -100  # Должно быть сообщение и цена не изменится
    print(f"Цена product2 после попытки -100: {product2.price}")

    print("Попытка установить цену 0:")
    product2.price = 0  # Должно быть сообщение и цена не изменится
    print(f"Цена product2 после попытки 0: {product2.price}")

    print("Попытка понизить цену (с подтверждением):")
    product2.price = 700  # Должно запросить подтверждение
    print(f"Цена product2 после попытки понижения: {product2.price}")

    print("Попытка повысить цену:")
    product2.price = 1000  # Должно просто измениться без подтверждения
    print(f"Цена product2 после попытки повышения: {product2.price}")

    # Дополнительная проверка на некорректный тип данных для цены
    print("\nПопытка установить нечисловую цену:")
    product2.price = "пятьсот"
    print(f"Цена product2 после попытки нечисловой цены: {product2.price}")

    print("\n--- Итоговые счетчики ---")
    print(f"Общее количество категорий: {Category.category_count}")
    # Обрати внимание: product_count теперь считается только при добавлении в категорию.
    # Продукты, созданные через new_product, но не добавленные в категорию, не учитываются.
    print(f"Общее количество всех продуктов: {Category.product_count}")
