from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django import forms
from .widgets import CustomClearableFileInput

from .models import CustomUser


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
                field.label = "プロフィール画像"


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class ProfileImageUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('profile_image',)
        widgets = {
            'profile_image': CustomClearableFileInput
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['required'] = ''
