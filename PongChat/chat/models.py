import shortuuid
from django.conf import settings
from django.db import models

# from django.contrib.auth.models import User

# from django.templatetags.static import static


# Create your models here.
class ChatGroup(models.Model):
    objects = models.Manager()
    group_name: models.CharField = models.CharField(
        max_length=128, unique=True, default=shortuuid.uuid
    )
    users_online: models.ManyToManyField = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="online_in_groups", blank=True
    )
    members: models.ManyToManyField = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="chat_groups", blank=True
    )
    is_private: models.BooleanField = models.BooleanField(default=False)

    def __str__(self):
        return self.group_name

    @property
    def member_count(self):
        return self.members.count()



class GroupMessage(models.Model):
    group: models.ForeignKey = models.ForeignKey(
        ChatGroup, related_name="chat_messages", on_delete=models.CASCADE
    )
    author: models.ForeignKey = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    body: models.CharField = models.CharField(max_length=300)
    created: models.DateTimeField = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username} : {self.body}"

    class Meta:
        ordering = ["-created"]
