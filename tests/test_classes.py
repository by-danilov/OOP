import pytest
import sys
import os

# Определяем путь к корневой директории проекта (OOP)
# os.path.dirname(__file__) -> текущая директория (tests/)
# os.path.join(..., '..') -> поднимаемся на уровень выше (OOP/)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Добавляем корневую директорию проекта в sys.path
# Это позволяет Python найти 'src' как пакет.
sys.path.insert(0, project_root)

# Теперь импорт из src.main должен работать
from src.main import Product, Category

# Фикстура Pytest для сброса счетчиков перед каждым тестом
@pytest.fixture(autouse=True)
def reset_category_counts():
    """
    Сбрасывает счетчики класса Category перед каждым тестом.
    Это предотвращает влияние тестов друг на друга.
    """
    Category.category_count = 0
    Category.product_count = 0

# --- Старые тесты (проверяем, что они продолжают работать) ---

def test_product_initialization():
    """Проверяем корректность инициализации объекта Product."""
    product = Product("Тестовый Продукт", "Описание тестового продукта", 100.0, 10)

    assert product.name == "Тестовый Продукт"
    assert product.description == "Описание тестового продукта"
    assert product.price == 100.0 # Используем геттер price
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

# --- Новые тесты для новой функциональности ---

def test_add_product_method():
    """Проверяем метод add_product в Category и его влияние на product_count."""
    category = Category("ТестКат", "Описание", [])
    initial_product_count = Category.product_count
    assert len(category.products) == 0

    product1 = Product("Товар1", "О1", 10.0, 1)
    category.add_product(product1)
    assert len(category.products) == 1
    assert category.products[0] == "Товар1, 10.0 руб. Остаток: 1 шт."
    assert Category.product_count == initial_product_count + 1 # Счетчик должен увеличиться на 1

    product2 = Product("Товар2", "О2", 20.0, 2)
    category.add_product(product2)
    assert len(category.products) == 2
    assert category.products[1] == "Товар2, 20.0 руб. Остаток: 2 шт."
    assert Category.product_count == initial_product_count + 2 # Счетчик должен увеличиться еще на 1

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
    # Используем capsys для захвата вывода в консоль
    # pytest.raises не подходит, т.к. не выбрасывается исключение, а печатается сообщение
    # и значение не меняется
    initial_price = product.price

    # Тестируем цену 0
    product.price = 0
    assert product.price == initial_price # Цена не должна измениться
    # Проверка вывода сообщения (закомментировано, так как `input` блокирует тесты)
    # with capsys.disabled(): # Временно отключаем захват, чтобы имитировать ввод
    #     product.price = 0
    # captured = capsys.readouterr()
    # assert "Цена не должна быть нулевая или отрицательная" in captured.out

    # Тестируем отрицательную цену
    product.price = -50
    assert product.price == initial_price # Цена не должна измениться
    # with capsys.disabled():
    #     product.price = -50
    # captured = capsys.readouterr()
    # assert "Цена не должна быть нулевая или отрицательная" in captured.out

    # Проверка на нечисловое значение
    product.price = "abc"
    assert product.price == initial_price # Цена не должна измениться


# Для тестирования интерактивного ввода (input) в Pytest
# требуется использовать monkeypatch.setattr для подмены input.
# Это позволяет тестам "вводить" данные без ручного вмешательства.
def test_product_price_setter_lower_price_confirm(monkeypatch):
    """Проверяем понижение цены с подтверждением 'y'."""
    product = Product("Тест", "О", 100.0, 5)
    monkeypatch.setattr('builtins.input', lambda _: 'y') # Подменяем input на 'y'
    product.price = 50.0
    assert product.price == 50.0

def test_product_price_setter_lower_price_cancel(monkeypatch):
    """Проверяем понижение цены с отменой 'n'."""
    product = Product("Тест", "О", 100.0, 5)
    monkeypatch.setattr('builtins.input', lambda _: 'n') # Подменяем input на 'n'
    product.price = 50.0
    assert product.price == 100.0 # Цена не должна измениться

def test_product_price_setter_lower_price_invalid_input(monkeypatch):
    """Проверяем понижение цены с неверным вводом, затем 'y'."""
    product = Product("Тест", "О", 100.0, 5)
    # Симулируем несколько вводов: сначала 'x', потом 'y'
    inputs = iter(['x', 'y'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    product.price = 50.0
    assert product.price == 50.0 # Цена должна измениться после 'y'

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

    assert updated_prod is existing_product # Должен вернуть ссылку на существующий объект
    assert updated_prod.quantity == 8     # 5 (старое) + 3 (новое)
    assert updated_prod.price == 70.0     # Выбирается более высокая цена

    product_data_lower_price = {"name": "Existing Product", "description": "New Desc", "price": 40.0, "quantity": 2}
    updated_prod_again = Product.new_product(product_data_lower_price, products_list=products)

    assert updated_prod_again is existing_product
    assert updated_prod_again.quantity == 10    # 8 + 2
    assert updated_prod_again.price == 70.0     # Цена не должна понизиться (40 < 70)

def test_new_product_missing_data_raises_error():
    """Проверяем, что new_product выбрасывает ошибку при неполных данных."""
    product_data = {"name": "Неполный", "price": 100.0} # Нет описания и количества
    with pytest.raises(ValueError, match="Недостаточно данных для создания продукта."):
        Product.new_product(product_data)
