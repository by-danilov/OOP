class Product:
    def __init__(self, name, description, price, quantity):
        if quantity == 0:
            raise ValueError("Товар с нулевым количеством не может быть добавлен.")
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity

    def __add__(self, other):

        if not isinstance(other, Product):
            raise TypeError("Можно складывать только объекты Product.")

        return (self.price * self.quantity) + (other.price * other.quantity)

    def __str__(self):

        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."


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


    def middle_price(self):
        total_price = sum(product.price for product in self.__products)
        try:
            return total_price / len(self.__products)
        except ZeroDivisionError:
            return 0


if __name__ == '__main__':

    print("--- Проверка Задания 1: Создание продукта с нулевым количеством ---")
    try:
        product_invalid = Product("Бракованный товар", "Неверное количество", 1000.0, 0)
    except ValueError as e:
        print(
            "Возникла ошибка ValueError прерывающая работу программы при попытке добавить продукт с нулевым количеством")
        print(f"Сообщение об ошибке: {e}")
    else:
        print("Не возникла ошибка ValueError при попытке добавить продукт с нулевым количеством")

    print("\n--- Проверка создания обычных продуктов ---")
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    print(f"Продукт 1: {product1}")
    print(f"Продукт 2: {product2}")
    print(f"Продукт 3: {product3}")


    print("\n--- Проверка Задания 2: Метод middle_price в Category ---")
    category1 = Category("Смартфоны", "Категория смартфонов", [product1, product2, product3])
    print(f"Средний ценник категории '{category1.name}': {category1.middle_price()}")

    category_empty = Category("Пустая категория", "Категория без продуктов", [])
    print(f"Средний ценник пустой категории: {category_empty.middle_price()}")

    # Дополнительная проверка на счетчики и add_product
    print(f"\nОбщее количество категорий: {Category.category_count}")
    print(f"Общее количество продуктов: {Category.product_count}")

    # Пример сложения
    print(f"Стоимость product1 + product2 (quantity * price): {product1 + product2}")
    