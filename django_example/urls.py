"""django_example URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns, static, settings
from django.views.generic.base import RedirectView

# Django будет самостоятельно искать все файлы admin.py

admin.autodiscover()

favicon_view = RedirectView.as_view(url='/static/img/favicon.ico', permanent=True)

urlpatterns = [
    # path('riddles/', include('riddles.urls')),
    #path('registration/', include('register.urls')),
    path('admin/', admin.site.urls),
    path('products/', include('products.urls')),
    path('game/', include('products.urls')), #редактирование
    path('', include('riddles.urls')),
    path('riddles/', include('riddles.urls')),
    path('news/', include('riddles.urls')),
    path('register/', include('register.urls')),
    path('customer/', include('register.urls')), #редактирование
    path('user/', include('user.urls')),

    # path('', views.index, name='index'),
    # path('?var=1', views.index, name="index"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += staticfiles_urlpatterns()
# urlpatterns = [
#    path('admin/', admin.site.urls),
# ]
