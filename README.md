# Shop_LW

Shop_LW — это прототип интернет-магазина, разработанный с использованием Python и Django для бэкенда и JavaScript для интерактивных элементов на фронтенде. Проект позволяет управлять товарами, пользователями и заказами, а также предоставляет пользователям возможность добавлять товары в корзину и оформлять заказы.

## Функциональные возможности

- **Просмотр каталога товаров** — пользователи могут просматривать доступные товары, фильтровать их по категориям.
- **Добавление товаров в корзину** — возможность добавлять товары в корзину с последующим редактированием количества.
- **Оформление заказа** — создание и подтверждение заказа для товаров в корзине.
- **Регистрация и авторизация пользователей** — безопасная регистрация и вход для постоянных покупателей.
- **Панель администратора** — управление товарами, категориями и заказами для администраторов сайта.

## Основные технологии

- **Python 3.x** — основной язык для логики бэкенда.
- **Django** — фреймворк для разработки бэкенд-части.
- **JavaScript** — для динамических элементов на фронтенде.
- **SQLite** (по умолчанию) — база данных для хранения информации о товарах, заказах и пользователях.
- **HTML и CSS** — для базового интерфейса.

## Установка и запуск

1. Клонируйте репозиторий:

   ```bash
   git clone https://github.com/AleksandraV02/Shop_LW.git
   ```

2. Перейдите в директорию проекта:

   ```bash
   cd Shop_LW
   ```

3. Создайте виртуальное окружение и активируйте его:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # для Windows: venv\Scripts\activate
   ```

4. Установите зависимости:

   ```bash
   pip install -r requirements.txt
   ```

5. Проведите миграции базы данных:

   ```bash
   python manage.py migrate
   ```

6. Запустите сервер:

   ```bash
   python manage.py runserver
   ```

7. Откройте [http://127.0.0.1:8000/](http://127.0.0.1:8000/) в браузере для доступа к проекту.

## Примеры использования (Python и JavaScript)

### На стороне сервера (Python/Django)

1. **Создание нового товара**:
   
   ```python
   from products.models import Product

   product = Product.objects.create(
       name="Product Name",
       description="Product description",
       price=100.0,
       stock=10,
       category="Electronics"
   )
   ```

2. **Добавление товара в корзину пользователя**:

   ```python
   from cart.models import Cart, CartItem

   def add_to_cart(user, product_id, quantity):
       cart, created = Cart.objects.get_or_create(user=user)
       item, created = CartItem.objects.get_or_create(cart=cart, product_id=product_id)
       item.quantity += quantity
       item.save()
   ```

3. **Оформление заказа**:

   ```python
   from orders.models import Order, OrderItem

   def create_order(user):
       cart = Cart.objects.get(user=user)
       order = Order.objects.create(user=user, total_price=cart.get_total_price())
       for item in cart.items.all():
           OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)
       cart.clear()
   ```

### На стороне клиента (JavaScript)

1. **Динамическое обновление количества товаров в корзине**:

   ```javascript
   // Функция для обновления количества товаров в корзине
   function updateCartQuantity(productId, newQuantity) {
       fetch(`/cart/update_quantity/`, {
           method: "POST",
           headers: {
               "Content-Type": "application/json",
               "X-CSRFToken": csrftoken,
           },
           body: JSON.stringify({ product_id: productId, quantity: newQuantity }),
       })
       .then(response => response.json())
       .then(data => {
           document.getElementById("cart-total").innerText = data.cart_total;
           document.getElementById(`product-${productId}-quantity`).innerText = newQuantity;
       });
   }
   ```

2. **Асинхронное добавление товара в корзину**:

   ```javascript
   // Асинхронная функция для добавления товара в корзину
   function addToCart(productId) {
       fetch(`/cart/add/`, {
           method: "POST",
           headers: {
               "Content-Type": "application/json",
               "X-CSRFToken": csrftoken,
           },
           body: JSON.stringify({ product_id: productId }),
       })
       .then(response => response.json())
       .then(data => {
           alert("Товар добавлен в корзину!");
           document.getElementById("cart-count").innerText = data.cart_count;
       });
   }
   ```

3. **Удаление товара из корзины**:

   ```javascript
   // Функция для удаления товара из корзины
   function removeFromCart(productId) {
       fetch(`/cart/remove/`, {
           method: "POST",
           headers: {
               "Content-Type": "application/json",
               "X-CSRFToken": csrftoken,
           },
           body: JSON.stringify({ product_id: productId }),
       })
       .then(response => response.json())
       .then(data => {
           document.getElementById(`product-${productId}`).remove();
           document.getElementById("cart-total").innerText = data.cart_total;
       });
   }
   ```

## Тестирование

Для запуска всех тестов проекта используйте команду:

   ```bash
   python manage.py test
   ```

### Пример теста для функции добавления товара

```python
from django.test import TestCase
from products.models import Product
from cart.models import Cart, CartItem
from django.contrib.auth.models import User

class CartTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.product = Product.objects.create(name="Test Product", price=50.0, stock=5)

    def test_add_to_cart(self):
        cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=cart, product=self.product, quantity=2)
        self.assertEqual(cart.items.count(), 1)
```

## Архитектура проекта

- `products` — приложение для управления товарами.
- `cart` — приложение для корзины пользователя.
- `orders` — приложение для оформления и обработки заказов.
- `users` — приложение для регистрации и авторизации пользователей.

## Контакты

Если у вас есть вопросы, свяжитесь со мной через [email@example.com](mailto:email@example.com) или через GitHub Issues.

## Лицензия

Проект распространяется под лицензией MIT.
 
