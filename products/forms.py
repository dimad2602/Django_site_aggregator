from django import forms  # подключаем базовый класс forms от которого наследуються все наши формы
from .models import *
from django.forms import DateTimeInput, MultipleChoiceField
from model_utils import Choices


class CreateProductForm(forms.ModelForm):
    field_order = ['name', 'description', 'Status', 'genre', 'developer', 'publisher', 'date_release',
                  'visibility', 'removed'
                  ]

    OPTIONS = [
        ('Пройдено', 'Пройдено'),
        ('Планирую пройти', 'Планирую пройти'),
        ('Играю', 'Играю'),
        ('Заброшено', 'Заброшено'),
    ]
    #Status = models.PositiveSmallIntegerField(("Status"), choices=OPTIONS)

    Status = forms.ChoiceField(
        choices=OPTIONS,
        initial='0',
        #widget=forms.SelectMultiple(),
        required=True,
        label='Статус',
    )

    def __init__(self, *args, **kwargs):
        super(CreateProductForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            print("редактирование")
            self.fields.pop('removed', None)
        else:
            self.fields.pop('visibility', None)
            self.fields.pop('removed', None)


    class Meta:
        model = Game

        fields = ['name', 'description', 'Status', 'genre', 'developer', 'publisher', 'date_release',
                  'visibility', 'removed', #'photo'
                  ]

        #exclude = ['game', 'status']

        labels = {
            'name': 'Название',
            'description': 'Описание',
            'genre': 'Жанр',
            'Status': 'Статус',
            'developer': 'Разработчик',
            'publisher': 'Издатель',
            'date_release': 'Дата выхода',
            'visibility': 'Скрыть',
            'removed': 'Удалить',
            'photo': 'Обложка',
        }

        widgets = {
            "date_release": DateTimeInput(attrs={
                'class': "form-control",
                'type': 'date',
                'placeholder': "Дата публикации"
            }),
        }


class RegisterPhotoGameForm(forms.ModelForm):
    class Meta:
        model = PhotoGame

        fields = ['photo']

        exclude = ['game', 'status']

        labels = {
            'photo': 'Обложка',
        }


"""
class CreateProductForm(forms.Form):  # создаем собственный класс формы и определим для него поля
    # атрибут - экземпляр класса CharField
    name = forms.CharField(
        label="Победитель",
        widget=forms.TextInput(attrs={'placeholder': 'Победитель'})  # атрибут для html элементов(виджет); attrs - словарь
    )
    award = forms.CharField(
        label="Название награды",
        widget=forms.TextInput(attrs={'placeholder': 'Название награды'})
        # атрибут для html элементов(виджет); attrs - словарь
    )
    count = forms.IntegerField(
        label="Место",
        widget=forms.NumberInput(attrs={'placeholder': 'Место'})  # placeholder это не значение, а "подсказка"
    )
    datee = forms.DateField(
        label="Дата",
        widget=forms.DateTimeInput()
    )
    photo = forms.ImageField(label="Фото")
    """
