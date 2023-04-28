import re

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse_lazy
from django.views.generic import View
from .forms import *
from django.contrib.auth.hashers import make_password
from products.models import Game, PhotoGame
import random

from .utils import *


# Create your views here.


class RegisterView(View):
    def get(self, request):

        code = random.randrange(1121, 9899)
        global str_code
        str_code = str(code)

        form = RegisterUserForm(request.POST, request.FILES)
        formPhoto = RegisterUserPhotoForm(request.POST)
        context = {
            'form': form,
            'formPhoto': formPhoto,
            'captcha': str_code
        }

        return render(request, 'register/register.html', context=context)

    def post(self, request):
        form = RegisterUserForm(request.POST)

        if form.is_valid():
            captcha = request.POST.get('captcha')
            if str_code == str(captcha):

                if form.cleaned_data['password'] == form.cleaned_data['password2']:

                    userdata = form.save(commit=False)
                    # Хешируем пароль
                    userdata.password = make_password(form.cleaned_data['password2'])
                    userdata.save()
                    print(userdata.id)

                    if userdata.id is not None:
                        user = User.objects.get(pk=userdata.id)
                        formPhoto = RegisterUserPhotoForm(request.POST, request.FILES)
                        if formPhoto.is_valid():
                            print("FORM IS VALID!")
                            photodata = formPhoto.save(commit=False)
                            photodata.user = user
                            photodata.save()
                        else:
                            print("FORM IS NOT VALID!")

                        # Задаем множество прав по умолчанию для созданного пользователя
                        userRight = User_Right()
                        userRight.id_user = user
                        right = Right.objects.get(pk=2)
                        userRight.id_right = right
                        userRight.save()
                    return HttpResponse(
                        "<nav><a href='/'>Главная страница</a></nav> <h4>Регистрация выполнена</h4>")
                else:
                    return HttpResponse(
                        "<nav> <a href='/'>Главная страница</a> "
                        "<a href='/customer/register'>Регистрация</a> </nav> <h4>Пароли не совпадают</h4>")
            else:
                print("{} {}".format(str_code, captcha))
                return HttpResponse(
                    "<nav> <a href='/'>Главная страница</a> "
                    "<a href='/customer/register'>Регистрация</a> </nav> <h4>Коды не совпали</h4>")


class LoginUser(DataMixin, LoginView):
    form = AuthenticationForm
    template_name = 'register/login.html'
    success_url = '/'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # context = {
        #     'form': form,
        # }
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.item()) + list(c_def.items()))

    # def post(self, request, *args, **kwargs):
    #     return HttpResponse('3425336')
    # def get_success_url(self):
    #     return reverse_lazy('/')


class UserListView(View):
    def get(self, request):
        """
        Поскольку предполагается, что пользователь сможет блокировать
        свой профиль, то в список должны попасть только незаблокированные
        (is_blocked=False) записи.
        """
        users = User.objects.filter(is_blocked=False)

        """ Paginator """
        # /register/list/?page=1
        page = request.GET.get('page', 1)
        paginator = Paginator(users, 5)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)

        # -------------------
        try:
            json_users = []
            x = 0
            y = 0
            page_number = request.GET.get('page')
            for i in users:
                if page_number:
                    if int(page_number) == 1:
                        x = x + 1
                    else:
                        print("1")
                        if y == 0:
                            y = 1
                            x = 1 + 5 * (int(page_number) - 1)
                            # x = 2 * int(page_number) + (int(page_number) - 2)
                        else:
                            x = x + 1
                else:
                    x = x + 1
                userphoto = UserPhoto.objects.get(user=i).photo.url
                json_users.append({"name": i.name, "count": x, "id": i.id, "photo_url": userphoto})
        except UserPhoto.DoesNotExist:
            newsphoto = False
        if userphoto:
            gamephoto = userphoto[0]
        # -------------------

        context = {
            "message": "Список пользователей",
            "users": json_users,
            "pages": users,
        }
        return render(request, 'register/list.html', context=context)


class UserDetailView(View):
    def get(self, request, **kwargs):
        user = User.objects.get(pk=kwargs['pk'])
        games = Game.objects.filter(creator=user).filter(visibility=False, removed=False).order_by('-pk')[:5]
        json_games = []
        x = 0
        if games:

            # -------------------
            try:
                for i in games:
                    x = x + 1
                    gamephoto = PhotoGame.objects.get(game=i).photo.url
                    json_games.append(
                        {"name": i.name, "id": x, "description": i.description, "genre": i.genre,
                         "photo_url": gamephoto})

                # gamephoto2 = PhotoGame.object.filter()
            except PhotoGame.DoesNotExist:
                gamephoto = False
            # По умолчанию берется первая найденная фотография gamephoto[0].
            if gamephoto:
                gamephoto = gamephoto[0]
            # -------------------
        try:
            # Вместо get() используется filter(), т.к. с одним пользователем
            # может быть связано N фото.
            # Если использовать get(), то он вернет несколько записей,
            # что приведет к ошибке.
            userphoto = UserPhoto.objects.filter(user=user)
        except UserPhoto.DoesNotExist:
            userphoto = False
        # По умолчанию берется первая найденная фотография userphoto[0].
        if userphoto:
            userphoto = userphoto[0]
        context = {
            "message": "Профиль пользователя",
            "message2": "Записи пользователя",
            "user": user,
            "userphoto": userphoto,
            "games": json_games,
        }
        return render(request, 'register/detail.html', context=context)


class UserEditView(View):
    def get(self, request, **kwargs):
        user = User.objects.get(pk=kwargs['pk'])
        form = RegisterUserForm(request.POST or None, instance=user)
        form.id = user.id

        # form.fields.pop('password')
        # form.fields.pop('password2')

        context = {
            "message": "Редактирование пользователя",
            "form": form,
        }
        return render(request, 'register/edit.html', context=context)


class UserSaveView(View):
    def post(self, request):
        user = User.objects.get(pk=request.POST.get('id'))
        form = RegisterUserForm(request.POST, instance=user)

        if form.is_valid():
            user = form.save(commit=True)
        return redirect('register:user_list')


class UserRemoveView(View):
    def get(self, request, **kwargs):
        User.objects.filter(pk=kwargs['pk']).update(is_blocked=True)
        return redirect('register:user_list')


class AjaxViewForForm(View):
    def post(self, request):
        data = {}

        myemailid = request.POST.get('myemailid')

        resultemail = re.search(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+$', myemailid)

        if resultemail:
            data = {
                'message': 'Эл. почта указан <b style="color: green; style="right: 20px" ">Правильно</b>!',
                'match': resultemail.group(0),
            }
        else:
            data = {
                'message': 'Эл. почта указан <b style="color: red;">Некорректно</b>!',
                'otkl': '1',
            }
        return JsonResponse(data)


class AjaxViewForlogin(View):
    def post(self, request):
        data = {}

        myloginid = request.POST.get('myloginid')

        resultlogin = re.search('^(?=[a-zA-Z0-9._]{4,24}$)(?!.*[_.]{2})[^_.].*[^_.]$', myloginid)

        if resultlogin:
            data = {
                'message': 'Логин указан <b style="color: green; style="right: 20px" ">Правильно</b>!',
                'match': resultlogin.group(0),
            }
            if resultlogin and User.objects.filter(login=myloginid):
                data = {
                    'message': 'Пользователь с таким именем <b style="color: red; style="right: 20px" "> уже существует</b>!',
                    'otkl': '1',
                }
        else:
            data = {
                'message': 'Логин указан <b style="color: red;">Некорректно</b>! Минимум 4 символа',
                'otkl': '1',
            }
        return JsonResponse(data)


class AjaxViewForPass(View):
    def post(self, request):
        data = {}

        mypassid = request.POST.get('mypassid')

        resultpass = re.search('^.*(?=.{4,20})(?=.*[a-zA-Z])(?=.*\d)(?=.*[!#$%&? "]).*$', mypassid)

        if resultpass:
            data = {
                'message': 'Пароль указан <b style="color: green; style="right: 20px" ">Правильно</b>!',
                'match': resultpass.group(0),
            }
        else:
            data = {
                'message': 'Пароль указан <b style="color: red;">Некорректно</b>! '
                           'Латинские буквы, цифры, спецсимволы. Минимум 4 символа.',
                'otkl': '1',
            }
        return JsonResponse(data)


class AjaxViewForPass2(View):
    def post(self, request):
        data = {}

        mypass2id = request.POST.get('mypass2id')

        resultpass2 = re.search('^.*(?=.{4,20})(?=.*[a-zA-Z])(?=.*\d)(?=.*[!#$%&? "]).*$', mypass2id)

        if resultpass2:
            data = {
                'message': 'Пароль указан <b style="color: green; style="right: 20px" ">Правильно</b>!',
                'match': resultpass2.group(0),
            }
        else:
            data = {
                'message': 'Пароль указан <b style="color: red;">Некорректно</b>! '
                           'Латинские буквы, цифры, спецсимволы. Минимум 4 символа.',
                'otkl': '1',
            }
        return JsonResponse(data)
