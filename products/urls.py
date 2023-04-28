from django.urls import path, re_path
from .views import *
from . import views

app_name = 'products'

urlpatterns = [
    #re_path(r'^$', products, name='products'),
    # path("list/", ProductsList.as_view(), name="products_list"),
    path("create/", CreateProduct.as_view(), name="product_create"),  # добовляем путь к предстовлению CreateProducts
    path('list_game/', GamesListView.as_view(), name='game_list_by_id'),
    path('list_game/sort_id/', ListSortedByIdView.as_view(), name='game_list_by_id'),
    path('list_game/sort_name/', ListSortedByNameView.as_view(), name='game_list_by_name'),
    path('list_game/sort_status/', ListSortedByStatusView.as_view(), name='game_list_by_status'),
    path('list_game/search_name/', ListSearchView.as_view(), name='search_list'),
    path('game/detail_game/<int:pk>/', GameDetailView.as_view(), name='game_detail'),
    path('game/edit/<int:pk>/', GameEditView.as_view(), name='game_edit'),
    path('game/save/', GameSaveView.as_view(), name='game_save'),
    path('game/remove/<int:pk>/', GameRemoveView.as_view(), name='game_remove'),
]
