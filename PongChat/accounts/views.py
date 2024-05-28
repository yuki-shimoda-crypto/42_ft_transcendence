from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.views import generic
from .forms import LoginForm, SignupForm
from django.shortcuts import redirect


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


class Signup(generic.CreateView):
    template_name = 'accounts/user_form.html'
    form_class = SignupForm

    def form_valid(self, form):
        form.save()
        return redirect('accounts:signup_done')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["process_name"] = "Sign up"
        return context


class SignupDone(generic.TemplateView):
    template_name = 'accounts/signup_done.html'
