import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.insert(0, project_root)


from src.main import Product, Category

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

print(f"\nОбщее количество категорий: {Category.category_count}")
print(f"Общее количество продуктов: {Category.product_count}")

print(f"Стоимость product1 + product2 (quantity * price): {product1 + product2}")
