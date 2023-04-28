from django.db import models
from register.models import User
from django.conf import settings

# Create your models here.

class News(models.Model):
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=256, blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    visibility = models.BooleanField(default=False)
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    # photo = models.ImageField(upload_to='media/game_photo/', null=True)  # media
    removed = models.BooleanField(default=False)


class PhotoNews(models.Model):
    news = models.ForeignKey(News, blank=False, null=False, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='media/news_photos/')
    status = models.BooleanField(default=True)
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
