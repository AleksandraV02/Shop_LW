from blog.models import *
from django.views.generic import DetailView, ListView


# Метод отображающий все статьи
class ArticleListView(ListView):
    model = Article  # Модель из которой будем читать объекты
    paginate_by = 3  # Сколько объектов будет передано в шаблон

    def get_queryset(self):
        return Article.objects.filter(status='published').order_by('-created')  # Фильтр + Сортировка


# Подробная информация о каждой статье
class ArticleDetailView(DetailView):
    model = Article

    # Метод, который передает список из ListView в DetailView.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['other_articles'] = (Article.objects.exclude(pk=self.object.pk).filter(status='published').order_by
                                     ('-created'))
        return context
