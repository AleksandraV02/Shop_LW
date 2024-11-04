from django.db.models import Q
from django.shortcuts import render
from .forms import Registration
from django.db.utils import IntegrityError  # Импорт ошибки - Регистрация с таким же username
from blog.models import *
from orders.models import *
from django.views.generic import ListView


def index(request):
    products_all = Product.objects.filter(is_active=True)
    products_constructors = Product.objects.filter(category='CONSTRUCTOR', is_active=True)
    products_accessories = Product.objects.filter(category='ACCESSORIES', is_active=True)
    products_books = Product.objects.filter(category='BOOKS', is_active=True)
    sale = Product.objects.filter(discount__discount_active=True, is_active=True)
    blog_all = Article.objects.filter(status="published").order_by('-created')
    products = Wishlist.objects.all()
    user = request.user if request.user.is_authenticated else None
    context = {"products_all": products_all, "products_constructors": products_constructors,
               "products_accessories": products_accessories, "products_books": products_books,
               "sale": sale, "blog_all": blog_all, "products": products, "user": user}
    return render(request, "index.html", context=context)


class Search(ListView):
    template_name = 'search_results.html'
    context_object_name = 'search_results'
    paginate_by = 15

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Product.objects.filter(
            Q(name__icontains=query) |
            Q(collection__icontains=query) |
            Q(category__icontains=query) |
            Q(model_number__icontains=query)
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q')
        return context


def registration(request):
    # Логика [Показ формы регистрации]
    if request.method == "GET":
        context = {"form": Registration()}
        return render(request, "registration/registration.html", context=context)
    # Логика [Сохранение в БД] + [Показ результата сохранения]
    if request.method == "POST":
        try:
            # Получение данных из формы (нового пользователя)
            username = request.POST.get("username")
            email = request.POST.get("email") if request.POST.get("email") != "" else None
            password = request.POST.get("password")
            # Запись нового пользователя в БД
            if email is None:
                User.objects.create_user(username=username, password=password).save()  # Без email
            else:
                User.objects.create_user(username, email, password).save()  # C email
            # Вызвать шаблон
            context = {"text": "Процесс регистрации завершен успешно!"}
            return render(request, "registration/registration.html", context=context)
        except IntegrityError:
            context = {"text": "Процесс регистрации завершен с ошибкой!"}
            return render(request, "registration/registration.html", context=context)


def sale_catalog(request):
    products_sale = Product.objects.filter(discount__discount_active=True, is_active=True)
    return render(request, "sale_catalog.html", locals())


def contact(request):
    return render(request, "contact.html", locals())


def delivery(request):
    return render(request, "delivery.html", locals())



