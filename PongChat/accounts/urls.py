from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("", views.TempView.as_view(), name="top"),
]
