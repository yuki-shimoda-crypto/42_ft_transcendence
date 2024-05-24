from django.contrib.auth.views import LoginView
from django.views import generic

from .forms import LoginForm


class TopView(generic.TemplateView):
    template_name = "accounts/top.html"


class Login(LoginView):
    form_class = LoginForm
    template_name = "accounts/login.html"
