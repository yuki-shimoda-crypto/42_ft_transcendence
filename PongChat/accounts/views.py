from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View, generic

from .forms import CustomUserCreationForm, LoginForm
from .models import CustomUser


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
    model = CustomUser
    template_name = "accounts/my_page.html"


# class Signup(generic.CreateView):
#     template_name = 'accounts/user_form.html'
#     form_class = SignupForm

#     def form_valid(self, form):
#         form.save()
#         return redirect('accounts:signup_done')

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["process_name"] = "Sign up"
#         return context


class SignUpView(View):
    form_class = CustomUserCreationForm
    template_name = "accounts/user_form.html"

    def get(self, request):
        form = self.form_class()
        context = {"form": form, "process_name": "Sign Up"}
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy("accounts:signup_done"))
        context = {"form": form, "process_name": "Sign Up"}
        return render(request, reverse("accounts:signup_done"), context)


class SignupDone(generic.TemplateView):
    template_name = "accounts/signup_done.html"
