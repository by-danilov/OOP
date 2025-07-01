import pytest
import sys
import os


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

sys.path.insert(0, project_root)


from src.main import Product, Category


@pytest.fixture(autouse=True)
def reset_category_counts():
    """
    Сбрасывает счетчики класса Category перед каждым тестом.
    Это предотвращает влияние тестов друг на друга.
    """
    Category.category_count = 0
    Category.product_count = 0


def test_product_initialization():
    """Проверяем корректность инициализации объекта Product."""
    product = Product("Тестовый Продукт", "Описание тестового продукта", 100.0, 10)

    assert product.name == "Тестовый Продукт"
    assert product.description == "Описание тестового продукта"
    assert product.price == 100.0
    assert product.quantity == 10


def test_category_initialization():
    """Проверяем корректность инициализации объекта Category."""
    product1 = Product("Тест1", "О1", 10.0, 1)
    product2 = Product("Тест2", "О2", 20.0, 2)
    products_list = [product1, product2]

    category = Category("Тестовая Категория", "Описание тестовой категории", products_list)

    assert category.name == "Тестовая Категория"
    assert category.description == "Описание тестовой категории"
    assert category.products == products_list
    assert len(category.products) == 2


def test_category_count():
    """Проверяем корректность подсчета количества категорий."""
    category1 = Category("Категория A", "Описание A", [])
    assert Category.category_count == 1

    # Создаем вторую категорию
    product_item = Product("Ещё Продукт", "О", 1, 1)
    category2 = Category("Категория B", "Описание B", [product_item])
    assert Category.category_count == 2


    category3 = Category("Категория C", "Описание C", [])
    assert Category.category_count == 3


def test_product_count():
    """Проверяем корректность подсчета общего количества продуктов."""
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
