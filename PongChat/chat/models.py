import shortuuid
from django.conf import settings
from django.db import models

# from django.contrib.auth.models import User

# from django.templatetags.static import static


# Create your models here.
class ChatGroup(models.Model):
    objects = models.Manager()
    group_name = models.CharField(max_length=128, unique=True, default=shortuuid.uuid)
    users_online = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="online_in_groups", blank=True
    )
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="chat_groups", blank=True
    )
    is_private = models.BooleanField(default=False)

    def __str__(self):
        return self.group_name


class GroupMessage(models.Model):
    group = models.ForeignKey(
        ChatGroup, related_name="chat_messages", on_delete=models.CASCADE
    )
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.CharField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username} : {self.body}"

    class Meta:
        ordering = ["-created"]


# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     image = models.ImageField(upload_to="avatars/", null=True, blank=True)
#     displayname = models.CharField(max_length=20, null=True, blank=True)
#     info = models.TextField(null=True, blank=True)

#     def __str__(self):
#         return str(self.user)

#     @property
#     def name(self):
#         if self.displayname:
#             return self.displayname
#         return self.user.username

#     @property
#     def avatar(self):
#         if self.image:
#             return self.image.url
#         return static("images/avatar.svg")
