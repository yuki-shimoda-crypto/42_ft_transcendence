from django.urls import path

from . import views
from .views import switch_language

app_name = "accounts"

urlpatterns = [
    path("", views.TopView.as_view(), name="top"),
    path("login", views.Login.as_view(), name="login"),
    path("logout", views.Logout.as_view(), name="logout"),
    path("my_page/<int:pk>/", views.MyPage.as_view(), name="my_page"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("signup_done/", views.SignupDone.as_view(), name="signup_done"),
    path(
        "username_update/<int:pk>",
        views.UsernameUpdate.as_view(),
        name="username_update",
    ),
    path("password_change/", views.PasswordChange.as_view(), name="password_change"),
    path(
        "password_change_done/",
        views.PasswordChangeDone.as_view(),
        name="password_change_done",
    ),
    path(
        "profile_image_update/<int:pk>",
        views.ProfileImageUpdate.as_view(),
        name="profile_image_update",
    ),
    path("switch-language/<str:language>/", switch_language, name="switch_language"),
]
