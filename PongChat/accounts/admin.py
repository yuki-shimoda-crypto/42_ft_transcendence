from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    # 表示するフィールドを指定
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "profile_image_display",
    )
    # 読み取り専用フィールドを追加
    readonly_fields = ["profile_image_display"]
    # フィールドの表示方法を指定
    fieldsets = UserAdmin.fieldsets + (
        (None, {"fields": ("profile_image", "profile_image_display")}),
    )

    def profile_image_display(self, obj):
        if obj.profile_image:
            return obj.profile_image.url
        return "(No image)"

    profile_image_display.short_description = "Profile Image"


admin.site.register(CustomUser, UserAdmin)
