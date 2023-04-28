from django import forms  # подключаем базовый класс forms от которого наследуються все наши формы
from django.forms import TextInput

from .models import *


class RegisterUserForm(forms.ModelForm):
    field_order = ['login', 'password', 'password2', 'email']

    # login = forms.TextInput(attrs={
    #    'id': 'myloginid',
    # })

    password = forms.CharField(
        max_length=24,
        label='Введите пароль',
        widget=forms.PasswordInput(
            attrs={'id': 'mypassid', 'placeholder': 'Enter your password'}
        ),
    )
    password2 = forms.CharField(
        max_length=24,
        label='Подтвердите пароль',
        widget=forms.PasswordInput(
            attrs={'id': 'mypass2id', 'placeholder': 'Repeat your password'}
        )
    )

    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)
        self.fields['login'].widget = TextInput(attrs={
            'id': 'myloginid',
            # 'class': 'myCustomClass',
            # 'name': 'myCustomName',
            'placeholder': 'myCustomPlaceholder'})
        self.fields['email'].widget = TextInput(attrs={
            'id': 'myemailid',
            # 'class': 'myCustomClass',
            # 'name': 'myCustomName',
            'placeholder': 'email'})
        if self.instance and self.instance.pk:
            self.fields.pop('password', None)
            self.fields.pop('password2', None)

    class Meta:
        model = User
        exclude = ['is_blocked', 'last_login', 'is_superuser', 'groups', 'user_permissions', 'is_staff', ]

        labels = {
            'login': 'Логин',
            'email': 'E-mail',
            'name': 'Имя',
        }


class RegisterUserPhotoForm(forms.ModelForm):
    class Meta:
        model = UserPhoto

        fields = ['photo']

        exclude = ['user', 'status']

        labels = {
            'photo': 'Фотография',
        }
