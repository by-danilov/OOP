import pytest
import sys
import os
import warnings
from abc import ABC, abstractmethod

# Определяем путь к корневой директории проекта
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from src.main import Product, Category, Smartphone, LawnGrass, BaseProduct, CreationLoggerMixin

@pytest.fixture(autouse=True)
def reset_category_counts():
    """Сбрасывает счетчики класса Category перед каждым тестом."""
    Category.category_count = 0
    Category.product_count = 0

def test_base_product_is_abstract():
    assert issubclass(BaseProduct, ABC)

def test_base_product_cannot_be_instantiated():
    # ИЗМЕНЕНО: Обновлено регулярное выражение
    with pytest.raises(TypeError, match="Can't instantiate abstract class BaseProduct without an implementation for abstract methods '__add__', '__str__', 'price'"):
        BaseProduct("Тест", "Описание", 10.0, 1)

def test_product_inherits_from_base_product():
    assert issubclass(Product, BaseProduct)

def test_creation_logger_mixin_prints_on_init(capsys):
    _ = Product("Тест", "О", 100.0, 10)
    captured = capsys.readouterr()

    assert "Создан объект класса: Product" in captured.out
    assert "Параметры: args=('Тест', 'О', 100.0, 10), kwargs={}" in captured.out

def test_creation_logger_mixin_prints_on_init_smartphone(capsys):
    # ИЗМЕНЕНО: Ожидаемые параметры миксина только те, что передаются Product.__init__
    _ = Smartphone("ТестСмарт", "О", 1000.0, 1, 90, "ModelX", 128, "Black")
    captured = capsys.readouterr()

    assert "Создан объект класса: Smartphone" in captured.out
    assert "Параметры: args=('ТестСмарт', 'О', 1000.0, 1), kwargs={}" in captured.out


def test_creation_logger_mixin_prints_on_init_lawngrass(capsys):
    # ИЗМЕНЕНО: Ожидаемые параметры миксина только те, что передаются Product.__init__
    _ = LawnGrass("ТестТрава", "О", 10.0, 5, "Страна", "10 дней", "Green")
    captured = capsys.readouterr()

    assert "Создан объект класса: LawnGrass" in captured.out
    assert "Параметры: args=('ТестТрава', 'О', 10.0, 5), kwargs={}" in captured.out

def test_product_initialization():
    product = Product("Тестовый Продукт", "Описание тестового продукта", 100.0, 10)

    assert product.name == "Тестовый Продукт"
    assert product.description == "Описание тестового продукта"
    assert product.price == 100.0
    assert product.quantity == 10

def test_category_initialization():
    product1 = Product("Тест1", "О1", 10.0, 1)
    product2 = Product("Тест2", "О2", 20.0, 2)
    products_list = [product1, product2]

    category = Category("Тестовая Категория", "Описание тестовой категории", products_list)

    assert category.name == "Тестовая Категория"
    assert category.description == "Описание тестовой категории"
    assert len(category.products) == 2
    assert category.products[0] == "Тест1, 10.0 руб. Остаток: 1 шт."
    assert category.products[1] == "Тест2, 20.0 руб. Остаток: 2 шт."

def test_category_count():
    category1 = Category("Категория A", "Описание A", [])
    assert Category.category_count == 1

    product_item = Product("Ещё Продукт", "О", 1, 1)
    category2 = Category("Категория B", "Описание B", [product_item])
    assert Category.category_count == 2

    category3 = Category("Категория C", "Описание C", [])
    assert Category.category_count == 3

def test_product_count():
    prod1 = Product("П1", "О1", 1, 1)
    prod2 = Product("П2", "О2", 2, 2)
    prod3 = Product("П3", "О3", 3, 3)
    category1 = Category("Кат1", "Опис1", [prod1, prod2, prod3])
    assert Category.product_count == 3

    prod4 = Product("П4", "О4", 4, 4)
    category2 = Category("Кат2", "Опис2", [prod4])
    assert Category.product_count == 4

    category3 = Category("Кат3", "Опис3", [])
    assert Category.product_count == 4

def test_add_product_method():
    category = Category("ТестКат", "Описание", [])
    initial_product_count = Category.product_count
    assert len(category.products) == 0

    product1 = Product("Товар1", "О1", 10.0, 1)
    category.add_product(product1)
    assert len(category.products) == 1
    assert category.products[0] == "Товар1, 10.0 руб. Остаток: 1 шт."
    assert Category.product_count == initial_product_count + 1

    product2 = Product("Товар2", "О2", 20.0, 2)
    category.add_product(product2)
    assert len(category.products) == 2
    assert category.products[1] == "Товар2, 20.0 руб. Остаток: 2 шт."
    assert Category.product_count == initial_product_count + 2

def test_add_product_type_error_category():
    category = Category("ТестКат", "Описание", [])
    with pytest.raises(TypeError, match="Можно добавлять только объекты классов Product или его наследников."):
        category.add_product("Не продукт")
    with pytest.raises(TypeError, match="Можно добавлять только объекты классов Product или его наследников."):
        category.add_product(123)
    smartphone = Smartphone("ТестСмарт", "О", 1000.0, 1, 90, "ModelX", 128, "Black")
    grass = LawnGrass("ТестТрава", "О", 10.0, 5, "Страна", "10 дней", "Green")
    try:
        category.add_product(smartphone)
        category.add_product(grass)
    except TypeError:
        pytest.fail("Не должно было быть TypeError при добавлении наследников Product")


def test_product_price_setter_valid():
    product = Product("Тест", "О", 100.0, 5)
    product.price = 150.0
    assert product.price == 150.0

def test_product_price_setter_zero_or_negative():
    product = Product("Тест", "О", 100.0, 5)
    initial_price = product.price

    with pytest.warns(UserWarning):
        product.price = 0
    assert product.price == initial_price

    with pytest.warns(UserWarning):
        product.price = -50
    assert product.price == initial_price

    with pytest.warns(UserWarning):
        product.price = "abc"
    assert product.price == initial_price

def test_product_price_setter_lower_price_confirm(monkeypatch):
    product = Product("Тест", "О", 100.0, 5)
    monkeypatch.setattr('builtins.input', lambda _: 'y')
    product.price = 50.0
    assert product.price == 50.0

def test_product_price_setter_lower_price_cancel(monkeypatch):
    product = Product("Тест", "О", 100.0, 5)
    monkeypatch.setattr('builtins.input', lambda _: 'n')
    product.price = 50.0
    assert product.price == 100.0

def test_product_price_setter_lower_price_invalid_input(monkeypatch):
    product = Product("Тест", "О", 100.0, 5)
    inputs = iter(['x', 'y'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    product.price = 50.0
    assert product.price == 50.0

def test_new_product_creates_new():
    products = []
    product_data = {"name": "Новый Товар", "description": "Описание", "price": 100.0, "quantity": 10}
    new_prod = Product.new_product(product_data, products_list=products)

    assert isinstance(new_prod, Product)
    assert new_prod.name == "Новый Товар"
    assert new_prod.price == 100.0
    assert new_prod.quantity == 10

def test_new_product_handles_duplicates():
    existing_product = Product("Existing Product", "Old Desc", 50.0, 5)
    products = [existing_product]

    product_data_higher_price = {"name": "Existing Product", "description": "New Desc", "price": 70.0, "quantity": 3}
    updated_prod = Product.new_product(product_data_higher_price, products_list=products)

    assert updated_prod is existing_product
    assert updated_prod.quantity == 8
    assert updated_prod.price == 70.0

    product_data_lower_price = {"name": "Existing Product", "description": "New Desc", "price": 40.0, "quantity": 2}
    updated_prod_again = Product.new_product(product_data_lower_price, products_list=products)

    assert updated_prod_again is existing_product
    assert updated_prod_again.quantity == 10
    assert updated_prod_again.price == 70.0

def test_new_product_missing_data_raises_error():
    product_data = {"name": "Неполный", "price": 100.0}
    with pytest.raises(ValueError, match="Недостаточно данных для создания продукта."):
        Product.new_product(product_data)

def test_product_str_representation():
    product = Product("Телевизор", "Большой экран", 50000.0, 3)
    expected_str = "Телевизор, 50000.0 руб. Остаток: 3 шт."
    assert str(product) == expected_str

def test_category_str_representation():
    product1 = Product("Мышь", "Компьютерная", 500.0, 10)
    product2 = Product("Клавиатура", "Механическая", 2000.0, 5)
    products_list = [product1, product2]
    category = Category("Аксессуары", "Для компьютера", products_list)

    expected_str = "Аксессуары, количество продуктов: 15 шт."
    assert str(category) == expected_str

    product3 = Product("Монитор", "Игровой", 30000.0, 2)
    category.add_product(product3)
    expected_str_after_add = "Аксессуары, количество продуктов: 17 шт."
    assert str(category) == expected_str_after_add

def test_smartphone_initialization():
    smartphone = Smartphone("Galaxy S24", "Флагман", 100000.0, 5, 99.9, "S24", 512, "Черный")
    assert smartphone.name == "Galaxy S24"
    assert smartphone.description == "Флагман"
    assert smartphone.price == 100000.0
    assert smartphone.quantity == 5
    assert smartphone.efficiency == 99.9
    assert smartphone.model == "S24"
    assert smartphone.memory == 512
    assert smartphone.color == "Черный"

def test_lawngrass_initialization():
    grass = LawnGrass("Изумруд", "Для тенистых мест", 1000.0, 10, "Германия", "14 дней", "Светло-зеленый")
    assert grass.name == "Изумруд"
    assert grass.description == "Для тенистых мест"
    assert grass.price == 1000.0
    assert grass.quantity == 10
    assert grass.country == "Германия"
    assert grass.germination_period == "14 дней"
    assert grass.color == "Светло-зеленый"

def test_product_add_method_same_type_smartphone():
    s1 = Smartphone("S1", "Desc1", 100.0, 2, 90, "M1", 64, "Red")
    s2 = Smartphone("S2", "Desc2", 200.0, 3, 95, "M2", 128, "Blue")
    assert (s1 + s2) == 800.0

def test_product_add_method_same_type_lawngrass():
    l1 = LawnGrass("L1", "Desc1", 10.0, 5, "RU", "7", "Green")
    l2 = LawnGrass("L2", "Desc2", 20.0, 10, "US", "5", "Dark Green")
    assert (l1 + l2) == 250.0

def test_product_add_method_different_types_raises_typeerror():
    smartphone = Smartphone("S", "D", 100.0, 1, 90, "M", 64, "B")
    grass = LawnGrass("L", "D", 10.0, 1, "C", "7", "G")
    product = Product("P", "D", 50.0, 1)

    with pytest.raises(TypeError, match="Можно складывать товары только из одинаковых классов продуктов."):
        _ = smartphone + grass
    with pytest.raises(TypeError, match="Можно складывать товары только из одинаковых классов продуктов."):
        _ = smartphone + product
    with pytest.raises(TypeError, match="Можно складывать товары только из одинаковых классов продуктов."):
        _ = grass + product


def test_category_add_product_accepts_subclasses():
    category = Category("ТестНаследники", "Тест добавления наследников", [])
    smartphone = Smartphone("ТестСмарт", "О", 1000.0, 1, 90, "ModelX", 128, "Black")
    grass = LawnGrass("ТестТрава", "О", 10.0, 5, "Страна", "10 дней", "Green")

    category.add_product(smartphone)
    category.add_product(grass)

    assert len(category.products) == 2
    assert category.products[0] == "ТестСмарт, 1000.0 руб. Остаток: 1 шт."
    assert category.products[1] == "ТестТрава, 10.0 руб. Остаток: 5 шт."
    assert Category.product_count == 2
