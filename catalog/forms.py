from django import forms
from django.forms import widgets as wg  # Импорт widget
from .models import *  # Импорт всех моделей


# Форма для регистрации нового пользователя
class Registration(forms.Form):
    username = forms.CharField(label="Логин", max_length=50, widget=wg.TextInput(attrs={"class": "form-control"}))
    email = forms.CharField(label="Email", required=False, max_length=50, widget=wg.TextInput(attrs={
        "class": "form-control"}))
    password = forms.CharField(label="Пароль", max_length=50, widget=wg.PasswordInput(attrs={"class": "form-control"}))
