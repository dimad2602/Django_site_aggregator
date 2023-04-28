from django.urls import path
from .views import *
from . import views

app_name = 'riddles'

urlpatterns = [
    #path('$', views.index, name='index'),
    path('riddles/', views.riddles, name="index"),
    #path('', views.riddles, name="home"),
    path('', views.index, name="home"), #работает
    path('?var=1', views.riddles, name="riddles"),
    path("create/", CreateNews.as_view(), name="news_create"),  # добовляем путь к предстовлению CreateProducts
    path('list_news/', NewsListView.as_view(), name='news_list'),
    path('news/detail_news/<int:pk>/', NewsDetailView.as_view(), name='news_detail'),
    path('news/edit/<int:pk>/', NewsEditView.as_view(), name='news_edit'),
    path('news/save/', NewsSaveView.as_view(), name='news_save'),
    path('news/remove/<int:pk>/', NewsRemoveView.as_view(), name='news_remove'),

    path('riddles/ajaxnews', views.AjaxNewsView, name='ajax_news'),
    path('riddles/ajaxmodalnews', views.AjaxModalForNewsView, name='ajax_news'),
    path('riddles/ajaxoverlay', views.AjaxOvelayView, name='ajax_overlay'),
    path('riddles/ajaxerror', views.AjaxErrorView, name='ajax_error'),
]
