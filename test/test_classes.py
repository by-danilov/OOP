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
    # Теперь category.products возвращает форматированные строки,
    # поэтому проверяем их количество, а не сами объекты
    assert len(category.products) == 2
    # Проверяем, что форматирование использует Product.__str__
    assert category.products[0] == "Тест1, 10.0 руб. Остаток: 1 шт."
    assert category.products[1] == "Тест2, 20.0 руб. Остаток: 2 шт."


def test_category_count():
    """Проверяем корректность подсчета количества категорий."""
    category1 = Category("Категория A", "Описание A", [])
    assert Category.category_count == 1

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


def test_add_product_method():
    """Проверяем метод add_product в Category и его влияние на product_count."""
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


def test_add_product_type_error():
    """Проверяем, что add_product отклоняет не-Product объекты."""
    category = Category("ТестКат", "Описание", [])
    with pytest.raises(TypeError, match="Можно добавлять только объекты класса Product."):
        category.add_product("Не продукт")
    with pytest.raises(TypeError, match="Можно добавлять только объекты класса Product."):
        category.add_product(123)


def test_product_price_setter_valid():
    """Проверяем сеттер цены на валидные положительные значения."""
    product = Product("Тест", "О", 100.0, 5)
    product.price = 150.0
    assert product.price == 150.0


def test_product_price_setter_zero_or_negative():
    """Проверяем сеттер цены на нулевые и отрицательные значения."""
    product = Product("Тест", "О", 100.0, 5)
    initial_price = product.price

    product.price = 0
    assert product.price == initial_price

    product.price = -50
    assert product.price == initial_price

    product.price = "abc"
    assert product.price == initial_price


def test_product_price_setter_lower_price_confirm(monkeypatch):
    """Проверяем понижение цены с подтверждением 'y'."""
    product = Product("Тест", "О", 100.0, 5)
    monkeypatch.setattr('builtins.input', lambda _: 'y')
    product.price = 50.0
    assert product.price == 50.0


def test_product_price_setter_lower_price_cancel(monkeypatch):
    """Проверяем понижение цены с отменой 'n'."""
    product = Product("Тест", "О", 100.0, 5)
    monkeypatch.setattr('builtins.input', lambda _: 'n')
    product.price = 50.0
    assert product.price == 100.0


def test_product_price_setter_lower_price_invalid_input(monkeypatch):
    """Проверяем понижение цены с неверным вводом, затем 'y'."""
    product = Product("Тест", "О", 100.0, 5)
    inputs = iter(['x', 'y'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    product.price = 50.0
    assert product.price == 50.0


def test_new_product_creates_new():
    """Проверяем, что new_product создает новый объект, если нет дубликатов."""
    products = []
    product_data = {"name": "Новый Товар", "description": "Описание", "price": 100.0, "quantity": 10}
    new_prod = Product.new_product(product_data, products_list=products)

    assert isinstance(new_prod, Product)
    assert new_prod.name == "Новый Товар"
    assert new_prod.price == 100.0
    assert new_prod.quantity == 10


def test_new_product_handles_duplicates():
    """Проверяем, что new_product обрабатывает дубликаты."""
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
    """Проверяем, что new_product выбрасывает ошибку при неполных данных."""
    product_data = {"name": "Неполный", "price": 100.0}
    with pytest.raises(ValueError, match="Недостаточно данных для создания продукта."):
        Product.new_product(product_data)


def test_product_str_representation():
    """Проверяет строковое представление объекта Product."""
    product = Product("Телевизор", "Большой экран", 50000.0, 3)
    expected_str = "Телевизор, 50000.0 руб. Остаток: 3 шт."
    assert str(product) == expected_str


def test_category_str_representation():
    """Проверяет строковое представление объекта Category."""
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


def test_product_add_method():
    """Проверяет магический метод сложения __add__ для Product."""
    product_a = Product("Товар А", "Описание А", 100.0, 10) # Стоимость: 100 * 10 = 1000
    product_b = Product("Товар Б", "Описание Б", 200.0, 2)  # Стоимость: 200 * 2 = 400
    product_c = Product("Товар В", "Описание В", 50.0, 20)  # Стоимость: 50 * 20 = 1000

    assert (product_a + product_b) == 1400.0
    assert (product_a + product_c) == 2000.0
    assert (product_b + product_c) == 1400.0


def test_product_add_type_error():
    """Проверяет, что __add__ выбрасывает TypeError для не-Product объектов."""
    product_a = Product("Товар А", "Описание А", 100.0, 10)

    with pytest.raises(TypeError, match="Можно складывать только объекты Product"):
        _ = product_a + 50
    with pytest.raises(TypeError, match="Можно складывать только объекты Product"):
        _ = product_a + "строка"
    with pytest.raises(TypeError, match="Можно складывать только объекты Product"):
        _ = product_a + [1, 2]
