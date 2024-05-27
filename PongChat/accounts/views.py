from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
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


class OnlyYouMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        user = self.request.user
        return user.pk == self.kwargs["pk"]


class MyPage(OnlyYouMixin, generic.DetailView):
    model = User
    template_name = "accounts/my_page.html"
