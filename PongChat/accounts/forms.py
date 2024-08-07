from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    UserCreationForm,
)
from django.utils.translation import gettext_lazy

from .models import CustomUser
from .widgets import CustomClearableFileInput


class LoginForm(AuthenticationForm):
    """Form for user login.

    This form is used for authenticating users. It customizes the
    appearance of the form fields by adding Bootstrap classes and
    placeholders.

    Args:
        AuthenticationForm (class): Inherits from Django's AuthenticationForm.

    Attributes:
        fields (dict): The form fields for username and password.
    """

    def __init__(self, *args, **kwargs):
        """Initializes the form.

        Customizes each form field to include Bootstrap CSS classes and
        placeholders derived from the field labels.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
            field.widget.attrs["placeholder"] = field.label


class CustomUserCreationForm(UserCreationForm):
    """Form for creating a new user.

    This form is used for registering new users. It includes fields for
    username, password, and profile image. It customizes the appearance
    of the form fields by adding Bootstrap classes and setting labels.

    Args:
        UserCreationForm (class): Inherits from Django's UserCreationForm.

    Attributes:
        Meta (class): Meta class to specify the model and fields used in the form.
        fields (dict): The form fields for username, password, and profile image.
    """

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("username", "password1", "password2", "profile_image")

    def __init__(self, *args, **kwargs):
        """Initializes the form.

        Customizes each form field to include Bootstrap CSS classes.
        Sets a custom label for the profile image field.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            field = self.fields[field_name]
            field.widget.attrs["class"] = "form-control"
            if field_name == "profile_image":
                field.label = gettext_lazy("プロフィール画像")


class UsernameUpdateForm(forms.ModelForm):
    """Form for updating the username.

    This form allows users to update their username.

    Attributes:
        model (Model): The model associated with this form.
        fields (tuple): The fields to be included in the form.
    """

    class Meta:
        model = CustomUser
        fields = ("username",)

    def __init__(self, *args, **kwargs):
        """Initializes the form with Bootstrap CSS classes.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"


class CustomPasswordChangeForm(PasswordChangeForm):
    """Form for changing the user's password.

    This form allows users to change their password.

    Attributes:
        model (Model): The model associated with this form.
        fields (tuple): The fields to be included in the form.
    """

    def __init__(self, *args, **kwargs):
        """Initializes the form with Bootstrap CSS classes.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"


class ProfileImageUpdateForm(forms.ModelForm):
    """Form for updating the profile image.

    This form allows users to update their profile image.

    Attributes:
        model (Model): The model associated with this form.
        fields (tuple): The fields to be included in the form.
        widgets (dict): Custom widgets for the form fields.
    """

    class Meta:
        model = CustomUser
        fields = ("profile_image",)
        widgets = {"profile_image": CustomClearableFileInput}

    def __init__(self, *args, **kwargs):
        """Initializes the form with Bootstrap CSS classes and custom labels.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.label = "プロフィール画像"
            field.widget.attrs["class"] = "form-control"
            field.widget.attrs["required"] = ""
