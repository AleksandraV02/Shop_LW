from products.models import *
from orders.models import *
from django.views.generic import DetailView, ListView
from products.filters import ProductFilter


class ProductListView(ListView):
    model = Product  # Модель из которой будем читать объекты
    context_object_name = 'product_list'
    paginate_by = 15  # Сколько объектов будет передано в шаблон
    product_filter = ProductFilter

    def get_queryset(self):
        queryset = self.product_filter(self.request.GET, queryset=Product.objects.filter(is_active=True)).qs
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.product_filter(self.request.GET, queryset=self.get_queryset())
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        request = self.request
        discounts = Discount.objects.filter(product=product).first()
        images = ProductImage.objects.filter(product=product)
        other_product = Product.objects.exclude(pk=self.object.pk).filter(is_active=True)

        session_key = request.session.session_key
        if not session_key:
            request.session.cycle_key()
        print(request.session.session_key)

        context['discounts'] = discounts
        context['images'] = images
        context['other_product'] = other_product
        context['session_key'] = request.session.session_key

        return context
