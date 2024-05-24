from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("", views.TopView.as_view(), name="top"),
    path("login", views.Login.as_view(), name="login"),
    path("logout", views.Logout.as_view(), name="logout"),
]
