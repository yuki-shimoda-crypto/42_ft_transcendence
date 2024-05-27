from django.contrib.auth.views import LoginView, LogoutView
from django.views import generic

from .forms import LoginForm


class TopView(generic.TemplateView):
    template_name = "accounts/top.html"


class Login(LoginView):
    form_class = LoginForm
    template_name = "accounts/login.html"


class Logout(LogoutView):
    template_name = "accounts/logout_done.html"
