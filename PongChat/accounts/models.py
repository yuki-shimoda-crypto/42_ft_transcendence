from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from .utils import generate_default_profile_image


class CustomUser(AbstractUser):
    """Custom user model that extends the default Django user model.

    This model includes an additional profile_image field to store the
    user's profile image. If no profile image is provided, a default
    image is generated based on the user's initials.

    Attributes:
        profile_image (ImageField): The user's profile image.
    """

    profile_image = models.ImageField(
        upload_to="profile_images/", null=True, blank=True
    )

    block_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="blocked", blank=True
    )

    def __str__(self):
        """Returns the string representation of the user.

        Returns:
            str: The username of the user.
        """
        return self.username

    def save(self, *args, **kwargs):
        """Saves the user instance.

        If no profile image is provided, this method generates a default
        profile image using the first two characters of the username.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        if not self.profile_image:
            self.profile_image = generate_default_profile_image(self.username)
        super().save(*args, **kwargs)

    @property
    def avatar(self):
        if self.profile_image:
            return self.profile_image.url
        return generate_default_profile_image(self.username)
