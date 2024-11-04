from django.contrib import admin
from blog.models import *


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ["title", "created", "thumbnail"]
    list_filter = ["title", "created", "status"]
