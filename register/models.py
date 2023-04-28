from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.conf import settings

# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    login_validator = UnicodeUsernameValidator()
    login = models.CharField(
        max_length=150,
        unique=True,
        validators=[login_validator],
    )
    password = models.CharField(max_length=24, blank=False, null=False)
    email = models.EmailField(blank=False, null=False)
    name = models.CharField(max_length=128, blank=False, null=False)
    # is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = ['email', 'name']
    objects = UserManager()

    def get_short_name(self):
        return self.email

    def get_name(self):
        return self.name


class UserPhoto(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, null=False, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='media/users_photos/')
    status = models.BooleanField(default=True)
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)


class Right(models.Model):
    name = models.CharField(max_length=16, blank=False, null=False)
    default_state = models.BooleanField(default=False)


class User_Right(models.Model):
    id_user = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE)
    id_right = models.ForeignKey(Right, blank=False, null=False, on_delete=models.CASCADE)
    actual_state = models.BooleanField(default=True)


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, login, email, name, password, **extra_fields):
        """
        Create and save a user with the given username, email,
        full_name, and password.
        """
        if not login:
            raise ValueError('The given username must be set')
        if not email:
            raise ValueError('The given email must be set')
        if not name:
            raise ValueError('The given full name must be set')
        login = self.model.normalize_username(login)
        email = self.normalize_email(email)
        user = self.model(
            login=login, email=email, name=name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, login, email, name, password=None, **extra_fields):
        #extra_fields.setdefault('is_staff', False)
        #extra_fields.setdefault('is_superuser', False)
        return self._create_user(
            email, login, name, password, **extra_fields
        )

    def create_superuser(self, login, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(
            email, login, password, **extra_fields
        )
