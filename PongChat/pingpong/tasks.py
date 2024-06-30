from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone


def deactivate_inactive_users():
    User = get_user_model()
    timeout = timezone.now() - timedelta(minutes=1)
    inactive_users = User.objects.filter(
        is_remote_multiplayer_active=True, last_activity__lt=timeout
    )
    inactive_users.update(is_remote_multiplayer_active=False)
