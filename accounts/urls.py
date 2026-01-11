from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register, profile

app_name = "accounts"

urlpatterns = [
    path("register/", register, name="register"),
    path("profile/", profile, name="profile"),

    # Use Django’s built-in LoginView and LogoutView
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="accounts:login"), name="logout"),
]
