from .models import *


def getting_cart_info(request):
    session_key = request.session.session_key
    if not session_key:
        request.session["session_key"] = 123
        request.session.cycle_key()

    products_in_cart = ProductInCart.objects.filter(session_key=session_key, is_active=True, order__isnull=True)
    products_total_nmb = products_in_cart.count()

    return locals()




