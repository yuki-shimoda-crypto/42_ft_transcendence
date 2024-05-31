from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeDoneView,
    PasswordChangeView,
)
from django.shortcuts import redirect, render, resolve_url
from django.urls import reverse_lazy
from django.views import View, generic

from .forms import (
    CustomPasswordChangeForm,
    CustomUserCreationForm,
    LoginForm,
    ProfileImageUpdateForm,
    UsernameUpdateForm,
)
from .models import CustomUser


class TopView(generic.TemplateView):
    """View for the top page.

    This view renders the top page template.

    Attributes:
        template_name (str): The template to be used for the top page.
    """

    template_name = "accounts/top.html"


class Login(LoginView):
    """View for the login page.

    This view handles user login.

    Attributes:
        form_class (Form): The form used for login.
        template_name (str): The template to be used for the login page.
    """

    form_class = LoginForm
    template_name = "accounts/login.html"


class Logout(LogoutView):
    """View for the logout page.

    This view handles user logout and renders the logout completion page.

    Attributes:
        template_name (str): The template to be used for the logout completion page.
    """

    template_name = "accounts/logout_done.html"


class OnlyYouMixin(UserPassesTestMixin):
    """Mixin that allows access only to the user with the matching primary key.

    This mixin ensures that the view can only be accessed by the user
    whose primary key matches the 'pk' URL parameter.

    Attributes:
        raise_exception (bool): Whether to raise an exception if the test fails.
    """

    raise_exception = True

    def test_func(self):
        """Test if the current user matches the 'pk' URL parameter.

        Returns:
            bool: True if the current user's primary key matches
            the 'pk' parameter, False otherwise.
        """
        user = self.request.user
        return user.pk == self.kwargs["pk"]


class MyPage(OnlyYouMixin, generic.DetailView):
    """View for the user's personal page.

    This view displays the personal page of the user whose primary key
    matches the 'pk' URL parameter. Access is restricted to the user
    themselves.

    Attributes:
        model (Model): The model to be used for the detail view.
        template_name (str): The template to be used for the personal page.
    """

    model = CustomUser
    template_name = "accounts/my_page.html"


class SignUpView(View):
    """View for the user sign-up page.

    This view handles the user registration process.

    Attributes:
        form_class (Form): The form used for user registration.
        template_name (str): The template to be used for the registration page.
    """

    form_class = CustomUserCreationForm
    template_name = "accounts/user_form.html"

    def get(self, request):
        """Handles GET requests and displays the registration form.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: The rendered registration form page.
        """
        form = self.form_class()
        context = {"form": form, "process_name": "Sign Up"}
        return render(request, self.template_name, context)

    def post(self, request):
        """Handles POST requests and processes the registration form.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: Redirects to the sign-up done page if the form is valid,
                          otherwise re-renders the registration form with errors.
        """
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy("accounts:signup_done"))
        else:
            context = {"form": form, "process_name": "Sign Up"}
            return render(request, "accounts/user_form.html", context)


class SignupDone(generic.TemplateView):
    """View for the sign-up completion page.

    This view renders the template that confirms the user has successfully signed up.

    Attributes:
        template_name (str): The template to be used for the sign-up completion page.
    """

    template_name = "accounts/signup_done.html"


class UsernameUpdate(OnlyYouMixin, generic.UpdateView):
    """View for updating the username.

    This view allows users to update their username.

    Attributes:
        model (Model): The model associated with this view.
        form_class (Form): The form used for updating the username.
        template_name (str): The template used for rendering the view.
    """

    model = CustomUser
    form_class = UsernameUpdateForm
    template_name = "accounts/user_form.html"

    def get_success_url(self):
        """Returns the URL to redirect to after successful form submission.

        Returns:
            str: The URL to redirect to.
        """
        return resolve_url("accounts:my_page", pk=self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        """Adds extra context data to the view.

        Args:
            **kwargs: Arbitrary keyword arguments.

        Returns:
            dict: The context data.
        """
        context = super().get_context_data(**kwargs)
        context["process_name"] = "Update Username"
        return context


class ProfileImageUpdate(OnlyYouMixin, generic.UpdateView):
    """View for updating the profile image.

    This view allows users to update their profile image.

    Attributes:
        model (Model): The model associated with this view.
        form_class (Form): The form used for updating the profile image.
        template_name (str): The template used for rendering the view.
    """
    model = CustomUser
    form_class = ProfileImageUpdateForm
    template_name = "accounts/user_form.html"

    def get_success_url(self):
        """Returns the URL to redirect to after successful form submission.

        Returns:
            str: The URL to redirect to.
        """
        return resolve_url("accounts:my_page", pk=self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        """Adds extra context data to the view.

        Args:
            **kwargs: Arbitrary keyword arguments.

        Returns:
            dict: The context data.
        """
        context = super().get_context_data(**kwargs)
        context["process_name"] = "Update Profile Image"
        return context


class PasswordChange(PasswordChangeView):
    """View for changing the password.

    This view allows users to change their password.

    Attributes:
        form_class (Form): The form used for changing the password.
        success_url (str): The URL to redirect to after successful password change.
        template_name (str): The template used for rendering the view.
    """

    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy("accounts:password_change_done")
    template_name = "accounts/user_form.html"

    def get_context_data(self, **kwargs):
        """Adds extra context data to the view.

        Args:
            **kwargs: Arbitrary keyword arguments.

        Returns:
            dict: The context data.
        """
        context = super().get_context_data(**kwargs)
        context["process_name"] = "Change Password"
        return context


class PasswordChangeDone(PasswordChangeDoneView):
    """View for password change confirmation.

    This view confirms that the user's password has been successfully changed.

    Attributes:
        template_name (str): The template used for rendering the view.
    """
    template_name = "accounts/password_change_done.html"
