from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from products.models import Product


# Метод добавления в БД статусов о заказе
class Status(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True, default=None, verbose_name="Статус",
                            help_text="Укажите статус")
    is_active = models.BooleanField(default=True, verbose_name="Активность")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Дата создания")
    updated = models.DateTimeField(auto_now_add=False, auto_now=True, verbose_name="Дата обновления")
    objects = models.Model

    def __str__(self):
        return "Статус %s" % self.name

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы заказа"


# Метод добавления в БД данных о человеке, который сделал заказ
class Order(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, default=None, on_delete=models.CASCADE, verbose_name="Пользователь")
    price_cart = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="К оплате")#total price for all products in order
    customer_name = models.CharField(max_length=64, blank=True, null=True, default=None, verbose_name="Имя")
    customer_email = models.EmailField(blank=True, null=True, default=None, verbose_name="Фамилия")
    customer_phone = models.CharField(max_length=48, blank=True, null=True, default=None, verbose_name="Номер телефона")
    customer_address = models.CharField(max_length=128, blank=True, null=True, default=None, verbose_name="Адрес")
    comments = models.TextField(blank=True, null=True, default=None, verbose_name="Комментарий к заказу")
    status = models.ForeignKey(Status, on_delete=models.CASCADE, verbose_name="Статус")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Дата создания")
    updated = models.DateTimeField(auto_now_add=False, auto_now=True, verbose_name="Дата обновления")
    objects = models.Model

    def __str__(self):
        return "Заказ %s %s" % (self.pk, self.status.name)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def save(self, *args, **kwargs):

        super(Order, self).save(*args, **kwargs)


class ProductInOrder(models.Model):
    order = models.ForeignKey(Order, blank=True, null=True, default=None, on_delete=models.CASCADE, verbose_name="Заказ")
    product = models.ForeignKey(Product, blank=True, null=True, default=None, on_delete=models.CASCADE, verbose_name="Товар")
    nmb = models.IntegerField(default=1, verbose_name="Количество")
    price_per_item = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Цена за единицу")
    price_cart = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Итоговая цена") #price*nmb
    is_active = models.BooleanField(default=True, verbose_name="Активность")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Дата создания")
    updated = models.DateTimeField(auto_now_add=False, auto_now=True, verbose_name="Дата обновления")
    objects = models.Model
    def __str__(self):
        return "%s" % self.product.name

    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказе'

    def save(self, *args, **kwargs):
        price_per_item = self.product.total_price
        self.price_per_item = price_per_item
        print (self.nmb)

        self.total_price = int(self.nmb) * price_per_item

        super(ProductInOrder, self).save(*args, **kwargs)


def product_in_order_post_save(sender, instance, created, **kwargs):
    order = instance.order
    all_products_in_order = ProductInOrder.objects.filter(order=order, is_active=True)

    order_price_cart = 0
    for item in all_products_in_order:
        order_price_cart += item.price_cart

    instance.order.price_cart = order_price_cart
    instance.order.save(force_update=True)


post_save.connect(product_in_order_post_save, sender=ProductInOrder)


class ProductInCart(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, default=None, on_delete=models.CASCADE,
                             verbose_name="Пользователь")
    session_key = models.CharField(max_length=128, blank=True, null=True, default=None, verbose_name="Ключ сессии")
    order = models.ForeignKey(Order, blank=True, null=True, default=None, on_delete=models.CASCADE, verbose_name="Заказ")
    product = models.ForeignKey(Product, blank=True, null=True, default=None, on_delete=models.CASCADE, verbose_name="Товар")
    nmb = models.IntegerField(default=1, verbose_name="Количество")
    price_per_item = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Цена за единицу")
    price_cart = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Итоговая цена")#price*nmb
    is_active = models.BooleanField(default=True, verbose_name="Активность")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Дата создания")
    updated = models.DateTimeField(auto_now_add=False, auto_now=True, verbose_name="Дата обновления")
    objects = models.Model

    def __str__(self):
        return "%s" % self.product.name

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'

    def save(self, *args, **kwargs):
        price_per_item = self.product.total_price
        self.price_per_item = price_per_item
        self.price_cart = int(self.nmb) * price_per_item

        super(ProductInCart, self).save(*args, **kwargs)


class Wishlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, verbose_name="Товар", help_text="Выберите товар")
    objects = models.Model

    def __str__(self):
        return f'Избранной для {self.user.username}'

    class Meta:
        verbose_name = "Избранное"
        verbose_name_plural = "Избранные товары"


@receiver(post_save, sender=User)
def create_wishlist(sender, instance, created, **kwargs):
    if created:
        Wishlist.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_wishlist(sender, instance, **kwargs):
    instance.wishlist.save()
