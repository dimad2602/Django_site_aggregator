from django.shortcuts import render, HttpResponse, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
# from django.http import HttpResponse;   import http.client;  from django import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import View
from .forms import *  # подключаем CreateProductForm
from .utils import handle_uploaded_file
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.functions import Lower
from django.contrib import messages


# Create your views here.from pyproj import settings

def products(request):  # скорее всего нужно для моментального отображения, думаю можно будет вторично использовать
    context = {}
    if request.method == "POST":
        context = {
            "message": "Здесь будет перечень игр",
            "name": request.POST["name"]
        }
        return render(request, 'products/products.html', context=context)
    else:
        return render(request, 'products/products.html')


def get(self, reguest):  # скорее всего нужно для моментального отображения, думаю можно будет вторично использовать
    return HttpResponse('Method GET')


class CreateProduct(LoginRequiredMixin, View):  # создаем класс для представления, наследуеться от класса view
    # login_url = '/admin/'
    # login_url = reverse_lazy('riddles:home')
    login_url = reverse_lazy('register:login_in_register')

    # raise_exception = True # 403
    def post(self, request):
        form = CreateProductForm(request.POST, request.FILES)
        context = {}
        if form.is_valid():
            gamedata = form.save(commit=False)
            gamedata.creator = request.user
            gamedata.save()

            if gamedata.id is not None:
                game = Game.objects.get(pk=gamedata.id)
                formPhoto = RegisterPhotoGameForm(request.POST, request.FILES)
                if formPhoto.is_valid():
                    print("FORM IS VALID!")
                    photodata = formPhoto.save(commit=False)
                    photodata.game = game
                    photodata.save()

                else:
                    print("FORM IS NOT VALID!")
            game = Game.objects.get(pk=gamedata.id)
            try:
                # Вместо get() используется filter(), т.к. с одним пользователем
                # может быть связано N фото.
                # Если использовать get(), то он вернет несколько записей,
                # что приведет к ошибке.
                photogame = PhotoGame.objects.filter(game=game)
                print("AU")
            except PhotoGame.DoesNotExist:
                photogame = False
            # По умолчанию берется первая найденная фотография userphoto[0].
            if photogame:
                photogame = photogame[0]
            context = {
                "message": "Список игр",
                "name": form.cleaned_data["name"],
                "description": form.cleaned_data["description"],
                "game": gamedata,
                "photogame": photogame,
            }
            # return render(request, "products/products.html", context=context)
            return redirect('riddles:home')

    def get(self, request):
        form = CreateProductForm()
        photogame = RegisterPhotoGameForm(request.POST)
        context = {
            "message": "Форма создания",
            "form": form,
            "photogame": photogame,
        }
        return render(request, "products/create.html", context=context)


class GamesListView(LoginRequiredMixin, View):
    login_url = reverse_lazy('register:login_in_register')

    def get(self, request):
        """
        Поскольку предполагается, что пользователь сможет блокировать
        свой профиль, то в список должны попасть только незаблокированные
        (is_blocked=False) записи.
        """
        games = Game.objects.filter(creator=self.request.user).filter(visibility=False, removed=False)
        if not games:
            return redirect('products:product_create')
        """ Paginator """
        # /register/list/?page=1
        page = request.GET.get('page', 1)
        paginator = Paginator(games, 5)
        try:
            games = paginator.page(page)
        except PageNotAnInteger:
            games = paginator.page(1)
        except EmptyPage:
            games = paginator.page(paginator.num_pages)

        # -------------------
        try:
            # game = Game.objects.get()

            # Вместо get() используется filter(), т.к. с одним пользователем
            # может быть связано N фото.
            # Если использовать get(), то он вернет несколько записей,
            # что приведет к ошибке.
            json_games = []
            x = 0
            y = 0
            page_number = request.GET.get('page')
            for i in games:
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
                gamephoto = PhotoGame.objects.get(game=i).photo.url
                json_games.append(
                    {"name": i.name, "count": x, "id": i.id, "description": i.description, "genre": i.genre,
                     "Status": i.Status,
                     "photo_url": gamephoto})

            # gamephoto2 = PhotoGame.object.filter()
        except PhotoGame.DoesNotExist:
            gamephoto = False
        # По умолчанию берется первая найденная фотография gamephoto[0].
        if gamephoto:
            gamephoto = gamephoto[0]
        # -------------------

        context = {
            "message": "Список игр",
            "games": json_games,
            "pages": games,
            # "gamephoto": gamephoto
        }
        return render(request, 'products/list_game.html', context=context)


class ListSearchView(LoginRequiredMixin, View):
    login_url = reverse_lazy('register:login_in_register')

    def get(self, request):
        query = self.request.GET.get('q')
        print(query)
        games = Game.objects.filter(creator=self.request.user).filter(removed=False).filter(name__contains=f'{query}')
        # (Lower('name')).values_list('name', flat=True)
        if not games:
            messages.info(request, 'Your password has been changed successfully!')
            return render(request, 'products/list_game.html')
            #return redirect('products:product_create')
        """ Paginator """
        # /register/list/?page=1
        page = request.GET.get('page', 1)
        paginator = Paginator(games, 5)
        try:
            games = paginator.page(page)
        except PageNotAnInteger:
            games = paginator.page(1)
        except EmptyPage:
            games = paginator.page(paginator.num_pages)
        # -------------------
        try:
            json_games = []
            x = 0
            y = 0
            page_number = request.GET.get('page')
            for i in games:
                if page_number:
                    if int(page_number) == 1:
                        x = x + 1
                    else:
                        print("1")
                        if y == 0:
                            y = 1
                            x = 1 + 5 * (int(page_number) - 1)
                        else:
                            x = x + 1
                else:
                    x = x + 1
                gamephoto = PhotoGame.objects.get(game=i).photo.url
                json_games.append(
                    {"name": i.name, "count": x, "id": i.id, "description": i.description, "genre": i.genre,
                     "Status": i.Status,
                     "photo_url": gamephoto})
        except PhotoGame.DoesNotExist:
            gamephoto = False
        if gamephoto:
            gamephoto = gamephoto[0]

        context = {
            "message": "Список игр",
            "games": json_games,
            "pages": games,
        }
        return render(request, 'products/list_game.html', context=context)


class ListSortedByNameView(LoginRequiredMixin, View):
    login_url = reverse_lazy('register:login_in_register')

    def get(self, request):
        games = Game.objects.filter(creator=self.request.user).filter(removed=False).order_by(Lower('name'))
        # (Lower('name')).values_list('name', flat=True)
        if not games:
            return redirect('products:product_create')
        """ Paginator """
        # /register/list/?page=1
        page = request.GET.get('page', 1)
        paginator = Paginator(games, 5)
        try:
            games = paginator.page(page)
        except PageNotAnInteger:
            games = paginator.page(1)
        except EmptyPage:
            games = paginator.page(paginator.num_pages)
        # -------------------
        try:
            json_games = []
            x = 0
            y = 0
            page_number = request.GET.get('page')
            for i in games:
                if page_number:
                    if int(page_number) == 1:
                        x = x + 1
                    else:
                        print("1")
                        if y == 0:
                            y = 1
                            x = 1 + 5 * (int(page_number) - 1)
                        else:
                            x = x + 1
                else:
                    x = x + 1
                gamephoto = PhotoGame.objects.get(game=i).photo.url
                json_games.append(
                    {"name": i.name, "count": x, "id": i.id, "description": i.description, "genre": i.genre,
                     "Status": i.Status,
                     "photo_url": gamephoto})
        except PhotoGame.DoesNotExist:
            gamephoto = False
        if gamephoto:
            gamephoto = gamephoto[0]

        context = {
            "message": "Список игр",
            "games": json_games,
            "pages": games,
        }
        return render(request, 'products/list_game.html', context=context)


class ListSortedByIdView(LoginRequiredMixin, View):
    login_url = reverse_lazy('register:login_in_register')

    def get(self, request):
        games = Game.objects.filter(creator=self.request.user).filter(removed=False).order_by('-id')
        if not games:
            return redirect('products:product_create')
        """ Paginator """
        # /register/list/?page=1
        page = request.GET.get('page', 1)
        paginator = Paginator(games, 5)
        try:
            games = paginator.page(page)
        except PageNotAnInteger:
            games = paginator.page(1)
        except EmptyPage:
            games = paginator.page(paginator.num_pages)
        # -------------------
        try:
            json_games = []
            x = 0
            y = 0
            page_number = request.GET.get('page')
            for i in games:
                if page_number:
                    if int(page_number) == 1:
                        x = x + 1
                    else:
                        print("1")
                        if y == 0:
                            y = 1
                            x = 1 + 5 * (int(page_number) - 1)
                        else:
                            x = x + 1
                else:
                    x = x + 1
                gamephoto = PhotoGame.objects.get(game=i).photo.url
                json_games.append(
                    {"name": i.name, "count": x, "id": i.id, "description": i.description, "genre": i.genre,
                     "Status": i.Status,
                     "photo_url": gamephoto})
        except PhotoGame.DoesNotExist:
            gamephoto = False
        if gamephoto:
            gamephoto = gamephoto[0]

        context = {
            "message": "Список игр",
            "games": json_games,
            "pages": games,
        }
        return render(request, 'products/list_game.html', context=context)


class ListSortedByStatusView(LoginRequiredMixin, View):
    login_url = reverse_lazy('register:login_in_register')

    def get(self, request):
        games = Game.objects.filter(creator=self.request.user).filter(removed=False).order_by('-Status')
        if not games:
            return redirect('products:product_create')
        """ Paginator """
        # /register/list/?page=1
        page = request.GET.get('page', 1)
        paginator = Paginator(games, 5)
        try:
            games = paginator.page(page)
        except PageNotAnInteger:
            games = paginator.page(1)
        except EmptyPage:
            games = paginator.page(paginator.num_pages)
        # -------------------
        try:
            json_games = []
            x = 0
            y = 0
            page_number = request.GET.get('page')
            for i in games:
                if page_number:
                    if int(page_number) == 1:
                        x = x + 1
                    else:
                        print("1")
                        if y == 0:
                            y = 1
                            x = 1 + 5 * (int(page_number) - 1)
                        else:
                            x = x + 1
                else:
                    x = x + 1
                gamephoto = PhotoGame.objects.get(game=i).photo.url
                json_games.append(
                    {"name": i.name, "count": x, "id": i.id, "description": i.description, "genre": i.genre,
                     "Status": i.Status,
                     "photo_url": gamephoto})
        except PhotoGame.DoesNotExist:
            gamephoto = False
        if gamephoto:
            gamephoto = gamephoto[0]

        context = {
            "message": "Список игр",
            "games": json_games,
            "pages": games,
        }
        return render(request, 'products/list_game.html', context=context)


class GameDetailView(View):

    def get(self, request, **kwargs):
        game = Game.objects.get(pk=kwargs['pk'])

        try:
            # Вместо get() используется filter(), т.к. с одним пользователем
            # может быть связано N фото.
            # Если использовать get(), то он вернет несколько записей,
            # что приведет к ошибке.
            gamephoto = PhotoGame.objects.filter(game=game)
        except PhotoGame.DoesNotExist:
            gamephoto = False
        # По умолчанию берется первая найденная фотография gamephoto[0].
        if gamephoto:
            gamephoto = gamephoto[0]
        context = {
            "message": "Игра",
            "game": game,
            "gamephoto": gamephoto,
        }
        return render(request, 'products/detail_game.html', context=context)


class GameEditView(View):
    def get(self, request, **kwargs):
        game = Game.objects.get(pk=kwargs['pk'])
        form = CreateProductForm(request.POST or None, instance=game)
        form.id = game.id

        # form.fields.pop('password')
        # form.fields.pop('password2')

        context = {
            "message": "Редактирование игры",
            "form": form,
        }
        return render(request, 'products/edit.html', context=context)


class GameSaveView(View):
    def post(self, request):
        game = Game.objects.get(pk=request.POST.get('id'))
        form = CreateProductForm(request.POST, instance=game)

        if form.is_valid():
            user = form.save(commit=True)
        return redirect('products:game_list')


class GameRemoveView(View):
    def get(self, request, **kwargs):
        Game.objects.filter(pk=kwargs['pk']).update(removed=True)
        return redirect('products:game_list')
