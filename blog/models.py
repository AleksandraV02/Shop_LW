from django.db import models
from ckeditor.fields import RichTextField
from django.core.validators import FileExtensionValidator
from tinymce.models import HTMLField


# 1. ---- Модель Блог (Article) ----
class Article(models.Model):

    STATUS_OPTIONS = (
        ('published', 'Опубликовано'),
        ('draft', 'Черновик')
    )

    title = models.CharField(max_length=50, help_text="Введите название статьи", verbose_name="Название")
    thumbnail = models.ImageField(
        verbose_name="Превью поста",
        blank=True,
        upload_to="img/blog_images/",
        validators=[FileExtensionValidator(allowed_extensions=('png', 'jpg', 'webp', 'jpeg', 'gif'))]
    )
    status = models.CharField(choices=STATUS_OPTIONS, default="published", verbose_name="Статус поста", max_length=10)
    text = HTMLField(max_length=15000, help_text="Введите основной текст статьи", verbose_name="Текст")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Дата создания")
    objects = models.Model

    def __str__(self):
        return "%s" % self.title

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Блог"
        ordering = ["created"]

    def get_href(self):
        return "/article/{}".format(self.pk)



