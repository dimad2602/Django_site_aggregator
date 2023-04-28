from django import forms  # подключаем базовый класс forms от которого наследуються все наши формы
from .models import *


class CreateNewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['name', 'description', 'visibility', 'removed']
        labels = {
            'name': 'Название',
            'description': 'Описание',
            'visibility': 'Скрыть',
            'removed': 'Удалить',
        }


class RegisterPhotoNewsForm(forms.ModelForm):
    class Meta:
        model = PhotoNews

        fields = ['photo']

        exclude = ['news', 'status']

        labels = {
            'photo': 'Новость',
        }
