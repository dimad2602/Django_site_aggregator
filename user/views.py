from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from .forms import UserLoginForm, UserSignupForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView


class UserDjangoLogin(LoginView):
    form_class = UserLoginForm
    template_name = 'user/login.html'

    def get_success_url(self):
        return reverse_lazy('riddles:index')  # riddles:home


class UserDjangoSignup(CreateView):
    form_class = UserSignupForm
    template_name = "user/signup.html"
    success_url = reverse_lazy("login")


class UserLogout(LogoutView):
    template_name = "user/logout.html"

    def userLogout(request):
        logout(request)
        return redirect('login')
