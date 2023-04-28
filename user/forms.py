from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User


class UserLoginForm(AuthenticationForm):
    """
        Переопределяем стандартную форму авторизации пользователя
    """
    username = forms.CharField(
        label="Логин",
        widget=forms.TextInput(
            attrs={  # "class": "form-control",
                "placeholder": "Введите логин"}))
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(
            attrs={  # "class": "form-control",
                "placeholder": "Введите пароль"}))


class UserSignupForm(UserCreationForm):
    username = forms.CharField(label="Логин", widget=forms.TextInput(attrs={}))
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={}))
    password2 = forms.CharField(label="Повтор пароля", widget=forms.PasswordInput(attrs={}))

    first_name = forms.CharField(label="Имя", widget=forms.TextInput(attrs={}))
    last_name = forms.CharField(label="Фамилия", widget=forms.TextInput(attrs={}))
    email = forms.CharField(label="E-mail", widget=forms.EmailInput(attrs={}))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email', 'first_name', 'last_name')
