from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("", views.TopView.as_view(), name="top"),
    path("login", views.Login.as_view(), name="login"),
    path("logout", views.Logout.as_view(), name="logout"),
    path("my_page/<int:pk>/", views.MyPage.as_view(), name="my_page"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("signup_done/", views.SignupDone.as_view(), name="signup_done"),
]
