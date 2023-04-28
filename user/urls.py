from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.UserDjangoLogin.as_view(), name='login'),
    path('signup/', views.UserDjangoSignup.as_view(), name='signup'),
    path('logout/', views.UserLogout.as_view(), name='logout'),
]