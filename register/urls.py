from django.urls import path, re_path, include
from .views import *

app_name = 'register'

urlpatterns = [
    # re_path(r'^$', products, name='products'),
    # path("list/", ProductsList.as_view(), name="products_list"),
    path('login/', LoginView.as_view(success_url='/'), name="login_in_register"),
    path("register/", RegisterView.as_view(), name="user_register"),  # добовляем путь к предстовлению CreateProducts
    path('list/', UserListView.as_view(), name='user_list'),
    path('customer/detail/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('customer/edit/<int:pk>/', UserEditView.as_view(), name='user_edit'),
    path('customer/save/', UserSaveView.as_view(), name='user_save'),
    path('user/remove/<int:pk>/', UserRemoveView.as_view(), name='user_remove'),
    path('register/ajax/form/', AjaxViewForForm.as_view(), name='ajax_Form'),
    path('register/ajax/formlogin/', AjaxViewForlogin.as_view(), name='ajax_Form_login'),
    path('register/ajax/formpass/', AjaxViewForPass.as_view(), name='ajax_Form_pass'),
    path('register/ajax/formpass2/', AjaxViewForPass2.as_view(), name='ajax_Form_pass2'),
]
