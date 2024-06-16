from django.apps import AppConfig
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger


class PingpongConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "pingpong"

    def ready(self):
        from pingpong.tasks import deactivate_inactive_users
        scheduler = BackgroundScheduler()
        scheduler.add_job(
            deactivate_inactive_users,
            IntervalTrigger(minutes=1),
            id="deactivate_inactive_users",
            name="Deactivate inactive users every minute",
        )
        scheduler.start()
