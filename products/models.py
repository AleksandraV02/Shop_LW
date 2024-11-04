from django.db import models
from django.db.models.signals import post_save


class ProductEducations(models.Model):
    name = models.CharField(max_length=64, blank=False, null=False, default=None,
                            help_text="Введите категорию группы 'Educations'",
                            verbose_name="Группа товаров 'Educations'")
    objects = models.Model

    def __str__(self):
        return "%s" % self.name

    class Meta:
        verbose_name = "Группа товаров 'Educations'"
        verbose_name_plural = "Группы товаров 'Educations'"
        ordering = ["id"]


# Метод добавления товара в БД
class Product(models.Model):
    class CollectionChoices(models.TextChoices):
        AVATAR = 'AVATAR', 'Avatar'
        DC = 'DC', 'DC'
        MARVEL = 'MARVEL', 'Marvel'
        INDIANA_JONES = 'INDIANA JONES', 'Indiana Jones'
        ICONS = 'ICONS', 'Icons'
        JURASSIC_WORLD = 'JURASSIC WORLD', 'Jurassic World'
        FRIENDS = 'FRIENDS', 'Friends'
        CITY = 'CITY', 'City'

    class CategoryChoices(models.TextChoices):
        CONSTRUCTOR = 'CONSTRUCTOR', 'Конструктор'
        ACCESSORIES = 'ACCESSORIES', 'Аксессуары'
        BOOKS = 'BOOKS', 'Книги и журналы'

    category = models.CharField(max_length=25, choices=CategoryChoices.choices, default=None,
                                help_text="Выберите Категорию", verbose_name="Категория")
    collection = models.CharField(max_length=25, choices=CollectionChoices.choices, help_text="Выберите Коллекцию",
                                  verbose_name="Коллекция")
    name = models.CharField(max_length=64, verbose_name="Название товара")
    model_number = models.CharField(default=0, max_length=20, verbose_name="Артикул товара", blank=False, null=False)
    price = models.DecimalField(max_digits=7, decimal_places=2, default=0, verbose_name="Цена товара")
    total_price = models.DecimalField(max_digits=7, decimal_places=2, default=0, help_text="Цена с учетом скидки",
                                    verbose_name = "Скидочная цена")
    main_image = models.ImageField(upload_to="img/products", verbose_name="Основное изображение товара", null=True)
    description = models.TextField(verbose_name="Описание товара", blank=True, null=True)
    age = models.IntegerField(default=0, verbose_name="Возрастное ограничение", null=False, blank=False)
    elements = models.IntegerField(default=0, verbose_name="Количество деталей", help_text=
    "Укажите число кол-ва деталей", blank=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name="Наличие")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Дата создания")
    updated = models.DateTimeField(auto_now_add=False, auto_now=True, verbose_name="Дата обновления")
    objects = models.Model

    def __str__(self):
        return "%s" % self.name

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ["name"]

    def get_href(self):
        return "/product/{}".format(self.pk)  # self.pk то же самое что self.id


class ProductImage(models.Model):
    product = models.ForeignKey(Product, blank=True, null=True, default=None, on_delete=models.CASCADE,
                                verbose_name="Товар", related_name='images')
    image = models.ImageField(upload_to="img/products", verbose_name="Изображение товара")
    is_active = models.BooleanField(default=True, verbose_name="Наличие изображений")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Дата создания")
    updated = models.DateTimeField(auto_now_add=False, auto_now=True, verbose_name="Дата обновления")
    objects = models.Model

    def __str__(self):
        return "%s" % self.pk

    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"


# Модель отображающая товары со скидкой + автоматика подсчета скидки
class Discount(models.Model):
    product = models.OneToOneField(Product, blank=True, null=True, default=None, on_delete=models.CASCADE,
                                verbose_name="Товар", help_text="Выберите товар")
    price_no_discount = models.DecimalField(max_digits=5, decimal_places=2,default=0, verbose_name="Начальная цена")
    discount_active = models.BooleanField(default=True, verbose_name="Активность скидки")
    discount = models.IntegerField(default=0, verbose_name="Скидка %", help_text="Укажите % скидки")
    discount_price = models.DecimalField(max_digits=5, decimal_places=2,default=0, verbose_name="Итоговая цена товара")
    objects = models.Model

    def __str__(self):
        return "%s" % self.product

    class Meta:
        verbose_name = "Товар со скидкой"
        verbose_name_plural = "Товары со скидкой"
        ordering = ["discount"]

    def save(self, *args, **kwargs):
        price_no_discount = self.product.price
        self.price_no_discount = price_no_discount
        disc = ((self.price_no_discount / 100) * self.discount)
        self.discount_price = (self.price_no_discount - disc)

        super(Discount, self).save(*args, **kwargs)


# Метод для отображения цен со скидкой в админ панели
def product_in_discount_post_save(sender, instance, created, **kwargs):
    product = instance.product
    all_products = (Discount.objects.filter(product=product, discount_active=True))

    product_total_price = product.price
    for item in all_products:
        product_total_price = item.discount_price

    instance.product.total_price = product_total_price
    instance.product.save(force_update=True)


post_save.connect(product_in_discount_post_save, sender=Discount)





