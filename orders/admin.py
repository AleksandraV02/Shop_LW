from django.contrib import admin
from .models import *

admin.site.register(Wishlist)


class ProductInOrderInline(admin.TabularInline):
    model = ProductInOrder
    extra = 0


@admin.register(Order)
class OrderAdmin (admin.ModelAdmin):
    list_display = ["id", "user", "price_cart", "status", "created", "updated"]
    list_filter = ["status", "user", "created", "updated"]
    inlines = [ProductInOrderInline]


@admin.register(Status)
class StatusAdmin (admin.ModelAdmin):
    list_display = ["name"]


@admin.register(ProductInOrder)
class ProductInOrderAdmin (admin.ModelAdmin):
    list_display = ["id", "product", "nmb", "price_cart", "is_active", "created", "updated"]


@admin.register(ProductInCart)
class ProductInCartAdmin (admin.ModelAdmin):
    list_display = ["id", "session_key", "product", "nmb", "price_per_item", "price_cart", "is_active", "created", "updated"]




