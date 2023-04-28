from django.db import models
from register.models import User
from django.conf import settings


# Create your models here.

class Game(models.Model):
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=256, blank=False, null=False)
    description = models.TextField(blank=False, null=False)  #
    Status = models.CharField(max_length=20, blank=False, null=False)
    genre = models.CharField(max_length=256, default="unknown", blank=False, null=True)  # Жанр
    developer = models.CharField(max_length=256, default="unknown", blank=False, null=False)
    publisher = models.CharField(max_length=256, default="unknown", blank=False, null=False)
    visibility = models.BooleanField(default=False)
    date_release = models.DateField(blank=False, null=False)
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    # photo = models.ImageField(upload_to='media/game_photo/', null=True)  # media
    removed = models.BooleanField(default=False)


class PhotoGame(models.Model):
    game = models.ForeignKey(Game, blank=False, null=False, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='media/games_photos/')
    status = models.BooleanField(default=True)
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)


class GameGenre(models.Model):
    game = models.ForeignKey(Game, blank=False, null=False, on_delete=models.CASCADE)
    name = models.CharField(max_length=256, blank=False, null=False)
    status = models.BooleanField(default=True)


class GameDeveloped(models.Model):
    game = models.ForeignKey(Game, blank=False, null=False, on_delete=models.CASCADE)
    name = models.CharField(max_length=256, blank=False, null=False)
    status = models.BooleanField(default=True)


class GamePublisher(models.Model):
    game = models.ForeignKey(Game, blank=False, null=False, on_delete=models.CASCADE)
    name = models.CharField(max_length=256, blank=False, null=False)
    status = models.BooleanField(default=True)


# class User_Game(models.Model):
#     id_user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, null=False, on_delete=models.CASCADE)
#     id_game = models.ForeignKey(Game, blank=False, null=False, on_delete=models.CASCADE)
#     actual_state = models.BooleanField(default=True)
