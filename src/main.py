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
