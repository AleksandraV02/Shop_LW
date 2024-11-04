from django import forms
from django.forms import widgets as wg  # Импорт widget
from .models import *  # Импорт всех моделей


# Форма для регистрации нового пользователя
class CheckoutContactForm(forms.Form):
    name = forms.CharField(required=True)
    phone = forms.CharField(required=True)
