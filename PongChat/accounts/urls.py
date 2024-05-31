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
    path('user_update/<int:pk>', views.UserUpdate.as_view(), name='user_update'),
    path('profile_image_update/<int:pk>', views.ProfileImageUpdate.as_view(), name='profile_image_update'),
]
