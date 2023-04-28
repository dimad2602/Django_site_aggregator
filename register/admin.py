from django.contrib import admin
from .models import *
from django.contrib.auth.hashers import make_password


# Register your models here.

class UserAdmin(admin.ModelAdmin):
    # Без явного перечисления полей модели User будет выводиться
    # список коллекций
    list_display = [field.name for field in User._meta.fields]

    # Поля в таблице редактируемые
    list_editable = ("name",)

    # Список полей, по которым будет поиск в таблице
    search_fields = ['login', 'email']

    # Список полей, по которым будут фильтроваться записи в админке (панель)
    list_filter = ['email', 'login']

    # Можно обработать значения полей перед сохранением в БД
    def save_model(self, request, obj, form, change):
        obj.password == make_password(form.cleaned_data['password'])
        obj.save()

    class Meta:
        # Привязываем модель User
        model = User

    # Регистрируем модель User в админке


admin.site.register(User, UserAdmin)
