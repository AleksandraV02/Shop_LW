import django_filters
from products.models import Product
from django import forms


class ProductFilter(django_filters.FilterSet):
    total_price = django_filters.RangeFilter()
    age = django_filters.RangeFilter()
    elements = django_filters.RangeFilter()
    collection = django_filters.MultipleChoiceFilter(
        choices=Product.CollectionChoices.choices,
        widget=forms.CheckboxSelectMultiple()
    )
    category = django_filters.MultipleChoiceFilter(
        choices=Product.CategoryChoices.choices,
        widget=forms.CheckboxSelectMultiple()
    )

    class Meta:
        model = Product
        fields = {
        }
