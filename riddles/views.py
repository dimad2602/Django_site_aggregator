from django.shortcuts import render, HttpResponse, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
# from django.http import HttpResponse;   import http.client;  from django import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import View
from .forms import *  # подключаем CreateProductForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse


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


def index(request):
    if request.method == "GET":
        # d = {}
        # if request.GET.get("var") == "1":
        #     d = {'message': "Hello world!"}
        # if request.GET.get("var") == "2":
        #     d = {'message': "Значение 2"}
        # return render(request, "firstheader.html", d)
        news = News.objects.filter(visibility=False, removed=False).order_by('-pk')[:3]
        # if not news:
        #     return redirect('riddles:home')

        # """ Paginator """
        # page = request.GET.get('page', 999)
        # paginator = Paginator(news, 3)
        # try:
        #     news = paginator.page(page)
        # except PageNotAnInteger:
        #     news = paginator.page(1)
        # except EmptyPage:
        #     news = paginator.page(paginator.num_pages)

        # -------------------
        try:
            json_news = []
            for i in news:
                newsphoto = PhotoNews.objects.get(news=i).photo.url
                json_news.append({"name": i.name, "id": i.id, "description": i.description, "photo_url": newsphoto})
        except PhotoNews.DoesNotExist:
            newsphoto = False
        if newsphoto:
            gamephoto = newsphoto[0]
        # -------------------

        context = {
            "message": "Список новостей",
            "news": json_news,
            # "pages": news,
            # "newsphoto": gamephoto
        }
        return render(request, 'firstheader.html', context=context)
    else:
        d = {'message': "Нажми на ссылку"}
        return render(request, "firstheader.html", d)


class NewHome(View):
    def get(self, request):
        """
        Поскольку предполагается, что пользователь сможет блокировать
        свой профиль, то в список должны попасть только незаблокированные
        (is_blocked=False) записи.
        """
        news = News.objects.filter(visibility=False, removed=False)
        if not news:
            return redirect('riddles:home')

        """ Paginator """
        page = request.GET.get('page', 1)
        paginator = Paginator(news, 5)
        try:
            news = paginator.page(page)
        except PageNotAnInteger:
            news = paginator.page(1)
        except EmptyPage:
            news = paginator.page(paginator.num_pages)

        # -------------------
        try:
            json_news = []
            for i in news:
                newsphoto = PhotoNews.objects.get(news=i).photo.url
                json_news.append({"name": i.name, "id": i.id, "description": i.description, "photo_url": newsphoto})
        except PhotoNews.DoesNotExist:
            newsphoto = False
        if newsphoto:
            gamephoto = newsphoto[0]
        # -------------------

        context = {
            "message": "Список новостей",
            "news": json_news,
            # "newsphoto": gamephoto
        }
        return render(request, 'firsheader.html', context=context)


def gameList(request):
    return render(request, "list_game.html", )


def riddles(request):
    if request.method == "GET":
        d = {}
        if request.GET.get("var") == "1":
            d = {'message': "Hello world!"}
        if request.GET.get("var") == "2":
            d = {'message': "Значение 2"}
        return render(request, "riddles/riddles.html", d)
    else:
        d = {'message': "Нажми на ссылку"}
        return render(request, "riddles/riddles.html", d)


# Create your views here.

class CreateNews(LoginRequiredMixin, View):  # создаем класс для представления, наследуеться от класса view
    # login_url = '/admin/'
    login_url = reverse_lazy('riddles:home')

    # raise_exception = True # 403
    def post(self, request):
        form = CreateNewsForm(request.POST, request.FILES)
        context = {}
        if form.is_valid():
            newsdata = form.save(commit=False)
            newsdata.creator = request.user
            newsdata.save()

            if newsdata.id is not None:
                news = News.objects.get(pk=newsdata.id)
                formPhoto = RegisterPhotoNewsForm(request.POST, request.FILES)
                if formPhoto.is_valid():
                    print("FORM IS VALID!")
                    photodata = formPhoto.save(commit=False)
                    photodata.news = news
                    photodata.save()

                else:
                    print("FORM IS NOT VALID!")
            news = News.objects.get(pk=newsdata.id)
            try:
                # Вместо get() используется filter(), т.к. с одним пользователем
                # может быть связано N фото.
                # Если использовать get(), то он вернет несколько записей,
                # что приведет к ошибке.
                photonews = PhotoNews.objects.filter(news=news)
                print("AU")
            except PhotoNews.DoesNotExist:
                photonews = False
            # По умолчанию берется первая найденная фотография userphoto[0].
            if photonews:
                photonews = photonews[0]
            context = {
                "message": "Список игр",
                "name": form.cleaned_data["name"],
                "description": form.cleaned_data["description"],
                "news": newsdata,
                "photonews": photonews,
            }
            return render(request, "riddles/news.html", context=context)

    def get(self, request):
        form = CreateNewsForm()
        photonews = RegisterPhotoNewsForm(request.POST)
        context = {
            "message": "Форма создания",
            "form": form,
            "photonews": photonews,
        }
        return render(request, "riddles/create.html", context=context)  # HttpResponse('riddles:home')  #


class NewsListView(View):
    def get(self, request):
        """
        Поскольку предполагается, что пользователь сможет блокировать
        свой профиль, то в список должны попасть только незаблокированные
        (is_blocked=False) записи.
        """
        news = News.objects.filter(visibility=False, removed=False)
        if not news:
            return redirect('riddles:home')

        """ Paginator """
        page = request.GET.get('page', 1)
        paginator = Paginator(news, 5)
        try:
            news = paginator.page(page)
        except PageNotAnInteger:
            news = paginator.page(1)
        except EmptyPage:
            news = paginator.page(paginator.num_pages)

        # -------------------
        try:
            json_news = []
            x = 0
            y = 0
            page_number = request.GET.get('page')
            for i in news:
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
                newsphoto = PhotoNews.objects.get(news=i).photo.url
                json_news.append(
                    {"name": i.name, "count": x, "id": i.id, "description": i.description, "photo_url": newsphoto})
        except PhotoNews.DoesNotExist:
            newsphoto = False
        if newsphoto:
            gamephoto = newsphoto[0]
        # -------------------

        context = {
            "message": "Список новостей",
            "news": json_news,
            "pages": news,
            # "newsphoto": gamephoto
        }
        return render(request, 'riddles/list_news.html', context=context)


class NewsDetailView(View):

    def get(self, request, **kwargs):
        news = News.objects.get(pk=kwargs['pk'])

        try:
            # Вместо get() используется filter(), т.к. с одним пользователем
            # может быть связано N фото.
            # Если использовать get(), то он вернет несколько записей,
            # что приведет к ошибке.
            newsphoto = PhotoNews.objects.filter(news=news)
        except PhotoNews.DoesNotExist:
            newsphoto = False
        # По умолчанию берется первая найденная фотография gamephoto[0].
        if newsphoto:
            newsphoto = newsphoto[0]
        context = {
            "message": "Новость",
            "news": news,
            "newsphoto": newsphoto,
        }
        return render(request, 'riddles/detail_news.html', context=context)


class NewsEditView(View):
    def get(self, request, **kwargs):
        news = News.objects.get(pk=kwargs['pk'])
        form = CreateNewsForm(request.POST or None, instance=news)
        form.id = news.id

        # form.fields.pop('password')
        # form.fields.pop('password2')

        context = {
            "message": "Редактирование игры",
            "form": form,
        }
        return render(request, 'riddles/edit.html', context=context)


class NewsSaveView(View):
    def post(self, request):
        news = News.objects.get(pk=request.POST.get('id'))
        form = CreateNewsForm(request.POST, instance=news)

        if form.is_valid():
            user = form.save(commit=True)
        return redirect('riddles:news_list')


class NewsRemoveView(View):
    def get(self, request, **kwargs):
        News.objects.filter(pk=kwargs['pk']).update(removed=True)
        return redirect('riddles:news_list')


def AjaxNewsView(request):
    return render(request, 'riddles/ajaxnews.html')


def AjaxModalForNewsView(request):
    return render(request, 'riddles/newsmodal.html')


def AjaxOvelayView(request):
    return render(request, 'riddles/overlay.html')

def AjaxErrorView(request):
    return render(request, 'riddles/error.html')
