from django.contrib import admin
from products.models import *


admin.site.register(ProductEducations)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0


class ProductDiscountInline(admin.TabularInline):
    model = Discount
    extra = 0
    max_num = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "price", "total_price", "is_active", "category", "collection", "updated"]
    list_filter = ["is_active", "category", "collection"]
    inlines = [ProductImageInline, ProductDiscountInline]


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ["product", "id", "image", "is_active", "created", "updated"]
    list_filter = ["product"]


@admin.register(Discount)
class ProductDiscountAdmin(admin.ModelAdmin):
    list_display = ["product", "price_no_discount", "discount_active", "discount", "discount_price"]
    list_filter = ["product", "discount_active", "discount"]


