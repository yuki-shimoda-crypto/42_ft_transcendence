from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    profile_image = models.ImageField(
        upload_to="profile_images/", null=True, blank=True
    )

    def __str__(self):
        return self.username
