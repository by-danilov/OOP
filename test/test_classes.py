import pytest
import sys
import os

# Добавляем корневую директорию проекта в sys.path, чтобы импортировать src.main
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from src.main import Product, Category

# Фикстура для сброса счетчиков Category перед каждым тестом
@pytest.fixture(autouse=True)
def reset_category_counts():
    """Сбрасывает счетчики класса Category перед каждым тестом."""
    Category.category_count = 0
    Category.product_count = 0

# --- Тесты для Задания 1: Обработка нулевого количества в Product ---
def test_product_init_zero_quantity_raises_value_error():
    """
    Проверяет, что Product.__init__ выбрасывает ValueError,
    если quantity равно 0.
    """
    with pytest.raises(ValueError, match="Товар с нулевым количеством не может быть добавлен."):
        Product("Тестовый товар", "Описание", 100.0, 0)

def test_product_init_positive_quantity_succeeds():
    """
    Проверяет, что Product.__init__ успешно создает объект,
    если quantity больше 0.
    """
    product = Product("Хороший товар", "Описание", 100.0, 1)
    assert product.quantity == 1
    assert product.name == "Хороший товар"

# --- Тесты для Задания 2: Метод middle_price в Category ---
def test_category_middle_price_with_products():
    """
    Проверяет корректность подсчета среднего ценника для категории с продуктами.
    """
    product1 = Product("Тест Продукт 1", "Один", 100.0, 5)
    product2 = Product("Тест Продукт 2", "Два", 200.0, 3)
    product3 = Product("Тест Продукт 3", "Три", 300.0, 2)
    category = Category("Тестовая категория", "Для проверки middle_price", [product1, product2, product3])

    # Средняя цена: (100 + 200 + 300) / 3 = 600 / 3 = 200.0
    assert category.middle_price() == 200.0

def test_category_middle_price_empty_category():
    """
    Проверяет, что middle_price возвращает 0 для пустой категории.
    """
    empty_category = Category("Пустая", "Категория без продуктов", [])
    assert empty_category.middle_price() == 0

def test_category_middle_price_single_product():
    """
    Проверяет middle_price для категории с одним продуктом.
    """
    product = Product("Один товар", "Единственный", 500.0, 10)
    category = Category("Категория с одним", "Один продукт", [product])
    assert category.middle_price() == 500.0

# --- Существующие тесты (базовая функциональность) ---
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
    assert len(category.products) == 2 # Проверяем количество продуктов через свойство
    assert category.products[0] == "Тест1, 10.0 руб. Остаток: 1 шт."
    assert category.products[1] == "Тест2, 20.0 руб. Остаток: 2 шт."

def test_category_count_increment():
    _ = Category("Категория A", "Описание A", [])
    assert Category.category_count == 1
    _ = Category("Категория B", "Описание B", [])
    assert Category.category_count == 2

def test_product_count_increment():
    prod1 = Product("П1", "О1", 1, 1)
    prod2 = Product("П2", "О2", 2, 2)
    category1 = Category("Кат1", "Опис1", [prod1, prod2])
    assert Category.product_count == 2
    prod3 = Product("П3", "О3", 3, 3)
    category2 = Category("Кат2", "Опис2", [prod3])
    assert Category.product_count == 3 # Должен увеличиваться глобальный счетчик

def test_add_product_method_type_error():
    category = Category("ТестКат", "Описание", [])
    with pytest.raises(TypeError, match="Можно добавлять только объекты классов Product или его наследников."):
        category.add_product("Не продукт")
    with pytest.raises(TypeError, match="Можно добавлять только объекты классов Product или его наследников."):
        category.add_product(123)

def test_product_str_representation():
    product = Product("Монитор", "Игровой", 30000.0, 2)
    assert str(product) == "Монитор, 30000.0 руб. Остаток: 2 шт."

def test_category_str_representation():
    product1 = Product("Мышь", "Компьютерная", 500.0, 10)
    product2 = Product("Клавиатура", "Механическая", 2000.0, 5)
    category = Category("Аксессуары", "Для компьютера", [product1, product2])
    assert str(category) == "Аксессуары, количество продуктов: 15 шт."

def test_product_add_method():
    product1 = Product("Стул", "Мягкий", 1000.0, 2)
    product2 = Product("Стол", "Деревянный", 2000.0, 1)
    # 1000 * 2 + 2000 * 1 = 2000 + 2000 = 4000
    assert (product1 + product2) == 4000.0

def test_product_add_method_type_error():
    product = Product("Тест", "О", 100.0, 1)
    with pytest.raises(TypeError, match="Можно складывать только объекты Product."):
        _ = product + "не продукт"
    with pytest.raises(TypeError, match="Можно складывать только объекты Product."):
        _ = product + 123
