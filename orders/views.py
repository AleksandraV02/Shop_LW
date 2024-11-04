from django.shortcuts import render, get_object_or_404, redirect
from orders.models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect
from .forms import CheckoutContactForm


@login_required  # Метод отображающий страницу избранного авторизированным пользователям
def wishlist_view(request):
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    return render(request, 'wishlist.html', {'wishlist': wishlist})


@login_required
def add_to_wishlist(request, product_id):  # Метод для добавления товаров в избранное
    product = get_object_or_404(Product, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist.products.add(product)
    messages.success(request, "Товар в избранном!")
    return redirect('wishlist')


@login_required
def remove_from_wishlist(request, product_id):
    # Находим товар по его идентификатору
    wishlist = Wishlist.objects.get(user=request.user, products=product_id)
    wishlist.products.remove(product_id)
    messages.success(request, "Товар удален!")
    # Перенаправляем пользователя обратно на страницу избранного
    return redirect('wishlist')


@login_required
def cart_adding(request):
    return_dict = dict()
    session_key = request.session.session_key
    if not session_key:
        request.session.cycle_key()

    data = request.POST
    product_id = data.get("product_id")
    nmb = int(data.get("nmb", 1))  # Устанавливаем количество из переданного значения, по умолчанию 1
    is_delete = data.get("is_delete")

    if is_delete == 'true' or is_delete is True:
        # Устанавливаем is_active в False для удаления товара
        ProductInCart.objects.filter(id=product_id, session_key=session_key).update(is_active=False)
    else:
        # Ищем существующий товар, включая неактивные
        existing_product = ProductInCart.objects.filter(
            session_key=session_key, product_id=product_id
        ).first()

        if existing_product:
            # Если товар уже в корзине, активируем его и устанавливаем количество на переданное значение
            existing_product.is_active = True
            existing_product.nmb = nmb  # Используем значение nmb, переданное в запросе
            existing_product.save()
        else:
            # Если товара нет, создаем новый
            ProductInCart.objects.create(
                session_key=session_key,
                product_id=product_id,
                nmb=nmb,
                is_active=True
            )

    # Подготавливаем данные для ответа
    products_in_cart = ProductInCart.objects.filter(session_key=session_key, is_agitctive=True, order__isnull=True)
    return_dict["products_total_nmb"] = products_in_cart.count()
    return_dict["products"] = [
        {
            "id": item.id,
            "name": item.product.name,
            "price_per_item": item.price_per_item,
            "nmb": item.nmb
        }
        for item in products_in_cart
    ]

    return JsonResponse(return_dict)


@login_required
def cart(request):
    data = request.POST
    session_key = request.session.session_key
    if not session_key:
        request.session["session_key"] = 123
        request.session.cycle_key()
    products_in_cart = ProductInCart.objects.filter(session_key=session_key, is_active=True, order__isnull=True)
    print(products_in_cart)
    for item in products_in_cart:
        print(item.order)

    form = CheckoutContactForm(request.POST or None)
    if request.POST:
        print(request.POST)

        if form.is_valid():
            print("yes")
            data = request.POST
            name = data.get("name", "3423453")
            phone = data["phone"]
            user, created = User.objects.get_or_create(username=request.user, defaults={"first_name": name})

            order = Order.objects.create(user=user, customer_name=name, customer_phone=phone, status_id=1)

            for name, value in data.items():
                if name.startswith("product_in_cart_"):
                    product_in_cart_id = name.split("product_in_cart_")[1]
                    product_in_cart = ProductInCart.objects.get(id=product_in_cart_id)
                    print(type(value))

                    product_in_cart.nmb = value
                    product_in_cart.order = order
                    product_in_cart.save(force_update=True)

                    ProductInOrder.objects.create(product=product_in_cart.product, nmb=product_in_cart.nmb,
                                                  price_per_item=product_in_cart.price_per_item,
                                                  price_cart=product_in_cart.price_cart,
                                                  order=order)

            return HttpResponseRedirect(request.META['HTTP_REFERER'])
        else:
            print("no")
    return render(request, 'cart.html', locals())