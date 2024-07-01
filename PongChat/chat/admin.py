from django.contrib import admin

from .models import ChatGroup, GroupMessage

# Register your models here.
admin.site.register(ChatGroup)
admin.site.register(GroupMessage)
