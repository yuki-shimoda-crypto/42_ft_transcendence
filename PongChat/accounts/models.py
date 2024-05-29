from django.contrib.auth.models import AbstractUser
from django.db import models

from .utils import generate_default_profile_image


class CustomUser(AbstractUser):
    profile_image = models.ImageField(
        upload_to="profile_images/", null=True, blank=True
    )

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if not self.profile_image:
            self.profile_image = generate_default_profile_image(self.username)
        super().save(*args, **kwargs)
