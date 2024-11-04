"""
URL configuration for shop_lw project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from blog.views import ArticleListView, ArticleDetailView
from products.views import ProductListView, ProductDetailView
from orders.views import *
from catalog import views


urlpatterns = [
    path('admin/', admin.site.urls),  # Страница админ панели
    path('tinymce/', include('tinymce.urls')),  # Маршрут для работы с редактором текста в админ панели
    path('accounts/', include("django.contrib.auth.urls")),  # Маршрут для работы с пользователями
    path('accounts/registration', views.registration, name="registration"),  # Маршрут для регистрации

    path('', views.index, name="home"),  # Главная страница
    path('search/', views.Search.as_view(), name='search_results'),  # Поиск по сайту

    path('add-to-wishlist/<int:product_id>/', add_to_wishlist, name='add_to_wishlist'), # Маршрут для добавления товара в избранное
    path('wishlist/', wishlist_view, name='wishlist'), # Страница - Избранное
    path('remove-from-wishlist/<int:product_id>/', remove_from_wishlist, name='remove_from_wishlist'),  # Маршрут для удаления товара из избранного

    path('cart/', cart, name='cart'),
    path('cart-adding/', cart_adding, name='cart_adding'),


    path('blog', ArticleListView.as_view(), name="blog"),  # Страница - Блог
    path('article/<int:pk>', ArticleDetailView.as_view(), name="article"),  # Маршрут для статей блога

    path('products', ProductListView.as_view(), name="products"),  # Каталог (все товары с фильтром)
    path('product/<int:pk>', ProductDetailView.as_view(), name="product"), # Маршрут товара из каталога
    path('products/<int:collection_id>/', ProductListView.as_view(), name='products'),

    path('sale-catalog', views.sale_catalog, name="sale_catalog"),  # Распродажа (все товары со скидкой)
    path('contact', views.contact, name="contact"),  # Страница - Контакты
    path('delivery', views.delivery, name="delivery"),  # Страница - Доставка


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
